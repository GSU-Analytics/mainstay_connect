# Mainstay Data Fetching
## Environment Setup
### External tools
import click
import pandas as pd
from datetime import datetime, timedelta
from itertools import pairwise
from pathlib import Path

### Custom tools
from mainstay_connect import MainstayConnect
from mainstay_connect.utils.dt_utils import generate_dt_days_range
from mainstay_connect.utils.pagination_utils import extract_paginated_results
from mainstay_connect.utils.cli_utils import get_interactive_params, INTERACTIVE_ENDPOINTS

### Constants 
SEMESTER_START = datetime(year=2024, month= 8, day=26)
SEMESTER_END   = datetime(year=2024, month=12, day=17)

### Generating the Desired Date Pairs
dt_day_range = generate_dt_days_range(
    SEMESTER_START,
    SEMESTER_END
)

str_day_range = [dt.isoformat() + "Z" for dt in dt_day_range]
str_day_pairs = list(pairwise(str_day_range))

@click.command('mainstay-fetch')
@click.option('-e', '--endpoint',
              type=str, help='The URL endpoint you want to hit e.g. "messages/"',
              prompt=True)
@click.option('-o', '--output-name',
              type=str, help='The prefix for your output files.',
              prompt=True)
@click.option('-p', '--parameter', nargs=2, type=click.Tuple([str, str]), multiple=True, help='The parameter name and value, e.g. -p "since" "2025-05-20T12:00:00Z"')
@click.option('--interactive', is_flag=True)
@click.option('--to-csv', is_flag=True)
def fetch_cli(endpoint: str, output_name: str, parameter: list, interactive: bool, to_csv: bool):
    ## Initializing the API Connection
    ## Create a connection instance
    connector: MainstayConnect = MainstayConnect()
    ## Reset the API token, if necessary.
    ## Log into Mainstay and generate one if you do not have one.
    #connector.reset_token()

    ## This should pass. If it doesn't, you need to reset your token.
    connection_test = connector.test_connection()
    assert connection_test['ok']

    ## Build the kwargs dictionary
    kwargs = {
        param_key: param_val
        for param_key, param_val
        in parameter
    }
    kwargs['endpoint'] = endpoint

    ## Allow for users to specify their inputs directly
    if interactive:
        assert endpoint.lower() in INTERACTIVE_ENDPOINTS, f"Your endpoint must be one of {INTERACTIVE_ENDPOINTS.keys()}"
        interactive_params = get_interactive_params(endpoint.lower())
        kwargs.update(interactive_params)

    ## Build the pagination function
    paginator = connector.create_pagination_wrapper(
        connector.get_mainstay_endpoint,
        serialize=True,
        checkpoint_location=Path(f'./{output_name}'),
        output_name=output_name
    )

    ## Call the paginator function.
    pagination_results = paginator(**kwargs)

    ## Process the results
    loaded_output = connector.load_paginated_checkpoints(f'./{output_name}', output_name, raw=False)
    if to_csv:
        assert isinstance(loaded_output, pd.DataFrame)
        output_path = Path(f'./data/{output_name}.csv')
        if not output_path.parent.exists():
            output_path.parent.mkdir()
        loaded_output.to_csv(output_path)
    return loaded_output
        


def iterate_generic_fetch(connector: MainstayConnect):
    def get_daily_messages_by_time(str_date_pairs: list[tuple[str, str]]):
        # Build the coroutines
        output = []
        for start, end in str_date_pairs:
            try:
                paginated_output = extract_paginated_results(
                    connector,
                    connector.get_messages,
                    checkpoint_location='./message_checkpoints',
                    output_name=f'{start}',
                    serialize=True,
                    since=start,
                    before=end
                )
                output.append(paginated_output)
            except Exception as e:
                print(e)
        return output
    return get_daily_messages_by_time(str_day_pairs)


if __name__ == '__main__':
    fetch_cli()