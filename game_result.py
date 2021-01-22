from dataclasses import dataclass


@dataclass(frozen=True)
class GameResult:
    question_asked: int
    mistakes_made: int
    is_won: bool
