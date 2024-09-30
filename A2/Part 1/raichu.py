# raichu.py : Play the game of Raichu
# Team/Contributor: Chetan Sahrudhai Kimidi (ckimidi)
# Based on skeleton code by D. Crandall, Oct 2021
import sys, time, copy

def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

def totalMovingPoss(board, color):
    possibilities = []
    for loopvar1 in range(len(board[0])):
        for loopvar2 in range(len(board[0])):
            if board[loopvar1][loopvar2] == 'w' or board[loopvar1][loopvar2] == 'b':
               possibilities.extend(Pichu(board, loopvar1, loopvar2, color))
            if board[loopvar1][loopvar2] == 'W' or board[loopvar1][loopvar2] == 'B':
               possibilities.extend(Pikachu(board, loopvar1, loopvar2, color))
            if board[loopvar1][loopvar2] == '@' or board[loopvar1][loopvar2] == '$':
               possibilities.extend(Raichu(board, loopvar1, loopvar2, color))
    possibilities.reverse()
    return sorted(possibilities, key = lambda val:(-val[1], val[0]))

def UpgradeToRai(board, color, die):
    points = 0
    temp = copy.deepcopy(board)
    for loopvar in range(0, len(temp)):
        if temp[0][loopvar] == 'b' or temp[0][loopvar] == 'B':
            temp[0][loopvar] = '$'
        elif temp[len(temp) - 1][loopvar] == 'w' or temp[len(temp) - 1][loopvar] == 'W':
            temp[len(temp)-1][loopvar] = '@'
    points = cost(temp, color, die)
    return (temp, points)

def Pichu(board, x, y, color):
    result = []
    if board[x][y] == color and color == 'w':
        PichuCoordinates = []
        if y != 0 and y != len(board) - 1 and x < len(board) - 1:
            PichuCoordinates = [(x+1,y-1), (x+1,y+1)]
        elif y == 0 and x < x <len(board) - 1:
            PichuCoordinates = [(x+1, y+1)]
        elif y == len(board) - 1 and x < len(board) - 1:
            PichuCoordinates = [(x+1, y-1)]
        for coord in PichuCoordinates:
            if board[coord[0]][coord[1]] == '.':
                PichuTempB = copy.deepcopy(board)
                PichuTempB[coord[0]][coord[1]] = 'w'
                PichuTempB[x][y] = '.'
                result.append(UpgradeToRai(PichuTempB, color, 0))
            if board[coord[0]][coord[1]] == 'b': 
                if coord[1] < y and coord[0] < len(board) - 1:
                    if coord[1] == 0:
                        break
                    else:
                        PichuTempB = copy.deepcopy(board)
                        if PichuTempB[coord[0] + 1][coord[1] - 1] == '.':
                            PichuTempB[coord[0] + 1][coord[1] - 1] = 'w'
                            PichuTempB[coord[0]][coord[1]] = '.'
                            PichuTempB[x][y] = '.'
                            result.append(UpgradeToRai(PichuTempB, color, 1))
                elif coord[1] != len(board) - 1 and coord[0] < len(board) - 1 and coord[1] > y:
                    PichuTempB = copy.deepcopy(board)
                    if PichuTempB[coord[0] + 1][coord[1] + 1] == '.':
                        PichuTempB[coord[0] + 1][coord[1] + 1] = 'w'
                        PichuTempB[coord[0]][coord[1]] = '.'
                        PichuTempB[x][y] = '.'
                        result.append(UpgradeToRai(PichuTempB, color, 1))                                
    elif color == 'b' and board[x][y] == 'b':
        PichuCoordinates = []
        if y != 0 and y != len(board) - 1 and x > 0:
            PichuCoordinates = [(x-1,y-1), (x-1,y+1)]
        elif y == 0 and x > 0:
            PichuCoordinates = [(x-1, y+1)]
        elif y == len(board) - 1 and x > 0:
            PichuCoordinates=[(x-1, y-1)]
        for coord in PichuCoordinates:
            if board[coord[0]][coord[1]] == '.':
                PichuTempB = copy.deepcopy(board)
                PichuTempB[coord[0]][coord[1]] = 'b'
                PichuTempB[x][y] = '.'
                result.append(UpgradeToRai(PichuTempB, color, 0))
            if board[coord[0]][coord[1]] == 'w': 
                if coord[1] < y and coord[1] != 0 and coord[0] > 0:
                    PichuTempB = copy.deepcopy(board)
                    if PichuTempB[coord[0] - 1][coord[1] - 1] == '.':
                        PichuTempB[coord[0] - 1][coord[1] - 1] = 'b'
                        PichuTempB[coord[0]][coord[1]] = '.'
                        PichuTempB[x][y] = '.'
                        result.append(UpgradeToRai(PichuTempB, color, 1))
                elif coord[1] < len(board) - 1 and coord[0] > 0 and coord[1] > y:
                    PichuTempB = copy.deepcopy(board)
                    if PichuTempB[coord[0] - 1][coord[1] + 1] == '.':
                        PichuTempB[coord[0] - 1][coord[1] + 1] = 'b'
                        PichuTempB[coord[0]][coord[1]] = '.'
                        PichuTempB[x][y] = '.'
                        result.append(UpgradeToRai(PichuTempB, color, 1))
    return result

def Pikachu(board, x, y, color):
    result = []
    if color.upper() == 'W' and board[x][y] == 'W':
        PikachuCoordinates = []
        if y > 0 and y < len(board) - 1:
            if x < len(board) - 1:
                PikachuCoordinates = [(x + 1, y), (x, y-1), (x, y+1)]
            else:
                PikachuCoordinates = [(x, y - 1),(x, y + 1)]
        elif y == 0:
            if x < len(board) - 1:
                PikachuCoordinates = [(x+1, y),(x, y+1)]
            else:
                PikachuCoordinates = [(x, y+1)]
        elif y == len(board) - 1:
            if x < len(board) - 1:
                PikachuCoordinates = [(x+1, y), (x, y-1)]
            else:
                PikachuCoordinates = [(x, y-1)]

        for coord in PikachuCoordinates:
            if board[coord[0]][coord[1]] == '.':
                PikaTempB = copy.deepcopy(board)
                PikaTempB[coord[0]][coord[1]] = 'W'
                PikaTempB[x][y] = '.'
                result.append(UpgradeToRai(PikaTempB, color, 0))
                if coord[1] == y  and coord[0] < len(board) - 1:
                    if board[coord[0] + 1][coord[1]] == '.':
                        PikaTempB = copy.deepcopy(board)
                        PikaTempB[coord[0] + 1][coord[1]] = 'W'
                        PikaTempB[x][y] = '.'
                        result.append(UpgradeToRai(PikaTempB, color, 0))
                    if (board[coord[0] + 1][coord[1]] == 'B' or board[coord[0] + 1][coord[1]] == 'b') and coord[0] + 1 < len(board) - 1: 
                            PikaTempB = copy.deepcopy(board)
                            if PikaTempB[coord[0] + 2][coord[1]] == '.':
                                PikaTempB[coord[0] + 2][coord[1]] = 'W'
                                PikaTempB[coord[0] + 1][coord[1]] = '.'
                                PikaTempB[x][y] = '.'
                                result.append(UpgradeToRai(PikaTempB, color, 2))
                if  coord[1] > 0 and coord[1] < y:
                    if board[coord[0]][coord[1] - 1] == '.':
                        PikaTempB = copy.deepcopy(board)
                        PikaTempB[coord[0]][coord[1] - 1] = 'W'
                        PikaTempB[x][y] = '.'
                        result.append(UpgradeToRai(PikaTempB, color, 0))
                    if (board[coord[0]][coord[1] - 1] == 'B' or board[coord[0]][coord[1] - 1] == 'b') and coord[1] -1 > 0: 
                            PikaTempB = copy.deepcopy(board)
                            if PikaTempB[coord[0]][coord[1] - 2] == '.':
                                PikaTempB[coord[0]][coord[1] - 2] = 'W'
                                PikaTempB[coord[0]][coord[1] - 1] = '.'
                                PikaTempB[x][y] = '.'
                                result.append(UpgradeToRai(PikaTempB, color, 2))

                if  coord[1]<len(board)-1 and coord[1]>y:
                    if board[coord[0]][coord[1]+1] == '.':
                        PikaTempB = copy.deepcopy(board)
                        PikaTempB[coord[0]][coord[1]+1]='W'
                        PikaTempB[x][y]='.'
                        result.append(UpgradeToRai(PikaTempB,color,0))
                    if (board[coord[0]][coord[1]+1] == 'B'  or board[coord[0]][coord[1]+1] == 'b') and coord[1]+1<len(board)-1: 
                            PikaTempB = copy.deepcopy(board)
                            if PikaTempB[coord[0]][coord[1]+2] == '.':
                                PikaTempB[coord[0]][coord[1]+2] = 'W'
                                PikaTempB[coord[0]][coord[1]+1]='.'
                                PikaTempB[x][y]='.'
                                result.append(UpgradeToRai(PikaTempB,color,2))
            elif board[coord[0]][coord[1]] == 'b' or board[coord[0]][coord[1]] == 'B':
                if coord[1]==y  and coord[0]<len(board)-1:
                    if board[coord[0]+1][coord[1]] == '.':
                        PikaTempB = copy.deepcopy(board)
                        PikaTempB[coord[0]][coord[1]]='.'
                        PikaTempB[coord[0]+1][coord[1]]='W'
                        PikaTempB[x][y]='.'
                        result.append(UpgradeToRai(PikaTempB,color,2))
                if  coord[1]>0 and coord[1]<y:
                    if board[coord[0]][coord[1]-1] == '.':
                        PikaTempB = copy.deepcopy(board)
                        PikaTempB[coord[0]][coord[1]]='.'
                        PikaTempB[coord[0]][coord[1]-1]='W'
                        PikaTempB[x][y]='.'
                        result.append(UpgradeToRai(PikaTempB,color,2))
                if  coord[1]<len(board)-1 and coord[1]>y:
                    if board[coord[0]][coord[1]+1] == '.':
                        PikaTempB = copy.deepcopy(board)
                        PikaTempB[coord[0]][coord[1]]='.'
                        PikaTempB[coord[0]][coord[1]+1]='W'
                        PikaTempB[x][y]='.'
                        result.append(UpgradeToRai(PikaTempB,color,2))

    elif color=='b' and board[x][y]=='B':
        PikachuCoordinates=[]
        if y>0 and y< len(board)-1:
            if x>0:
                PikachuCoordinates=[(x-1,y),(x,y-1),(x,y+1)]
            else:
                PikachuCoordinates=[(x,y-1),(x,y+1)]
        elif y==0:
            if x>0:
                PikachuCoordinates=[(x-1,y),(x,y+1)]
            else:
                PikachuCoordinates=[(x,y+1)]
        elif y == len(board)-1:
            if x>0:
                PikachuCoordinates=[(x-1,y),(x,y-1)]
            else:
                PikachuCoordinates=[(x,y-1)]

        for coord in PikachuCoordinates:
            if board[coord[0]][coord[1]] == '.':
                PikaTempB = copy.deepcopy(board)
                PikaTempB[coord[0]][coord[1]]='B'
                PikaTempB[x][y]='.'
                result.append(UpgradeToRai(PikaTempB,color,0))
                if coord[1]==y  and coord[0]>0:
                    if board[coord[0]-1][coord[1]] == '.':
                        PikaTempB = copy.deepcopy(board)
                        PikaTempB[coord[0]-1][coord[1]]='B'
                        PikaTempB[x][y]='.'
                        result.append(UpgradeToRai(PikaTempB,color,0))
                    elif (board[coord[0]-1][coord[1]] == 'W' or board[coord[0]-1][coord[1]] =='w')  and coord[0]-1 > 0: 
                            PikaTempB = copy.deepcopy(board)
                            if PikaTempB[coord[0]-2][coord[1]] == '.':
                                PikaTempB[coord[0]-2][coord[1]] = 'B'
                                #replace B to .
                                PikaTempB[coord[0]-1][coord[1]] = '.'
                                PikaTempB[x][y]='.'
                                result.append(UpgradeToRai(PikaTempB, color, 2))

                if  coord[1]>0 and coord[1]<y:
                    if board[coord[0]][coord[1]-1] == '.':
                        PikaTempB = copy.deepcopy(board)
                        PikaTempB[coord[0]][coord[1]-1]='B'
                        PikaTempB[x][y]='.'
                        result.append(UpgradeToRai(PikaTempB,color,0))
                    if (board[coord[0]][coord[1]-1] == 'W' or board[coord[0]][coord[1]-1] == 'w') and coord[0]-1>0: 
                            PikaTempB = copy.deepcopy(board)
                            if PikaTempB[coord[0]][coord[1]-2] == '.':
                                PikaTempB[coord[0]][coord[1]-2] = 'B'
                                #replace B to .
                                PikaTempB[coord[0]][coord[1]-1]='.'
                                PikaTempB[x][y]='.'
                                result.append(UpgradeToRai(PikaTempB,color,2))

                if  coord[1] < len(board)-1 and coord[1] > y:
                    if board[coord[0]][coord[1]+1] == '.':
                        PikaTempB = copy.deepcopy(board)
                        PikaTempB[coord[0]][coord[1]+1]='B'
                        PikaTempB[x][y] = '.'
                        result.append(UpgradeToRai(PikaTempB,color,0))
                    if (board[coord[0]][coord[1]+1] == 'W' or board[coord[0]][coord[1]+1] == 'w') and coord[1]+1<len(board)-1: 
                            PikaTempB = copy.deepcopy(board)
                            if PikaTempB[coord[0]][coord[1]+2] == '.':
                                PikaTempB[coord[0]][coord[1]+2] = 'B'
                                #replace B to .
                                PikaTempB[coord[0]][coord[1]+1]='.'
                                PikaTempB[x][y]='.'
                                result.append(UpgradeToRai(PikaTempB,color,2))
                                
            elif board[coord[0]][coord[1]] == 'w' or board[coord[0]][coord[1]] == 'W':
                if coord[1]==y  and coord[0]>0:
                    if board[coord[0]-1][coord[1]] == '.':
                        PikaTempB = copy.deepcopy(board)
                        PikaTempB[coord[0]][coord[1]]='.'
                        PikaTempB[coord[0]-1][coord[1]]='B'
                        PikaTempB[x][y]='.'
                        result.append(UpgradeToRai(PikaTempB,color,2))
                    else:
                        continue
                if  coord[1]>0 and coord[1]<y:
                    if board[coord[0]][coord[1]-1] == '.':
                        PikaTempB = copy.deepcopy(board)
                        PikaTempB[coord[0]][coord[1]]='.'
                        PikaTempB[coord[0]][coord[1]-1]='B'
                        PikaTempB[x][y]='.'
                        result.append(UpgradeToRai(PikaTempB,color,2))
                if  coord[1]<len(board)-1 and coord[1]>y:
                    if board[coord[0]][coord[1]+1] == '.':
                        PikaTempB = copy.deepcopy(board)
                        PikaTempB[coord[0]][coord[1]]='.'
                        PikaTempB[coord[0]][coord[1]+1]='B'
                        PikaTempB[x][y]='.'
                        result.append(UpgradeToRai(PikaTempB,color,2))
    return result

def Raichu(board, a, b, color):
    VulnerBlacks = '@wW'
    VulnerWhites = '$bB'
    result = []
    if board[a][b]=='@' and color=='w':
        for v1 in range(a-1,-1,-1):
            if board[v1][b]=='.':
                RaiTempB = copy.deepcopy(board)
                RaiTempB[v1][b]='@'
                RaiTempB[a][b]='.'
                result.append(UpgradeToRai(RaiTempB,color,0))
            elif board[v1][b] in VulnerWhites and v1>0:
                if board[v1-1][b]!='.':
                    break
                else:
                    RaiTempB = copy.deepcopy(board)
                    RaiTempB[v1-1][b]='@'
                    RaiTempB[a][b]='.'
                    RaiTempB[v1][b]='.'
                    if  board[v1][b] == '$':
                        result.append(UpgradeToRai(RaiTempB,color,20))
                    elif board[v1][b] == 'B':
                        result.append(UpgradeToRai(RaiTempB,color,10))
                    else:
                        result.append(UpgradeToRai(RaiTempB,color,5))
                    break
            else:
                break
        
        for v1 in range(a+1,len(board)):
            if board[v1][b]=='.':
                RaiTempB = copy.deepcopy(board)
                RaiTempB[v1][b]='@'
                RaiTempB[a][b]='.'
                result.append(UpgradeToRai(RaiTempB,color,0))
            elif board[v1][b] in VulnerWhites and v1<len(board)-1 :
                if board[v1+1][b]!='.':
                    break
                else:
                    RaiTempB = copy.deepcopy(board)
                    RaiTempB[v1+1][b]='@'
                    RaiTempB[a][b]='.'
                    RaiTempB[v1][b]='.'
                    if  board[v1][b] == '$':
                        result.append(UpgradeToRai(RaiTempB,color,20))
                    elif board[v1][b] == 'B':
                        result.append(UpgradeToRai(RaiTempB,color,10))
                    else:
                        result.append(UpgradeToRai(RaiTempB,color,5))
                    break
            else:
                break

        for v1 in range(b-1,-1,-1):
            if board[a][v1]=='.':
                RaiTempB = copy.deepcopy(board)
                RaiTempB[a][v1]='@'
                RaiTempB[a][b]='.'
                result.append(UpgradeToRai(RaiTempB,color,0))
            elif board[a][v1] in VulnerWhites and v1>0:
                if board[a][v1-1]!='.':
                    break
                else:
                    RaiTempB = copy.deepcopy(board)
                    RaiTempB[a][v1-1]='@'
                    RaiTempB[a][b]='.'
                    RaiTempB[a][v1]='.'
                    if  board[a][v1] == '$':
                        result.append(UpgradeToRai(RaiTempB,color,20))
                    elif board[a][v1] == 'B':
                        result.append(UpgradeToRai(RaiTempB,color,10))
                    else:
                        result.append(UpgradeToRai(RaiTempB,color,5))
                    break
            else:
                break
        
        for v1 in range(b+1,len(board)):
            if board[a][v1]=='.':
                RaiTempB = copy.deepcopy(board)
                RaiTempB[a][v1]='@'
                RaiTempB[a][b]='.'
                result.append(UpgradeToRai(RaiTempB,color,0))
            elif board[a][v1] in VulnerWhites and v1<len(board)-1:
                if board[a][v1+1]!='.':
                    break
                else:
                    RaiTempB = copy.deepcopy(board)
                    RaiTempB[a][v1+1]='@'
                    RaiTempB[a][b]='.'
                    RaiTempB[a][v1]='.'
                    if board[a][v1] == '$':
                        result.append(UpgradeToRai(RaiTempB,color,20))
                    elif board[a][v1] == 'B':
                        result.append(UpgradeToRai(RaiTempB,color,10))
                    else:
                        result.append(UpgradeToRai(RaiTempB,color,5))
                    break
            else:
                break
        
        for (v1,v2) in zip(range(a-1,-1,-1),range(b+1,len(board))):
            if board[v1][v2]=='.':
                RaiTempB = copy.deepcopy(board)
                RaiTempB[v1][v2]='@'
                RaiTempB[a][b]='.'
                result.append(UpgradeToRai(RaiTempB,color,0))
            elif board[v1][v2] in VulnerWhites and v1>0 and v2<len(board)-1:
                if board[v1-1][v2+1]!='.':
                    break
                else:
                    RaiTempB = copy.deepcopy(board)
                    RaiTempB[v1-1][v2+1]='@'
                    RaiTempB[a][b]='.'
                    RaiTempB[v1][v2]='.'
                    if board[v1][v2] == '$':
                        result.append(UpgradeToRai(RaiTempB,color,20))
                    elif board[v1][v2] == 'B':
                        result.append(UpgradeToRai(RaiTempB,color,10))
                    else:
                        result.append(UpgradeToRai(RaiTempB,color,5))
                    break
            else:
                break
                
        
        for (v1,v2) in zip(range(a+1,len(board)),range(b-1,-1,-1)):
            if board[v1][v2]=='.':
                RaiTempB = copy.deepcopy(board)
                RaiTempB[v1][v2]='@'
                RaiTempB[a][b]='.'
                result.append(UpgradeToRai(RaiTempB,color,0))
            elif (board[v1][v2] in VulnerWhites) and v1<len(board)-1 and v2>0 : 
                if board[v1+1][v2-1]!='.':
                    break
                else:
                    RaiTempB = copy.deepcopy(board)
                    RaiTempB[v1+1][v2-1]='@'
                    RaiTempB[a][b]='.'
                    RaiTempB[v1][v2]='.'
                    if board[v1][v2] == '$':
                        result.append(UpgradeToRai(RaiTempB,color,20))
                    elif board[v1][v2] == 'B':
                        result.append(UpgradeToRai(RaiTempB,color,10))
                    else:
                        result.append(UpgradeToRai(RaiTempB,color,5))
                    break
            else:
                break
            
        
        for (v1,v2) in zip(range(a-1,-1,-1),range(b-1,-1,-1)):
            if board[v1][v2]=='.':
                RaiTempB = copy.deepcopy(board)
                RaiTempB[v1][v2]='@'
                RaiTempB[a][b]='.'
                result.append(UpgradeToRai(RaiTempB,color,0))
            elif board[v1][v2] in VulnerWhites and v1>0 and v2>0:
                if board[v1-1][v2-1]!='.':
                    break
                else:
                    RaiTempB = copy.deepcopy(board)
                    RaiTempB[v1-1][v2-1]='@'
                    RaiTempB[a][b]='.'
                    RaiTempB[v1][v2]='.'
                    if board[v1][v2] == '$':
                        result.append(UpgradeToRai(RaiTempB,color,20))
                    elif board[v1][v2] == 'B':
                        result.append(UpgradeToRai(RaiTempB,color,10))
                    else:
                        result.append(UpgradeToRai(RaiTempB,color,5))
                    break
            else:
                break
        
        for (v1,v2) in zip(range(a+1,len(board)),range(b+1,len(board))):
            if board[v1][v2]=='.':
                RaiTempB = copy.deepcopy(board)
                RaiTempB[v1][v2]='@'
                RaiTempB[a][b]='.'
                result.append(UpgradeToRai(RaiTempB,color,0))
            elif board[v1][v2] in VulnerWhites and v1<len(board)-1 and v2< len(board)-1 :
                if board[v1+1][v2+1]!='.':
                    break
                else:
                    RaiTempB = copy.deepcopy(board)
                    RaiTempB[v1+1][v2+1]='@'
                    RaiTempB[a][b]='.'
                    RaiTempB[v1][v2]='.'
                    if board[v1][v2] == '$':
                        result.append(UpgradeToRai(RaiTempB,color,20))
                    elif board[v1][v2] == 'B':
                        result.append(UpgradeToRai(RaiTempB,color,10))
                    else:
                        result.append(UpgradeToRai(RaiTempB,color,5))
                    break
            else:
                break
                
    elif board[a][b]=='$' and color=='b':
        
        for v1 in range(a-1,-1,-1):
            if board[v1][b]=='.':
                RaiTempB = copy.deepcopy(board)
                RaiTempB[v1][b]='$'
                RaiTempB[a][b]='.'
                result.append(UpgradeToRai(RaiTempB,color,0))
            elif board[v1][b] in VulnerBlacks and v1>0:
                if board[v1-1][b]!='.':
                    break
                else:
                    RaiTempB = copy.deepcopy(board)
                    RaiTempB[v1-1][b]='$'
                    RaiTempB[a][b]='.'
                    RaiTempB[v1][b]='.'
                    if board[v1][b] == '@':
                        result.append(UpgradeToRai(RaiTempB,color,20))
                    elif board[v1][b] == 'W':
                        result.append(UpgradeToRai(RaiTempB,color,10))
                    else:
                        result.append(UpgradeToRai(RaiTempB,color,5))
                    break
            else:
                break
        
        for v1 in range(a+1,len(board)):
            if board[v1][b]=='.':
                RaiTempB = copy.deepcopy(board)
                RaiTempB[v1][b]='$'
                RaiTempB[a][b]='.'
                result.append(UpgradeToRai(RaiTempB,color,0))
            elif board[v1][b] in VulnerBlacks and v1<len(board)-1:
                if board[v1+1][b]!='.':
                    break
                else:
                    RaiTempB = copy.deepcopy(board)
                    RaiTempB[v1+1][b]='$'
                    RaiTempB[a][b]='.'
                    RaiTempB[v1][b]='.'
                    if board[v1][b] == '@':
                        result.append(UpgradeToRai(RaiTempB,color,20))
                    elif board[v1][b] == 'W':
                        result.append(UpgradeToRai(RaiTempB,color,10))
                    else:
                        result.append(UpgradeToRai(RaiTempB,color,5))
                    break
            else:
                break
        
        for v1 in range(b-1,-1,-1):
            if board[a][v1]=='.':
                RaiTempB = copy.deepcopy(board)
                RaiTempB[a][v1]='$'
                RaiTempB[a][b]='.'
                result.append(UpgradeToRai(RaiTempB,color,0))
            elif board[a][v1] in VulnerBlacks and v1>0 :
                if board[a][v1-1]!='.':
                    break
                else:
                    RaiTempB = copy.deepcopy(board)
                    RaiTempB[a][v1-1]='$'
                    RaiTempB[a][b]='.'
                    RaiTempB[a][v1]='.'
                    if board[a][v1] == '@':
                        result.append(UpgradeToRai(RaiTempB,color,20))
                    elif board[a][v1] == 'W':
                        result.append(UpgradeToRai(RaiTempB,color,10))
                    else:
                        result.append(UpgradeToRai(RaiTempB,color,5))
                    break
            else:
                break
        
        for v1 in range(b+1,len(board)):
            if board[a][v1]=='.':
                RaiTempB = copy.deepcopy(board)
                RaiTempB[a][v1]='$'
                RaiTempB[a][b]='.'
                result.append(UpgradeToRai(RaiTempB,color,0))
            elif board[a][v1] in VulnerBlacks and v1<len(board)-1:
                if board[a][v1+1]!='.':
                    break
                else:
                    RaiTempB = copy.deepcopy(board)
                    RaiTempB[a][v1+1]='$'
                    RaiTempB[a][b]='.'
                    RaiTempB[a][v1]='.'
                    if board[a][v1] == '@':
                        result.append(UpgradeToRai(RaiTempB,color,20))
                    elif board[a][v1] == 'W':
                        result.append(UpgradeToRai(RaiTempB,color,10))
                    else:
                        result.append(UpgradeToRai(RaiTempB,color,5))
                    break
            else:
                break
        
        for (v1,v2) in zip(range(a-1,-1,-1),range(b+1,len(board))):
            if board[v1][v2]=='.':
                RaiTempB = copy.deepcopy(board)
                RaiTempB[v1][v2]='$'
                RaiTempB[a][b]='.'
                result.append(UpgradeToRai(RaiTempB,color,0))
            elif board[v1][v2] in VulnerBlacks and v1>0 and v2<len(board)-1:
                if board[v1-1][v2+1]!='.':
                    break
                else:
                    RaiTempB = copy.deepcopy(board)
                    RaiTempB[v1-1][v2+1]='$'
                    RaiTempB[a][b]='.'
                    RaiTempB[v1][v2]='.'
                    if board[v1][v2] == '@':
                        result.append(UpgradeToRai(RaiTempB,color,20))
                    elif board[v1][v2] == 'W':
                        result.append(UpgradeToRai(RaiTempB,color,10))
                    else:
                        result.append(UpgradeToRai(RaiTempB,color,5))
                    break
            else:
                break
                    
        
        for (v1,v2) in zip(range(a+1,len(board)),range(b-1,-1,-1)):
            if board[v1][v2]=='.':
                RaiTempB = copy.deepcopy(board)
                RaiTempB[v1][v2]='$'
                RaiTempB[a][b]='.'
                result.append(UpgradeToRai(RaiTempB,color,0))
            elif (board[v1][v2] in VulnerBlacks) and v1<len(board)-1 and v2>0:
                if board[v1+1][v2-1]!='.':
                    break
                else:
                    RaiTempB = copy.deepcopy(board)
                    RaiTempB[v1+1][v2-1]='$'
                    RaiTempB[a][b]='.'
                    RaiTempB[v1][v2]='.'
                    if board[v1][v2] == '@':
                        result.append(UpgradeToRai(RaiTempB,color,20))
                    elif board[v1][v2] == 'W':
                        result.append(UpgradeToRai(RaiTempB,color,10))
                    else:
                        result.append(UpgradeToRai(RaiTempB,color,5))
                    break
            else:
                break
            
        
        for (v1,v2) in zip(range(a-1,-1,-1),range(b-1,-1,-1)):
            if board[v1][v2]=='.':
                RaiTempB = copy.deepcopy(board)
                RaiTempB[v1][v2]='$'
                RaiTempB[a][b]='.'
                result.append(UpgradeToRai(RaiTempB,color,0))
            elif board[v1][v2] in VulnerBlacks and  v1>0 and v2>0:
                if board[v1-1][v2-1]!='.':
                    break
                else:
                    RaiTempB = copy.deepcopy(board)
                    RaiTempB[v1-1][v2-1]='$'
                    RaiTempB[a][b]='.'
                    RaiTempB[v1][v2]='.'
                    if board[v1][v2] == '@':
                        result.append(UpgradeToRai(RaiTempB,color,20))
                    elif board[v1][v2] == 'W':
                        result.append(UpgradeToRai(RaiTempB,color,10))
                    else:
                        result.append(UpgradeToRai(RaiTempB,color,5))
                    break
            else:
                break
        
        for (v1,v2) in zip(range(a+1,len(board)),range(b+1,len(board))):
            if board[v1][v2]=='.':
                RaiTempB = copy.deepcopy(board)
                RaiTempB[v1][v2]='$'
                RaiTempB[a][b]='.'
                result.append(UpgradeToRai(RaiTempB,color,0))
            elif board[v1][v2] in VulnerBlacks and v1<len(board)-1 and v2<len(board)-1:
                if board[v1+1][v2+1]!='.':
                    break
                else:
                    RaiTempB = copy.deepcopy(board)
                    RaiTempB[v1+1][v2+1]='$'
                    RaiTempB[a][b]='.'
                    RaiTempB[v1][v2]='.'
                    if board[v1][v2] == '@':
                        result.append(UpgradeToRai(RaiTempB,color,20))
                    elif board[v1][v2] == 'W':
                        result.append(UpgradeToRai(RaiTempB,color,10))
                    else:
                        result.append(UpgradeToRai(RaiTempB,color,5))
                    break
            else:
                break                    
    return result

def cost(board, color, die):
    whitePich = blackPich = whitePika = blackPika = whiteRai = blackRai = 0
    for loopvar1 in range(len(board[0])):
        for loopvar2 in range(len(board[0])):
            if board[loopvar1][loopvar2] == 'w':
                whitePich += 1
            elif board[loopvar1][loopvar2] == 'W':
                whitePika += 2
            elif board[loopvar1][loopvar2] == '@':
                whiteRai += 3
            elif board[loopvar1][loopvar2] == 'b':
                blackPich += 1
            elif board[loopvar1][loopvar2] == 'B':
                blackPika += 2
            elif board[loopvar1][loopvar2] == '$':
                blackRai += 3
    Pich = (whitePich-blackPich) + 1
    Pika = (whitePika-blackPika) + 3
    Rai = (whiteRai-blackRai) + 5
    if die:
        result = (Pich+Pika+Rai)*die*40
    else:
        result = (Pich+Pika+Rai)*20
    if color == 'w':
        return result
    else:
        return -result

def goal(board):
    whitePich = blackPich = 0
    for loopvar1 in range(len(board)):
        for loopvar2 in range(len(board[0])):
            if board[loopvar1][loopvar2]=='w' or board[loopvar1][loopvar2]=='W' or board[loopvar1][loopvar2]=='@':
                whitePich += 1
            if board[loopvar1][loopvar2]=='b' or board[loopvar1][loopvar2]=='B'or board[loopvar1][loopvar2]=='$':
                blackPich += 1
    if whitePich == 0 or blackPich == 0:
        return True
    else:
        return False

def prune(A, B, board, color, primary, depth): # Reference: AB (aplha-beta) pruning from https://www.youtube.com/watch?v=l-hh51ncgDI
    pruned = None
    for next,value in sorted(totalMovingPoss(board,color),key=lambda val:(val[1],val[0])):
        s = smallest(next,A,B,depth-1,color, primary)
        if s > value:
            value = s 
            pruned = next
    if pruned != None:
        pruned = ''.join([''.join(sigma) for sigma in pruned])
    return pruned
        
def smallest(board, A, B, depth, color, primary):
    if depth == 0 or goal(board):
       return cost(board, primary, B)
    sres = 1000000000
    color = 'b' if color == 'w' else 'w'
    for next,value in sorted(totalMovingPoss(board,color), key=lambda val:(-val[1],val[0])):
        g = greatest(next,A,B,depth-1,color, primary)
        g = max(sres,A)
        if g < B:
            B = g
        return g
    return sres

def greatest(board, A, B, depth, color, primary):
    if depth == 0 or goal(board):
       return cost(board, primary, A)
    gres = -1000000000000
    color = 'b' if color == 'w' else 'w'
    for next,value in sorted(totalMovingPoss(board,color),key=lambda val:(val[1],val[0])):
        s=smallest(next,A,B,depth-1,color, primary)
        gres = max(s,gres)
        if s >= B:
            return gres
        A = max(s,A)
    return gres

def find_best_move(board, N, player, timelimit):
    primary = player
    depth = 2
    while timelimit > 0:
        initial = time.time()
        new_board = prune(-1000000000000, 9999999999999, board, player, primary, depth)
        depth += 2
        timelimit -= (time.time()-initial)
        yield new_board

if __name__ == "__main__":
    mat = []
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")
    (_, N, color, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if color not in "wb":
        raise Exception("Invalid player.")
    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")
    print("Searching for best move for " + color + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    for var in range(0,N*N,N):
        matlist = []
        rep = board[var:var+N]
        for ent in rep:
            matlist.append(ent)
        mat.append(matlist)
    for new_board in find_best_move(mat, N, color, timelimit):
        print(new_board)