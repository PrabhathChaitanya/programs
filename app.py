from flask import Flask, render_template, jsonify, request
import random
from copy import deepcopy

app = Flask(__name__,template_folder='templates')

# Game2048 class
class Game2048:
    def __init__(self):
        self.board = [[0] * 4 for _ in range(4)]
        self.prev_boards = []
        self.undo_count = 0
        self.max_undo_count = 3
        self.score = 0
        self.highest_score = self.load_highest_score()

    def new_game(self):
        self.score = 0
        self.board = [[0] * 4 for _ in range(4)]
        self.prev_boards = []
        for _ in range(2):
            self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.board[row][col] = 2 if random.random() < 0.9 else 4

    def move_tiles(self, direction):
        if direction == 'Up':
            self.board = [list(x) for x in zip(*self.board)]
            self.board = [self.move_row(row) for row in self.board]
            self.board = [list(x) for x in zip(*self.board)]
        elif direction == 'Down':
            self.board = [list(x) for x in zip(*self.board[::-1])]
            self.board = [self.move_row(row) for row in self.board]
            self.board = [list(x[::-1]) for x in zip(*self.board)]
        elif direction == 'Left':
            self.board = [self.move_row(row) for row in self.board]
        elif direction == 'Right':
            self.board = [row[::-1] for row in self.board]
            self.board = [self.move_row(row) for row in self.board]
            self.board = [row[::-1] for row in self.board]

    def move_row(self, row):
        new_row = [tile for tile in row if tile != 0]
        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                self.score += new_row[i]
                new_row.pop(i + 1)
                new_row.append(0)
        return new_row + [0] * (4 - len(new_row))

    def is_game_over(self):
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    return False
                if j < 3 and self.board[i][j] == self.board[i][j + 1]:
                    return False
                if i < 3 and self.board[i][j] == self.board[i + 1][j]:
                    return False
        return True

    def save_highest_score(self):
        # Implement saving highest score logic (file/db/etc.)
        pass

    def load_highest_score(self):
        # Implement loading highest score logic (file/db/etc.)
        return 0

# Instantiate the game
game = Game2048()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    direction = request.json['direction']
    game.prev_boards.append(deepcopy(game.board))
    game.move_tiles(direction)
    game.add_new_tile()
    game_data = {
        'board': game.board,
        'score': game.score,
        'highest_score': game.highest_score,
        'game_over': game.is_game_over()
    }
    return jsonify(game_data)

if __name__ == '__main__':
    app.run(debug=True)
