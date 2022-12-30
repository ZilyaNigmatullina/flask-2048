import logic
from flask import Flask, render_template

app = Flask(__name__)

GRID_LEN = 4


def grid_string_to_grid(grid_string):
    grid = []
    rows = grid_string.split('x')
    for row in rows:
        cols = row.split('-')
        grid.append([int(c) for c in cols])
    return grid


def grid_to_grid_string(grid):
    row_strings = []
    for row in grid:
        row_strings.append('-'.join([str(x) for x in row]))
    return 'x'.join(row_strings)


def render_grid(g, game_state='play'):
    gg = [["" if r == 0 else r for r in row] for row in g]
    return render_template('gui.html', r1c1=gg[0][0], r1c2=gg[0][1], r1c3=gg[0][2], r1c4=gg[0][3],
                           r2c1=gg[1][0], r2c2=gg[1][1], r2c3=gg[1][2], r2c4=gg[1][3],
                           r3c1=gg[2][0], r3c2=gg[2][1], r3c3=gg[2][2], r3c4=gg[2][3],
                           r4c1=gg[3][0], r4c2=gg[3][1], r4c3=gg[3][2], r4c4=gg[3][3],
                           grid_encoding=grid_to_grid_string(g), game_state=game_state)


@app.route('/')
def index():
    matrix = logic.initial_rows(GRID_LEN)
    return render_grid(matrix)


@app.route('/move/<string:direction>/<string:last_encoding>/')
def move(direction, last_encoding):
    grid = grid_string_to_grid(last_encoding)
    changed = False
    game = []
    if direction == 'up':
        game, changed = logic.up(grid)
    if direction == 'down':
        game, changed = logic.down(grid)
    if direction == 'left':
        game, changed = logic.left(grid)
    if direction == 'right':
        game, changed = logic.right(grid)

    if changed:
        game = logic.insert_random_base_value(game)
        state = logic.game_state(game)
        return render_grid(game, state)
    else:
        game = logic.initial_rows(GRID_LEN)
        return render_grid(game)


if __name__ == "__main__":
    app.run(debug=False, port=8000, host="0.0.0.0")
