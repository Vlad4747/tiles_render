import numpy as np
import moderngl
import pygame
from pygame.locals import *
from PIL import Image

WIN_SIZE = (1024, 720)

# мир, который надо рендерить
tiles = set()

WORLD_WIDTH = 20
WORLD_HEIGHT = 20
for i in range(WORLD_HEIGHT):
    for j in range(WORLD_WIDTH):

        # можешь генирацию написать

        tiles.add((j,i,0,(0,0))) # (0,0) координаты текстуры на атласе


class WindowGame:
    def __init__(self):
        self.init()

    def init(self):
        pygame.init()
        pygame.display.set_mode(WIN_SIZE, DOUBLEBUF | OPENGL)
        self.ctx = moderngl.create_context()

        with open("shaders/shader_vert.glsl", "r", encoding='utf-8') as f:
            vert = f.read()
        with open("shaders/shader_frag.glsl", "r", encoding='utf-8') as f:
            frag = f.read()

        img = Image.open("atlas.png").convert("RGB")
        texture = self.ctx.texture(img.size, 3, img.tobytes())
        texture.use(location=0)

        self.shader_program = self.ctx.program(
            vertex_shader=vert,
            fragment_shader=frag
        )

        # Создание VAO для квадрата
        self.vertices = np.array([
            -1, -1,  # Нижний левый угол
            1, -1,  # Нижний правый угол
            1, 1,  # Верхний правый угол
            -1, 1,  # Верхний левый угол
        ], dtype='f4')

        # Индексы для отрисовки квадрата
        self.indices = np.array([
            0, 1, 2,  # Первый треугольник
            0, 2, 3  # Второй треугольник
        ], dtype='i4')

        # Создание VAO и VBO
        self.vbo = self.ctx.buffer(self.vertices)
        self.ibo = self.ctx.buffer(self.indices)
        self.vao = self.ctx.simple_vertex_array(self.shader_program, self.vbo, 'in_vert', index_buffer=self.ibo)

        self.clock = pygame.time.Clock()
        self.shader_program['u_resolution'].value = WIN_SIZE
        self.shader_program['tex'].value = 0

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    def draw(self):
        self.ctx.clear()  # Очистка экрана
        self.vao.render(moderngl.TRIANGLES)  # Рендеринг квадрата

    def run(self):
        while True:
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(6000)  # Ограничение FPS до 60
            pygame.display.set_caption(f"FPS: {self.clock.get_fps():.2f}")


if __name__ == '__main__':
    game = WindowGame()
    game.run()
