from flask import Flask, send_file, request
import sys
from board import Board
from ai import GreedyAI, AStarAI, RandomAI
import json
app = Flask(__name__)


ai_class = GreedyAI


@app.route("/")
def root():
    return send_file('index.html')


@app.route("/new-game")
def new_game():
    difficulty = request.args.get('level')
    b = Board(times=10)
    if difficulty == 'moderate':
        b = Board(times=20)
    elif difficulty == 'difficult':
        b = Board(times=50)

    game = {
        "game": b.tiles
    }
    return json.dumps(game)


@app.route("/move")
def next_move():
    tiles = request.args.get("tiles")
    tiles = tiles.split(',')
    new_tiles = [
        [int(x) if x else None for x in tiles[0:3]],
        [int(x) if x else None for x in tiles[3:6]],
        [int(x) if x else None for x in tiles[6:9]]
    ]
    b = Board(tiles=new_tiles)

    ai = ai_class(b)
    move = ai.make_move()
    print(move)
    return json.dumps({
        "move": move
    })


if __name__ == '__main__':
    global ai
    if "astar" in sys.argv:
        ai_class = AStarAI
        print("Running interface with A* AI")
    elif "greedy" in sys.argv:
        ai_class = GreedyAI
        print("Running interface with Greedy AI")
    elif "greedy" in sys.argv:
        ai_class = RandomAI
        print("Running interface with Random AI")

    app.run()
