import json
import random

data = {
    "game": {
      "id": "game-id-string"
    },
    "turn": 4,
    "board": {
      "height": 11,
      "width": 11,
      "food": [
        {'x': 3, 'y': 8}
      ],
      "snakes": [
        {
          "id": "snake-id-string",
          "name": "Sneky Snek",
          "health": 90,
          "body": [
            {'x': 10, 'y': 1}, {"x": 9, "y": 1}, {'x': 8, 'y':1}, {'x': 7, 'y':1}, {'x': 6, 'y': 1}, {'x': 5, 'y': 1}, {'x': 4, 'y': 1}
          ],
          "shout": "Hello my name is Sneky Snek"
        },
        {
      "id": "snake-id-string",
      "name": "Sneky Snek",
      "health": 90,
      "body": [
        {"x": 0, "y": 0}, {'x': 0, 'y':1}, {'x': 0, 'y':2}, {'x': 0, 'y': 3}
      ],
      "shout": "Hello my name is Sneky Snek"
    }
      ]
    },
    "you": {
      "id": "snake-id-string",
      "name": "Sneky Snek",
      "health": 90,
      "body": [
        {"x": 8, "y": 0}, {'x': 8, 'y':1}, {'x': 7, 'y':1}, {'x': 6, 'y': 1}, {'x': 5, 'y': 1}, {'x': 4, 'y': 1}
      ],
      "shout": "Hello my name is Sneky Snek"
    }
  }

class coord:
        def __init__(self, xcoord, ycoord):
            self.x = xcoord
            self.y = ycoord

class snake:
    def __init__(self, num, size):
        self.head = coord(data.get("board").get("snakes")[num].get("body")[0].get("x"), \
                              data.get("board").get("snakes")[num].get("body")[0].get("y"))
        self.body = [coord(data.get("board").get("snakes")[num].get("body")[i].get("x") , \
                               data.get("board").get("snakes")[num].get("body")[i].get("y")) \
                    for i in range(0, len(data.get("board").get("snakes")[num].get("body")))]
        self.health = data.get("board").get("snakes")[num].get("health")

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

def update_board(board, snakes):

    # print("board before update:")
    # print_board(board)
    #clear board
    board_copy = board
    board_copy = [["empty" for i in range(0, data.get("board").get("width"))] for j in range(0, data.get("board").get("height"))]
    
    #Flag board indicies that are occupied by a snake to "head" or "body"
    for s in range(0, len(snakes)): #For every snake
        for p in range(0, len(snakes[s].body)): #For each body part of snake "s"
            # print("snake coords:")
            # print(snakes[s].body[p].x)
            # print(snakes[s].body[p].y)
            # print("s,p")
            # print(s)
            # print(p)
            if (board_copy[snakes[s].body[p].x][snakes[s].body[p].y] == "empty"): 
                if (p == 0):
                    board_copy[snakes[s].body[p].x][snakes[s].body[p].y] = "head " 
                else: board_copy[snakes[s].body[p].x][snakes[s].body[p].y] = "body "
    
    # print("board after update:")
    # print_board(board)

    return board_copy

def check_moves(moves, board, mysnake, snakes):

    
    # if (snakes.head.x == 0 and "left" in moves):
    #     moves.remove('left')
    # elif (mysnake.head.x == boardsize.x - 1 and "right" in moves):
    #     moves.remove('right')

    # if (mysnake.head.y == 0 and "up" in moves):
    #     moves.remove('up')
    # elif (mysnake.head.y == boardsize.y - 1 and "down" in moves):
    #     moves.remove('down')

    if (snakes[0].body[0].x == 0 and "left" in moves):
        moves.remove('left')
    elif (snakes[0].body[0].x == boardsize.x - 1 and "right" in moves):
        moves.remove('right')

    if (snakes[0].body[0].y == 0 and "up" in moves):
        moves.remove('up')
    elif (snakes[0].body[0].y == boardsize.y - 1 and "down" in moves):
        moves.remove('down')


    #Remove possibilty of hitting a snake
    if "left" in moves:
        if (board[snakes[0].body[0].x - 1][snakes[0].body[0].y] != "empty" ):
            moves.remove('left')

    if "right" in moves:
        if (board[snakes[0].body[0].x + 1][snakes[0].body[0].y] != "empty" ):
            moves.remove('right')

    if "up" in moves:
        if (board[snakes[0].body[0].x][snakes[0].body[0].y - 1] != "empty" ):
            moves.remove('up')       

    if "down" in moves:
        if (board[snakes[0].body[0].x][snakes[0].body[0].y + 1] != "empty" ):
            moves.remove('down')     
    

def simulate_move(move, board, mysnake, snakes):

    print(f"simulating {move}")
    board_copy = board
    snakes_copy = snakes
    mysnake_copy = mysnake
    next_moves = ["up", "down", "left", "right"]

    for s in range(0, len(snakes_copy)):
        #For each body part 
        for p in range(len(snakes_copy[s].body) -1, 0, -1):
            #Shift one turn forward
            snakes_copy[s].body[p] = coord(snakes_copy[s].body[p-1].x, snakes_copy[s].body[p-1].y)

    #For my snake

    if (move == "left"):
        snakes_copy[0].head.x -= 1
        next_moves.remove("right")

    if (move == "right"):
        snakes_copy[0].head.x += 1
        next_moves.remove("left")

    if (move == "up"):
        snakes_copy[0].head.y -= 1
        next_moves.remove("down")

    if (move == "down"):
        snakes_copy[0].head.y += 1 
        next_moves.remove("up")

    snakes_copy[0].body[0] = snakes_copy[0].head 
   
    mysnake_copy = snakes_copy[0]

    board_copy = update_board(board_copy, snakes_copy)

    check_moves(next_moves, board_copy, mysnake_copy, snakes_copy)

    print(f"next moves: {next_moves}")

    if (len(next_moves) == 1):
        print(f"move {move} inconclusive, recurring")
        return simulate_move(next_moves[0], board_copy, mysnake_copy, snakes_copy)
    elif (len(next_moves) == 0):
        print(f"move {move} not valid, exiting")
        return False
    else: 
        print(f"move {move} valid, exiting")
        return True
        


#Interepert game data

turn = data.get("turn")
snakes = [snake(num, len(data.get("board").get("snakes")[num].get("body"))) for num in range(0, len(data.get("board").get("snakes")))]
mysnake = snake(0, len(data.get("board").get("snakes")[0].get("body")))
board = [["empty" for i in range(0, data.get("board").get("width"))] for j in range(0, data.get("board").get("height"))] 

boardsize = coord(data.get("board").get("width"), data.get("board").get("height"))



#Flag board indicies that are occupied by a snake to "head" or "body"
for s in range(0, len(snakes)): #For every snake
    for p in range(0, len(snakes[s].body)): #For each body part of snake "s"
        if (board[snakes[s].body[p].x][snakes[s].body[p].y] == "empty"): 
            if (p == 0):
                board[snakes[s].body[p].x][snakes[s].body[p].y] = "head " 
            else: board[snakes[s].body[p].x][snakes[s].body[p].y] = "body "

#TODO Flag board indicies that contain food

#Contains possible moves

print("original board:")
print_board(board)
possible_moves = ["up", "down", "right", "left"]

check_moves(possible_moves, board, mysnake, snakes)

print (f"possible moves at start: {possible_moves}")

for i in range(len(possible_moves)-1, -1 , -1):
    if simulate_move(possible_moves[i], board, mysnake, [snake(num, len(data.get("board").get("snakes")[num].get("body"))) for num in range(0, len(data.get("board").get("snakes")))]) == False:
        possible_moves.remove(possible_moves[i])
        
print(f"possible moves after recursion:{possible_moves}")

move = random.choice(possible_moves)
print(f"random move: {move}")