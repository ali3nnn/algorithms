import numpy as np
import sys
import matplotlib.pyplot as plt

class Sudoku():

  def __init__(self):
    self.reset()

  def reset(self):
    self.board = (np.indices((9,9)) + 1)[1]
    for i in range(len(self.board)):
      self.board[i] = np.random.permutation(self.board[i])
    self.fixedValues = np.array([
      #(val, row, col)
      (7, 0, 3),
      (1, 1, 0),
      (4, 2, 3),
      (3, 2, 4),
      (2, 2, 6),
      (6, 3, 8),
      (5, 4, 3),
      (9, 4, 5),
      (4, 5, 6),
      (1, 5, 7),
      (8, 5, 8),
      (8, 6, 4),
      (1, 6, 5),
      (2, 7, 2),
      (5, 7, 7),
      (4, 8, 1),
      (3, 8, 6)
      ])
    self.old = []
    self.setup()
    print("SOLUTIE GENERATA RANDOM")
    self.printBoard(self.board.copy())
    print()
      
  def setup(self):
        for (val, row, col) in self.fixedValues:
            self.swapToPlace(val, row, col)
      # [1, 2, 3, 4, 5, 6, 7, 8, 9] -> [1, 2, 3, 7, 5, 6, 4, 8, 9] 

  def swapToPlace(self, val, line, col):
        valIndex = np.where(self.board[line]==val)[0][0]
        self.swap(self.board[line], valIndex, col)

  def swap(self, arr, pos1, pos2):
        arr[pos1], arr[pos2] = arr[pos2], arr[pos1]
    
  def climbHill(self):
        scores = []
        maxScore = self.fitness()
        # print("Initial score: " + str(maxScore))
        while True:
            # print("Current score: " + str(maxScore))
            scores.append(maxScore)
            (row, (col1, col2), nextScore) = self.bestNeighbor()
            print(f"Vechiul scor {maxScore} - noul scor {nextScore}")
            if(nextScore <= maxScore):
                return scores
            self.swap(self.board[row], col1, col2)
            # print(self.board[row], (row, (col1, col2), nextScore))
            maxScore = nextScore

  def fitness(self, board=[]):
        if(board == []):
            board = self.board
        score = 0
        rows, cols = board.shape
        for row in board:
            score += len(np.unique(row))
        for col in board.T:
            score += len(np.unique(col))
        for i in range(0, 3):
            for j in range(0, 3):
                sub = board[3*i:3*i+3, 3*j:3*j+3]
                score += len(np.unique(sub))
        return score

  def bestNeighbor(self):
        tempBoard = self.board.copy()
        # best = (row, (col1, col2), val)
        # col1 si col2 vor fi schimbate cu swap.
        best = (0, (0,0), -1)
        # print('before')
        # self.printBoard(self.board.copy())
        for i in range(len(tempBoard)):
            for j in range(len(tempBoard[i])):
                for k in range(i,len(tempBoard)):
                    if (self.isFixed(i,j) or self.isFixed(i,k)):
                        # printmd(f'Pe randul **{i}** interschimba coloanele **{j} si {k}** - valori fixe')
                        continue
                    # printmd(f'Pe randul **{i}** interschimba coloanele **{j} si {k}**')
                    self.swap(tempBoard[i], j, k)
                    contestant = (i, (j,k), self.fitness(tempBoard))
                    # print('swap', contestant[2], best[2])
                    # self.printBoard(tempBoard)
                    # printmd(f"Scorul obtinut dupa schimbare {contestant[2]} mai { '**MARE**' if contestant[2] > best[2] else 'MIC'} decat scorul precedent **{best[2]}**")
                    if(contestant[2] > best[2]):
                        best = contestant
                    # anulez swap pt a reutiliza tabelul
                    self.swap(tempBoard[i], j, k)
        # print('after')
        # self.printBoard(self.board.copy())
        # printmd(f"**Scorul cel mai mare {best}**")
        return best

  def isFixed(self, row, col):
        for t in self.fixedValues:
            if(row == t[1] and col == t[2]):
                return True
        return False

  def printBoard(self, board=[]):
        if (board == []):
            board = self.board
        
        for i in range(len(board)):
            if(i % 3 == 0 and i != 0):
                print("------+------+------")
            for j in range(len(board[i])):
                if(j % 3 == 0 and j != 0):
                    print("|", end='')
                print(str(board[i][j]) + " ", end='')
            print("")


sud = Sudoku()
# sud.printBoard(sud.board.copy())

print("Hill Climbing START")

trials = []
maxScore = -1
bestBoard = []
for i in range(1):
    sud.reset()
    # sud.printBoard(sud.board.copy())
    finalScore = sud.climbHill()
    maxFinalScore = max(finalScore)
    # print(f'Scorul initial: {maxFinalScore}')
    if(maxScore < maxFinalScore):
        maxScore = maxFinalScore
        bestBoard = sud.board.copy()
    print(str(i) + ") " + str(finalScore[-1]) + "/243")
    # sud.printBoard(bestBoard)
    # print()
    if(finalScore == 243):
        print("SOLUTIA CORECTA A FOST GASITA")
        sud.printBoard()
        break
    trials.append(finalScore)
    # print(finalScore)
print("Cel mai bun scor: %i" % maxScore)
sud.printBoard(bestBoard)


#Desenha um gráfico do desempenho de cada execução do hill climbing
for trial in trials:
    plt.plot(trial)
plt.title('Hill Climbing')
plt.ylabel('scor (max 243)')
plt.xlabel('iteratii')
plt.show()