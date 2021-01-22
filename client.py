from game import Game
from game_result import GameResult
from game_status import GameStatus


def end_of_game_info(result: GameResult):
    print(f"Question asked {result.question_asked}")
    print(f"Mistakes made {result.mistakes_made}")
    print("You won!" if result.is_won else "You lost...")


game = Game("data/Questions.csv", 3, end_of_game_info)
count = 0
while game.game_status == GameStatus.IN_PROGRESS:

    count += 1
    print(f"Question no.{count}")
    q = game.get_next_question()
    print(q.text)
    answer = input("Enter answer(Yes/No): ")
    if answer == q.is_true:
        print("True!\n")
    else:
        print("False.")
        print(q.explanation)
    game.give_answer(answer)
