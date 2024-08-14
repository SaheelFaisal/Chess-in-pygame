import pygame

pygame.init()

# Constants
WIDTH = 720
HEIGHT = 720
SQUARE_SIZE = 90
PIECE_SIZE = (59, 70)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Define square colors
DARK_SQUARES = {'a1', 'a3', 'a5', 'a7', 'b2', 'b4', 'b6', 'b8', 'c1', 'c3', 'c5', 'c7',
                'd2', 'd4', 'd6', 'd8', 'e1', 'e3', 'e5', 'e7', 'f2', 'f4', 'f6', 'f8',
                'g1', 'g3', 'g5', 'g7', 'h2', 'h4', 'h6', 'h8'}
LIGHT_SQUARES = {'a2', 'a4', 'a6', 'a8', 'b1', 'b3', 'b5', 'b7', 'c2', 'c4', 'c6', 'c8',
                  'd1', 'd3', 'd5', 'd7', 'e2', 'e4', 'e6', 'e8', 'f1', 'f3', 'f5', 'f7',
                  'g2', 'g4', 'g6', 'g8', 'h1', 'h3', 'h5', 'h7'}

# Set up window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# Game constants
FPS = 60
CLOCK = pygame.time.Clock()

# Load images
DARK_SQUARE_IMG = pygame.image.load("assets/dark_square.png").convert()
LIGHT_SQUARE_IMG = pygame.image.load("assets/light_square.png").convert()

WHITE_PAWN = pygame.image.load("assets/w_pawn.png").convert_alpha()
WHITE_BISHOP = pygame.image.load("assets/w_bishop.png").convert_alpha()
WHITE_KNIGHT = pygame.image.load("assets/w_knight.png").convert_alpha()
WHITE_ROOK = pygame.image.load("assets/w_rook.png").convert_alpha()
WHITE_QUEEN = pygame.image.load("assets/w_queen.png").convert_alpha()
WHITE_KING = pygame.image.load("assets/w_king.png").convert_alpha()

BLACK_PAWN = pygame.image.load("assets/b_pawn.png").convert_alpha()
BLACK_BISHOP = pygame.image.load("assets/b_bishop.png").convert_alpha()
BLACK_KNIGHT = pygame.image.load("assets/b_knight.png").convert_alpha()
BLACK_ROOK = pygame.image.load("assets/b_rook.png").convert_alpha()
BLACK_QUEEN = pygame.image.load("assets/b_queen.png").convert_alpha()
BLACK_KING = pygame.image.load("assets/b_king.png").convert_alpha()

class Square:
    def __init__(self, name):
        self.length = SQUARE_SIZE
        self.name = name
        self.piece = None
        self.border = None

        if self.name in DARK_SQUARES:
            self.color = "dark"
        elif self.name in LIGHT_SQUARES:
            self.color = "light"
        else:
            raise Exception("Square name not valid")
        
        if self.color == "dark":
            self.img = DARK_SQUARE_IMG
        else:
            self.img = LIGHT_SQUARE_IMG
        
    def get_position(self):
        x_pos = ord(self.name[0]) - ord('a')
        y_pos = 8 - int(self.name[1])
        return (x_pos * SQUARE_SIZE, y_pos * SQUARE_SIZE)
    
    def draw(self):
        WIN.blit(self.img, self.get_position())

        if self.border:
            pygame.draw.rect(WIN, self.border, (self.get_position()[0], self.get_position()[1], SQUARE_SIZE, SQUARE_SIZE), 3)

        if self.piece:
            piece_img = {
                "w_pawn": WHITE_PAWN,
                "b_pawn": BLACK_PAWN,
                "w_bishop": WHITE_BISHOP,
                "b_bishop": BLACK_BISHOP,
                "w_knight": WHITE_KNIGHT,
                "b_knight": BLACK_KNIGHT,
                "w_rook": WHITE_ROOK,
                "b_rook": BLACK_ROOK,
                "w_queen": WHITE_QUEEN,
                "b_queen": BLACK_QUEEN,
                "w_king": WHITE_KING,
                "b_king": BLACK_KING
            }.get(self.piece)
            WIN.blit(piece_img, self.piece_coord())

    def piece_coord(self):
        coords = {
            "w_pawn": (17, 10),
            "b_pawn": (17, 10),
            "w_bishop": (8, 4),
            "b_bishop": (8, 4),
            "w_knight": (8, 4),
            "b_knight": (8, 4),
            "w_queen": (5, 7),
            "b_queen": (5, 7),
            "w_rook": (10, 6),
            "b_rook": (10, 6),
            "w_king": (8, 4),
            "b_king": (8, 4)
        }
        return (self.get_position()[0] + coords[self.piece][0], self.get_position()[1] + coords[self.piece][1])

class Board:
    def __init__(self):
        self.size = 8 * SQUARE_SIZE
        self.squares = []

        self.board = [['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'], 
                      ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'], 
                      ['a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6'], 
                      ['a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5'], 
                      ['a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4'], 
                      ['a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3'], 
                      ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2'], 
                      ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']]
        
        for rank in self.board:
            for square_name in rank:
                self.squares.append(Square(square_name))

        self.reset_board()
        self.selected_square = None
        self.turn = "white"
                
    def draw(self):
        for square in self.squares:
            square.draw()
    
    def get_square(self, name):
        for square in self.squares:
            if square.name == name:
                return square

        raise Exception("Square name not valid")

    def reset_board(self):
        for square in self.squares:
            if square.name[1] == "2":
                square.piece = "w_pawn"
            elif square.name[1] == "7":
                square.piece = "b_pawn"
            elif square.name in ["c1", "f1"]:
                square.piece = "w_bishop"
            elif square.name in ["c8", "f8"]:
                square.piece = "b_bishop"
            elif square.name in ["b1", "g1"]:
                square.piece = "w_knight"
            elif square.name in ["b8", "g8"]:
                square.piece = "b_knight"
            elif square.name in ["a1", "h1"]:
                square.piece = "w_rook"
            elif square.name in ["a8", "h8"]:
                square.piece = "b_rook"
            elif square.name == "d1":
                square.piece = "w_queen"
            elif square.name == "d8":
                square.piece = "b_queen"
            elif square.name == "e1":
                square.piece = "w_king"
            elif square.name == "e8":
                square.piece = "b_king"

def main():
    running = True
    chess_board = Board()

    while running:
        CLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:  # left click
                    pos_x, pos_y = pygame.mouse.get_pos()
                    col = pos_x // SQUARE_SIZE
                    row = 7 - (pos_y // SQUARE_SIZE)
                    square_name = chr(ord('a') + col) + str(row + 1)
                    clicked_square = chess_board.get_square(square_name)

                    if chess_board.selected_square:
                        # Move piece logic
                        from_square = chess_board.get_square(chess_board.selected_square.name)
                        to_square = clicked_square

                        # Simple movement logic: Move if the piece belongs to the current player and the destination is empty
                        if from_square.piece and from_square.piece.startswith(chess_board.turn[0]) and not to_square.piece:
                            to_square.piece = from_square.piece
                            from_square.piece = None
                            chess_board.turn = "black" if chess_board.turn == "white" else "white"
                        
                        chess_board.selected_square.border = None
                        chess_board.selected_square = None
                    else:
                        # Select piece logic
                        if clicked_square.piece and clicked_square.piece.startswith(chess_board.turn[0]):
                            clicked_square.border = GREEN
                            chess_board.selected_square = clicked_square

        WIN.fill(BLACK)
        chess_board.draw()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

    
