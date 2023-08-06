"""PrintingFunctionExercise class module"""

from ccheck.domain.token.token import Token
from ccheck.domain.exercise.exercise import Exercise
from ccheck.domain.token.token_type import TokenType


class PrintingFunctionExercise(Exercise):
    """PrintingFunctionExercise class"""

    def __inti__(self) -> None:
        super().__init__()
        self.__create_validations()

    def __create_validations(self) -> None:
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.IDENTIFIER, "void")], "Błędny typ funkcji!"
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.IDENTIFIER, "output")], "Błędna nazwa funkcji!"
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.OPEN_PAREN, "(")], "Błąd w zapisie funkcji!"
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.IDENTIFIER, "char"), Token(TokenType.OPERATOR, "*")],
                "Błędny typ argumentu funkcji!",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.IDENTIFIER, "tekst")],
                "Błędna nazwa argumentu funkcji!",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.CLOSE_PAREN, ")"), Token(TokenType.OPEN_CURLY, "{")],
                "Błąd w zapisie funkcji!",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.IDENTIFIER, "puts"), Token(TokenType.OPEN_PAREN, "(")],
                "Błąd w wywołaniu funkcji puts!",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.IDENTIFIER, "tekst")],
                "Błąd w wywołaniu funkcji puts! (złe odwołanie do argumentu?)",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.CLOSE_PAREN, ")")], "Błąd w wywołaniu funkcji puts!"
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.OPERATOR, ";")],
                "Błąd w wywołaniu funkcji puts! (brak średnika na końcu linii)",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.CLOSE_CURLY, "}")],
                "Błąd w zapisie funkcji! (brak zamknięcia nawiasu klamrowego)",
            )
        )

    def get_description(self) -> str:
        return (
            "Zapisz funkcję typu void o nazwie output,"
            + " która przyjmie jako argument tekst (typ argumentu - char*) i wypisze go funkcją puts."
            + " Niech argument nazywa się tekst. Nie używaj zmiennych pomocniczych."
        )
