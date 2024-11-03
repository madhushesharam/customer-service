from behave import when, then
import requests

BASE_URL = "http://127.0.0.1:5000/"


@when('I send a GET request to "{endpoint}"')
def step_send_get_request(context, endpoint):
    context.response = requests.get(f"{BASE_URL}{endpoint}")


@then("I should receive a {status_code:d} status code")
def step_check_status_code(context, status_code):
    assert (
        context.response.status_code == status_code
    ), f"Expected status code {status_code}, but got {context.response.status_code}"


@then('the response should contain "{expected_text}"')
def step_check_response_content(context, expected_text):
    assert (
        expected_text in context.response.text
    ), f"Expected '{expected_text}' in response, but got '{context.response.text}'"
