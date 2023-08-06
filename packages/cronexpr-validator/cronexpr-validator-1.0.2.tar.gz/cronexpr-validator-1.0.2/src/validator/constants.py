SECONDS_AND_MINUTES_REGEX_EXPRESSION = "^\\b([1-5]?\\d)\\b$|^((\\b([1-5]?\\d)\\b,)|(\\b([1-5]?\\d)\\b-\\b([" \
                                       "1-5]?\\d)\\b,))*((\\b([1-5]?\\d)\\b)|(\\b([1-5]?\\d)\\b-\\b([" \
                                       "1-5]?\\d)\\b))+$|^\\b([1-5]?\\d)\\b-\\b([1-5]?\\d)\\b$|^\\*$|^(\\*|\\b([" \
                                       "1-5]?\\d)\\b)\\/\\b([1-5]?\\d)\\b$"
HOURS_REGEX_EXPRESSION = "^\\b(\\d|1\\d|2[0-3])\\b$|^((\\b(\\d|1\\d|2[0-3])\\b,)|(\\b(\\d|1\\d|2[0-3])\\b-\\b(" \
                         "\\d|1\\d|2[0-3])\\b),)*((\\b(\\d|1\\d|2[0-3])\\b)|(\\b(\\d|1\\d|2[0-3])\\b-\\b(\\d|1\\d|2[" \
                         "0-3])\\b))+$|^((\\b(\\d|1\\d|2[0-3])\\b)|\\*)\\/(\\b(\\d|1\\d|2[0-3])\\b)$|^\\*$"
DAY_OF_MONTH_REGEX_EXPRESSION = "^\\b(([1-9])|([1-2]\\d)|(3[0-1]))\\b$|^((\\b(([1-9])|([1-2]\\d)|(3[0-1]))\\b," \
                                ")|(\\b([1-2]?\\d|3[0-1])\\b-\\b(([1-9])|([1-2]\\d)|(3[0-1]))\\b),)*((\\b(([1-9])|([" \
                                "1-2]\\d)|(3[0-1]))\\b)|(\\b([1-2]?\\d|3[0-1])\\b-\\b(([1-9])|([1-2]\\d)|(3[" \
                                "0-1]))\\b))+$|^((\\b(([1-9])|([1-2]\\d)|(3[0-1]))\\b)|\\*)\\/(\\b([1-2]?\\d|3[" \
                                "0-1])\\b)$|^\\?$|^\\b(([1-9])|([1-2]\\d)|(3[0-1]))W\\b$|^L$|^\\*$|" \
                                "^\\bW(([1-9])|([1-2]\\d)|(3[0-1]))\\b$|^WL$|^LW$"
MONTH_NUMBERS_REGEX_EXPRESSION = "^\\b([1-9]|1[0-2])\\b$|^((\\b([1-9]|1[0-2])\\b,)|(\\b([1-9]|1[0-2])\\b-\\b([1-9]|1[" \
                                 "0-2])\\b,))*((\\b([1-9]|1[0-2])\\b)|(\\b([1-9]|1[0-2])\\b-\\b([1-9]|1[" \
                                 "0-2])\\b))+$|^\\*$|^(\\b([1-9]|1[0-2])\\b|\\*)\\/(\\b([1-9]|1[0-2])\\b)$"
MONTH_ALTERNATIVE_VALUES_REGEX_EXPRESSION = "^(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)$|^(((" \
                                            "JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)," \
                                            ")|((JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)-(" \
                                            "JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)," \
                                            "))*((JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)|((" \
                                            "JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)-(" \
                                            "JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)))+$|^\\*$|^((" \
                                            "JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)|\\*)\\/(" \
                                            "JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)$"
DAY_OF_WEEK_NUMBERS_REGEX_EXPRESSION = "^[0-6]$|^(([0-6],)|([0-6]-[0-6],))*([0-6]|([0-6]-[0-6]))+$|^[\\*\\?]$|^([" \
                                       "0-6]|\\*)\\/[0-6]$|^[0-6]?L$|^L[0-6]?$"
DAY_OF_WEEK_ALTERNATIVE_VALUES_REGEX_EXPRESSION = "^(SUN|MON|TUE|WED|THU|FRI|SAT)$|^(((SUN|MON|TUE|WED|THU|FRI|SAT)," \
                                                  ")|((SUN|MON|TUE|WED|THU|FRI|SAT)-(SUN|MON|TUE|WED|THU|FRI|SAT)," \
                                                  "))*((SUN|MON|TUE|WED|THU|FRI|SAT)|((SUN|MON|TUE|WED|THU|FRI|SAT)-(" \
                                                  "SUN|MON|TUE|WED|THU|FRI|SAT)))+$|^[\\*\\?]$|^((" \
                                                  "SUN|MON|TUE|WED|THU|FRI|SAT)|\\*)\\/(" \
                                                  "SUN|MON|TUE|WED|THU|FRI|SAT)$|^(SUN|MON|TUE|WED|THU|FRI|SAT)?L$|" \
                                                  "^L(SUN|MON|TUE|WED|THU|FRI|SAT)?$"
YEAR_REGEX_EXPRESSION = "^\\b(197\\d|198\\d|199\\d|20\\d\\d)\\b$|^\\*$|^((\\b(197\\d|198\\d|199\\d|20\\d\\d)\\b," \
                        ")|(\\b(197\\d|198\\d|199\\d|20\\d\\d)\\b-\\b(197\\d|198\\d|199\\d|20\\d\\d)\\b," \
                        "))*((\\b(197\\d|198\\d|199\\d|20\\d\\d)\\b)|(\\b(197\\d|198\\d|199\\d|20\\d\\d)\\b-\\b(" \
                        "197\\d|198\\d|199\\d|20\\d\\d)\\b))+$|^(\\b(197\\d|198\\d|199\\d|20\\d\\d)\\b|\\*)\\/(\\b(" \
                        "197\\d|198\\d|199\\d|20\\d\\d)\\b)$"

CRON_EXPRESSION_MIN_ARGUMENTS = 6
CRON_EXPRESSION_MAX_ARGUMENTS = 7
SECONDS_INDEX = 0
MINUTES_INDEX = 1
HOURS_INDEX = 2
DAY_OF_MONTH_INDEX = 3
MONTH_INDEX = 4
DAY_OF_WEEK_INDEX = 5
YEAR_INDEX = 6
FIRST_RANGE_ELEMENT_INDEX = 0
SECOND_RANGE_ELEMENT_INDEX = 1
RANGE_ELEMENT_DELIMITER = "-"
LIST_ELEMENT_DELIMITER = ","
CRON_EXPRESSION_DELIMITER = " "

REGEX_EXPRESSIONS_DICTIONARY = {SECOND_RANGE_ELEMENT_INDEX: (SECONDS_AND_MINUTES_REGEX_EXPRESSION, None),
                                MINUTES_INDEX: (SECONDS_AND_MINUTES_REGEX_EXPRESSION, None),
                                HOURS_INDEX: (HOURS_REGEX_EXPRESSION, None),
                                DAY_OF_MONTH_INDEX: (DAY_OF_MONTH_REGEX_EXPRESSION, None),
                                MONTH_INDEX: (MONTH_NUMBERS_REGEX_EXPRESSION,
                                              MONTH_ALTERNATIVE_VALUES_REGEX_EXPRESSION),
                                DAY_OF_WEEK_INDEX: (DAY_OF_WEEK_NUMBERS_REGEX_EXPRESSION,
                                                    DAY_OF_WEEK_ALTERNATIVE_VALUES_REGEX_EXPRESSION),
                                YEAR_INDEX: (YEAR_REGEX_EXPRESSION, None)}

MONTHS_LIST = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
DAY_OF_WEEK_LIST = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]

ALTERNATIVE_LIST_VALUES_DICTIONARY = {MONTH_INDEX: MONTHS_LIST, DAY_OF_WEEK_INDEX: DAY_OF_WEEK_LIST}
