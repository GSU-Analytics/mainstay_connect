import inquirer

INTERACTIVE_ENDPOINTS = {
    'messages': ['since', 'before', 'admisthub_contact_id', 'contact_crm_id', 'test_user', 'include_test_user', 'page'],
    'contacts': ['texting_status', 'can_text', 'custom', 'include_test_contacts', 'include_nonpermitted_contacts', 'modified_since', 'modified_before', 'page'],
    'campaigns': ['since', 'before', 'script', 'status', 'scheduler', 'show_hidden', 'show_text', 'crm_id', 'admithub_contact_id', 'page']
}

def build_param_checkbox(param_list):
    parameters = [
        inquirer.Checkbox(
            "parameters",
            message="Which parameters would you like to specify?",
            choices=param_list,
        ),
    ]
    return parameters

def build_param_entry(param_list):
    parameters = [
        inquirer.Text(name=param, message=f'Please enter `{param}`')
        for param
        in param_list
    ]
    return parameters

def get_interactive_params(endpoint) -> dict:
    parameter_checkbox = build_param_checkbox(INTERACTIVE_ENDPOINTS[endpoint])
    selected_parameters = inquirer.prompt(parameter_checkbox)
    if selected_parameters:
        parameter_prompts = build_param_entry(selected_parameters['parameters'])
        interactive_parameters = inquirer.prompt(parameter_prompts)
        if interactive_parameters:
            return interactive_parameters
    return {}
