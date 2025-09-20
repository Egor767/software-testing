Feature: Authentication

  Scenario Outline: Attempt to auth decline after n unsuccessful login attempts
    Given the maximum number of attempts to auth is <max_attempts>
    When current attempt is <current_attempt>
    Then the account should be <expected_access>

  Examples:
    | max_attempts | current_attempt | expected_access |
    | 3            | 2               | True            |
    | 3            | 3               | True            |
    | 3            | 4               | False           |
    | 3            | 5               | False           |
