import os
import random
import json
import cherrypy

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

        class snake:
            def __init__(self, num, size):
                self.head = coord(data.get("board").get("snakes")[num].get("body")[0].get("x"), \
                                    data.get("board").get("snakes")[num].get("body")[0].get("y"))
                self.body = [coord(data.get("board").get("snakes")[num].get("body")[i].get("x") , \
                                    data.get("board").get("snakes")[num].get("body")[i].get("y")) \
                            for i in range (0, len(data.get("board").get("snakes")[num].get("body")))]
                self.health = data.get("board").get("snakes")[num].get("health")



        def check_moves(moves, board, mysnake, snakes):
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

        def simulate_move(move, board, mysnake, snakes):

            board_copy = board
            snakes_copy = snakes
            mysnake_copy = mysnake
            next_moves = ["up", "down", "left", "right"]

            #For my snake

            if (move == "left"):
                snakes_copy[0].head.x -= 1
                snakes_copy[0].body[0].x -= 1 
                next_moves.remove("right")

            if (move == "right"):
                snakes_copy[0].head.x += 1
                snakes_copy[0].body[0].x += 1
                next_moves.remove("left")

            if (move == "up"):
                snakes_copy[0].head.y -= 1
                snakes_copy[0].body[0].y -= 1 
                next_moves.remove("down")

            if (move == "down"):
                snakes_copy[0].head.y += 1
                snakes_copy[0].body[0].y += 1 
                next_moves.remove("up")

            #For all snakes
            for s in range (0, len(snakes_copy)):
                #For each body part 
                for p in range(0, len(snakes_copy[s].body) - 1):
                    #Shift one turn forward
                    snakes_copy[s].body[p+1] = snakes_copy[s].body[p]
                #Delete tail
                del (snakes_copy[s].body[len(snakes_copy[s].body) - 1])

            check_moves(next_moves, board_copy, mysnake_copy, snakes_copy)


            if (len(next_moves) == 1):
                return simulate_move(next_moves[0], board_copy, mysnake_copy, snakes_copy)
            elif (len(next_moves) == 0):
                return False
            else: return True




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

        print (possible_moves)

        move_sim = mysnake

        for i in range(len(possible_moves)-1, -1 , -1):
            if simulate_move(possible_moves[i], board, mysnake, snakes) == False:
                possible_moves[i].remove

        print(f"possible moves:{possible_moves}")

        move = random.choice(possible_moves)
        print(f"MOVE: {move}")
        return {"move": move}

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
