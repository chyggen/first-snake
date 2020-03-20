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
                            for i in range(0, len(data.get("board").get("snakes")[num].get("body")))]
                self.health = data.get("board").get("snakes")[num].get("health")


        class priority:
            def __init__(self, move, num):
                self.move = move
                self.priority = num


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


        def update_board(board, snakes, mysnake):

            # print("board before update:")
            # print_board(board)
            #clear board
            board_copy = board
            board_copy = [["empty" for i in range(0, data.get("board").get("width"))] for j in range(0, data.get("board").get("height"))]
            
            #Flag board indecies that are occupied by another snake to "head" or "body"
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

            #Flag board indecies that contain my snake
            for p in range(0, len(mysnake.body)):
                if (p == 0):
                    board_copy[mysnake.body[p].x][mysnake.body[p].y] = "Mhead" 
                else: board_copy[mysnake.body[p].x][mysnake.body[p].y] = "Mbody"

            
            print("board after update:")
            print_board(board_copy)

            return board_copy


        def check_moves(moves, board, mysnake, snakes):

            if (mysnake.body[0].x == 0 and "left" in moves):
                moves.remove('left')
            elif (mysnake.body[0].x == boardsize.x - 1 and "right" in moves):
                moves.remove('right')

            if (mysnake.body[0].y == 0 and "up" in moves):
                moves.remove('up')
            elif (mysnake.body[0].y == boardsize.y - 1 and "down" in moves):
                moves.remove('down')


            #Remove possibilty of hitting a snake
            if "left" in moves and (board[mysnake.body[0].x - 1][mysnake.body[0].y] != "empty" ):
                moves.remove('left')

            if "right" in moves and (board[mysnake.body[0].x + 1][mysnake.body[0].y] != "empty" ):
                moves.remove('right')

            if "up" in moves and (board[mysnake.body[0].x][mysnake.body[0].y - 1] != "empty" ):
                moves.remove('up')       

            if "down" in moves and (board[mysnake.body[0].x][mysnake.body[0].y + 1] != "empty" ):
                moves.remove('down')     
            

        def simulate_move(move, board, mysnake_copy, snakes):

            print(f"simulating {move}")
            board_copy = board
            snakes_copy = snakes
            next_moves = ["up", "down", "left", "right"]

            #For all snakes
            for s in range(0, len(snakes_copy)):
                #For each body part 
                for p in range(len(snakes_copy[s].body) -1, 0, -1):
                    #Shift one turn forward
                    snakes_copy[s].body[p] = coord(snakes_copy[s].body[p-1].x, snakes_copy[s].body[p-1].y)

            #For my snake
            for p in range(len(mysnake_copy.body) -1, 0, -1):
                #Shift one turn forward
                mysnake_copy.body[p] = coord(mysnake_copy.body[p-1].x, mysnake_copy.body[p-1].y)

            if (move == "left"):
                mysnake_copy.head.x -= 1
                next_moves.remove("right")

            if (move == "right"):
                mysnake_copy.head.x += 1
                next_moves.remove("left")

            if (move == "up"):
                mysnake_copy.head.y -= 1
                next_moves.remove("down")

            if (move == "down"):
                mysnake_copy.head.y += 1 
                next_moves.remove("up")

            mysnake_copy.body[0] = mysnake_copy.head 

            board_copy = update_board(board_copy, snakes_copy, mysnake_copy)

            print("printing my snake copy:")
            print_snake(mysnake_copy)

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


        # TODO:
        # Fix snakes[0] issue                                 -- NOT done
        # Implement head to head collision prediction         
        # Allow snake to follow tail                          -- NOTE need to update everything except mysnake.head, then check moves
        # Add food detection



        #Interepert game data

        turn = data.get("turn")
        snakes = [snake(num, len(data.get("board").get("snakes")[num].get("body"))) for num in range(0, len(data.get("board").get("snakes")))]

        mine = 0
        for i in range (len(snakes)):
            if (data.get("board").get("snakes")[i] == data.get("you")):
                mine = i

        mysnake = snake(mine, len(data.get("you").get("body")))
        print_snake(mysnake)

        board = [["empty" for i in range(0, data.get("board").get("width"))] for j in range(0, data.get("board").get("height"))] 

        boardsize = coord(data.get("board").get("width"), data.get("board").get("height"))



        #Flag board indicies that are occupied by a snake to "head" or "body"
        for s in range(0, len(snakes)): #For every snake
            for p in range(0, len(snakes[s].body)): #For each body part of snake "s"
                if (board[snakes[s].body[p].x][snakes[s].body[p].y] == "empty"): 
                    if (p == 0):
                        board[snakes[s].body[p].x][snakes[s].body[p].y] = "head " 
                    else: board[snakes[s].body[p].x][snakes[s].body[p].y] = "body "

        # #TODO Flag board indicies that contain food

        # #Contains possible moves

        # print("original board:")
        # print_board(board)
        possible_moves = ["up", "down", "right", "left"]



        check_moves(possible_moves, board, mysnake, snakes)

        print (f"possible moves at start: {possible_moves}")

        for i in range(len(possible_moves)-1, -1 , -1):
            if simulate_move(possible_moves[i], board, snake(mine, len(mysnake.body)), [snake(num, len(snakes[num].body)) for num in range(0, len(snakes))]) == False:
                possible_moves.remove(possible_moves[i])

        print(f"possible moves after recursion:{possible_moves}")

        if (mysnake.health > 50):
            max_idx = 0
            priorities = [0, 0, 0, 0]

            for i in range(0, len(possible_moves)):
                if (possible_moves[i] == "left"):
                    priorities[i] = mysnake.body[0].x
                elif (possible_moves[i] == "right"):
                    priorities[i] = boardsize.x - mysnake.body[0].x - 1
                elif (possible_moves[i] == "up"):
                    priorities[i] = mysnake.body[0].y
                elif (possible_moves[i] == "down"):
                    priorities[i] = boardsize.y - mysnake.body[0].y - 1

            move_priority = [priority(possible_moves[i], priorities[i]) for i in range(0, len(possible_moves))]

            for i in range(len(possible_moves)):
                print(move_priority[i].move, move_priority[i].priority)
                if (move_priority[max_idx].priority < move_priority[i].priority):
                    max_idx = i


            move = move_priority[max_idx].move
            print(f"moving towards middle: {move}")
            return{"move": move}
        else:
            move = random.choice(possible_moves)
            print (f"picking random: {move}")
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
