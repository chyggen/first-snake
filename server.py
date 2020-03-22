import os
import random
import json
import cherrypy
import copy

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
        return {"color": "#888888", "headType": "smile", "tailType": "fat-rattle"}

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

                    if (updated_board[head.x + 1][head.y] in {"empty", "food"}) and head.x != Gdata.boardsize.x - 1:
                        updated_board[head.x + 1][head.y] = f"{i}next"
                    if (updated_board[head.x - 1][head.y] in {"empty", "food"}) and head.x != 0:
                        updated_board[head.x - 1][head.y] = f"{i}next"
                    if (updated_board[head.x][head.y + 1] in {"empty", "food"}) and head.y != Gdata.boardsize.y - 1:
                        updated_board[head.x][head.y + 1] = f"{i}next"
                    if (updated_board[head.x][head.y - 1] in {"empty", "food"}) and head.y != 0:
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
            elif (mysnake.body[0].x == Gdata.boardsize.x - 1 or board[mysnake.body[0].x + 1][mysnake.body[0].y][1:5] == "body"):
                del moves["right"]
            if (mysnake.body[0].y == 0 or board[mysnake.body[0].x][mysnake.body[0].y - 1][1:5] == "body"):
                del moves["up"]
            elif (mysnake.body[0].y == Gdata.boardsize.y - 1 or board[mysnake.body[0].x][mysnake.body[0].y - 1][1:5] == "body"):
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
                for k in possible_moves.keys() :
                    allsnakes_copy2 = copy.deepcopy(allsnakes_copy)
                    move(allsnakes_copy2[mine], k)
                    if simulate_move(allsnakes_copy2, itteration + 1) == False:
                        possible_moves.remove(k)
                    
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

                    for k in possible_moves.keys: 
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
