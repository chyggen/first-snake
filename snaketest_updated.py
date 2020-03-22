import json
import random
import time
import copy

data ={'game': {'id': 'e7d4abee-bbab-4589-8bb0-1bf0b5b1a340'}, 'turn': 74, 'board': {'height': 11, 'width': 11, 'food': [{'x': 5, 'y': 6}, {'x': 6, 'y': 6}, {'x': 10, 'y': 10}, {'x': 7, 'y': 4}, {'x': 0, 'y': 8}, {'x': 2, 'y': 4}, {'x': 0, 'y': 7}, {'x': 0, 'y': 10}, {'x': 3, 'y': 5}, {'x': 6, 'y': 4}], 'snakes': [{'id': 'gs_wPKpCDDrQBTC6XTVPyJR4PBK', 'name': 'ChyggSnake', 'health': 82, 'body': [{'x': 10, 'y': 0}, {'x': 9, 'y': 0}, {'x': 9, 'y': 1}, {'x': 8, 'y': 1}, {'x': 8, 'y': 0}], 'shout': ''}]}, 'you': {'id': 'gs_wPKpCDDrQBTC6XTVPyJR4PBK', 'name': 'ChyggSnake', 'health': 82, 'body': [{'x': 10, 'y': 0}, {'x': 9, 'y': 0}, {'x': 9, 'y': 1}, {'x': 8, 'y': 1}, {'x': 8, 'y': 0}], 'shout': ''}}
#     {
#     "game": {
#       "id": "game-id-string"
#     },
#     "turn": 4,
#     "board": {
#       "height": 11,
#       "width": 11,
#       "food": [
#         {'x': 3, 'y': 8}
#       ],
#       "snakes": [
#         {
#           "id": "snake-id-string",
#           "name": "Sneky Snek",
#           "health": 90,
#           "body": [
#             {'x': 4, 'y': 6}, {"x": 4, "y": 5}, {'x': 4, 'y':4}
#           ],
#           "shout": "Hello my name is Sneky Snek"
#         },
#         {
#           "id": "snake-id-string",
#           "name": "Sneky Snek",
#           "health": 90,
#           "body": [
#             {'x': 2, 'y': 10}, {'x': 2, 'y': 9}, {'x': 2, 'y': 8}
#           ],
#           "shout": "Hello my name is Sneky Snek"
#     }
#       ]
#     },
#     "you": {
#       "id": "snake-id-string",
#       "name": "Sneky Snek",
#       "health": 90,
#       "body": [
#         {'x': 2, 'y': 10}, {'x': 2, 'y': 9}, {'x': 2, 'y': 8} 
#           ],
#       "shout": "Hello my name is Sneky Snek"
#     }
#   }

class coord:
    def __init__(self, xcoord, ycoord):
        self.x = xcoord
        self.y = ycoord


class get_data:
    def __init__(self):
        self.boardsize = coord(data.get("board").get("width"), data.get("board").get("height"))
        self.food = [coord(data.get("board").get("food")[i].get("x"), data.get("board").get("food")[i].get("y")) \
                    for i in range(len(data.get("board").get("food")))]
        self.turn = data.get("turn")
        self.snakes = len(data.get("board").get("snakes"))


class snake:
    def __init__(self, num):
        self.body = [coord(data.get("board").get("snakes")[num].get("body")[i].get("x") , \
                        data.get("board").get("snakes")[num].get("body")[i].get("y")) \
                    for i in range(0, len(data.get("board").get("snakes")[num].get("body")))]
        self.head = self.body[0]
        self.health = data.get("board").get("snakes")[num].get("health")
        self.size = len(data.get("board").get("snakes")[num].get("body"))



def empty_board():
    board = [["empty" for i in range(Gdata.boardsize.x)] for j in range(Gdata.boardsize.y)]
    return board


def update_board(allsnakes):
    updated_board = empty_board()

    #Add food to board
    for i in range(len(Gdata.food)):
        updated_board[Gdata.food[i].x][Gdata.food[i].y] = "food "

    #Add snakes to board
    for i in range(Gdata.snakes):
        for j in range(allsnakes[i].size -1, -1, -1):
            if (i == mine): # If its my snake, label body parts with M
                if (j == 0):
                    updated_board[allsnakes[i].head.x][allsnakes[i].head.y] = "Mhead"
                else:
                    updated_board[allsnakes[i].body[j].x][allsnakes[i].body[j].y] = "Mbody"
            else: # If its not my snake, label body parts with that snake's index
                if (j == 0):
                    updated_board[allsnakes[i].head.x][allsnakes[i].head.y] = f"{i}head"
                else:
                    updated_board[allsnakes[i].body[j].x][allsnakes[i].body[j].y] = f"{i}body"

    #Add potential next moves
    for i in range(Gdata.snakes):
        #Only want other snake's moves and only want potential moves in open spaces
        if (i != mine):
            head = coord(allsnakes[i].head.x, allsnakes[i].head.y)
            if head.x != Gdata.boardsize.x - 1:
                if updated_board[head.x + 1][head.y] in {"empty", "food"}:
                    updated_board[head.x + 1][head.y] = f"{i}next"
            if head.x != 0:
                if updated_board[head.x - 1][head.y] in {"empty", "food"}:
                    updated_board[head.x - 1][head.y] = f"{i}next"
            if head.y != Gdata.boardsize.y - 1:
                if updated_board[head.x][head.y + 1] in {"empty", "food"}:
                    updated_board[head.x][head.y + 1] = f"{i}next"
            if head.y != 0:
                if updated_board[head.x][head.y - 1] in {"empty", "food"}:
                    updated_board[head.x][head.y - 1] = f"{i}next"
        
    return updated_board


def print_board(board):
    for y in range(len(board[0])):
        for x in range(len(board)):
            if (board[x][y] == "empty"):
                print("-----", end = " ")
            else: print(board[x][y], end = " ")
            if (x == len(board)-1):
                print("")


def print_snake(snake):
    for i in range(len(snake.body)):
        print(f"x : {snake.body[i].x}, y : {snake.body[i].y} ")

def move(snake, move):
    if move == "left":
        snake.head.x -= 1
    if move == "right":
        snake.head.x += 1
    if move == "up":
        snake.head.y -= 1
    if move == "down":
        snake.head.y += 1

def check_moves(mysnake, board):

    moves = {"left": 0, "right": 0, "up": 0, "down": 0}

    #Remove possibility of hitting a wall or the body of a snake
    if (mysnake.body[0].x == 0 or board[mysnake.body[0].x - 1][mysnake.body[0].y][1:5] == "body"): 
        del moves["left"]
    if (mysnake.body[0].x == Gdata.boardsize.x - 1 or board[mysnake.body[0].x + 1][mysnake.body[0].y][1:5] == "body"):
        del moves["right"]
    if (mysnake.body[0].y == 0 or board[mysnake.body[0].x][mysnake.body[0].y - 1][1:5] == "body"):
        del moves["up"]
    if (mysnake.body[0].y == Gdata.boardsize.y - 1 or board[mysnake.body[0].x][mysnake.body[0].y + 1][1:5] == "body"):
        del moves["down"]
        

    #Assign a score to each move based on whats in that square
    if "left" in moves.keys():
        square = board[mysnake.body[0].x - 1][mysnake.body[0].y]
        if square in {"empty", "food "}:
            moves["left"] = 2
        elif square[1:5] == "next":
            if mysnake.size > allsnakes[int(square[0])].size:
                moves["left"] = 3
            else:
                moves["left"] = 1

    if "right" in moves.keys():
        square = board[mysnake.body[0].x + 1][mysnake.body[0].y]
        if square in {"empty", "food "}:
            moves["right"] = 2
        elif square[1:5] == "next":
            if mysnake.size > allsnakes[int(square[0])].size:
                moves["right"] = 3
            else:
                moves["right"] = 1

    if "up" in moves.keys():
        square = board[mysnake.body[0].x][mysnake.body[0].y - 1]
        if square in {"empty", "food "}:
            moves["up"] = 2
        elif square[1:5] == "next":
            if mysnake.size > allsnakes[int(square[0])].size:
                moves["up"] = 3
            else:
                moves["up"] = 1

    if "down" in moves.keys():
        square = board[mysnake.body[0].x][mysnake.body[0].y + 1]
        if square in {"empty", "food "}:
            moves["down"] = 2
        elif square[1:5] == "next":
            if mysnake.size > allsnakes[int(square[0])].size:
                moves["down"] = 3
            else:
                moves["down"] = 1


    print(f"moves priority:{moves}")
    return moves
    

def simulate_move(allsnakes, itteration):

    allsnakes_copy = copy.deepcopy(allsnakes)
    mysnake_copy = allsnakes_copy[mine]
    #For all snakes
    for s in range(Gdata.snakes):
        #For each body part, starting at the tail
        for p in range(allsnakes_copy[s].size -1, 0, -1):
            #Shift one turn forward
            allsnakes_copy[s].body[p] = coord(allsnakes_copy[s].body[p-1].x, allsnakes_copy[s].body[p-1].y)

    new_board = update_board(allsnakes_copy)  

    print("Updated board:")
    print_board(new_board)

    possible_moves = check_moves(mysnake_copy, new_board)
    print (f"Possible moves: {possible_moves}")

    if itteration == 0:

        for k in copy.deepcopy(possible_moves).keys() :
            allsnakes_copy2 = copy.deepcopy(allsnakes_copy)
            move(allsnakes_copy2[mine], k)
            if simulate_move(allsnakes_copy2, itteration + 1) == False:
                del possible_moves[k]
            
        max = 0
        for k in possible_moves.keys():
            if possible_moves[k] > max:
                max = possible_moves[k]

        final_moves = copy.deepcopy(possible_moves)

        for k in possible_moves.keys():
            if possible_moves[k] != max:
                del final_moves[k]
                

        return final_moves

    else: 
        if len(possible_moves) == 0:
            return False
        if len(possible_moves) >= 2:
            return True
        if len(possible_moves) == 1:

            for k in possible_moves.keys(): 
                move(copy.deepcopy(mysnake_copy), k)
                return simulate_move(allsnakes_copy, itteration + 1)



Gdata = get_data()
allsnakes = [snake(i) for i in range(Gdata.snakes)]

mine = 0
for i in range (len(allsnakes)):
    if (data.get("board").get("snakes")[i] == data.get("you")):
        mine = i
        break

mysnake = allsnakes[mine]

board = update_board(allsnakes)
print_board(board)
possible_moves = simulate_move(allsnakes, 0)

final_moves = list(possible_moves.keys())
print(f"final moves: {final_moves}")

move = random.choice(final_moves)

print(f"chose: {move}")


