import numpy as np
import moderngl
import pygame
from pygame.locals import *
from PIL import Image
from random import randint

# Константы
WIN_SIZE = (800, 600)
WORLD_WIDTH = 20
WORLD_HEIGHT = 20
ATLAS_COLS = 32
ATLAS_ROWS = 2
TILE_SIZE = 2.0 / max(WORLD_WIDTH, WORLD_HEIGHT)

# Генерация данных тайлов
tiles = np.array([
    randint(0, 2) for _ in range(WORLD_WIDTH * WORLD_HEIGHT)
], dtype='i4')

class WindowGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode(WIN_SIZE, pygame.DOUBLEBUF | pygame.OPENGL)
        self.ctx = moderngl.create_context()
        self.ctx.viewport = (0, 0, *WIN_SIZE)

        # Загрузка текстуры
        img = Image.open("atlas.png").transpose(Image.FLIP_TOP_BOTTOM).convert("RGBA")
        self.texture = self.ctx.texture(img.size, 4, img.tobytes())
        self.texture.build_mipmaps()

        # Шейдеры с исправлениями
        self.program = self.ctx.program(
            vertex_shader='''
                #version 330
                in vec2 in_pos;  // Добавлено объявление атрибута
                uniform int tile_indices[400];
                out vec2 uv;

                void main() {
                    int tileIndex = tile_indices[gl_VertexID / 4];
                    int tex_x = tileIndex % 32;
                    int tex_y = tileIndex / 32;

                    float u0 = float(tex_x) / 32.0;
                    float v0 = 1.0 - (float(tex_y) + 1.0) / 2.0;
                    float u1 = float(tex_x + 1) / 32.0;
                    float v1 = 1.0 - float(tex_y) / 2.0;

                    // Используем переданные позиции вершин
                    gl_Position = vec4(in_pos, 0.0, 1.0);

                    if (gl_VertexID % 4 == 0) uv = vec2(u0, v0);
                    else if (gl_VertexID % 4 == 1) uv = vec2(u1, v0);
                    else if (gl_VertexID % 4 == 2) uv = vec2(u1, v1);
                    else uv = vec2(u0, v1);
                }
            ''',
            fragment_shader='''
                #version 330
                uniform sampler2D atlas;
                in vec2 uv;
                out vec4 f_color;

                void main() {
                    f_color = texture(atlas, uv);
                }
            '''
        )

        # Буфер вершин (позиции квадрата)
        self.vbo = self.ctx.buffer(np.array([
            -1.0, -1.0,  # Левый нижний
             1.0, -1.0,  # Правый нижний
             1.0,  1.0,  # Правый верхний
            -1.0,  1.0,  # Левый верхний
        ], dtype='f4'))

        # Индексный буфер
        self.ibo = self.ctx.buffer(np.array([0, 1, 2, 2, 3, 0], dtype='i4'))

        # VAO
        self.vao = self.ctx.vertex_array(
            self.program,
            [(self.vbo, '2f', 'in_pos')],  # Правильная привязка атрибута
            index_buffer=self.ibo
        )

        # Передача данных
        self.program['tile_indices'].write(tiles)

    def draw(self):
        self.ctx.clear(0.1, 0.1, 0.1)
        self.texture.use(location=0)
        self.vao.render(moderngl.TRIANGLES)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
            self.draw()
            pygame.display.flip()

if __name__ == '__main__':
    game = WindowGame()
    game.run()