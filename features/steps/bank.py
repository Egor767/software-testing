from behave import *

class Account:
    def __init__(self, balance: float) -> None:
        self.balance = balance

    def cashout(self, amount):
        if amount > self.balance:
            raise Exception('The cashout amount is more than balance')
        self.balance -= amount

# Given
@given('the account balance is {balance}')
def step_impl(context, balance):
    context.account = Account(int(balance))

# When
@when('i attempt to cashout {cashout_amount}')
def step_impl(context, cashout_amount):
    try:
        context.account.cashout(float(cashout_amount))
        context.cashout_successful = True
    except Exception:
        context.cashout_successful = False

# Then
# exceeding
@then('the cashout should be declined')
def step_impl(context):
    assert context.cashout_successful is False

# successful
@then('the cashout should be successful')
def step_impl(context):
    assert context.cashout_successful is True

@then('final account balance should be {expected_balance}')
def step_impl(context, expected_balance):
    assert context.account.balance == float(expected_balance)

