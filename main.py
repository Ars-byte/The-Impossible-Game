from turtle import Screen, Turtle
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
HALF_WIDTH = SCREEN_WIDTH // 2
HALF_HEIGHT = SCREEN_HEIGHT // 2

player = None
goal = None
enemies = []
message = None
attempts_display = None
wins_display = None

total_score = 0
game_over = False
attempts = 0
total_wins = 0

class Sprite(Turtle):
    def __init__(self, x, y, step, shape="circle", color="blue"):
        super().__init__()
        self.penup()
        self.goto(x, y)
        self.shape(shape)
        self.color(color)
        self.step = step
        self.direction = random.choice([-1, 1])

    def is_collide(self, sprite):
        return self.distance(sprite) < 30

    def mover_arriba(self):
        if self.ycor() < HALF_HEIGHT - 20:
            self.goto(self.xcor(), self.ycor() + self.step)

    def mover_abajo(self):
        if self.ycor() > -HALF_HEIGHT + 20:
            self.goto(self.xcor(), self.ycor() - self.step)

    def mover_izquierda(self):
        if self.xcor() > -HALF_WIDTH + 20:
            self.goto(self.xcor() - self.step, self.ycor())

    def mover_derecha(self):
        if self.xcor() < HALF_WIDTH - 20:
            self.goto(self.xcor() + self.step, self.ycor())

    def move_auto(self):
        new_x = self.xcor() + (self.step * self.direction)
        if abs(new_x) > HALF_WIDTH - 20:
            self.direction *= -1
            new_x = self.xcor() + (self.step * self.direction)
        self.goto(new_x, self.ycor())

def update_global_dimensions(screen_instance):
    global SCREEN_WIDTH, SCREEN_HEIGHT, HALF_WIDTH, HALF_HEIGHT
    SCREEN_WIDTH = screen_instance.window_width()
    SCREEN_HEIGHT = screen_instance.window_height()
    HALF_WIDTH = SCREEN_WIDTH // 2
    HALF_HEIGHT = SCREEN_HEIGHT // 2

def setup_game():
    global player, goal, enemies, total_score, game_over, message, attempts, attempts_display, total_wins, wins_display

    if message is not None:
        message.clear()
        message.hideturtle()

    player_start_y = -HALF_HEIGHT + 50
    player_step = 25
    player = Sprite(0, player_start_y, player_step, "turtle", "green")

    goal = Sprite(0, HALF_HEIGHT - 50, 0, "triangle", "gold")

    for enemy_sprite in enemies:
        enemy_sprite.hideturtle()
    enemies.clear()

    base_enemies = [
        Sprite(-HALF_WIDTH + 100, 0, random.randint(7, 10), "square", "red"),
        Sprite( HALF_WIDTH - 100, HALF_HEIGHT * 0.4, random.randint(8, 11), "square", "red"),
        Sprite(0, -HALF_HEIGHT * 0.4, random.randint(7,10), "square", "red"),
        Sprite( HALF_WIDTH - 200, -HALF_HEIGHT + 100, random.randint(6,9), "square", "red"),
        Sprite(-HALF_WIDTH + 200,  HALF_HEIGHT - 150, random.randint(7,10), "square", "red"),
        Sprite( HALF_WIDTH * 0.36, -HALF_HEIGHT * 0.65, random.randint(8,11), "square", "red"),
        Sprite(-HALF_WIDTH * 0.36,  HALF_HEIGHT - 88 , random.randint(6,9), "square", "red"),
        Sprite( HALF_WIDTH * 0.22,  HALF_HEIGHT * 0.39, random.randint(9,12), "square", "red"),
        Sprite(-HALF_WIDTH * 0.22, -HALF_HEIGHT * 0.52, random.randint(7,10), "square", "red"),
        Sprite( HALF_WIDTH * 0.44,  HALF_HEIGHT * 0.26, random.randint(8,11), "square", "red"),
        Sprite(0, HALF_HEIGHT * 0.6, random.randint(10, 14), "square", "maroon"),
        Sprite(0, -HALF_HEIGHT * 0.6, random.randint(10, 14), "square", "maroon"),
        Sprite(HALF_WIDTH * 0.75, 0, random.randint(9, 13), "square", "firebrick"),
        Sprite(-HALF_WIDTH * 0.75, 0, random.randint(9, 13), "square", "firebrick"),
        Sprite(HALF_WIDTH * 0.25, HALF_HEIGHT * 0.8, random.randint(6,9), "square", "darkred"),
        Sprite(-HALF_WIDTH * 0.25, -HALF_HEIGHT * 0.8, random.randint(6,9), "square", "darkred"),
        Sprite(HALF_WIDTH - 70, HALF_HEIGHT - 250, random.randint(8,11), "square", "red"),
        Sprite(-HALF_WIDTH + 70, -HALF_HEIGHT + 250, random.randint(8,11), "square", "red"),
        Sprite(HALF_WIDTH * 0.5, HALF_HEIGHT * 0.1, random.randint(11,15), "square", "purple"),
        Sprite(-HALF_WIDTH * 0.5, -HALF_HEIGHT * 0.1, random.randint(11,15), "square", "purple"),
    ]
    enemies.extend(base_enemies)

    total_score = 0
    game_over = False

    if attempts_display is not None:
        attempts_display.clear()
    attempts += 1
    if attempts_display is None:
        attempts_display = Turtle()
        attempts_display.hideturtle()
        attempts_display.penup()
        attempts_display.color("white")
    attempts_display.goto(-HALF_WIDTH + 30, HALF_HEIGHT - 40)
    attempts_display.write(f"Attempts: {attempts}", align="left", font=("Arial", 14, "bold"))

    if wins_display is not None:
        wins_display.clear()
    if wins_display is None:
        wins_display = Turtle()
        wins_display.hideturtle()
        wins_display.penup()
        wins_display.color("yellow")
    wins_display.goto(HALF_WIDTH - 30, HALF_HEIGHT - 40)
    wins_display.write(f"WINS: {total_wins}", align="right", font=("Arial", 14, "bold"))


def show_message(text, color_val):
    global message
    if message is None:
        message = Turtle()
        message.hideturtle()
        message.penup()
    else:
        message.clear()

    message.color(color_val)
    message.goto(0, 0)
    message.write(text, align="center", font=("Arial", 22, "bold"))

def reset_game():
    global player, goal, enemies
    if player: player.hideturtle()
    if goal: goal.hideturtle()
    for enemy_sprite in enemies:
        enemy_sprite.hideturtle()

    setup_game()
    game_loop()

def game_loop():
    global total_score, game_over, scr, player, goal, enemies, total_wins, wins_display

    if not player:
        return

    while total_score < 3 and not game_over:
        for enemy in enemies:
            enemy.move_auto()
            if player.is_collide(enemy):
                game_over = True
                show_message("¡LOOOOOOSER! (Q = RESET)", "red")
                break

        if game_over:
            scr.update()
            continue

        if player.is_collide(goal):
            player.goto(0, -HALF_HEIGHT + 50)
            total_score += 1

            new_goal_x = random.randint(-HALF_WIDTH + 70, HALF_WIDTH - 70)
            new_goal_y = random.randint(HALF_HEIGHT // 3, HALF_HEIGHT - 70)
            goal.goto(new_goal_x, new_goal_y)

            if total_score >= 3:
                total_wins += 1
                if wins_display:
                    wins_display.clear()
                    wins_display.write(f"Victorias: {total_wins}", align="right", font=("Arial", 14, "bold"))
                break

        scr.update()

    if not game_over and total_score >= 3:
        show_message(f"¡ROUND WIN! ({total_wins} WINS) (Q = RESET)", "gold")


scr = Screen()
scr.setup(width=800, height=600)
update_global_dimensions(scr)

scr.bgcolor("black")
scr.title("The IMPOSSIBLE Game - EXTREME HD Edition")
scr.listen()
scr.tracer(0)

attempts = 0
total_wins = 0

def safe_mover_arriba():
    if player and not game_over: player.mover_arriba()
def safe_mover_abajo():
    if player and not game_over: player.mover_abajo()
def safe_mover_izquierda():
    if player and not game_over: player.mover_izquierda()
def safe_mover_derecha():
    if player and not game_over: player.mover_derecha()

scr.onkey(safe_mover_arriba, "Up")
scr.onkey(safe_mover_arriba, "w")
scr.onkey(safe_mover_arriba, "W")
scr.onkey(safe_mover_abajo, "Down")
scr.onkey(safe_mover_abajo, "s")
scr.onkey(safe_mover_abajo, "S")
scr.onkey(safe_mover_izquierda, "Left")
scr.onkey(safe_mover_izquierda, "a")
scr.onkey(safe_mover_izquierda, "A")
scr.onkey(safe_mover_derecha, "Right")
scr.onkey(safe_mover_derecha, "d")
scr.onkey(safe_mover_derecha, "D")
scr.onkey(reset_game, "q")
scr.onkey(reset_game, "Q")

setup_game()
game_loop()

scr.mainloop()



