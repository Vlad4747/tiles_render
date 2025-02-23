import numpy as np
import moderngl
import pygame
from pygame.locals import *

# Инициализация Pygame
pygame.init()
pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
ctx = moderngl.create_context()

# Создание шейдера
shader_program = ctx.program(
    vertex_shader="""
    #version 330
    in vec2 in_vert;
    out vec3 color;

    void main() {
        gl_Position = vec4(in_vert, 0.0, 1.0);
        color = vec3(1.0, 0.0, 0.0); // Красный цвет
    }
    """,
    fragment_shader="""
    #version 330
    in vec3 color;
    out vec4 fragColor;

    void main() {
        fragColor = vec4(color, 1.0); // Используем цвет из вершинного шейдера
    }
    """
)

# Создание VAO для квадрата
vertices = np.array([
    -0.5, -0.5,  # Нижний левый угол
     0.5, -0.5,  # Нижний правый угол
     0.5,  0.5,  # Верхний правый угол
    -0.5,  0.5,  # Верхний левый угол
], dtype='f4')

# Индексы для отрисовки квадрата
indices = np.array([
    0, 1, 2,  # Первый треугольник
    0, 2, 3   # Второй треугольник
], dtype='i4')

# Создание VAO и VBO
vbo = ctx.buffer(vertices)
ibo = ctx.buffer(indices)
vao = ctx.simple_vertex_array(shader_program, vbo, 'in_vert', index_buffer=ibo)

# Основной цикл рендеринга
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    ctx.clear()  # Очистка экрана

    vao.render(moderngl.TRIANGLES)  # Рендеринг квадрата

    pygame.display.flip()  # Обновление экрана