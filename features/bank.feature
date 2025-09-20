Feature: Cash dispenser tests

    Scenario Outline: Attempt to cashout an amount exceeding the balance
        Given the account balance is <balance>
        When i attempt to cashout <cashout_amount>
        Then the cashout should be declined
        And final account balance should be <expected_balance>

        Examples:
            | balance | cashout_amount | expected_balance |
            | 150     | 151            | 150              |
            | 150     | 152            | 150              |


    Scenario Outline: Attempt to cashout an amount not exceeding the balance
        Given the account balance is <balance>
        When i attempt to cashout <cashout_amount>
        Then the cashout should be successful
        And final account balance should be <expected_balance>

        Examples:
            | balance | cashout_amount | expected_balance |
            | 150     | 149            | 1                |
            | 150     | 150            | 0                |
