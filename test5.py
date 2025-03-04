import numpy as np
import moderngl
import pygame
from pygame.locals import *
from PIL import Image
from random import randint,choice
from time import time
from perlin_noise import PerlinNoise

# Константы
WIN_SIZE = (800, 600)  # Размер окна
WORLD_WIDTH = 20  # Ширина мира
WORLD_HEIGHT = 20  # Высота мира
ATLAS_COLS = 32  # Количество колонок в атласе текстур
ATLAS_ROWS = 3  # Количество строк в атласе текстур
TILE_SIZE = 2.0 / max(WORLD_WIDTH, WORLD_HEIGHT)  # Размер тайла

# Генерация случайных тайлов
tiles = np.array([
    0 for _ in range(WORLD_WIDTH * WORLD_HEIGHT)
], dtype='i4')

# Генерация случайных высот тайлов
tilesh = np.array([
    randint(0, 4) for _ in range(WORLD_WIDTH * WORLD_HEIGHT)
], dtype='i4')

# Параметры для перлинского шума
noise = PerlinNoise(octaves=4)  # Создание объекта перлинского шума

# Генерация перлинского шума и добавление его к массивам
for i in range(WORLD_WIDTH):
    for j in range(WORLD_HEIGHT):
        # Генерация значения шума
        noise_value = noise([i / 10, j / 10])
        noise_value2 = noise([(i-68761325) / 8, (j+2145356) / 8])

        # Нормализация значения шума и добавление к тайлам
        # Приведение к диапазону [0, 4]
        tiles[i * WORLD_WIDTH + j] = int((noise_value2 + 0.5) * 3)  # Приведение к диапазону [0, 4]
        tilesh[i * WORLD_WIDTH + j] = int((noise_value + 0.5) * 7)  # Приведение к диапазону [0, 4]


class WindowGame:
    def __init__(self):
        pygame.init()  # Инициализация Pygame
        infoObject = pygame.display.Info()
        WIN_SIZE=(infoObject.current_w, infoObject.current_h)
        pygame.display.set_mode(WIN_SIZE, pygame.DOUBLEBUF | pygame.OPENGL,vsync=1)  # Создание окна с поддержкой OpenGL
        self.ctx = moderngl.create_context()  # Создание контекста ModernGL
        self.ctx.viewport = (0, 0, *WIN_SIZE)  # Установка области просмотра

        # Загрузка текстуры
        img = Image.open("atlas.png").transpose(Image.FLIP_TOP_BOTTOM).convert("RGBA")  # Открытие и преобразование текстуры
        self.texture = self.ctx.texture(img.size, 4, img.tobytes())  # Создание текстуры в контексте
        self.texture.build_mipmaps()  # Построение мип-карт для текстуры
        
        with open("shaders/world5_vert.glsl",'r',encoding="utf-8") as f:
            vert = f.read()
        with open("shaders/world5_frag.glsl",'r',encoding="utf-8") as f:
            frag = f.read()

        # Шейдеры с исправлениями
        self.program = self.ctx.program(
            vertex_shader=vert,
            fragment_shader=frag
        )

        # Буфер вершин (позиции квадрата)
        self.vbo = self.ctx.buffer(np.array([
            -1.0, -1.0,  # Левый нижний угол
             1.0, -1.0,  # Правый нижний угол
             1.0,  1.0,  # Правый верхний угол
            -1.0,  1.0,  # Левый верхний угол
        ], dtype='f4'))

        # Индексный буфер
        self.ibo = self.ctx.buffer(np.array([0, 1, 2, 2, 3, 0], dtype='i4'))  # Определение порядка отрисовки вершин

        # VAO (Vertex Array Object)
        self.vao = self.ctx.vertex_array(
            self.program,
            [(self.vbo, '2f', 'in_pos')],  # Привязка атрибута вершин
            index_buffer=self.ibo  # Привязка индексного буфера
        )

        # Передача данных в шейдеры
        self.program['tile_indices'].write(tiles)  # Запись индексов тайлов
        self.program['tile_heights'].write(tilesh)  # Запись высот тайлов
        self.program['res'] = WIN_SIZE  # Установка разрешения

    def draw(self):
        self.ctx.clear(0.1, 0.1, 0.1)  # Очистка экрана
        self.texture.use(location=0)  # Использование текстуры
        self.vao.render(moderngl.TRIANGLES)  # Отрисовка треугольников

    def run(self):
        start_time = time()  # Запись времени начала
        while True:  # Основной игровой цикл
            for event in pygame.event.get():  # Обработка событий
                if event.type == QUIT:  # Проверка на выход
                    pygame.quit()  # Завершение Pygame
                    return
            self.draw()  # Вызов функции отрисовки
            pygame.display.flip()  # Обновление экрана
            self.program['elapsed'] = time()-start_time  # (Закомментировано) Обновление времени

if __name__ == '__main__':
    game = WindowGame()  # Создание экземпляра игры
    game.run()  # Запуск игры