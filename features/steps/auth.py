from behave import *

@given('the maximum number of attempts to auth is {max_attempts}')
def step_given_max_attempts(context, max_attempts):
    context.max_attempts = int(max_attempts)

@when('current attempt is {current_attempt}')
def step_when_current_attempt(context, current_attempt):
    context.current_attempt = int(current_attempt)

@then('the account should be {expected_access}')
def step_then_expected_access(context, expected_access):
    actual_access = (context.current_attempt<=context.max_attempts)
    expected_access_bool = expected_access.lower() == 'true'
    assert actual_access == expected_access_bool # ==

