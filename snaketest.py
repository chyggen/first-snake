data = {}

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
                    for i in range (0, len(data.get("board").get("snakes")[num].get("body")))]
        self.health = data.get("board").get("snakes")[num].get("health")

def check_moves( moves, board, mysnake, snakes):
    if (mysnake.head.x == 0):
        moves.remove('left')
    elif (mysnake.head.x == boardsize.x - 1):
        moves.remove('right')

    if (mysnake.head.y == 0):
        moves.remove('up')
    elif (mysnake.head.y == boardsize.y - 1):
        moves.remove('down')

    #Remove possibilty of hitting a snake
    if "left" in moves:
        if (board[mysnake.head.x - 1][mysnake.head.y] != "empty" ):
            moves.remove('left')

    if "right" in moves:
        if (board[mysnake.head.x + 1][mysnake.head.y] != "empty" ):
            moves.remove('right')

    if "up" in moves:
        if (board[mysnake.head.x][mysnake.head.y - 1] != "empty" ):
            moves.remove('up')       

    if "down" in moves:
        if (board[mysnake.head.x][mysnake.head.y + 1] != "empty" ):
            moves.remove('down')     

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
            {"x": 1, "y": 1}, {'x': 0, 'y':1},
          ],
          "shout": "Hello my name is Sneky Snek"
        },
      ]
    },
    "you": {
      "id": "snake-id-string",
      "name": "Sneky Snek",
      "health": 90,
      "body": [
        {"x": 1, "y": 0}, {'x': 0, 'y':0},
      ],
      "shout": "Hello my name is Sneky Snek"
    }
  }

#Interepert game data

turn = data.get("turn")
snakes = [snake(num, len(data.get("board").get("snakes")[num].get("body"))) for num in range(0, len(data.get("board").get("snakes")))]
mysnake = snake(0, len(data.get("board").get("snakes")[0].get("body")))
board = [["empty" for i in range(0, data.get("board").get("width"))] for j in range(0, data.get("board").get("height"))] 

boardsize = coord(data.get("board").get("width"), data.get("board").get("height"))


#Flag board indicies that are occupied by a snake to "head" or "body"
for s in range (0, len(snakes)): #For every snake
    for p in range (0, len(snakes[s].body)): #For each body part of snake "s"
        if (board[snakes[s].body[p].x][snakes[s].body[p].y] == "empty"): 
            if (p == 0):
                board[snakes[s].body[p].x][snakes[s].body[p].y] = "head" 
            else: board[snakes[s].body[p].x][snakes[s].body[p].y] = "body"

#Flag board indicies that contain food

#Contains possible moves
possible_moves = ["up", "down", "left", "right"]

check_moves(possible_moves, board, mysnake, snakes)


print(f"possible moves:{possible_moves}")

move = random.choice(possible_moves)
print(f"MOVE: {move}")