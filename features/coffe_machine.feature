Feature: Coffee Machine

    Scenario Outline: Not enough milk to make cappuccino
    Given required volume of milk is <needed_volume> ml
    And actual volume of milk is <current_volume> ml
    When attempting to make cappuccino
    Then the attempt should be declined
    And final volume of milk in coffee machine should be <expected_volume> ml

    Examples:
    | needed_volume | current_volume | expected_volume |
    | 100           | 99             | 99              |
    | 100           | 98             | 98              |
