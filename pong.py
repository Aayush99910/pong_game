# Pong game

import turtle # importing turtle
import pygame # importing pygame

# Initialize pygame
pygame.init()

# player class
class Player():
    def __init__(self, name, score):
        self.name = name
        self.score = score
    
    def update_score(self):
        self.score = self.score + 1

# paddle class
class Paddle():
    def __init__(self, x, y, paddle_color):
        self.paddle = turtle.Turtle()
        self.paddle.speed(0)
        self.paddle.shape("square")
        self.paddle.color(paddle_color)
        self.paddle.shapesize(stretch_wid=5, stretch_len=1)
        self.paddle.penup()
        self.paddle.goto(x, y)

    def get_x_coordinate(self):
        return self.paddle.xcor()
    
    def get_y_coordinate(self):
        return self.paddle.ycor()

    def move_up(self):
        self.y = self.paddle.ycor()
        self.y += 20
        self.paddle.sety(self.y)

    def move_down(self):
        self.y = self.paddle.ycor()
        self.y -= 20
        self.paddle.sety(self.y)

# ball class
class Ball():
    bounce_sound = pygame.mixer.Sound("bounce.wav")
    clapping_sound = pygame.mixer.Sound("clapping.wav")
    changes_in_x_of_ball = 0.2
    changes_in_y_of_ball = -0.2

    def __init__(self):
        self.ball = turtle.Turtle()
        self.ball.speed(0)
        self.ball.shape("circle")
        self.ball.color("white")
        self.ball.penup()
        self.ball.goto(0, 0)

    def get_x_coordinate(self):
        return self.ball.xcor()
    
    def get_y_coordinate(self):
        return self.ball.ycor()
    
    def ball_movement(self):
        self.ball.setx(self.ball.xcor() + self.changes_in_x_of_ball)
        self.ball.sety(self.ball.ycor() + self.changes_in_y_of_ball)

    def ball_movement_reset(self):
        self.ball.goto(0, 0)
        self.changes_in_x_of_ball = self.changes_in_x_of_ball * -1
        self.clapping_sound.play()
    
    def ball_movement_reverse_x(self, position):
        self.ball.setx(position)
        self.changes_in_x_of_ball = self.changes_in_x_of_ball * -1
        self.bounce_sound.play()

    def ball_movement_reverse_y(self, position):
        self.ball.sety(position)
        self.changes_in_y_of_ball = self.changes_in_y_of_ball * -1
        self.bounce_sound.play()

# scoreboard
class ScoreBoard():
    def __init__(self, player1, player2):
        self.score_turtle = turtle.Turtle()
        self.player1 = player1
        self.player2 = player2 
        self.score_turtle.speed(0)
        self.score_turtle.color("white")
        self.score_turtle.penup()
        self.score_turtle.hideturtle()
        self.score_turtle.goto(0, 260)
    
    def show_score(self):
        self.score_turtle.write(f"{self.player1.name}: {self.player1.score} {self.player2.name}: {self.player2.score}", align="center", font=("Courier", 24, "normal")) 
    
    def show_updated_score(self):
        self.score_turtle.clear()
        self.score_turtle.write(f"{self.player1.name}: {self.player1.score} {self.player2.name}: {self.player2.score}", align="center", font=("Courier", 24, "normal")) 


# Window
window = turtle.Screen()
window.title("Pong game")
window.bgcolor("black")
window.setup(width=800, height=600)
window.tracer(0)

# Paddle A
paddle_a = Paddle(-350, 0, "red")

# Paddle B
paddle_b = Paddle(350, 0, "blue")

# Ball
game_ball = Ball()

# Player 1
user_input_1 = str(input("Enter player 1 name: "))
player_1 = Player(f"{user_input_1}", 0)

# Player 2
user_input_2 = str(input("Enter player 2 name: "))
player_2 = Player(f"{user_input_2}", 0)

# scoreboard
my_scoreboard = ScoreBoard(player_1, player_2)

# key bindings
window.listen()
window.onkeypress(paddle_a.move_up, "w")
window.onkeypress(paddle_b.move_up, "Up")
window.onkeypress(paddle_a.move_down, "s")
window.onkeypress(paddle_b.move_down, "Down")

my_scoreboard.show_score() # showing scoreboard

while True:
    window.update()
    game_ball.ball_movement()

    # y border top checking
    if (game_ball.get_y_coordinate() > 290):
        game_ball.ball_movement_reverse_y(290)
    
    # y border bottom checking 
    if (game_ball.get_y_coordinate() < -290):
        game_ball.ball_movement_reverse_y(-290)

    # x border checking 
    if (game_ball.get_x_coordinate() > 390): 
        game_ball.ball_movement_reset()
        player_1.update_score()
        my_scoreboard.show_updated_score()
    
    if (game_ball.get_x_coordinate() < -390):
        game_ball.ball_movement_reset()
        player_2.update_score()
        my_scoreboard.show_updated_score()

    # paddle and ball collision
    if (game_ball.get_x_coordinate() > 340 and game_ball.get_x_coordinate() < 350) and ((game_ball.get_y_coordinate() < paddle_b.get_y_coordinate() + 40) and (game_ball.get_y_coordinate() > paddle_b.get_y_coordinate() - 40)):
        game_ball.ball_movement_reverse_x(340)
    
    if (game_ball.get_x_coordinate() < -340 and game_ball.get_x_coordinate() > -350) and ((game_ball.get_y_coordinate() < paddle_a.get_y_coordinate() + 40) and (game_ball.get_y_coordinate() > paddle_a.get_y_coordinate() - 40)):
        game_ball.ball_movement_reverse_x(-340)
