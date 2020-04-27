from tkinter import Button, Tk, Toplevel, Frame, N,S,E,W,X,Y, LEFT,RIGHT, END, Scrollbar, Text, Message, Grid, StringVar
from game import Game, GameError
from sys import stderr
from itertools import product
from abc import ABC, abstractmethod


class Ui(ABC):

    @abstractmethod
    def run(self):
        raise NotImplementedError

class Gui(Ui):
    def __init__(self):
        root = Tk()
        root.title("Tic Tac Toe")
        self.game_win = None
        frame = Frame(root)
        frame.pack()
        Button(
            frame,
            text='Show Help',
            command=self.play_callback
        ).pack(fill=X)
        Button(
            frame,
            text='Play Game',
            command=self.play_callback
        ).pack(fill=X)

        console = Text(frame, height=4, width=50)
        scroll = Scrollbar(frame)
        scroll.pack(side=RIGHT, fill=Y)
        console.pack(side=LEFT, fill=Y)

        self._console = console
        self._root = root

    def help_callback(self):
        pass

    def game_close(self):
        self.game_win.destroy()
        self.game_win = None

    def play_callback(self):
        if self.game_win:
            return None
        self.game = Game()
        game_win = Toplevel(self._root)
        self.game_win = game_win
        game_win.title("Game")
        Grid.rowconfigure(game_win, 0, weight = 1)
        Grid.columnconfigure(game_win, 0, weight = 1)
        frame = Frame(game_win)
        frame.grid(row = 0, column = 0)

        self._buttons = [[None for _ in range (Game.dimension)] for _ in range (Game.dimension)]

        for row, column in product(range(Game.dimension), range(Game.dimension)):
            b = StringVar()
            b.set(self.game.at(row+1, column+1))

            cmd = lambda r=row, c=column : self.play_and_refresh(r, c)

            Button(
                frame,
                textvariable = b,
                command=cmd
            ).grid(row = row, column = column)

            self._buttons[row][column] = b

        Button(game_win, text="Dismiss", command=self.game_close).grid(row=1, column = 0)

    def play_and_refresh(self, row, column):
        try:
            self.game.play(row + 1, column + 1)
        except GameError as e:
            print (e)

        for row, column in product(range(Game.dimension), range(Game.dimension)):
            text = self.game.at(row + 1, column + 1)
            self._buttons[row][column].set(text)

        w = self.game.winner
        if w is not None:
            if self.game.drawn:
                self._console.insert(END, "The game was drawn")
            else:
                self._console.insert(END, f"The game was won by {w}")
    
    def run(self):
        self._root.mainloop()

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
