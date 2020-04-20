from abc import ABC, abstractmethod
from game import Game, GameError

class Ui(ABC):

    @abstractmethod
    def run(self):
        raise NotImplementedError

class Gui(Ui):
    def __init__(self):
        pass

    def run(self):
        pass

class Terminal(Ui):
    def __init__(self):
        self.__game = Game()

    def run(self):
        while not self.__game.winner and not self.__game.drawn:
            print (self.__game)
            while True:
                try:
                    row, col = int(input("Which row")), int(input("Which col"))
                    if not 0 < row <= Game.dimension:
                        raise GameError()
                    if not 0 < col <= Game.dimension:
                        raise GameError()
                    if self.__game.board[row-1][col-1] != Game.empty:
                        print("The space must be empty")
                    else:
                        break
                except ValueError:
                    print ("Row and column need to be in numbers")
                except GameError:
                    print ("Row and column need to be between 1 and 3 inclusive")
            self.__game.play(row, col)
                
        if self.__game.drawn:
            print (self.__game)
            print("The game was drawn")
        else:
            print (self.__game)
            print (f"The Winner was {self.__game.winner}")

if __name__ == "__main__":
    ui = Terminal()
    ui.run()
