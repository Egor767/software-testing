from behave import *

@given('required volume of milk is {needed_volume} ml')
def step_given_needed_volume(context, needed_volume):
    context.needed_volume = int(needed_volume)

@given('actual volume of milk is {current_volume} ml')
def step_given_current_volume(context, current_volume):
    context.current_volume = int(current_volume)

@when('attempting to make cappuccino')
def step_when_attempt_make_cappuccino(context):
    if context.current_volume < context.needed_volume:
        context.attempt_declined = True
    else:
        context.attempt_declined = False
        context.current_volume -= context.needed_volume

@then('the attempt should be declined')
def step_then_attempt_declined(context):
    assert context.attempt_declined, "Attempt was not declined but should be"

@then('final volume of milk in coffee machine should be {expected_volume} ml')
def step_then_final_volume(context, expected_volume):
    assert context.current_volume == int(expected_volume)
