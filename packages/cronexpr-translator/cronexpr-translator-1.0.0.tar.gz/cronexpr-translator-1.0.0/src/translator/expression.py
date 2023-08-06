from src.translator.enums import AllowedCharacters


class Expression:

    def __init__(self, expression: str):
        self._expression = expression

    @property
    def expression(self) -> str:
        return self._expression

    @expression.setter
    def expression(self, new_expression: str):
        self._expression = new_expression

    def is_star_expression(self) -> bool:
        return AllowedCharacters.STAR.value == self._expression

    def is_question_mark_expression(self) -> bool:
        return AllowedCharacters.QUESTION_MARK.value == self._expression

    def is_last_day_expression(self) -> bool:
        return self._expression.startswith(AllowedCharacters.LAST_DAY.value) or \
               self._expression.endswith(AllowedCharacters.LAST_DAY.value)

    def is_slashed_star_expression(self, zero_based: bool = True) -> bool:
        return_value = self._expression.startswith(f"{AllowedCharacters.STAR.value}{AllowedCharacters.SLASH.value}")
        if zero_based:
            return return_value or self._expression.startswith(f"0{AllowedCharacters.SLASH.value}")
        return return_value or self._expression.startswith(f"1{AllowedCharacters.SLASH.value}")

    def has_slash_in_expression(self) -> bool:
        return AllowedCharacters.SLASH.value in self._expression

    def is_list_expression(self) -> bool:
        return AllowedCharacters.LIST.value in self._expression

    def is_week_day_expression(self) -> bool:
        return self._expression.startswith(AllowedCharacters.WEEK_DAY.value) or \
               self._expression.endswith(AllowedCharacters.WEEK_DAY.value)

    def is_last_week_day_expression(self) -> bool:
        return self.is_week_day_expression() and self.is_last_day_expression()

    def is_range_expression(self) -> bool:
        return AllowedCharacters.RANGE.value in self._expression and not self.is_list_expression()
