import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400  # Screen dimensions
GRID_SIZE = 20  # Size of each grid cell
SPEED = 1  # Initial speed of the game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
SPEED_INCREMENT = 1  # Speed increment per score increase

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH / 2), (HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN

    def get_head_position(self):
        """Return the position of the snake's head."""
        return self.positions[0]

    def turn(self, point):
        """Change the direction of the snake."""
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        """Move the snake."""
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % WIDTH), (cur[1] + (y * GRID_SIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()  # Reset snake if it collides with itself
            return True
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            if len(self.positions) == 1:  # If snake length is 1, reset score to 0
                return True
        return False

    def reset(self):
        """Reset the snake to its initial position."""
        self.length = 1
        self.positions = [((WIDTH / 2), (HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):
        """Draw the snake on the screen."""
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, BLACK, r, 1)

    def handle_keys(self):
        """Handle user input to change the direction of the snake."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

# Food class
class Food:
    def __init__(self):
        """Initialize the food at a random position."""
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        """Set the position of the food to a random location."""
        self.position = (random.randint(0, (WIDTH / GRID_SIZE) - 1) * GRID_SIZE,
                         random.randint(0, (HEIGHT / GRID_SIZE) - 1) * GRID_SIZE)

    def draw(self, surface):
        """Draw the food on the screen."""
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, BLACK, r, 1)

# Menu class
class Menu:
    def __init__(self):
        """Initialize the menu."""
        self.font = pygame.font.Font(None, 50)
        self.best_score_font = pygame.font.Font(None, 36)  # Font for best score
        self.snake_font = pygame.font.Font(None, 72)  # Font for "SNAKE" text
        self.options = ['Start', 'Reset Best Score', 'Exit']
        self.selected_option = 0
        self.best_score = load_best_score()  # Load best score from a file

    def draw(self, surface):
        """Draw the menu on the screen."""
        # Render "SNAKE" text
        snake_text = self.snake_font.render("SNAKE", True, GREEN)
        snake_rect = snake_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        surface.blit(snake_text, snake_rect)

        # Render menu options
        for i, option in enumerate(self.options):
            text = self.font.render(option, True, WHITE if i == self.selected_option else GRAY)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))
            surface.blit(text, text_rect)

        # Render best score with the new font
        best_score_text = self.best_score_font.render("Best Score: " + str(self.best_score), True, WHITE)
        surface.blit(best_score_text, (10, 10))

    def handle_keys(self):
        """Handle user input in the menu."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.selected_option == 0:  # Start
                        return "start"
                    elif self.selected_option == 1:  # Reset Best Score
                        reset_best_score()  # Reset best score
                        self.best_score = 0  # Update best score attribute
                        self.draw(pygame.display.get_surface())  # Redraw menu
                    elif self.selected_option == 2:  # Exit
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_ESCAPE:  # Allow going back to menu with 'Esc' key
                        return "menu"  # Return "menu" to indicate going back to the menu

def main():
    global SPEED  # Declare SPEED as global
    # Initialize screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    # Initialize menu
    menu = Menu()

    while True:
        screen.fill(BLACK)
        option = menu.handle_keys()
        if option == "start":
            break
        menu.draw(screen)
        pygame.display.update()
        clock.tick(SPEED)

    # Start game loop
    snake = Snake()
    food = Food()
    score = 0
    best_score = load_best_score()  # Load best score from a file

    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Return to menu if 'esc' key is pressed
                    main()
                elif event.key == pygame.K_UP:
                    snake.turn(UP)
                elif event.key == pygame.K_DOWN:
                    snake.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.turn(RIGHT)
        collision = snake.move()  # Check if there was a collision
        if collision:
            score = 0  # Reset score to zero
            SPEED = 1

        if snake.get_head_position() == food.position:
            snake.length += 1
            food.randomize_position()
            score += 1
            if score > best_score:  # Update best score if current score is higher
                best_score = score
                save_best_score(best_score)  # Save best score to a file
            # Increase speed based on score
            SPEED += SPEED_INCREMENT

        snake.draw(screen)
        food.draw(screen)
            
        # Display scores
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(score), True, WHITE)
        best_score_text = font.render("Best Score: " + str(best_score), True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(best_score_text, (10, 40))

        pygame.display.update()
        clock.tick(SPEED)

def load_best_score():
    """Load the best score from a file."""
    try:
        with open("best_score.txt", "r") as file:
            best_score = int(file.read())
    except FileNotFoundError:
        best_score = 0
    return best_score

def save_best_score(best_score):
    """Save the best score to a file."""
    with open("best_score.txt", "w") as file:
        file.write(str(best_score))

def reset_best_score():
    """Reset the best score to 0."""
    save_best_score(0)

if __name__ == "__main__":
    main()
