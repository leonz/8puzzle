from flask import Flask, send_file, request
from board import Board
from ai import GreedyAI
import json
app = Flask(__name__)


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

    ai = GreedyAI(b)
    move = ai.make_move()
    print(move)
    return json.dumps({
        "move": move
    })


if __name__ == '__main__':
    app.run()
