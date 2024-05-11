# Place your creative task here!

# Be clever, be creative, have fun!

from cmu_graphics import *
import random
import math

def onAppStart(app):
    app.rows = 15
    app.cols = 10
    app.boardLeft = 95
    app.boardTop = 50
    app.boardWidth = 210
    app.boardHeight = 280
    app.cellBorderWidth = 1
    restartApp(app)
    
def restartApp(app):
    app.count=0
    app.paused=False
    app.board = [([None] * app.cols) for row in range(app.rows)]
    loadTetrisPieces(app)
    app.nextPieceIndex=0
    loadNextPiece(app)
    app.gameOver=False
    app.score=0

def onStep(app):
    app.count+=1
    if(app.count%10==0):
        if not app.paused:
            takeStep(app)
        
def takeStep(app):
    if not movePiece(app, +1, 0):
        # We could not move the piece, so place it on the board:
        placePieceOnBoard(app)
        removeFullRows(app)
        loadNextPiece(app)
        
        
def removeFullRows(app):
    i=0
    popedRows=0
    while i<app.rows:
        if checkRowIsFull(app.board[i]):
            app.board.pop(i)
            app.board.insert(0,[None]*app.cols)
            popedRows+=1
        else:
            i+=1
    # scoring system
    if(popedRows==1):
        app.score+=2
    if(popedRows==2):
        app.score+=5
    if(popedRows==3):
        app.score+=10
    if(popedRows==4):
        app.score+=15
        
def checkRowIsFull(row):
    for i in row:
        if i==None:
            return False
    return True
            
def placePieceOnBoard(app): 
    rows=len(app.piece)
    cols=len(app.piece[0])
    for row in range(rows):
        for col in range(cols):
            if app.piece[row][col]==True:
                rowInBoard=app.pieceTopRow+row
                colInBoard=app.pieceLeftCol+col
                # change color on board
                app.board[rowInBoard][colInBoard]=app.pieceColor
                
def loadNextPiece(app):
    pieceIndex = random.randrange(len(app.tetrisPieces))
    loadPiece(app,pieceIndex)
    # overelaping
    if (pieceIsLegal(app)):
        return 
    else:
        app.gameOver=True

def loadPiece(app,pieceIndex):
    app.piece=app.tetrisPieces[pieceIndex]
    app.pieceColor=app.tetrisPieceColors[pieceIndex]
    setPieceLocation(app)
    
def movePiece(app, drow, dcol):
    app.pieceTopRow+=drow
    app.pieceLeftCol+=dcol
    if(pieceIsLegal(app)):
        return True 
    else:
        app.pieceTopRow-=drow
        app.pieceLeftCol-=dcol
        return False
        
def hardDropPiece(app):
    while movePiece(app, +1, 0):
        pass
    
def pieceIsLegal(app):
    rows=len(app.piece)
    cols=len(app.piece[0])
    # check out of bounds
    if(rows+app.pieceTopRow>app.rows or app.pieceTopRow<0 or cols+app.pieceLeftCol>app.cols or app.pieceLeftCol<0):
        return False
    else:
        # check overlapping
        for row in range(rows):
            for col in range(cols):
                if app.piece[row][col]==True:
                    rowInBoard=app.pieceTopRow+row
                    colInBoard=app.pieceLeftCol+col
                    if not app.board[rowInBoard][colInBoard]==None:
                        return False
    return True 
    
def setPieceLocation(app):
    app.pieceTopRow=0
    pieceCols=len(app.piece[0])
    app.pieceLeftCol=app.cols//2-pieceCols//2
    if(app.cols%2==0 and pieceCols%2==1):
        app.pieceLeftCol-=1

def onKeyPress(app,key):
    if ('0'<=key<='6'):
        app.board = [([None] * app.cols) for row in range(app.rows)]
        loadPiece(app,int(key))
    if(key=='right'):
        movePiece(app, 0, 1)
    elif key == 'left':
        movePiece(app, 0, -1)
    elif key == 'down':
        movePiece(app, 1, 0)
    elif key == 'space':
        hardDropPiece(app)
    elif key=='up':
        rotatePieceClockwise(app)
    elif key == 's': takeStep(app)
    elif key in ['a','b','c','d','e','f','g','h']:
        loadTestBoard(app, key)
    elif(key=='p'):
        app.paused=not app.paused
    elif(key=='r'):
        restartApp(app)
    
def loadTestBoard(app, key):
    # DO NOT EDIT THIS FUNCTION
    # We are providing you with this function to set up the board
    # with some test cases for clearing the rows.
    # To use this: press 'a', 'b', through 'h' to select a test board.
    # Then press 'space' for a hard drop of the red I,
    # and then press 's' to step, which in most cases will result
    # in some full rows being cleared.

    # 1. Clear the board and load the red I piece 
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.nextPieceIndex = 0
    loadNextPiece(app)
    # 2. Move and rotate the I piece so it is vertical, in the
    #    top-left corner
    for keyName in ['down', 'down', 'up', 'left', 'left', 'left']:
        onKeyPress(app, keyName)
    # 3. Add a column of alternating plum and lavender cells down
    #    the rightmost column
    for row in range(app.rows):
        app.board[row][-1] = 'plum' if (row % 2 == 0) else 'lavender'
    # 4. Now almost fill some of the bottom rows, leaving just the
    #    leftmost column empty
    indexesFromBottom = [ [ ], [0], [0,1], [0,1,2], [0,2],
                          [1,2,3], [1,2,4], [0,2,3,5] ]
    colors = ['moccasin', 'aqua', 'khaki', 'aquamarine',
              'darkKhaki', 'peachPuff']
    for indexFromBottom in indexesFromBottom[ord(key) - ord('a')]:
        row = app.rows - 1 - indexFromBottom
        color = colors[indexFromBottom]
        for col in range(1, app.cols):
            app.board[row][col] = color
        
def rotatePieceClockwise(app):
    # old variables
    oldPiece = app.piece
    oldTopRow = app.pieceTopRow
    oldLeftCol = app.pieceLeftCol
    oldRows=len(app.piece)
    oldCols=len(app.piece[0])
    # rotate
    app.piece = rotate2dListClockwise(app.piece)
    # new positions
    newRows=len(app.piece)
    newCols=len(app.piece[0])
    centerRow = oldTopRow + oldRows//2
    app.pieceTopRow = centerRow - newRows//2
    centerCol = oldLeftCol + oldCols//2
    app.pieceLeftCol = centerCol - newCols//2
    # only rorate if is legal
    if(pieceIsLegal(app)):
        return 
    else:
        app.piece=oldPiece
        app.pieceTopRow=oldTopRow
        app.pieceLeftCol=oldLeftCol
        
def drawPiece(app):
    rows=len(app.piece)
    cols=len(app.piece[0])
    for row in range(rows):
        for col in range(cols):
            if app.piece[row][col]:
                drawCell(app, row+app.pieceTopRow, col+app.pieceLeftCol,app.pieceColor)
    
def loadTetrisPieces(app):
    # Seven "standard" pieces (tetrominoes)
    iPiece = [[  True,  True,  True,  True ]]
    jPiece = [[  True, False, False ],
              [  True,  True,  True ]]
    lPiece = [[ False, False,  True ],
              [  True,  True,  True ]]
    oPiece = [[  True,  True ],
              [  True,  True ]]
    sPiece = [[ False,  True,  True ],
              [  True,  True, False ]]
    tPiece = [[ False,  True, False ],
              [  True,  True,  True ]]
    zPiece = [[  True,  True, False ],
              [ False,  True,  True ]] 
    app.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece,
                         sPiece, tPiece, zPiece ]
    app.tetrisPieceColors = [ 'red', 'yellow', 'magenta', 'pink',
                              'cyan', 'green', 'orange' ]

def redrawAll(app):
    if(app.gameOver==True):
        drawLabel('Game Over',200,200,size=30)
        drawLabel(f'you have Scored {app.score}, points',200,250,size=16)
        drawLabel(f'press key r to restart',200,300,size=16)
    else:
        drawLabel(f'score: {app.score}',50,30,size=16)
        drawLabel('Tetris (Step 7)', 200, 30, size=16)
        drawBoard(app)
        if(app.piece!=None):
            drawPiece(app)
        drawBoardBorder(app)
    
# **********************************************
# drawBoard Section
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col,app.board[row][col])

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def resizeBoard(app, numRows, numCols, boardSize):
    app.rows = numRows
    app.cols = numCols
    app.boardLeft, app.boardWidth, app.boardHeight = boardSize
    app.board = [([None] * app.cols) for row in range(app.rows)]

def rotate2dListClockwise(L):
    oldRows=len(L)
    oldCols=len(L[0])
    newRows=oldCols
    newCols=oldRows
    newList=[]
    for oldCol in range(oldCols):
        newCurrRow=[]
        for oldRow in range(oldRows-1,-1,-1):
            newCurrRow.append(L[oldRow][oldCol])
        newList.append(newCurrRow)
    return newList
    


def main():
    # app = runApp()
    runApp()

main()