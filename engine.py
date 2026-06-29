import random

# define shapes as matrices and store in dictionary
SHAPES = {
    "I": [[1, 1, 1, 1]],
    "O": [[1, 1], [1, 1]],
    "T": [[1, 1, 1], [0, 1, 0]],
    "J": [[0, 0, 1], [1, 1, 1]],
    "L": [[1, 0, 0], [1, 1, 1]],
    "S": [[0, 1, 1], [1, 1, 0]],
    "Z": [[1, 1, 0], [0, 1, 1]],
}

COLORS = {
    "I": 1,
    "O": 2,
    "T": 3,
    "J": 4,
    "L": 5,
    "S": 6,
    "Z": 7,
}


class tetris_engine:
    def __init__(self, rows=20, cols=10):
        self.rows = rows
        self.cols = cols

        # create a board for tetris filled with zeros
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.game_over = False

        # current active piece setup
        self.piece_x = 0
        self.piece_y = 0

        self.current_piece_name = random.choice(list(SHAPES.keys()))
        self.current_piece = SHAPES[self.current_piece_name]
        self.current_color = COLORS[self.current_piece_name]

        # score setup
        self.score = 0
        self.high_score = self.load_high_score()
        self.lines_clear = 0

        self.spawn_piece()

    def spawn_piece(self):
        """Spawns a random piece in the middle of the board"""
        self.current_piece_name = random.choice(list(SHAPES.keys()))
        self.current_piece = SHAPES[self.current_piece_name]
        self.current_color = COLORS[self.current_piece_name]

        self.piece_x = self.cols // 2 - len(self.current_piece[0]) // 2
        self.piece_y = 0

        # if it collides then it is game over
        if self.check_collision(self.piece_x, self.piece_y, self.current_piece):
            self.game_over = True

    def get_board_with_pieces(self, x, y, piece):
        temp = [row[:] for row in self.board]
        for r_idx, row in enumerate(piece):
            for c_idx, val in enumerate(row):
                if val != 0:
                    board_x = x + c_idx  # column
                    board_y = y + r_idx  # row
                    temp[board_y][board_x] = self.current_color
        return temp

    def check_collision(self, x, y, piece):
        for r_idx, row in enumerate(piece):
            for c_idx, val in enumerate(row):
                if val != 0:
                    board_x = x + c_idx
                    board_y = y + r_idx
                    # outside left/right boundaries
                    if board_x < 0 or board_x >= self.cols:
                        # print(f"Collision! board_x = {board_x}, cols = {self.cols}")
                        return True
                    # outside top/bottom boundary
                    if board_y >= self.rows:
                        # print(f"Collsion detected = {board_y}, rows = {self.rows}")
                        return True

                    # hits an existing piece
                    if board_y >= 0 and self.board[board_y][board_x] != 0:
                        return True
        return False

    def moveleft(self):
        if not self.game_over:
            if not self.check_collision(
                self.piece_x - 1, self.piece_y, self.current_piece
            ):
                self.piece_x -= 1

    def moveright(self):
        if not self.game_over:
            if not self.check_collision(
                self.piece_x + 1, self.piece_y, self.current_piece
            ):
                self.piece_x += 1

    def update(self):  # Drops the piece by 1 unit at a time
        if self.game_over:
            return

        if not self.check_collision(self.piece_x, self.piece_y + 1, self.current_piece):
            self.piece_y += 1
        else:
            self.lock_piece()
            lines = self.clear_lines()
            self.update_score(lines)
            self.spawn_piece()

    def lock_piece(self):
        """Permanently burns the active piece to the board array"""
        for r_idx, row in enumerate(self.current_piece):
            for c_idx, val in enumerate(row):
                if val != 0:
                    self.board[self.piece_y + r_idx][self.piece_x + c_idx] = (
                        self.current_color
                    )

    def clear_lines(self):
        """Clear the lines in an array if all of them are connected"""
        self.lines_clear = 0
        new_board = []

        # scan the board for every row
        for row in self.board:
            if 0 in row:
                new_board.append(row)
            else:
                self.lines_clear += 1

        # Make the empty row at the top
        if self.lines_clear > 0:
            empty_row = [[0] * self.cols for _ in range(self.lines_clear)]
            self.board = empty_row + new_board
        return self.lines_clear

    def rotation(self):
        """Rotates the piece by 90 degrees if valid"""
        if not self.game_over:
            transposed = list(zip(*self.current_piece))

            # Reverses each row
            rotated_piece = [list(row)[::-1] for row in transposed]

            # check the collision
            if not self.check_collision(self.piece_x, self.piece_y, rotated_piece):
                self.current_piece = rotated_piece

    def update_score(self, lines):
        """Generate a score for each block"""
        points = {1: 100, 2: 300, 3: 600, 4: 1000}
        self.score += 40
        self.score += points.get(lines, 0)

    def load_high_score(self):
        try:
            with open("highscore.txt", "r") as file:
                return int(file.read())
        except (FileNotFoundError, ValueError):
            return 0

    def save_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
        with open("highscore.txt", "w") as file:
            file.write(str(self.high_score))  # write the high score to file

    def display(self):
        board = self.get_board_with_pieces(
            self.piece_x, self.piece_y, self.current_piece
        )
        board2 = self.check_collision(self.piece_x, self.piece_y, self.current_piece)
        for row in self.board:
            print(" ".join("." if cell == 0 else str(cell) for cell in row))

        print("Newline\n\n")

        for row in board:
            print(" ".join("." if cell == 0 else str(cell) for cell in row))

        print(self.current_piece)
        print("Newline\n\n")
        print(board2)


if __name__ == "__main__":
    game = tetris_engine()
    game.spawn_piece()
    game.moveright()
    game.moveleft()
    game.moveright()
    game.moveleft()
    game.moveleft()
    game.update()
    game.update()

    game.display()
