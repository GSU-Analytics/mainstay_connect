import requests
import time
import pickle
import sys
from loguru import logger
from pathlib import Path
from collections.abc import Callable
from typing import Union, Any

SERIALIZATION_NOTIF = "You have chosen not to serialize your checkpoints. At the end of this process, you will be asked if you want to automatically delete the checkpoints."


def extract_paginated_results(
        connector,
        mainstay_api_call: Callable,
        serialize: bool=False,
        checkpoint_location: Union[str | Path]='./checkpoints',
        output_name: Union[str | None]=None,
        sleep_duration=1.5,
        **mainstay_kwargs) -> dict:
    """
    Extracts all paginated results from the mainstay API.

    Args:
        connector: The connector object containing headers for API requests.
        mainstay_api_call (Callable): The mainstay API call function.
        serialize (bool, optional): Whether to serialize the results. Defaults to False.
        checkpoint_location (Union[str, Path], optional): Directory for storing checkpoints. Defaults to './checkpoints'.
        output_name (Union[str, None], optional): Name for the output files. If None, prompts the user. Defaults to None.
        sleep_duration (float, optional): Duration to sleep between API calls. Defaults to 1.5 seconds.
        **mainstay_kwargs: Additional keyword arguments for the mainstay API call.

    Returns:
        dict: A dictionary containing all paginated results.
    """

    if not output_name:
        output_name = input('Please provide a name for your pages: ')
    logger.add(Path('logs') / f"pagination_{output_name}" + "_{time}.log")
    logger.info(f"Calling with {mainstay_kwargs}...")
    if not serialize:
        logger.info(SERIALIZATION_NOTIF)
    checkpoint_location = Path(checkpoint_location)
    logger.info(f"Your pagination checkpoints will be located at {checkpoint_location.absolute()}.")
    # We're creating a do-while loop here, in effect.
    iteration = 0
    # Call and store the first request. We need to do this once, so that
    # we have the initial link in the linked-list.
    mainstay_results = mainstay_api_call(**mainstay_kwargs)
    process_output(mainstay_results, checkpoint_location, output_name, iteration, format=False)
    # Traverse the linked-list of pages until we reach the end.
    next_URI = mainstay_results.get('next')
    while next_URI:
        iteration += 1
        if sleep_duration:
            time.sleep(sleep_duration)
        next_results = requests.get(next_URI, headers=connector.headers)
        next_results = process_output(next_results, checkpoint_location, output_name, iteration)
        next_URI = next_results['next']
    if not serialize:
        paginated_dict = load_paginated_checkpoints(checkpoint_location, output_name)
        remove_paginated_checkpoints(checkpoint_location, output_name)
        return paginated_dict


def process_output(results, checkpoint_stem: str, name: str, iteration: Union[str | int], format=True) -> None:
    '''Used by extract_paginated_results.
    Optionally format the results, then validate them, and then serialize them.
    '''
    if format:
        results = format_output(results)
    validate_paginated_results(results)
    serialize_output(results, checkpoint_stem, name, iteration)
    return results


def validate_paginated_results(results: Any) -> None:
    '''Check the structure of the returned mainstay_api data.
    Will raise an error if certain criteria are not true.
    '''
    assert isinstance(results, dict), "Your results aren't a dictionary. Please check the format of your returned values."
    assert 'results' in results, "Your dictionary does not contain a 'results' field. Please check the format of your values."
    assert isinstance(results['results'], list), "Your results are not a list. Please check the format of your values."


def format_output(output) -> dict:
    '''Format the output from the mainstay API requests.
    '''
    if output.status_code == 200:
        return output.json()
    else:
        output.raise_for_status()


def serialize_output(output, directory: Path, name: str, iteration: Union[str | int]) -> None:
    '''Save the outputs to the specified directory.
    '''
    if not directory.exists():
        directory.mkdir()
    filepath = directory / f"{name}_page-{iteration}.pickle"
    logger.info(f"Writing results to {filepath.name}...")
    with open(filepath, "wb") as f:
        pickle.dump(output, f)
    logger.info("Successfully serialized output.")


def load_paginated_checkpoints(path: Path, name: str, extension='.pickle') -> dict:
    '''Load a sequence of pickle files, saved by `serialize_output`,
    into one dictionary.
    '''
    paginated_dict = {}
    checkpoint_files = path.glob(f'{name}*{extension}')
    for checkpoint_file in checkpoint_files:
        with open(checkpoint_file, 'rb') as f:
            paginated_dict[checkpoint_file.stem] = pickle.load(f)

    return paginated_dict


def remove_paginated_checkpoints(path: Path, name: str, extension='.pickle'):
    """Removes paginated checkpoint files from the specified directory.

    Args:
        path (Path): The directory path where checkpoint files are located.
        name (str): The base name of the checkpoint files to be removed.
        extension (str, optional): The file extension of the checkpoint files. Defaults to '.pickle'.

    This function will:
    1. Identify checkpoint files matching the specified name and extension in the given path.
    2. Log the selected checkpoint files for review.
    3. Prompt the user to confirm deletion by typing "DELETE".
    4. Delete the confirmed checkpoint files.
    5. Attempt to remove the directory if it is empty after deletion.

    Note:
    - The user must manually confirm the deletion by typing "DELETE".
    - If the directory contains other files, it will not be removed automatically.

    Example:
    ```
    remove_paginated_checkpoints(Path('/path/to/checkpoints'), 'my_checkpoint_name')
    ```
    """
    checkpoints_for_removal = path.glob(f'{name}*{extension}')
    logger.info(f'The following checkpoint files have been selected for deletion in {path.absolute()}.')
    logger.info('Please review them and confirm that you would like to delete them.')
    logger.info(sorted(file.name for file in checkpoints_for_removal))
    logger.info('ALERT: You are about to delete these files. Please type "DELETE" to continue.')
    confirm = input('Type DELETE to delete the files. Type anything else to exit.')
    if confirm.lower() == 'delete':
        for checkpoint in checkpoints_for_removal:
            logger.info(f'Deleting {checkpoint.name}...')
            checkpoint.unlink()
        try:
            path.rmdir()
            logger.info(f'{path.absolute()} has been removed. Your checkpoints have been deleted.')
        except OSError:
            logger.info(f'{path.absolute()} likely had other files in it, and so was not deleted. If you wish to delete your checkpoints, you may do so manually.')