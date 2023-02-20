#Connect Four
#board[row][col]
import random
import copy
import replit

def print_board(board_in):
  replit.clear()
  print('\n 0 1 2 3 4 5 6')
  for row in board_in:
    print ('|'+'|'.join(row)+'|')
  print()

def nthcolumn(n, matrix):
    return [row[n] for row in matrix]

#Check if given move is valid
def isValid(col,board_in):
  if col in moveRange and board_in[0][col]==defaultChar:
    return True
  else:
    return False

#Execute Player's move
def playerMove():
  global board
  while True:
    move = input('Enter your column: ')
    if move=='' or not move.isdigit():
      print('Enter a number!')
      continue
    move = int(move)
    if isValid(move,board):
      break
    else:
      print('That move is invalid!')
  board = placePiece('O',move,board)

#Place a gamepiece
def placePiece(char,col,board_in):
  foundSpot = False
  for row in range(6):
    if board_in[row][col]!=defaultChar:
      board_in[row-1][col] = char
      foundSpot = True
      break
  if not foundSpot:
    board_in[5][col] = char
  return board_in

#MonteCarlo AI Simulation
def AIMove(AIChar):
  global board
  bestWins = 0
  bestColumn = None
  #Go through each possible valid move
  for column in moveRange:
    if isValid(column,board):
      #Set aiWins to 0 to start fresh for each column
      aiWins = 0
      #Run x possible outcomes with selected column as first move
      for runs in range(100):
        #Set testGameOver to False to start fresh each test game
        testGameOver = 0
        #Copy the current gameboard to a test board
        testBoard = copy.deepcopy(board)
        #set first move to selected column
        aiMove = column
        testBoard = placePiece(AIChar,aiMove,testBoard)
        testGameOver = checkWin(AIChar,testBoard)
        if testGameOver==1: #If the next move wins the game
         aiWins+=1
        #Now randomly evaluate the rest of the game...

        while testGameOver==0:
            #Simulate random player and AI movements
            plMove = randMove(testBoard)#player moves first after AI
            testBoard = placePiece('O',plMove,testBoard)
            testGameOver = checkWin('O',testBoard)
            if testGameOver==1:#If player wins,run another game
              break
            aiMove = randMove(testBoard)#ai moves next
            testBoard = placePiece(AIChar,aiMove,testBoard)
            testGameOver = checkWin(AIChar,testBoard)
            if testGameOver==1:#If AI wins, note the win and run another game
              aiWins+=1 
              break
      #If the evaluated column yields the best results so far,
      #Save the results and the column
      if aiWins>bestWins: 
        bestWins = aiWins
        bestColumn = column
  
      #If every move results in immediate player win,
      #Set AI to move to first open spot (as it won't matter where it goes)
      if bestWins==None:
        for column in moveRange:
          if isValid(column,board):
            bestColumn = column
  #Return the best option for the AI's next move
  if bestWins>70 and bestWins<80:
    print('\nWatch out! The AI is closing in!')
  elif bestWins>80 and bestWins!=100:
    print('\nThere\'s no escape now...')
  board = placePiece(AIChar,bestColumn,board)

#Gets a random valid move
def randMove(board_in):
   while True:
    move = random.randint(0,6)
    if isValid(move,board_in):
      return move

#This can be used to have an easier AI that moves randomly
def easyAIMove(char):
  global board
  aiMove = randMove(board)
  board = placePiece(char,aiMove,board)


def checkWin(char,board_in):
  #Check if there is a win or tie condition
  for row in range(6):
    for col in range(7):
      if board_in[row][col]==char:
        if checkVert(row,col,board_in) or checkHorizontal(row,col,board_in) or checkDiag(row,col,board_in):
          return 1
  if all(not isValid(x,board_in) for x in moveRange):
    #If no valid moves remain
    return -1
  return 0

def checkVert(row,col,board_in):
  if row<=2:
    column = nthcolumn(col,board_in)
    if all(x==column[row] for x in column[row:row+4]):
      return True
  return False

def checkHorizontal(row,col,board_in):
  if col<=3:
    row = board_in[:][row]
    if all(x == row[col] for x in row[col:col+4]):
      return True
  return False

def checkDiag(row,col,board_in):
  #SE diag
  if row<=2 and col<=3:
    diag = [board_in[i-(col-row)][i] for i in range(col, col+4)]
    if all(x==diag[0] for x in diag):
      return True
  #SW diag
  if row<=2 and col>=3:
    diag = [board_in[row+(col-i)][i] for i in range(col,col-4,-1)]
    if all(x==diag[0] for x in diag):
      return True
  return False

def checkAllWins(board_in):
  global gameOver
  if checkWin('O',board_in)==1:
    gameOver = True
    print('O\'s win!')
  elif checkWin('X',board_in)==1:
    gameOver = True
    print('X\'s win!')
  elif checkWin('O',board_in)==-1:
    print('It\'s a tie!')



#Init blank board
board = []
defaultChar = ' '
for boardRows in range(6):
  board.append([defaultChar,defaultChar,defaultChar,defaultChar,defaultChar,defaultChar,defaultChar])

moveRange = list(range(7))
gameOver = False
print_board(board)
while not gameOver:
  playerMove()
  checkAllWins(board)
  print_board(board)
  if not gameOver:
    print('-----AI TURN-----')
    AIMove('X') #replace this with: 'easyAIMove('X')'  to have the AI move randomly
    print_board(board)
    checkAllWins(board)

  if gameOver:
    response = input('Hit \'R\' and enter to play again or just hit enter to quit: ')
    if response.upper()=='R':
      gameOver = False
      board = []
      for boardRows in range(6):
        board.append([defaultChar,defaultChar,defaultChar,defaultChar,defaultChar, defaultChar,  defaultChar])
      print_board(board)