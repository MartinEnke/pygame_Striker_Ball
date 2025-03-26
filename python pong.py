import pygame
import random

pygame.init()

# Font that is used to render the text
font20 = pygame.font.Font('freesansbold.ttf', 20)

# RGB values of standard colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Basic parameters of the screen
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()
FPS = 30


# Striker class


class Striker:
    # Take the initial position, dimensions, speed and color of the object
    def __init__(self, pos_x, pos_y, width, height, speed, color):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        # Rect that is used to control the position and collision of the object
        self.player_rect = pygame.Rect(pos_x, pos_y, width, height)
        # Object that is blit on the screen
        self.player = pygame.draw.rect(screen, self.color, self.player_rect)

    # Used to display the object on the screen
    def display(self):
        self.player = pygame.draw.rect(screen, self.color, self.player_rect)

    def update(self, y_fac):
        self.pos_y = self.pos_y + self.speed * y_fac

        # Restricting the striker to be below the top surface of the screen
        if self.pos_y <= 0:
            self.pos_y = 0
        # Restricting the striker to be above the bottom surface of the screen
        elif self.pos_y + self.height >= HEIGHT:
            self.pos_y = HEIGHT - self.height

        # Updating the rect with the new values
        self.player_rect = (self.pos_x, self.pos_y, self.width, self.height)

    def display_score(self, text, score, x, y, color):
        text = font20.render(text + str(score), True, color)
        text_rect = text.get_rect()
        text_rect.center = (x, y)

        screen.blit(text, text_rect)

    def get_rect(self):
        return self.player_rect


# Ball class


# Function to generate a random color
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

class Ball:
    def __init__(self, pos_x, pos_y, radius, speed, color):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.speed = speed*1.9
        self.color = color
        self.x_fac = 1
        self.y_fac = -1
        self.ball = pygame.draw.circle(
            screen, self.color, (self.pos_x, self.pos_y), self.radius)
        self.first_time = 1

    def display(self):
        self.ball = pygame.draw.circle(
            screen, self.color, (self.pos_x, self.pos_y), self.radius)

    def update(self):
        self.pos_x += self.speed * self.x_fac
        self.pos_y += self.speed * self.y_fac

        # If the ball hits the top or bottom surfaces,
        # then the sign of yFac is changed and
        # it results in a reflection
        if self.pos_y <= 0 or self.pos_y >= HEIGHT:
            self.y_fac *= -1

        if self.pos_x <= 0 and self.first_time:
            self.first_time = 0
            return 1
        elif self.pos_x >= WIDTH and self.first_time:
            self.first_time = 0
            return -1
        else:
            return 0

    def reset(self, last_point: int):
        """Resets the ball to the center and sets a new direction."""
        self.pos_x = WIDTH // 2
        self.pos_y = HEIGHT // 2

        # Der Ball startet in die entgegengesetzte Richtung des letzten Treffers
        self.x_fac = last_point  # -1 = nach links, 1 = nach rechts

        # Zufällige vertikale Richtung, damit das Spiel abwechslungsreich bleibt
        self.y_fac = random.choice([-1, 1])
        self.color = random_color()  # Change color randomly

        self.first_time = 1  # Ermöglicht neue Tore


    # Used to reflect the ball along the X-axis
    def hit(self):
        self.x_fac *= -1

    def get_rect(self):
        return self.ball


# Game Manager


def main():
    running = True

    # Defining the objects
    green_player = Striker(20, 0, 10, 100, 10, GREEN)
    red_player = Striker(WIDTH - 30, 0, 10, 100, 10, RED)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 7, 7, WHITE)

    players = [green_player, red_player]

    # Initial parameters of the players
    green_score, red_score = 0, 0
    green_y_fac, red_y_fac = 0, 0

    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    red_y_fac = -1
                if event.key == pygame.K_DOWN:
                    red_y_fac = 1
                if event.key == pygame.K_w:
                    green_y_fac = -1
                if event.key == pygame.K_s:
                    green_y_fac = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    red_y_fac = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    green_y_fac = 0

        # Collision detection
        for player in players:
            if pygame.Rect.colliderect(ball.get_rect(), player.get_rect()):
                ball.hit()

        # Updating the objects
        green_player.update(green_y_fac)
        red_player.update(red_y_fac)
        point = ball.update()

        # -1 -> Player_1 has scored
        # +1 -> Player_2 has scored
        #  0 -> None of them scored
        if point == -1:
            green_score += 1
        elif point == 1:
            red_score += 1

        # Someone has scored
        # a point and the ball is out of bounds.
        # So, we reset it's position
        if point:
            ball.reset(point)

        # Displaying the objects on the screen
        green_player.display()
        red_player.display()
        ball.display()

        # Displaying the scores of the players
        green_player.display_score("Green : ",
                           green_score, 100, 20, WHITE)
        red_player.display_score("Red : ",
                           red_score, WIDTH - 100, 20, WHITE)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    pygame.quit()