import pygame
import sys
from engine import tetris_engine

# pygame initialization
pygame.init()
pygame.mixer.init()

# Grid Visual
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

# color definitions
BLACK = (10, 10, 10)
GRID_COLOR = (50, 50, 50)
WHITE = (255, 255, 255)
SIDEBAR_COLOR = (50, 50, 50)

# map color to different matrix shape
COLOR_MAP = {
    0: BLACK,
    1: (0, 240, 240),  # cyan
    2: (240, 240, 0),  # yellow
    3: (160, 0, 240),  # purple
    4: (255, 0, 0),  # Red
    5: (33, 117, 57),  # Weird green
    6: (255, 198, 57),  # orange
    7: (168, 128, 128),  # Random color
}

# window layout
SCREEN_WIDTH = (GRID_WIDTH * BLOCK_SIZE) + 300
SCREEN_HEIGHT = GRID_HEIGHT * BLOCK_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("TETRIS GAME")

# Load the background music
pygame.mixer.music.load(
    "gameresources/gregorquendel-tetris-theme-korobeiniki-rearranged-arr-for-music-box-184978.mp3"
)
rotate_sound = pygame.mixer.Sound("gameresources/rotate.ogg")
clear_sound = pygame.mixer.Sound("gameresources/clear.ogg")

# set the background volume
pygame.mixer.music.set_volume(0.6)

# play the music (-1) makes it loop forever
pygame.mixer.music.play(-1)


# setup tetris engine
engine = tetris_engine(rows=GRID_HEIGHT, cols=GRID_WIDTH)

# Drop the tetrinos block by this much or gravity implement for tetris
DROP_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(DROP_EVENT, 500)

font = pygame.font.SysFont("Arial", 24)


def draw_blocks(x, y, color_index):
    """Makes a tetris shape"""
    color = COLOR_MAP.get(color_index, WHITE)
    rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(screen, color, rect)
    if color != BLACK:
        pygame.draw.rect(screen, (0, 0, 0), rect, 1)


pygame.key.set_repeat(150, 50)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not engine.game_over:
                if event.key == pygame.K_LEFT:
                    engine.moveleft()
                elif event.key == pygame.K_RIGHT:
                    engine.moveright()

                elif event.key == pygame.K_DOWN:
                    engine.update()

                elif event.key == pygame.K_UP:
                    engine.rotation()
                    pygame.mixer.Sound.play(rotate_sound)

            else:
                # press R to restart
                if event.key == pygame.K_r:
                    engine = tetris_engine(rows=GRID_HEIGHT, cols=GRID_WIDTH)
                    pygame.mixer.music.play(-1)

                # press esc to quit
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # drop the teris block
        elif event.type == DROP_EVENT:
            engine.update()

    screen.fill(BLACK)

    # Draw block on the board
    for r_idx, row in enumerate(engine.board):
        for c_idx, val in enumerate(row):
            if val != 0:
                draw_blocks(c_idx, r_idx, val)

    # load the current piece
    if engine.current_piece:
        for r_idx, row in enumerate(engine.current_piece):
            for c_idx, val in enumerate(row):
                if val != 0:
                    draw_blocks(
                        c_idx + engine.piece_x,
                        r_idx + engine.piece_y,
                        engine.current_color,
                    )

    # Grid
    for x in range(GRID_WIDTH):  # vertical
        pygame.draw.line(
            screen, GRID_COLOR, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, SCREEN_HEIGHT)
        )
    for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):  # horizontal
        pygame.draw.line(screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

    # Draw side bar UI
    sidebar_rect = pygame.Rect(GRID_WIDTH * BLOCK_SIZE, 0, 300, SCREEN_HEIGHT)
    pygame.draw.rect(screen, SIDEBAR_COLOR, sidebar_rect)

    # next_piece = pygame.Rect(5000, 0, 300, 90)
    # pygame.draw.rect(screen, WHITE, next_piece)

    # Render Score
    score_render = font.render(f"SCORE: {engine.score}", True, (WHITE))
    screen.blit(score_render, (GRID_WIDTH * BLOCK_SIZE + 20, 30))

    if engine.game_over:
        pygame.mixer.music.stop()
        engine.save_high_score()
        high_score = font.render(f"HIGH SCORE: {engine.high_score}", True, WHITE)
        render = font.render("GAME OVER ", True, (255, 100, 90))
        restart = font.render("PRESS R TO RESTART", True, (255, 70, 80))
        e_xit = font.render("Press esc to quit", True, (100, 250, 150))

        screen.blit(high_score, (GRID_WIDTH * BLOCK_SIZE + 20, 70))
        screen.blit(render, (GRID_WIDTH * BLOCK_SIZE + 50, 300))
        screen.blit(restart, (GRID_WIDTH * BLOCK_SIZE + 10, 190))
        screen.blit(e_xit, (GRID_WIDTH * BLOCK_SIZE + 10, 150))

    if engine.lines_clear > 0:  # play the clear sound
        pygame.mixer.Sound.play(clear_sound)
        engine.lines_clear = 0

    pygame.display.flip()

pygame.quit()
sys.exit()
