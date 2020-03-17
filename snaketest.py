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
            {"x": 1, "y": 0}, {'x': 0, 'y':0},
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

#print("current turn:")
#print(data)

#Empty board 
board = [["empty" for i in range(0, data.get("board").get("width"))] for j in range(0, data.get("board").get("height"))] 

print(data.get("board").get("snakes")[0].get("body")[0].get("y"))

#Set board indicies that are occupied to "head" or "body"
for s in range (0, len(data.get("board").get("snakes"))):
    for p in range (0, len(data.get("board").get("snakes")[s].get("body"))):
        if (board[data.get("board").get("snakes")[s].get("body")[p].get("x")][data.get("board").get("snakes")[s].get("body")[p].get("y")] == "empty"):
            if (p == 0):
                board[data.get("board").get("snakes")[s].get("body")[p].get("x")][data.get("board").get("snakes")[s].get("body")[p].get("y")] = "head" 
            else: board[data.get("board").get("snakes")[s].get("body")[p].get("x")][data.get("board").get("snakes")[s].get("body")[p].get("y")] = "body"

#Contains possible moves
possible_moves = ["up", "down", "left", "right"]

#Remove the possibility of hitting a wall
if (data.get("you").get("body")[0].get("x") == 0):
    possible_moves.remove('left')
elif (data.get("you").get("body")[0].get("x") == data.get("board").get("width") - 1):
    possible_moves.remove('right')

if (data.get("you").get("body")[0].get("y") == 0):
    possible_moves.remove('up')
elif (data.get("you").get("body")[0].get("y") == data.get("board").get("length") - 1):
    possible_moves.remove('down')

#Remove possibilty of hitting a snake
if "left" in possible_moves:
    if (board[data.get("you").get("body")[0].get("x") - 1][data.get("you").get("body")[0].get("y")] != "empty" ):
        possible_moves.remove('left')

if "right" in possible_moves:
    if (board[data.get("you").get("body")[0].get("x") + 1][data.get("you").get("body")[0].get("y")] != "empty" ):
        possible_moves.remove('right')

if "up" in possible_moves:
    if (board[data.get("you").get("body")[0].get("x")][data.get("you").get("body")[0].get("y") - 1] != "empty" ):
        possible_moves.remove('up')       

if "down" in possible_moves:
    if (board[data.get("you").get("body")[0].get("x")][data.get("you").get("body")[0].get("y") + 1] != "empty" ):
        possible_moves.remove('down')     

move = random.choice(possible_moves)

print(f"possible moves:{possible_moves}")
print(f"MOVE: {move}")