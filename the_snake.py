from random import choice, randint

import pygame

pygame.init()


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 5  # По умолчанию стояло 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = ...

    def draw(self):
        """
        Функция для отрисовки игрового объекта.
        Переопределяется для наследуемых классов.
        """
        pass


class Apple(GameObject):
    """Класс объекта 'Яблоко'."""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """
        Функция для определения позиции Яблока.
        Выбирает псевдорандомные координаты, находящиеся
        в пределах игрового поля, определенного константами GRID_WIDTH и GRID_HEIGHT.
        """
        random_position = ((randint(0, GRID_WIDTH) * GRID_SIZE), (randint(0, GRID_HEIGHT) * GRID_SIZE)) 
        return random_position

    def draw(self):
        """Отрисовка яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс объекта 'Змейка'."""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
#       self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.last = None

    def update_direction(self):
        """
        Метод для обновления направления движения.
        Проверяет, есть ли значение у атрибута self.next_direction.
        Если значение есть - переопределяет направление движения self.direction.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки (первый элемент в списке positions)."""
        return self.positions[0]

    def update_last_position(self):
        """Обновляет атрибут self.last, содержащий позицию последнего элемента змейки."""
        self.last = self.positions[-1]

    def move(self):
        """
        Обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions и
        удаляя последний элемент, если длина змейки не увеличилась.
        """
        head = self.get_head_position()
        if self.direction == RIGHT:
            new_head = ((head[0] + GRID_SIZE) if (head[0] + GRID_SIZE) < (GRID_WIDTH * GRID_SIZE) else 0, head[1])
        elif self.direction == LEFT:
            new_head = ((head[0] - GRID_SIZE) if (head[0] - GRID_SIZE) >= 0 else (GRID_WIDTH * GRID_SIZE), head[1])
        elif self.direction == UP:
            new_head = (head[0], (head[1] - GRID_SIZE) if (head[1] - GRID_SIZE) >= 0 else (GRID_HEIGHT * GRID_SIZE) )
        elif self.direction == DOWN:
            new_head = (head[0], head[1] + GRID_SIZE if (head[1] + GRID_SIZE) < (GRID_HEIGHT * GRID_SIZE) else 0)
        if len(self.positions) > 2 and new_head in self.positions[2:-1]:
            self.reset()
        self.positions.insert(0, new_head)
        self.positions.pop(-1)

    def reset(self):
        """
        Сбрасывает змейку в начальное состояние
        после столкновения с собой.
        """
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        screen.fill(BOARD_BACKGROUND_COLOR)

    def draw(self):
        """
        Отрисовка змейки. Отрисовывает тело змейки,
        затем отрисовывает голову змейки,
        затем - удаляет последний элемент, если self.last не равен None.
        """
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """
    Функция обработки действий пользователя.
    Обрабатывает нажатия на стрелки и передает в game_object
    сооветствующую каждой стрелке и направлению движения константу.
    """
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
    
    apple = Apple()
    snake = Snake()
    print(GRID_WIDTH * GRID_SIZE)
    print(GRID_HEIGHT * GRID_SIZE)

    apple.draw()
    print(apple.position)
    snake.draw()
    running = True

    while running:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.update_last_position()
        snake.move()
        
        if apple.position in snake.positions:
            
            snake.length += 1
            snake.positions.insert(-1, snake.positions[-1])
            counter = 0
            while True:
            # Это не помогает, проблема в другом


                counter += 1
                print(f'Количество вариантов координат яблока: {counter}')
                new_apple_position = apple.randomize_position()
                if new_apple_position not in snake.positions:
                    apple.position = new_apple_position
                    break
                else:
                    continue
            apple.draw()
                
            

        snake.draw()
        
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
