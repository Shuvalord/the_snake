from random import choice, randint

import pygame as pg


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


BOARD_BACKGROUND_COLOR = (0, 0, 0)


BORDER_COLOR = (0, 0, 0)  # Убрал рамку у клеток, лучше не возвращать
# Не могу найти ошибку, уже все потыкал, но если рамка есть то гг


APPLE_COLOR = (255, 0, 0)


SNAKE_COLOR = (0, 255, 0)


SPEED = 20

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pg.display.set_caption('Змейка')

clock = pg.time.Clock()


class GameObject():
    """Родительный класс для всех объектов змейки."""

    def __init__(self, position=CENTER_POSITION, body_color=None):
        """Инициализирует игровой объект с позицией по умолчанию и цветом."""
        self.position = position
        self.body_color = body_color

    def draw_cell(self, position=None, color=None):
        """Отрисовка одной ячейки."""
        position = position or self.position
        color = color or self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """
        Мы не забыли этот метод реализовать,

        а предполагаем его реализацию только в дочерних классах
        """
        raise NotImplementedError('будет реализовано в дочерних классах')


class Apple(GameObject):
    """
    Класс, представляющий яблоко в игре.

    Управляет позицией яблока и гарантирует, что оно не появится внутри змейки.
    """

    def __init__(self, occupied_positions=[]):
        """Инициализирует объект яблока с рандомной позицией."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """
        Рандомизирует позицию яблока.

        Гарантирует, что яблоко не появится внутри змейки.
        snake_positions Список кортежей, представляющих позиции тела змейки.
        """
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Отрисовка яблока."""
        self.draw_cell()


class Snake(GameObject):
    """
    Класс, представляющий змейку в игре.

    Управляет движением, ростом и обнаружением столкновений змейки.
    """

    def __init__(self):
        """Инициализирует змейкy с длиной и направлением по умолчанию."""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()
        self.direction = RIGHT

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Перемещает змейку в текущем направлении.

        Управляет ростом, движением змейки,обработкой выхода за границы экрана.
        """
        head_x, head_y = self.get_head_position()
        new_head = (
            (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)
        self.last = self.positions.pop()

    def draw(self):
        """Рисует змейку на экране."""
        self.draw_cell(self.positions[0])
        if self.last:
            self.draw_cell(self.last, color=BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """
        Сбрасывает состояние змейки в исходное положение.

        Сбрасывает длину, позицию и направление.
        """
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([LEFT, RIGHT, UP, DOWN])
        self.next_direction = None
        self.last = None

    def grow(self):
        """Увеличивает длину змейки после поедания яблока."""
        if self.last:
            self.positions.append(self.last)
            self.last = None


def handle_keys(game_object):
    """
    Обрабатывает пользовательский ввод для управления змейкой.

    Настраивает направление змейки на основе нажатий клавиш со стрелками.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главная функция для запуска игрового цикла."""
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position(snake.positions)

        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
