from random import choice, randint

import pygame


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


BOARD_BACKGROUND_COLOR = (0, 0, 0)


BORDER_COLOR = (93, 216, 228)


APPLE_COLOR = (255, 0, 0)


SNAKE_COLOR = (0, 255, 0)


SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameObject():
    """
    Родительный класс для всех объектов.
    Имеет 2 метода. Добавил сюда Draw чтоб сделать типо наследие.
    """

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):

    def __init__(self):
        self.body_color = APPLE_COLOR
        self.randomize_position([])

    def randomize_position(self, snake_positions):
        """
        Создает позицию яблока, -1 чтоб не создать за границей яблоко
        проверяет не создалось ли яблоко в змее, если да, то пересоздает.
        """
        while True:
            position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if position not in snake_positions:
                self.position = position
                break


class Snake(GameObject):

    def __init__(self):
        super().__init__()
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None
        self.positions = [self.position]

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Создает новую голову и удаляет хвост, если длина осталась прежней,
        так же '%' позволяет телепортировать змею по границам поля.
        """
        head_x, head_y = self.get_head_position()
        new_head = (
            (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        for posistion in self.positions:
            rect = pygame.Rect(posistion, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        """
        Сбрасывает состояние змейки в 0 положение.
        Выбирает новое направление.
        """
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([LEFT, RIGHT, UP, DOWN])


def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        apple.draw()
        snake.draw()

        pygame.display.update()

        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if any(_ == snake.positions[0] for _ in snake.positions[1:-1]):
            snake.reset()
            apple.randomize_position(snake.positions)


if __name__ == '__main__':
    main()
