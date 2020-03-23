import os
import random
import json
import cherrypy
import copy
import math

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


class Battlesnake(object):
    
    @cherrypy.expose
    def index(self):
        # If you open your snake URL in a browser you should see this message.
        return "Your Battlesnake is alive!"

    @cherrypy.expose
    def ping(self):
        # The Battlesnake engine calls this function to make sure your snake is working.
        return "pong"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        # TODO: Use this function to decide how your snake is going to look on the board.
        data = cherrypy.request.json
        print("START")
        return {"color": "#02fa44", "headType": "smile", "tailType": "skinny"}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json

        print("current turn:")
        print(data)

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

            #Add board edges
            for i in range(Gdata.boardsize.x):
                for j in range(Gdata.boardsize.y):
                    if i == 0 or j == 0 or i == Gdata.boardsize.x - 1 or j == Gdata.boardsize.y - 1:
                        updated_board[i][j] = "edge "
                        
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
                        if updated_board[head.x + 1][head.y] in {"empty", "food ", "edge "}:
                            updated_board[head.x + 1][head.y] = f"{i}next"
                    if head.x != 0:
                        if updated_board[head.x - 1][head.y] in {"empty", "food ", "edge "}:
                            updated_board[head.x - 1][head.y] = f"{i}next"
                    if head.y != Gdata.boardsize.y - 1:
                        if updated_board[head.x][head.y + 1] in {"empty", "food ", "edge "}:
                            updated_board[head.x][head.y + 1] = f"{i}next"
                    if head.y != 0:
                        if updated_board[head.x][head.y - 1] in {"empty", "food ", "edge "}:
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
            if (mysnake.body[0].x == 0 or board[mysnake.body[0].x - 1][mysnake.body[0].y][1:5] in {"body", "head"}): 
                del moves["left"]
            if (mysnake.body[0].x == Gdata.boardsize.x - 1 or board[mysnake.body[0].x + 1][mysnake.body[0].y][1:5] in {"body", "head"}):
                del moves["right"]
            if (mysnake.body[0].y == 0 or board[mysnake.body[0].x][mysnake.body[0].y - 1][1:5] in {"body", "head"}):
                del moves["up"]
            if (mysnake.body[0].y == Gdata.boardsize.y - 1 or board[mysnake.body[0].x][mysnake.body[0].y + 1][1:5] in {"body", "head"}):
                del moves["down"]

            #Assign a score to each move based on whats in that square
                
            if "left" in moves.keys():
                square = board[mysnake.body[0].x - 1][mysnake.body[0].y]
                if square in {"empty", "food "}:
                    moves["left"] = 3
                elif square == "edge ":
                    moves["left"] = 2
                elif square[1:5] == "next":
                    if mysnake.size > allsnakes[int(square[0])].size:
                        moves["left"] = 4
                    else:
                        moves["left"] = 1

            if "right" in moves.keys():
                square = board[mysnake.body[0].x + 1][mysnake.body[0].y]
                if square in {"empty", "food "}:
                    moves["right"] = 3
                elif square == "edge ":
                    moves["right"] = 2
                elif square[1:5] == "next":
                    if mysnake.size > allsnakes[int(square[0])].size:
                        moves["right"] = 4
                    else:
                        moves["right"] = 1

            if "up" in moves.keys():
                square = board[mysnake.body[0].x][mysnake.body[0].y - 1]
                if square in {"empty", "food "}:
                    moves["up"] = 3
                elif square == "edge ":
                    moves["up"] = 2
                elif square[1:5] == "next":
                    if mysnake.size > allsnakes[int(square[0])].size:
                        moves["up"] = 4
                    else:
                        moves["up"] = 1

            if "down" in moves.keys():
                square = board[mysnake.body[0].x][mysnake.body[0].y + 1]
                if square in {"empty", "food "}:
                    moves["down"] = 3
                elif square == "edge ":
                    moves["down"] = 2
                elif square[1:5] == "next":
                    if mysnake.size > allsnakes[int(square[0])].size:
                        moves["down"] = 4
                    else:
                        moves["down"] = 1

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

            possible_moves = check_moves(mysnake_copy, new_board)
            print (f"Possible moves: {possible_moves}")

            if itteration == 0:
                for k in copy.deepcopy(possible_moves).keys():
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
                        move(mysnake_copy, k)
                        return simulate_move(allsnakes_copy, itteration + 1)

        def closest_food():
            head = mysnake.head
            closest = coord((Gdata.boardsize.x - 1)/2, (Gdata.boardsize.y - 1)/2)
            min_dist = 20
            for i in range(len(Gdata.food)):
                distance = abs(head.x - Gdata.food[i].x) + abs(head.y - Gdata.food[i].y)

                if distance < min_dist:
                    min_dist = distance
                    closest = coord(Gdata.food[i].x, Gdata.food[i].y)

            #print(f"closest food is {min_dist} units away at x = {closest.x}, y = {closest.y}")
            return closest

        def move_to_target(moves, target):

            if len(moves) < 2:
                return moves
            
            x_dif = target.x - mysnake.head.x
            y_dif = target.y - mysnake.head.y

            if abs(x_dif) > abs(y_dif):
                if x_dif > 0 and "right" in moves:
                    return ["right"]
                if x_dif < 0 and "left" in moves:
                    return ["left"]
            else:
                if y_dif > 0 and "down" in moves:
                    return ["down"]
                if y_dif < 0 and "up" in moves:
                    return ["up"]

            return moves

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

        
        max_size = 3
        biggest_snake = 0
        for i in range(Gdata.snakes):
            if i != mine and max_size < allsnakes[i].size:
                max_size = allsnakes[i].size
                biggest_snake = i

        target = coord(0,0)
        if mysnake.size <= max_size:
            print("too small, targetting food")
            target = closest_food()
        else: 
            print("big enough, targetting biggest snake")
            target = allsnakes[biggest_snake].head
        final_moves = move_to_target(final_moves, target)

        move = random.choice(final_moves)

        print(f"chose: {move}")

        return{"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json
        print("END")
        return "ok"


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
