from itertools import product

class GameError(Exception):
    pass

class Game:

    dimension = 3
    empty = " "
    P1 = "o"
    P2 = "x"

    def __init__(self):
        self.board = [[Game.empty for _ in range (Game.dimension)] for _ in range (Game.dimension)]
        self._player = Game.P1

    def __repr__(self):
        def get(y, x):
            if self.board[y][x] == "x":
                return "x"
            if self.board[y][x] == "o":
                return "o"
            else:
                return " "
        return f"""

  1 2 3
1 {get(0,0)}|{get(0,1)}|{get(0,2)} 
  -----
2 {get(1,0)}|{get(1,1)}|{get(1,2)}
  -----
3 {get(2,0)}|{get(2,1)}|{get(2,2)}


It is {self._player}'s turn

"""

    def play(self,row,col):
        row -= 1
        col -= 1
        self.board[row][col] = self._player
        self._player = Game.P1 if self._player == Game.P2 else Game.P2
    
    @property
    def winner(self):
        for p in [Game.P1,Game.P2]:
            for row in range(Game.dimension):
                if all(self.board[row][col] is p for col in range(Game.dimension)):
                    return p
            for col in range(Game.dimension):
                if all(self.board[row][col] is p for row in range(Game.dimension)):
                    return p
            # Diagonals
            if all(self.board[i][i] is p for i in range(Game.dimension)):
                return p
            if all(self.board[i][2 - i] is p for i in range(Game.dimension)):
                return p
        # No winner
        return None

    @property
    def drawn(self):
        if all(self.board[r][c] is not Game.empty for (r,c) in product(range(Game.dimension),range(Game.dimension))) and self.winner == None:
            return True
        else:
            return False



if __name__ == "__main__":
    g = Game()
    print (g)
    pass
