import os
import random

import cherrypy

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "akash-sr",  
            "color": "#0A1931",  
            "head": "tiger-king", 
            "tail": "bolt",  
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        data = cherrypy.request.json

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # the request sent by the battlesnake server
        data = cherrypy.request.json
        # extract the board information from the data
        board = data["board"]
        # extract my snake's information from the data
        mySnake = data["you"]
        # Choose a random direction to move in
        possible_moves = ["up", "down", "left", "right"]
        # List of safe moves 
        safe_moves = self.getSafeMoves(possible_moves, mySnake, board)
        # List of moves with food 
        food_moves = self.getFoodMoves(safe_moves, mySnake, board)
        # print(safe_moves)
        if food_moves:
            move = random.choice(food_moves)
        elif safe_moves: 
            move = random.choice(safe_moves)
        # default choice
        else : 
            move = "up"
        return {"move":move}

    def getNext(self, currentHead, guess):
        # returns the coordinates of the head if "guess" is taken as the next move
        futureHead = currentHead.copy()
        if guess=="up":
            futureHead["y"] = currentHead["y"]+1
        elif guess=="down":
            futureHead["y"] = currentHead["y"]-1
        elif guess=="left":
            futureHead["x"] = currentHead["x"]-1
        elif guess=="right":
            futureHead["x"] = currentHead["x"]+1
        return futureHead

    def avoidsWalls(self, head, y, x):
        # checks if the guessed move avoids walls
        if head["x"] >= x or head["x"] < 0 :
            return False
        elif head["y"] >= y or head["y"] < 0:
            return False
        return True

    def avoidsSnakes(self, head, snakes):
        # checks if the guessed move avoids snakes
        for snake in snakes:
            if head in snake["body"]:
                return False
        return True

    def getAllMoves(self, coord):
        # returns all possible coordinates given inital coordinate
        return [
            {"x": coord["x"], "y": coord["y"]+1},   # up
            {"x": coord["x"], "y": coord["y"]-1},   # down
            {"x": coord["x"]+1, "y": coord["y"]},   # right
            {"x": coord["x"]-1, "y": coord["y"]}    # left
        ]

    def avoidConsumption(self, head, mySnake, snakes):
        if len(snakes)<2:
            return True
        myLength = mySnake["length"]
        for snake in snakes:
            if snake == mySnake:
                continue
            elif head in self.getAllMoves(snake["head"]) and myLength <= snake["length"]:
                return False
        return True

    def getFoodMoves(self, safe_moves, mySnake, board):
        food_moves = []
        for guess in safe_moves:
            guessCoord = self.getNext(mySnake["head"], guess)
            if guessCoord in board["food"]:
                food_moves.append(guess)
        return food_moves

    def getSafeMoves(self, possible_moves, mySnake, board):
        # !!Need to add squad support as well
        #  populates the safe moves list
        safe_moves =[]
        for guess in possible_moves:
            # body[0] gives the coordinates for the head
            guessCoord = self.getNext(mySnake["head"], guess)
            if self.avoidsWalls(guessCoord, board["height"], board["width"]) and self.avoidsSnakes(guessCoord, board["snakes"]) and self.avoidConsumption(guessCoord, mySnake, board["snakes"]):
                safe_moves.append(guess)
        return safe_moves

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
