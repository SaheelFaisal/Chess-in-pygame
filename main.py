import pygame

pygame.init()

# Constants
WIDTH = 720
HEIGHT = 720
SQUARE_LENGTH = 90
PIECE_SIZE = (59, 70)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

DARK_SQUARES = ('a1', 'a3', 'a5', 'a7', 
                'b2', 'b4', 'b6', 'b8', 
                'c1', 'c3', 'c5', 'c7', 
                'd2', 'd4', 'd6', 'd8', 
                'e1', 'e3', 'e5', 'e7', 
                'f2', 'f4', 'f6', 'f8', 
                'g1', 'g3', 'g5', 'g7', 
                'h2', 'h4', 'h6', 'h8')

LIGHT_SQUARES = ('a2', 'a4', 'a6', 'a8', 
                 'b1', 'b3', 'b5', 'b7', 
                 'c2', 'c4', 'c6', 'c8', 
                 'd1', 'd3', 'd5', 'd7', 
                 'e2', 'e4', 'e6', 'e8', 
                 'f1', 'f3', 'f5', 'f7', 
                 'g2', 'g4', 'g6', 'g8', 
                 'h1', 'h3', 'h5', 'h7')




# Setting up the window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# Game constants
FPS = 60
CLOCK = pygame.time.Clock()

# Load Images
# Squares
DARK_SQUARE = pygame.image.load("assets/dark_square.png").convert()
LIGHT_SQUARE = pygame.image.load("assets/light_square.png").convert()

# White pieces
WHITE_PAWN = pygame.image.load("assets/w_pawn.png").convert_alpha()
WHITE_BISHOP = pygame.image.load("assets/w_bishop.png").convert_alpha()
WHITE_KNIGHT = pygame.image.load("assets/w_knight.png").convert_alpha()
WHITE_ROOK = pygame.image.load("assets/w_rook.png").convert_alpha()
WHITE_QUEEN = pygame.image.load("assets/w_queen.png").convert_alpha()
WHITE_KING = pygame.image.load("assets/w_king.png").convert_alpha()

# Black pieces
BLACK_PAWN = pygame.image.load("assets/b_pawn.png").convert_alpha()
BLACK_BISHOP = pygame.image.load("assets/b_bishop.png").convert_alpha()
BLACK_KNIGHT = pygame.image.load("assets/b_knight.png").convert_alpha()
BLACK_ROOK = pygame.image.load("assets/b_rook.png").convert_alpha()
BLACK_QUEEN = pygame.image.load("assets/b_queen.png").convert_alpha()
BLACK_KING = pygame.image.load("assets/b_king.png").convert_alpha()

class Square:
    def __init__(self, name):
        self.length = SQUARE_LENGTH
        self.name = name
        self.piece = None

        if self.name in DARK_SQUARES:
            self.color = "dark"
        elif self.name in LIGHT_SQUARES:
            self.color = "light"
        else:
            raise Exception("Square name not valid")
        
        if self.color == "dark":
            self.img = DARK_SQUARE
        else:
            self.img = LIGHT_SQUARE
        
    def get_position(self):
        match self.name[0]:
            case "a":
                x_pos = 0
            case "b":
                x_pos = 90
            case "c":
                x_pos = 180
            case "d":
                x_pos = 270
            case "e":
                x_pos = 360
            case "f":
                x_pos = 450
            case "g":
                x_pos = 540
            case "h":
                x_pos = 630
            case _:
                raise Exception("Square name not valid")
            
        match self.name[1]:
            case "8":
                y_pos = 0
            case "7":
                y_pos = 90
            case "6":
                y_pos = 180
            case "5":
                y_pos = 270
            case "4":
                y_pos = 360
            case "3":
                y_pos = 450
            case "2":
                y_pos = 540
            case "1":
                y_pos = 630
            case _:
                raise Exception("Square name not valid")
        
        return (x_pos, y_pos)
    
    def draw(self):
        WIN.blit(self.img, self.get_position())
        match self.piece:
            case "w_pawn":
                WIN.blit(WHITE_PAWN, self.piece_coord())
            case "b_pawn":
                WIN.blit(BLACK_PAWN, self.piece_coord())
            case "w_bishop":
                WIN.blit(WHITE_BISHOP, self.piece_coord())
            case "b_bishop":
                WIN.blit(BLACK_BISHOP, self.piece_coord())
            case "w_knight":
                WIN.blit(WHITE_KNIGHT, self.piece_coord())
            case "b_knight":
                WIN.blit(BLACK_KNIGHT, self.piece_coord())
            case "w_rook":
                WIN.blit(WHITE_ROOK, self.piece_coord())
            case "b_rook":
                WIN.blit(BLACK_ROOK, self.piece_coord())
            case "w_queen":
                WIN.blit(WHITE_QUEEN, self.piece_coord())
            case "b_queen":
                WIN.blit(BLACK_QUEEN, self.piece_coord())
            case "w_king":
                WIN.blit(WHITE_KING, self.piece_coord())
            case "b_king":
                WIN.blit(BLACK_KING, self.piece_coord())
            case _:
                return

    def piece_coord(self):
        if self.piece in ["w_pawn", "b_pawn"]:
            return ((self.get_position()[0] + 17), (self.get_position()[1] + 10))

        elif self.piece in ["w_bishop", "b_bishop"]:
            return ((self.get_position()[0] + 8), (self.get_position()[1] + 4))
        
        else:
            return ((self.get_position()[0] + 8), (self.get_position()[1] + 4))

class Board:
    def __init__(self):
        self.length = 8 * SQUARE_LENGTH
        self.squares = []

        square_list =  ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8', 
                        'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7', 
                        'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6', 
                        'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5', 
                        'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4', 
                        'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3', 
                        'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2', 
                        'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']     
        
        for square_name in square_list:
            self.squares.append(Square(square_name))

        self.reset_board()
                
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
    # Event loop
    running = True

    board = Board()
    
    #pawn.set_colorkey(BLACK)
    #pawn = pygame.transform.scale(pawn, PIECE_SIZE)

    while running:
        CLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        WIN.fill(BLACK)                         # Black Background
        # square = board.get_square("d2")
        # square.img.blit(pawn, (10, 10))
        
        #board.reset_pos()
        board.draw()
        #pygame.time.delay()
        pygame.display.update()

    pygame.quit()
    #print(board.get_square("d2").img)

if __name__ == "__main__":
    main()