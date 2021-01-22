from typing import Callable, List

from game_result import GameResult
from game_status import GameStatus
from question import Question


class Game:

    def __init__(self, file_path: str, allowed_mistakes: int, end_of_game_event: Callable):
        if allowed_mistakes > 5 or allowed_mistakes < 1:
            raise ValueError(f"Allowed mistakes should be between 1 and 5. You passed:{allowed_mistakes}")

        self.__file_path = file_path
        self.__allowed_mistakes = allowed_mistakes
        self.__end_of_game_event = end_of_game_event
        self.__mistakes = 0
        self.__questions: List[Question] = []
        self.__counter = 0
        self.__game_status = GameStatus.IN_PROGRESS

        self.__fill_in_questions(file_path, self.__questions)

    def __fill_in_questions(self, file_path, questions):
        with open(file_path, encoding='utf8') as file:
            for line in file:
                q = self.__parse_line(line)
                questions.append(q)

    def __parse_line(self, line) -> Question:
        parts = line.split(';')
        text = parts[0]
        is_correct = parts[1]
        explanation = parts[2]
        return Question(text, is_correct, explanation)

    def get_next_question(self):
        return self.__questions[self.__counter]

    def give_answer(self, answer: str):
        def is_last_question():
            return self.__counter == len(self.__questions)

        def exceeded_allowed_mistakes():
            return self.__mistakes >= self.__allowed_mistakes

        if answer != self.__questions[self.__counter].is_true:
            self.__mistakes += 1
        self.__counter += 1
        if is_last_question() or exceeded_allowed_mistakes():
            self.__game_status = GameStatus.GAME_IS_OVER

            result = GameResult(self.__counter, self.__mistakes, self.__mistakes <= self.__allowed_mistakes)
            self.__end_of_game_event(result)

    @property
    def counter(self):
        return self.__counter

    @property
    def allowed_mistakes(self):
        return self.__allowed_mistakes

    @property
    def mistakes(self):
        return self.__mistakes

    @property
    def game_status(self):
        return self.__game_status
