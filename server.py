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
        me = data["you"]["head"]
        # Choose a random direction to move in
        possible_moves = ["up", "down", "left", "right"]
        # List of safe moves 
        safe_moves = self.getSafeMoves(possible_moves, me, board)
        print(safe_moves)
        if safe_moves:
            move = random.choice(safe_moves)
            return {"move":move}
        # default choice
        return {"move":"up"}

    def getSafeMoves(self, possible_moves, me, board):
        safe_moves =[]
        for move in possible_moves:
            if move=="up" and me["head"]["y"]+1 < board["height"]:
                safe_moves.append(move)
            elif move=="down" and me["head"]["y"]-1 >= 0:
                safe_moves.append(move)
            elif move=="left" and me["head"]["x"]+1 < board["width"]:
                safe_moves.append(move)
            elif move=="right" and me["head"]["x"]-1 >= 0:
                safe_moves.append(move)
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
