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

        board = [["empty" for i in range(0, data.get("board").get("width"))] for j in range(0, data.get("board").get("height"))] 

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
