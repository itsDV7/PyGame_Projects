import math
import menu
import os
import pygame as pg
import help
from random import randint, choices, choice

# Pygame Settings
pg.init()
pg.mouse.set_visible(False)

# Defaults
WIDTH, HEIGHT = (1280, 720)
BOARD_WIDTH, BOARD_HEIGHT = (20, 120)
POWER_WIDTH, POWER_HEIGHT = (75, 75)
RADIUS = 10
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("2 Player Pong! v2")
CLOCK = pg.time.Clock()
FPS = 60
COLOR = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "GREEN": (8, 255, 8),
    "GREEN2": (0, 255, 0),
    "RED": (255, 0, 0),
    "YELLOW": (255, 255, 0),
    "PINK": (255, 105, 180),
    "GOLD": (255, 215, 0),
    "AQUA": (127, 255, 212),
    "GRAY": (169, 169, 169)
}
POWER_NAMES = {
    "expand": "Expand Board!",
    "shrink": "Shrink Board!",
    "slow_board": "Slow Board!",
    "slow_ball": "Slow Ball!",
    "extreme_ball": "Extreme Ball!",
    "double_ball": "Double Ball!",
    "golden": "Golden Ability!",
    "shield": "Shields Activated!"
}
HIT_COUNTER = 0

# Userevents
SCORE_LEFT = pg.USEREVENT + 1
SCORE_RIGHT = pg.USEREVENT + 2
POWER_HIT = pg.USEREVENT + 3
DOUBLE_BALL = pg.USEREVENT + 4
REDUCE_SCORE_RIGHT = pg.USEREVENT + 5
REDUCE_SCORE_LEFT = pg.USEREVENT + 6
RIGHT_SHIELD = pg.USEREVENT + 7
LEFT_SHIELD = pg.USEREVENT + 8
SLOW_BOARD = pg.USEREVENT + 9

# Fonts
SCORE_FONT = pg.font.SysFont("Freshman", 400)
SYMBOL_FONT = pg.font.SysFont("Freshman", 60)
PROMPT_FONT = pg.font.SysFont("Freshman", 100)
PROMPT_FONT2 = pg.font.SysFont("Freshman", 40)

# Assets
GREEN_BALL_IMAGE = pg.image.load(os.path.join("Assets", "GreenBall.png"))
YELLOW_BALL_IMAGE = pg.image.load(os.path.join("Assets", "YellowBall.png"))
RED_BALL_IMAGE = pg.image.load(os.path.join("Assets", "RedBall.png"))
GREEN_BALL = pg.transform.scale(GREEN_BALL_IMAGE, (2*RADIUS + 6, 2*RADIUS + 6))
YELLOW_BALL = pg.transform.scale(YELLOW_BALL_IMAGE, (2*RADIUS + 6, 2*RADIUS + 6))
RED_BALL = pg.transform.scale(RED_BALL_IMAGE, (2*RADIUS + 6, 2*RADIUS + 6))

BOARD_IMAGE_PATH = pg.image.load(os.path.join("Assets", "Paddle.png"))
SLOW_BOARD_IMAGE_PATH = pg.image.load(os.path.join("Assets", "SlowPaddle.png"))

BG_IMAGE_PATH = pg.image.load(os.path.join("Assets", "SpaceBG.png"))
BG_IMAGE = pg.transform.scale(BG_IMAGE_PATH, (WIDTH, HEIGHT))

BLUE_BLOCK_PATH = pg.image.load(os.path.join("Assets", "BlueBlock.png"))
BLUE_BLOCK2_PATH = pg.image.load(os.path.join("Assets", "BlueBlock2.png"))
GREEN_BLOCK_PATH = pg.image.load(os.path.join("Assets", "GreenBlock.png"))
ORANGE_BLOCK_PATH = pg.image.load(os.path.join("Assets", "OrangeBlock.png"))
PINK_BLOCK_PATH = pg.image.load(os.path.join("Assets", "PinkBlock.png"))
PINK_BLOCK2_PATH = pg.image.load(os.path.join("Assets", "BlueBlock2.png"))
RED_BLOCK_PATH = pg.image.load(os.path.join("Assets", "RedBlock.png"))
YELLOW_BLOCK_PATH = pg.image.load(os.path.join("Assets", "YellowBlock.png"))
POINTER_IMAGE_PATH = pg.image.load(os.path.join("Assets", "MousePointer.png"))
POINTER_IMAGE = pg.transform.scale(POINTER_IMAGE_PATH, (40, 40))

BEEP_BOARD_SOUND = pg.mixer.Sound(os.path.join("Assets", "BeepBoard.ogg"))
BEEP_WALL_SOUND = pg.mixer.Sound(os.path.join("Assets", "BeepWall.ogg"))


class Board:
    # Class for Left and Right Boards
    VEL = 15

    def __init__(self, x, y, width, height):
        self.x = self.initial_x = x
        self.y = self.initial_y = y
        self.width = width
        self.height = self.initial_height = height
        self.vel = self.VEL
        self.color = COLOR["WHITE"]

    # Draw Board
    def draw(self, win):
        board_pos = pg.Rect(self.x, self.y, self.width, self.height)
        if self.color == COLOR["GRAY"]:
            slow_board_image = pg.transform.scale(SLOW_BOARD_IMAGE_PATH, (self.width, self.height))
            win.blit(slow_board_image, board_pos)
        else:
            board_image = pg.transform.scale(BOARD_IMAGE_PATH, (self.width, self.height))
            win.blit(board_image, board_pos)

    # Board Movement
    def move(self, up=False, down=False):
        if up:
            if self.y - self.vel >= -5:
                self.y -= self.vel
            else:
                self.y = -5
        if down:
            if self.y + self.height + self.vel <= HEIGHT + 5:
                self.y += self.vel
            else:
                self.y = HEIGHT - self.height + 5

    # Board Reset
    def reset(self):
        self.x = self.initial_x
        self.y = self.initial_y
        self.height = self.initial_height
        self.vel = self.VEL


class Ball:
    # Class for pong balls
    VEL = 5
    INITIAL_MAX_VEL = MAX_VEL = 10
    EX_VEL = 15

    def __init__(self, x, y, radius):
        self.x = self.initial_x = x
        self.y = self.initial_y = y
        self.radius = radius
        self.x_vel = choice([-1 * self.VEL, self.VEL])
        self.y_vel = randint(-5, 5)
        self.color = COLOR["GREEN"]
        self.max_r = math.sqrt(math.pow(self.MAX_VEL, 2) + math.pow(self.MAX_VEL, 2))

    # Draw pong balls
    def draw(self, win):
        ball_pos = (self.x, self.y)
        image_pos = (ball_pos[0] - self.radius, ball_pos[1] - self.radius)
        if self.color == COLOR["GREEN"]:
            win.blit(GREEN_BALL, image_pos)
        elif self.color == COLOR["YELLOW"]:
            win.blit(YELLOW_BALL, image_pos)
        elif self.color == COLOR["RED"]:
            win.blit(RED_BALL, (image_pos[0]+5, image_pos[1]+5))

    # Pong balls movement
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    # Reset pong balls
    def reset(self):
        self.x = self.initial_x
        self.y = self.initial_y
        self.x_vel = choice([-1 * self.VEL, self.VEL])
        self.y_vel = randint(-5, 5)
        self.color = COLOR["GREEN"]
        self.MAX_VEL = self.INITIAL_MAX_VEL


class Powerups:
    # Class for powerups
    def __init__(self, x, y, win):
        self.x = x
        self.y = y
        self.win = win
        self.symbol = ""
        self.power_color = ""
        self.symbol_color = ""
        self.width = POWER_WIDTH
        self.height = POWER_HEIGHT
        self.test_blit = None

    # Expand -> + Board Length -> +
    def expand(self):
        self.symbol = "+"
        self.power_color = COLOR["GREEN2"]
        self.symbol_color = COLOR["BLACK"]
        self.test_blit = GREEN_BLOCK_PATH

    # Shrink -> - Board Length -> -
    def shrink(self):
        self.symbol = "-"
        self.power_color = COLOR["RED"]
        self.symbol_color = COLOR["BLACK"]
        self.test_blit = ORANGE_BLOCK_PATH

    # Slow Board -> Slow Opponent -> S
    def slow_board(self):
        self.symbol = "S"
        self.power_color = COLOR["GREEN2"]
        self.symbol_color = COLOR["BLACK"]
        self.test_blit = PINK_BLOCK_PATH

    # Slow Ball -> Ball to Minimum speed -> 0
    def slow_ball(self):
        self.symbol = "0"
        self.power_color = COLOR["GREEN2"]
        self.symbol_color = COLOR["BLACK"]
        self.test_blit = PINK_BLOCK2_PATH

    # Extreme Ball -> Sudden Max Velocity -> Make ball Red -> F
    def extreme_ball(self):
        self.symbol = "F"
        self.power_color = COLOR["RED"]
        self.symbol_color = COLOR["BLACK"]
        self.test_blit = RED_BLOCK_PATH

    # Double Ball -> Double the number of balls -> Switch y_vel -> D
    def double_ball(self):
        self.symbol = "D"
        self.power_color = COLOR["RED"]
        self.symbol_color = COLOR["BLACK"]
        self.test_blit = YELLOW_BLOCK_PATH

    # Golden Ability -> -1 Point -> G
    def golden(self):
        self.symbol = "G"
        self.power_color = COLOR["GOLD"]
        self.symbol_color = COLOR["BLACK"]
        self.test_blit = BLUE_BLOCK_PATH

    # Shield -> Ball cant pass -> P
    def shield(self):
        self.symbol = "P"
        self.power_color = COLOR["GOLD"]
        self.symbol_color = COLOR["BLACK"]
        self.test_blit = BLUE_BLOCK2_PATH

    # Draw powerups
    def draw_powerup(self):
        outer_rect = pg.Rect(self.x, self.y, self.width, self.height)
        inner_rect = pg.Rect(self.x + 5, self.y + 5, self.width - 10, self.height - 10)
        inner_rect_x_middle = (self.x + 5 + inner_rect.width // 2)
        inner_rect_y_middle = (self.y + 5 + inner_rect.height // 2)
        symbol = SYMBOL_FONT.render(str(self.symbol), True, self.symbol_color)
        box = pg.transform.scale(self.test_blit, (outer_rect.width, outer_rect.height))
        self.win.blit(box, (outer_rect.x, outer_rect.y))
        self.win.blit(symbol, (inner_rect_x_middle - symbol.get_width() // 2,
                               inner_rect_y_middle - symbol.get_height() // 2))


class ApplyPowers:
    # Class to apply powerup effects
    def __init__(self, powerup_choice, ball, left_board, right_board, right_shield, left_shield, balls):
        self.powerup_name = powerup_choice.__name__
        self.left_board = left_board
        self.right_board = right_board
        self.ball = ball
        self.right_shield = right_shield
        self.left_shield = left_shield
        self.balls = balls

    # Apply the effect according to name
    def give(self):
        # Expand -> + Board Length -> +
        if self.powerup_name == "expand":
            if self.ball.x_vel >= 0:
                if self.left_board.height + 50 <= HEIGHT//2:
                    self.left_board.height += 50
            else:
                if self.right_board.height + 50 <= HEIGHT//2:
                    self.right_board.height += 50
        # Shrink -> - Board Length -> -
        if self.powerup_name == "shrink":
            if self.ball.x_vel >= 0:
                if self.left_board.height - 50 >= BOARD_HEIGHT:
                    self.left_board.height -= 50
            else:
                if self.right_board.height - 50 >= BOARD_HEIGHT:
                    self.right_board.height -= 50
        # Slow Board -> Slow Opponent -> S
        if self.powerup_name == "slow_board":
            pg.event.post(pg.event.Event(SLOW_BOARD))
        # Slow Ball -> Ball to Minimum speed -> 0
        if self.powerup_name == "slow_ball":
            for ball in self.balls:
                ball.color = COLOR["GREEN"]
                ball.MAX_VEL = ball.INITIAL_MAX_VEL
                theta = math.atan(ball.y_vel/ball.x_vel)
                r = math.sqrt(math.pow(ball.VEL, 2) + math.pow(ball.VEL, 2))
                if ball.x_vel > 0:
                    ball.x_vel = abs(r * math.cos(theta))
                else:
                    ball.x_vel = -1 * abs(r * math.cos(theta))
                if ball.y_vel >= 0:
                    ball.y_vel = abs(r * math.sin(theta))
                else:
                    ball.y_vel = -1 * abs(r * math.sin(theta))
        # Extreme Ball -> Sudden Max Velocity -> Make ball Red -> F
        if self.powerup_name == "extreme_ball":
            self.ball.MAX_VEL = self.ball.EX_VEL
            theta = math.atan(self.ball.y_vel/self.ball.x_vel)
            r = math.sqrt(math.pow(self.ball.EX_VEL, 2) + math.pow(self.ball.EX_VEL, 2))
            if self.ball.x_vel > 0:
                self.ball.x_vel = abs(r * math.cos(theta))
            else:
                self.ball.x_vel = -1 * abs(r * math.cos(theta))
            if self.ball.y_vel >= 0:
                self.ball.y_vel = abs(r * math.sin(theta))
            else:
                self.ball.y_vel = -1 * abs(r * math.sin(theta))
            self.ball.color = COLOR["RED"]
        # Double Ball -> Double the number of balls -> Switch y_vel -> D
        if self.powerup_name == "double_ball":
            pg.event.post(pg.event.Event(DOUBLE_BALL))
        # Golden Ability -> -1 Point -> G
        if self.powerup_name == "golden":
            if self.ball.x_vel >= 0:
                pg.event.post(pg.event.Event(REDUCE_SCORE_RIGHT))
            else:
                pg.event.post(pg.event.Event(REDUCE_SCORE_LEFT))
        # Shield -> Ball cant pass -> P
        if self.powerup_name == "shield":
            if self.ball.x_vel >= 0:
                if not self.left_shield:
                    pg.event.post(pg.event.Event(LEFT_SHIELD))
            else:
                if not self.right_shield:
                    pg.event.post(pg.event.Event(RIGHT_SHIELD))


def handle_board_movement(keys, left_board, right_board, balls, ai):
    if keys:
        pass
    # Handles board movements
    if ai:
        # Left Board Player
        if keys[pg.K_w] or keys[pg.K_UP]:
            left_board.move(up=True)
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            left_board.move(down=True)

        # Right Board AI
        closest_ball = math.inf
        incoming = -1
        for i, ball in enumerate(balls):
            if ball.x_vel >= 0:
                if closest_ball >= abs(right_board.x - ball.x):
                    closest_ball = abs(right_board.x - ball.x)
                    incoming = i
        if incoming == -1:
            follow_ball = balls[0]
        else:
            follow_ball = balls[incoming]
        if follow_ball.y > right_board.y + right_board.height//4:
            right_board.move(down=True)
        if follow_ball.y < right_board.y + right_board.height - right_board.height//4:
            right_board.move(up=True)

        # Left Board AI (For Test Purposes)
        # close = math.inf
        # inc = -1
        # for i, ball in enumerate(balls):
        #    if ball.x_vel <= 0:
        #        if close >= abs(left_board.x - ball.x):
        #            close = abs(left_board.x - ball.x)
        #            inc = i
        # if inc == -1:
        #    follow = balls[0]
        # else:
        #    follow = balls[inc]
        # if follow.y > left_board.y + left_board.height//2:
        #    left_board.move(down=True)
        # if follow.y < left_board.y + left_board.height//2:
        #    left_board.move(up=True)

    else:
        if keys[pg.K_w]:
            left_board.move(up=True)
        if keys[pg.K_s]:
            left_board.move(down=True)
        if keys[pg.K_UP]:
            right_board.move(up=True)
        if keys[pg.K_DOWN]:
            right_board.move(down=True)


def reset_game(balls, boards):
    # Resets game to default
    for ball in balls:
        ball.reset()
    for board in boards:
        board.reset()


def calculate_velocity(ball, board, keys):
    x = ball.x_vel
    y = ball.y_vel
    hit_distance = abs((board.y + board.height//2) - ball.y)
    angle_per_pixel = 45 / (board.height//2)
    reflect_angle = hit_distance * angle_per_pixel
    reflect_angle = math.radians(reflect_angle)
    r = min(math.sqrt(math.pow(ball.MAX_VEL, 2) + math.pow(ball.MAX_VEL, 2)),
            (math.sqrt(math.pow(x, 2) + math.pow(y, 2)))+1)
    if r < 10:
        ball.color = COLOR["GREEN"]
    elif 10 <= r <= 15:
        ball.color = COLOR["YELLOW"]
    if x >= 0:
        new_x = -1 * abs(r * math.cos(reflect_angle))
    else:
        new_x = abs(r * math.cos(reflect_angle))
    if y >= 0:
        new_y = abs(r * math.sin(reflect_angle))
    else:
        new_y = -1 * abs(r * math.sin(reflect_angle))
    if x >= 0 and keys[pg.K_UP]:
        new_y = -1 * abs(new_y)
    elif x >= 0 and keys[pg.K_DOWN]:
        new_y = abs(new_y)
    elif x < 0 and keys[pg.K_w]:
        new_y = -1 * abs(new_y)
    elif x < 0 and keys[pg.K_s]:
        new_y = abs(new_y)
    return new_x, new_y


def handle_ball_collision(balls, left_board, right_board, right_shield, left_shield, keys):
    global HIT_COUNTER

    left_board_rect = pg.Rect(left_board.x, left_board.y, left_board.width, left_board.height)
    right_board_rect = pg.Rect(right_board.x, right_board.y, right_board.width, right_board.height)
    # Handles ball collision and speed
    for ball in balls:
        # Right shield collision
        if right_shield:
            if ball.x - ball.radius >= WIDTH:
                ball.x_vel = -1 * ball.x_vel
                pg.event.post(pg.event.Event(RIGHT_SHIELD))
        else:
            if ball.x - ball.radius >= WIDTH:
                left_board.reset()
                right_board.reset()
                pg.event.post(pg.event.Event(SCORE_LEFT))
        # Left shield collision
        if left_shield:
            if ball.x + ball.radius <= 0:
                ball.x_vel = -1 * ball.x_vel
                pg.event.post(pg.event.Event(LEFT_SHIELD))
        else:
            if ball.x + ball.radius <= 0:
                left_board.reset()
                right_board.reset()
                pg.event.post(pg.event.Event(SCORE_RIGHT))
        # Collision with Ceil and Floor
        if (ball.y - ball.radius <= 0) or (ball.y + ball.radius >= HEIGHT):
            ball.y_vel *= -1
            pg.mixer.Sound.play(BEEP_WALL_SOUND)
        # Right board collision and speed
        if right_board_rect.collidepoint(((ball.x + ball.radius), ball.y)):
            ball.x_vel, ball.y_vel = calculate_velocity(ball, right_board, keys)
            ball.x = right_board.x - ball.radius - 1
            HIT_COUNTER += 1
            pg.mixer.Sound.play(BEEP_BOARD_SOUND)
            continue
        # Left board collision and speed
        if left_board_rect.collidepoint(((ball.x - ball.radius), ball.y)):
            ball.x_vel, ball.y_vel = calculate_velocity(ball, left_board, keys)
            ball.x = left_board.x + left_board.width + ball.radius + 1
            HIT_COUNTER += 1
            pg.mixer.Sound.play(BEEP_BOARD_SOUND)
            continue


def handle_powerup_collision(powerup, spawn_power, balls):
    # Handles collision of ball and powerups
    x = powerup.x
    y = powerup.y
    width = powerup.width
    height = powerup.height
    powerup_pos = [
        (x, y),
        (x+width, y),
        (x, y+height),
        (x+width, y+height),
        (x+(width//2), y),
        (x, y+(height//2)),
        (x+width, y+(height//2)),
        (x+(width//2), y+height)
    ]

    if spawn_power:
        for ball in balls:
            collide = False
            for pos in powerup_pos:
                if (((ball.x - pos[0])**2) + ((ball.y - pos[1])**2)) <= (ball.radius**2):
                    pg.event.post(pg.event.Event(POWER_HIT))
                    collide = True
                    break
                elif (x <= ball.x <= (x + width)) and (y <= ball.y <= (y + height)):
                    pg.event.post(pg.event.Event(POWER_HIT))
                    collide = True
                    break
            if collide:
                return ball


def powerup_randomizer():
    # Generates a random position for powerup to spawn
    powerup_x = randint(WIDTH // 4 - POWER_WIDTH, (WIDTH // 2 + WIDTH // 4) - POWER_WIDTH)
    powerup_y = randint(0, HEIGHT - POWER_HEIGHT)
    powerup = Powerups(powerup_x, powerup_y, WIN)
    powerup_list = [
        powerup.expand,
        powerup.shrink,
        powerup.slow_board,
        powerup.slow_ball,
        powerup.extreme_ball,
        powerup.double_ball,
        powerup.golden,
        powerup.shield
    ]
    powerup_weights = [
        65,
        50,
        25,
        40,
        15,
        30,
        1,
        10
    ]
    powerup_choice = choices(powerup_list, powerup_weights)
    return powerup, powerup_x, powerup_y, powerup_choice


def draw_dashed_line(win, color, start_pos, end_pos, width):
    # Draw dashed line in the middle of screen
    for i in range(start_pos, end_pos-5, 5):
        if i % 2 == 0:
            continue
        dash = pg.Rect(WIDTH//2 - width//2, i, width, 5)
        pg.draw.rect(win, color, dash)


def draw_assets(win, boards, balls, score_left, score_right, spawn_power, powerup_choice, powerup,
                right_shield, left_shield, winner, countdown, game_start, ai, power_prompt, power_name):
    global HIT_COUNTER
    # Draw all assets of the game
    win.fill(COLOR["BLACK"])
    win.blit(BG_IMAGE, (0, 0))
    draw_dashed_line(win, COLOR["WHITE"], 0, HEIGHT, 5)

    # Renders
    left_score_text = SCORE_FONT.render(str(score_left), True, COLOR["WHITE"])
    right_score_text = SCORE_FONT.render(str(score_right), True, COLOR["WHITE"])
    winner_text = PROMPT_FONT.render(str(winner), True, COLOR["GOLD"])
    countdown_text = PROMPT_FONT.render(f"Starts in... {str(countdown)}", True, COLOR["GOLD"])
    help_text = PROMPT_FONT2.render("Press R to Restart Game.", True, COLOR["GOLD"])
    help_text2 = PROMPT_FONT2.render("Press any key to start!", True, COLOR["GOLD"])
    left_paddle_help_text = PROMPT_FONT2.render("W KEY", True, COLOR["GOLD"])
    left_paddle_help_text2 = PROMPT_FONT2.render("S KEY", True, COLOR["GOLD"])
    right_paddle_help_text = PROMPT_FONT2.render("UP ARROW", True, COLOR["GOLD"])
    right_paddle_help_text2 = PROMPT_FONT2.render("DOWN ARROW", True, COLOR["GOLD"])
    ai_paddle_help_text = PROMPT_FONT2.render("AI", True, COLOR["GOLD"])
    right_shield_rect = pg.Rect(WIDTH - 2, 0, 2, HEIGHT)
    left_shield_rect = pg.Rect(0, 0, 2, HEIGHT)
    if power_prompt:
        power_name = PROMPT_FONT.render(POWER_NAMES[power_name], True, COLOR["GREEN2"])
    else:
        power_name = ""
    # Draw scores
    win.blit(left_score_text,
             (WIDTH // 4 - left_score_text.get_width() // 2,
              HEIGHT // 2 - left_score_text.get_height() // 2))
    win.blit(right_score_text,
             (WIDTH//2 + WIDTH // 4 - right_score_text.get_width() // 2,
              HEIGHT // 2 - right_score_text.get_height() // 2))
    # Draw right shields
    if right_shield:
        pg.draw.rect(win, COLOR["AQUA"], right_shield_rect)
    # Draw left shields
    if left_shield:
        pg.draw.rect(win, COLOR["AQUA"], left_shield_rect)
    # Draw boards
    for board in boards:
        board.draw(win)
    # Draw balls
    for ball in balls:
        ball.draw(win)
    # Draw powerups
    if spawn_power:
        if powerup_choice:
            powerup_choice[0]()
            powerup.draw_powerup()
    # Show countdown
    if countdown != 0 and not game_start:
        win.blit(countdown_text, ((WIDTH//2 - countdown_text.get_width()//2),
                                  (HEIGHT//2 - countdown_text.get_height()//2)))
    # Show winner
    if winner:
        win.blit(winner_text, ((WIDTH//2 - winner_text.get_width()//2),
                               (HEIGHT//2 - winner_text.get_height()//2)))
        win.blit(help_text, ((WIDTH//2 - help_text.get_width()//2),
                             (HEIGHT//2 + winner_text.get_height() - help_text.get_height()//2)))
        reset_game(balls, boards)
    # Show start game countdown
    if game_start:
        win.blit(help_text2, ((WIDTH//2 - help_text2.get_width()//2), (HEIGHT//2 - help_text2.get_height()//2)))
        win.blit(left_paddle_help_text, (0, (HEIGHT//4)))
        win.blit(left_paddle_help_text2, (0, (HEIGHT//2 + HEIGHT//4)))
        if ai:
            win.blit(ai_paddle_help_text, ((WIDTH - ai_paddle_help_text.get_width()), (HEIGHT//4)))
            win.blit(ai_paddle_help_text, ((WIDTH - ai_paddle_help_text.get_width()), (HEIGHT//2 + HEIGHT//4)))
        else:
            win.blit(right_paddle_help_text, ((WIDTH - right_paddle_help_text.get_width()), (HEIGHT//4)))
            win.blit(right_paddle_help_text2, ((WIDTH - right_paddle_help_text2.get_width()), (HEIGHT//2 + HEIGHT//4)))
        pg.draw.circle(win, COLOR["AQUA"], pg.mouse.get_pos(), 5)
        win.blit(POINTER_IMAGE, (pg.mouse.get_pos()))
    # Show FPS
    fps = PROMPT_FONT2.render(f"FPS: {str(int(CLOCK.get_fps()))}", True, COLOR["GOLD"])
    win.blit(fps, (0, 0))
    # Show HITS
    hits = PROMPT_FONT2.render(f"HITS: {HIT_COUNTER}", True, COLOR["GOLD"])
    win.blit(hits, ((WIDTH//2 - hits.get_width()//2), 0))
    # Display name of power hit
    if power_prompt:
        win.blit(power_name, ((WIDTH//2 - power_name.get_width()//2), (HEIGHT - 2 * power_name.get_height())))
    # Update Display
    pg.display.update()


def main(ai):
    global HIT_COUNTER
    # Main
    run = True
    # Boards
    left_board = Board(0, HEIGHT // 2 - BOARD_HEIGHT // 2 + 1, BOARD_WIDTH, BOARD_HEIGHT)
    right_board = Board(WIDTH - BOARD_WIDTH, HEIGHT // 2 - BOARD_HEIGHT // 2 - 1, BOARD_WIDTH, BOARD_HEIGHT)
    if ai:
        right_board.VEL = 20
    boards = [left_board, right_board]
    # Pong balls
    ball = Ball(WIDTH//2, HEIGHT//2, RADIUS)
    balls = [ball]
    num_balls = len(balls)
    # Scores
    score_left = 0
    score_right = 0
    # Timers and conditions
    countdown_time = powerup_time = current_time = pg.time.get_ticks()
    right_board_slow_timer = left_board_slow_timer = pg.time.get_ticks()
    power_prompt_timer = pg.time.get_ticks()
    spawn_power = False
    powerup_choice = None
    powerup = None
    hit_ball = None
    right_shield = False
    left_shield = False
    power_prompt = False
    power_name = ""
    winner = ""
    win_score = 10
    countdown = 3
    game_start = True
    # Start with any key
    pg.event.clear()
    while game_start:
        draw_assets(WIN, boards, balls, score_left, score_right, spawn_power, powerup_choice, powerup,
                    right_shield, left_shield, winner, countdown, game_start, ai, power_prompt, power_name)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit(0)
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                main_menu()
            if event.type == pg.KEYUP and event.key != pg.K_ESCAPE:
                game_start = False
                break
    # Main game loop
    while run:
        CLOCK.tick(FPS)
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                continue
            # Pause Game (Back to menu for now)
            if event.type == pg.KEYDOWN and (event.key == pg.K_ESCAPE or event.key == pg.K_p):
                main_menu()
            # Score increase left side
            if event.type == SCORE_LEFT:
                HIT_COUNTER = 0
                score_left += 1
                powerup_time = current_time
                right_shield = left_shield = spawn_power = False
                if score_left < win_score:
                    countdown_time = current_time
                    countdown = 3
                while len(balls) > 1:
                    balls.pop()
                for ball in balls:
                    ball.reset()
                for board in boards:
                    board.reset()
            # Score increase right side
            if event.type == SCORE_RIGHT:
                HIT_COUNTER = 0
                score_right += 1
                powerup_time = current_time
                right_shield = left_shield = spawn_power = False
                if score_right < win_score:
                    countdown_time = current_time
                    countdown = 3
                while len(balls) > 1:
                    balls.pop()
                for ball in balls:
                    ball.reset()
                for board in boards:
                    board.reset()
            # If ball hits powerup
            if event.type == POWER_HIT:
                powerup_time = current_time
                spawn_power = False
                num_balls = len(balls)
                apply_powers = ApplyPowers(powerup_choice[0], hit_ball, left_board,
                                           right_board, right_shield, left_shield, balls)
                apply_powers.give()
                power_prompt = True
                power_prompt_timer = current_time
                power_name = powerup_choice[0].__name__
            # If ball hits Double Ball powerup
            if event.type == DOUBLE_BALL:
                if num_balls <= 2:
                    for i in range(num_balls):
                        new_ball = Ball(balls[i].x, balls[i].y, balls[i].radius)
                        new_ball.x_vel = -1 * (balls[i].x_vel * balls[i].VEL / abs(balls[i].x_vel))
                        new_ball.y_vel = (balls[i].y_vel * balls[i].VEL / abs(balls[i].y_vel))
                        balls.append(new_ball)
            if event.type == SLOW_BOARD:
                if ball.x_vel >= 0:
                    if right_board.vel >= right_board.VEL - 4:
                        right_board.vel -= 2
                        right_board.color = COLOR["GRAY"]
                        right_board_slow_timer = current_time
                else:
                    if left_board.vel >= left_board.VEL - 4:
                        left_board.vel -= 2
                        left_board.color = COLOR["GRAY"]
                        left_board_slow_timer = current_time
            # If ball hits golden powerup from right
            if event.type == REDUCE_SCORE_RIGHT:
                if score_right:
                    score_right -= 1
            # If ball hits golden powerup from left
            if event.type == REDUCE_SCORE_LEFT:
                if score_left:
                    score_left -= 1
            # If ball hits right shield
            if event.type == RIGHT_SHIELD:
                right_shield = True ^ right_shield
            # If ball hits left shield
            if event.type == LEFT_SHIELD:
                left_shield = True ^ left_shield
        # Powerups spawn timer
        current_time = pg.time.get_ticks()
        time_elapsed = current_time - powerup_time
        if time_elapsed >= 10000:
            spawn_power = True ^ spawn_power
            powerup_time = current_time
        if not spawn_power:
            powerup, powerup_x, powerup_y, powerup_choice = powerup_randomizer()

        draw_assets(WIN, boards, balls, score_left, score_right, spawn_power, powerup_choice, powerup,
                    right_shield, left_shield, winner, countdown, game_start, ai, power_prompt, power_name)
        # Countdown
        if countdown > 0:
            if current_time - countdown_time >= 1000:
                countdown -= 1
                countdown_time = current_time
            powerup_time = current_time
            continue

        if current_time - right_board_slow_timer >= 5000:
            right_board.vel = right_board.VEL
            right_board.color = COLOR["WHITE"]
        if current_time - left_board_slow_timer >= 5000:
            left_board.vel = left_board.VEL
            left_board.color = COLOR["WHITE"]

        if current_time - power_prompt_timer >= 3000:
            power_prompt = False

        handle_board_movement(keys, left_board, right_board, balls, ai)
        # Winner prompts
        if winner:
            pg.event.clear()
            while winner:
                win_event = pg.event.wait()
                if win_event.type == pg.KEYDOWN:
                    if win_event.key == pg.K_ESCAPE:
                        run = False
                        main_menu()
                    elif win_event.key == pg.K_r:
                        main(ai)
                if win_event.type == pg.QUIT:
                    quit()
        # Score prompts
        if score_right >= win_score:
            winner = "RIGHT WINS!"
            right_shield = left_shield = spawn_power = False
            powerup_time = current_time
        elif score_left >= win_score:
            winner = "LEFT WINS!"
            right_shield = left_shield = spawn_power = False
            powerup_time = current_time

        for ball in balls:
            ball.move()

        handle_ball_collision(balls, left_board, right_board, right_shield, left_shield, keys)

        hit_ball = handle_powerup_collision(powerup, spawn_power, balls)

    pg.quit()
    quit()


def main_menu():
    on_menu = True
    while on_menu:
        menu.draw_menu(WIN, WIDTH, HEIGHT, COLOR)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                on_menu = False
                quit(0)
            selection = menu.draw_menu(WIN, WIDTH, HEIGHT, COLOR, event)
            if selection == "1":
                main(True)
            if selection == "2":
                main(False)
            if selection == "h":
                help_menu()
            if selection == "q":
                quit(0)
        pg.display.update()
    pg.display.update()


def help_menu():
    help.draw_help(WIN, WIDTH, HEIGHT, COLOR)
    on_help = True
    while on_help:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                on_help = False
                break
            stop = help.draw_help(WIN, WIDTH, HEIGHT, COLOR, event)
            if stop:
                on_help = False
                break
        pg.display.update()
    return


if __name__ == "__main__":
    main_menu()
