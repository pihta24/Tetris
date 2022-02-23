from structures import Board, Figure


def generate_board(w: int, h: int):
    board = Board(w, h)
    board.set_view(25, 25, 20)
    FULL_LINE = [1] * w
    return board, FULL_LINE
    
    
def generate_square(b: Board):
    return Figure(b, [b.width // 2, 0], [b.width // 2, 1], [b.width // 2 + 1, 0], [b.width // 2 + 1, 1])
