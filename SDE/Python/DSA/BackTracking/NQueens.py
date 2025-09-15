board = 0
n = 0


def print_board():
    for v in board:
        for i in v:
            if i == 0:
                print('*', end=" ")
            else:
                print('Q', end=" ")
        print('\n')
#00 01 02 03 04
#10 11 12 13 14
#20 21 22 23 24
#30 31 32 33 34

def canplace(i,j):
    #check up
    x = i
    y = j
    while  x>=0 :
        if board[x][y] ==1:
            return False
        x-=1

    #check left up
    x = i
    y = j
    while x >= 0 and y >= 0:
        if board[x][y] == 1:
            return False
        x -= 1
        y -= 1
    #chec right up
    x = i
    y = j
    while x >= 0 and y < n:
        if board[x][y] == 1:
            return False
        x -= 1
        y += 1
    return True

def solvenqueens(i):
    if i>=n:
        return True
    for k in range(0,n):
        if(canplace(i,k)):
            board[i][k]= 1
            if(solvenqueens(i+1)):
                return True
            board[i][k]=0
    return False

n = int(input(('enter number of Queens..')))
print()
board = [[0 for _ in range(n)] for _ in range(n)]


if(solvenqueens(0)):
    print_board()
else:
    print("solution not possible")
   # print_board()

