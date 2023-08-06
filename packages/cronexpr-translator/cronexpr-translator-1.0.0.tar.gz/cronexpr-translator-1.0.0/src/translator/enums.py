from enum import Enum, auto


class CronField(Enum):
    SECOND = 1
    MINUTE = 2
    HOUR = 3
    DAY_OF_MONTH = 4
    MONTH = 5
    DAY_OF_WEEK = 6
    YEAR = 7


class AllowedCharacters(Enum):
    STAR = "*"
    SLASH = "/"
    RANGE = "-"
    LIST = ","
    QUESTION_MARK = "?"
    LAST_DAY = "L"
    WEEK_DAY = "W"
    CRON_DELIMITER = " "
