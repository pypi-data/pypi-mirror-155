# cronexpr-validator

The python validator for cron expressions

`cronexpr-validator` leverages regex expressions to do syntax validations on your cron expressions.

| **Fields**   | **Required** | **Allowed values** | **Allowed Special Characters** |
|--------------|--------------|--------------------|--------------------------------|
| Seconds      |       Y      | 0-59               | , - * /                        |
| Minutes      |       Y      | 0-59               | , - * /                        |
| Hours        |       Y      | 0-23               | , - * /                        |
| Day of Month |       Y      | 1-31               | , - * / ? L W                  |
| Month        |       Y      | 1-12 or JAN-DEC    | , - * /                        |
| Day of Week  |       Y      | 0-6 or SUN-SAT     | , - * / ? L                    |
| Year         |       N      | empty or 1970-2099 | , - * /                        |

### Methods available

`validate` -> Validates a given cron expression and returns a boolean evaluated value. 
Example: `Validator.validate("0 0 12 * * *")`

`validate_seconds_and_minutes` -> Validates a cron subexpression of seconds or minutes and returns a boolean evaluated values.
Example: `Validator.validate_seconds_and_minutes("*/5")`

`validate_hours` -> Validates a cron subexpression of hours and returns a boolean evaluated values.
Example: `Validator.validate_hours("*/5")`

`validate_day_of_month` -> Validates a cron subexpression of the day of the month and returns a boolean evaluated value.
Example: `Validator.validate_day_of_month("31")`

`validate_month` -> Validates a cron subexpression of the month and returns a boolean evaluated value.
Example: `Validator.validate_month("DEC")`

`validate_day_of_week` -> Validates a cron subexpression of the day of the week and returns a boolean evaluated value.
Example: `Validator.validate_day_of_week("0")`

`validate_year` -> Validates a cron subexpression of the year and returns a boolean evaluated value.
Example: `Validator.validate_year("0")`


