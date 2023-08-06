import re
from src.validator.constants import *


class Validator:

    @staticmethod
    def validate(cron_expression: str) -> bool:
        """
            Validates a given cron expression and returns a boolean evaluated value.

            Fields -------- Required -------- Allowed values -------- Allowed Special Characters
            Seconds            Y              0-59                    ,-*/
            Minutes            Y              0-59                    ,-*/
            Hours              Y              0-23                    ,-*/
            Day of Month       Y              1-31                    ,-*/? L W
            Month              Y              1-12 or JAN-DEC         ,-*/
            Day of Week        Y              0-6 or SUN-SAT          ,-*/? L
            Year               N              empty or 1970-2099      ,-*/
        """
        cron_arguments = cron_expression.rsplit(CRON_EXPRESSION_DELIMITER)
        if len(cron_arguments) < CRON_EXPRESSION_MIN_ARGUMENTS or len(cron_arguments) > CRON_EXPRESSION_MAX_ARGUMENTS:
            return False
        is_seven_expression = len(cron_arguments) == CRON_EXPRESSION_MAX_ARGUMENTS
        is_valid = True
        for regex_key in REGEX_EXPRESSIONS_DICTIONARY:
            if not is_seven_expression and regex_key == YEAR_INDEX:
                break
            is_valid = is_valid and Validator.__validate_subexpression(
                regex_expression=REGEX_EXPRESSIONS_DICTIONARY[regex_key][0], subexpression=cron_arguments[regex_key],
                alternative_regex=REGEX_EXPRESSIONS_DICTIONARY[regex_key][1],
                alternative_values_list=ALTERNATIVE_LIST_VALUES_DICTIONARY.get(regex_key, None))
        return is_valid

    @staticmethod
    def validate_seconds_and_minutes(seconds_and_minutes_expression: str) -> bool:
        """
            Validates a cron subexpression of seconds or minutes and returns a boolean evaluated value.
        """
        return Validator.__validate_subexpression(regex_expression=SECONDS_AND_MINUTES_REGEX_EXPRESSION,
                                                  subexpression=seconds_and_minutes_expression)

    @staticmethod
    def validate_hours(hours_expression: str) -> bool:
        """
            Validates a cron subexpression of hours and returns a boolean evaluated value.
        """
        return Validator.__validate_subexpression(regex_expression=HOURS_REGEX_EXPRESSION,
                                                  subexpression=hours_expression)

    @staticmethod
    def validate_day_of_month(day_of_month_expression: str) -> bool:
        """
            Validates a cron subexpression of the day of the month and returns a boolean evaluated value.
        """
        return Validator.__validate_subexpression(regex_expression=DAY_OF_MONTH_REGEX_EXPRESSION,
                                                  subexpression=day_of_month_expression)

    @staticmethod
    def validate_month(month_expression: str) -> bool:
        """
            Validates a cron subexpression of the month and returns a boolean evaluated value.
        """
        return Validator.__validate_subexpression(regex_expression=MONTH_NUMBERS_REGEX_EXPRESSION,
                                                  subexpression=month_expression,
                                                  alternative_regex=MONTH_ALTERNATIVE_VALUES_REGEX_EXPRESSION,
                                                  alternative_values_list=MONTHS_LIST)

    @staticmethod
    def validate_day_of_week(day_of_week_expression: str) -> bool:
        """
            Validates a cron subexpression of the day of the week and returns a boolean evaluated value.
        """
        return Validator.__validate_subexpression(regex_expression=DAY_OF_WEEK_NUMBERS_REGEX_EXPRESSION,
                                                  subexpression=day_of_week_expression,
                                                  alternative_regex=DAY_OF_WEEK_ALTERNATIVE_VALUES_REGEX_EXPRESSION,
                                                  alternative_values_list=DAY_OF_WEEK_LIST)

    @staticmethod
    def validate_year(year_expression: str) -> bool:
        """
            Validates a cron subexpression of the year and returns a boolean evaluated value.
        """
        return Validator.__validate_subexpression(regex_expression=YEAR_REGEX_EXPRESSION, subexpression=year_expression)

    @staticmethod
    def __validate_subexpression(regex_expression: str, subexpression: str, alternative_regex: str = None,
                                 alternative_values_list: list = None) -> bool:
        if alternative_regex:
            if any(alternative_value in subexpression.upper() for alternative_value in alternative_values_list):
                return len(re.findall(alternative_regex, subexpression.upper())) > 0 and \
                       Validator.__validate_list_with_ranges(subexpression, alternative_values_list)
        return len(re.findall(regex_expression, subexpression)) > 0 and \
               Validator.__validate_list_with_ranges(subexpression)

    @staticmethod
    def __validate_range(range_expression: str, range_list: list = None) -> bool:
        range_values = range_expression.rsplit(RANGE_ELEMENT_DELIMITER)
        if not len(range_values) > 0:
            return False
        if range_list:
            return range_list.index(range_values[FIRST_RANGE_ELEMENT_INDEX]) < \
                   range_list.index(range_values[SECOND_RANGE_ELEMENT_INDEX])
        return int(range_values[FIRST_RANGE_ELEMENT_INDEX]) < \
               int(range_values[SECOND_RANGE_ELEMENT_INDEX])

    @staticmethod
    def __validate_list_with_ranges(list_expression: str, range_list: list = None) -> bool:
        if Validator.__is_range_expression(list_expression):
            if Validator.__is_list_expression(list_expression):
                list_values = list_expression.rsplit(LIST_ELEMENT_DELIMITER)
                range_values = [arg for arg in list_values if Validator.__is_range_expression(arg)]
                valid_ranges = [range_value for range_value in range_values
                                if Validator.__validate_range(range_value, range_list)]
                return len(valid_ranges) == len(range_values)
            return Validator.__validate_range(list_expression, range_list)
        return True

    @staticmethod
    def __is_list_expression(expression: str) -> bool:
        return LIST_ELEMENT_DELIMITER in expression

    @staticmethod
    def __is_range_expression(expression: str) -> bool:
        return RANGE_ELEMENT_DELIMITER in expression
