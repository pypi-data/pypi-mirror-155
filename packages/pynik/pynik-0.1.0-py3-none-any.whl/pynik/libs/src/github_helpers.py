import os
import requests

def trigger_workflow_options(repository, repository_dispatch, client_payload):
    assert os.getenv('PAT_TOKEN') is not None, logger.error("Environment variable PAT_TOKEN is not set")
    token = os.getenv('PAT_TOKEN')
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }
    payload = {
        "event_type": repository_dispatch,
        "client_payload": client_payload
    }
    url = f"https://api.github.com/repos/{repository}/dispatches"
    trigger = requests.post(
        url=url,
        headers=headers,
        json=payload
    )
    logger.info('webhook function called')
    logger.debug(f'endpoint {url}')
    logger.debug(f'dispatch {repository_dispatch} with status code {trigger.status_code}')
    github_url = "https://github.com/objectivesia/workflows/actions/workflows/dispatcher.yaml"
    if trigger.ok:
        workflow_state = "trigger looks good"
    elif not trigger.ok:
        workflow_state = "trigger looks bad"
    message_output = f"{repository} and {repository_dispatch}" \
                     f" with status code {trigger.status_code} and {workflow_state}" \
                     f" with status code {trigger.text} " \
                     f" check workflow status here: <a href=\"{github_url}\">Workflow Page</a>"
    logger.info(message_output)
    return message_output
