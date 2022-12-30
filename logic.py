import random


def create_empty_matrix(dim):
    matrix = []
    for i in range(dim):
        matrix.append([0] * dim)
    return matrix


def insert_random_base_value(rows):
    i = random.randint(0, len(rows) - 1)
    j = random.randint(0, len(rows) - 1)

    while rows[i][j] != 0:
        i = random.randint(0, len(rows) - 1)
        j = random.randint(0, len(rows) - 1)

    rows[i][j] = 4 if random.random() > 0.9 else 2

    return rows


def initial_rows(n):
    rows = create_empty_matrix(n)
    rows = insert_random_base_value(rows)
    rows = insert_random_base_value(rows)
    return rows


def game_state(rows):
    for i in range(len(rows)):
        for j in range(len(rows[0])):
            if rows[i][j] == 2048:
                return 'win'

    for i in range(len(rows)):
        for j in range(len(rows[0])):
            if rows[i][j] == 0:
                return 'play'

    for i in range(len(rows) - 1):
        for j in range(len(rows[0]) - 1):
            if rows[i][j] == rows[i + 1][j] or rows[i][j + 1] == rows[i][j]:
                return 'play'

    for j in range(len(rows) - 1):
        if rows[len(rows) - 1][j] == rows[len(rows) - 1][j + 1]:
            return 'play'

    for i in range(len(rows) - 1):
        if rows[i][len(rows) - 1] == rows[i + 1][len(rows) - 1]:
            return 'play'

    return 'lose'


def cover_up(rows):
    new = create_empty_matrix(len(rows))
    changed = False
    for i in range(len(rows)):
        count = 0
        for j in range(len(rows)):
            if rows[i][j] != 0:
                new[i][count] = rows[i][j]
                if j != count:
                    changed = True
                count += 1
    return new, changed


def merge(rows):
    changed = False

    for i in range(len(rows)):
        for j in range(len(rows) - 1):
            if rows[i][j] == rows[i][j + 1] and rows[i][j] != 0:
                rows[i][j] = rows[i][j] * 2
                rows[i][j + 1] = 0
                changed = True

    return rows, changed


def reverse(rows):
    new = []
    for i in range(len(rows)):
        new.append([])
        new[i] = rows[i][::-1]
    return new


def transpose(rows):
    new = []
    for i in range(len(rows[0])):
        new.append([])
        for j in range(len(rows)):
            new[i].append(rows[j][i])
    return new


def left(game):
    game, changed1 = cover_up(game)
    game, changed2 = merge(game)
    changed = changed1 or changed2
    game, temp = cover_up(game)
    return game, changed


def right(game):
    game = reverse(game)
    game, changed = left(game)
    game = reverse(game)
    return game, changed


def up(game):
    game = transpose(game)
    game, changed = left(game)
    game = transpose(game)
    return game, changed


def down(game):
    game = transpose(game)
    game, changed = right(game)
    game = transpose(game)
    return game, changed
