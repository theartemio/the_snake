from random import choice, randint

from typing import Optional

import pygame as pg

pg.init()


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Константы типов:
POINTER = tuple[int, int]
POSITION = tuple[int, int]
COLOR = tuple[int, int, int]

# Направления движения:
UP: POINTER = (0, -1)
DOWN: POINTER = (0, 1)
LEFT: POINTER = (-1, 0)
RIGHT: POINTER = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR: COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR: COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR: COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR: COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED: int = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Настройка времени:
clock = pg.time.Clock()

# Тут опишите все классы игры.


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self) -> None:
        self.position: POSITION = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color: Optional[COLOR] = APPLE_COLOR

    def draw(self) -> None:
        """
        Функция для отрисовки игрового объекта.
        Переопределяется для наследуемых классов.
        """
        raise NotImplementedError()

    def draw_cell(self,
                  position: POSITION = None,
                  color: COLOR = None
                  ) -> None:
        """
        Метод для отрисовки одной ячейки.
        Служит для вызова при отрисовке объектов.
        """
        rect: pg.Rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс объекта 'Яблоко'."""

    def __init__(self) -> None:
        super().__init__()
        self.body_color: COLOR = APPLE_COLOR
        self.occupied_positions: list = []
        self.position: POSITION = self.randomize_position()
        self.draw()

    def randomize_position(self) -> POSITION:
        """
        Функция для определения позиции Яблока.
        Выбирает псевдорандомные координаты, находящиеся
        в пределах игрового поля, определенного константами
        GRID_WIDTH и GRID_HEIGHT.
        """
        while True:
            rand_position: POSITION = (
                (randint(0, GRID_WIDTH - 1) * GRID_SIZE),
                (randint(0, GRID_HEIGHT - 1) * GRID_SIZE),
            )
            if rand_position not in self.occupied_positions:
                break
        return rand_position

    def draw(self):
        """Отрисовка яблока"""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Класс объекта 'Змейка'."""

    def __init__(self) -> None:
        super().__init__()
        self.body_color: COLOR = SNAKE_COLOR
        self.direction: POINTER = RIGHT
        self.next_direction: Optional[POINTER] = None
        self.length: int = 1
        self.position: POSITION = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.positions: list = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.reseted: bool = False
        self.last: Optional[POSITION] = None

    def update_direction(self) -> None:
        """
        Метод для обновления направления движения.
        Проверяет, есть ли значение у атрибута self.next_direction.
        Если значение есть - переопределяет направление
        движения self.direction.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self) -> POSITION:
        """
        Возвращает позицию головы змейки
        (первый элемент в списке positions).
        """
        return self.positions[0]

    def update_last_position(self) -> None:
        """
        Обновляет атрибут self.last, содержащий позицию
        последнего элемента змейки.
        """
        self.last = self.positions[-1]

    def move(self) -> None:
        """
        Обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions и
        удаляя последний элемент, если длина змейки не увеличилась.
        """
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_head: POSITION = (
            (head_x + (dir_x * GRID_SIZE)) % SCREEN_WIDTH,
            (head_y + (dir_y * GRID_SIZE)) % SCREEN_HEIGHT,
        )
        if len(self.positions) > 2 and new_head in self.positions[2:-1]:
            self.reset()
        else:
            self.positions.insert(0, (new_head))
            self.positions.pop(-1)

    def reset(self) -> None:
        """
        Сбрасывает змейку в начальное состояние
        после столкновения с собой.
        """
        self.direction = choice([UP, RIGHT, LEFT, DOWN])
        self.next_direction = None
        self.length = 1
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.reseted = True

    def draw(self) -> None:
        """
        Отрисовка змейки. Отрисовывает тело змейки,
        затем отрисовывает голову змейки,
        затем - удаляет последний элемент, если self.last не равен None.
        """
        for position in self.positions[:-1]:
            self.draw_cell(position, self.body_color)
        self.draw_cell(self.get_head_position(), self.body_color)
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """
    Функция обработки действий пользователя.
    Обрабатывает нажатия на стрелки и передает в game_object
    сооветствующую каждой стрелке и направлению движения константу.
    """
    keys: dict = {
        (pg.K_UP): (UP, DOWN),
        (pg.K_DOWN): (DOWN, UP),
        (pg.K_LEFT): (LEFT, RIGHT),
        (pg.K_RIGHT): (RIGHT, LEFT),
    }
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN and keys.get(event.key):
            if game_object.direction != keys.get(event.key)[1]:
                game_object.next_direction = keys.get(event.key)[0]
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.quit()
            raise SystemExit


def main():
    """Основная функция игры"""
    apple: Apple = Apple()
    snake: Snake = Snake()
    running: bool = True
    max_len: int = 1
    while running:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.update_last_position()
        snake.move()
        apple.occupied_positions: list = snake.positions
        if snake.reseted:
            apple.position: POSITION = apple.randomize_position()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.draw()
            snake.reseted: bool = False
        if apple.position == snake.get_head_position():
            snake.length += 1
            max_len: int = snake.length if snake.length > max_len else max_len
            snake.positions.insert(-1, snake.positions[-1])
            apple.position = apple.randomize_position()
            apple.draw()
        snake.draw()
        pg.display.update()
        pg.display.set_caption(f"Змейка :: "
                               f"Рекорд: {max_len} :: Выход: Esc"
                               )
    pg.quit()


if __name__ == "__main__":
    main()
