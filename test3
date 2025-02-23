import pygame
import moderngl
import numpy as np
from PIL import Image
from random import randint

# Генерация мира
WORLD_WIDTH = 20
WORLD_HEIGHT = 20
tiles = set()

for y in range(WORLD_HEIGHT):
    for x in range(WORLD_WIDTH):
        # Генерация случайного типа тайла (0-2)
        texture_id = randint(0, 2)
        tiles.add((x, y, 0, (texture_id, 0)))  # (x, y, z, (texture_id, variant))


def main():
    pygame.init()
    width, height = 800, 600
    pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
    ctx = moderngl.create_context()
    ctx.viewport = (0, 0, width, height)

    # Загрузка текстуры
    img = Image.open("atlas.png").transpose(Image.FLIP_TOP_BOTTOM).convert("RGBA")
    texture = ctx.texture(img.size, 4, img.tobytes())
    texture.build_mipmaps()

    # Параметры атласа
    ATLAS_COLS = 32
    ATLAS_ROWS = 2
    TILE_SIZE = 2.0 / max(WORLD_WIDTH, WORLD_HEIGHT)  # Размер тайла в NDC

    # Сбор данных
    vertex_data = []
    indices = []
    index = 0

    for tile in tiles:
        x, y, z, (texture_id, variant) = tile

        # Позиция в атласе
        tex_x = texture_id % ATLAS_COLS
        tex_y = texture_id // ATLAS_COLS

        # UV-координаты
        u0 = tex_x / ATLAS_COLS
        v0 = 1.0 - (tex_y + 1) / ATLAS_ROWS
        u1 = (tex_x + 1) / ATLAS_COLS
        v1 = 1.0 - tex_y / ATLAS_ROWS

        # Координаты вершин
        x0 = x * TILE_SIZE - 1.0
        y0 = y * TILE_SIZE - 1.0
        x1 = x0 + TILE_SIZE
        y1 = y0 + TILE_SIZE

        # Вершины и UV
        vertex_data.extend([
            x0, y0, u0, v1,
            x1, y0, u1, v1,
            x1, y1, u1, v0,
            x0, y1, u0, v0
        ])

        # Индексы
        indices.extend([
            index, index + 1, index + 2,
                   index + 2, index + 3, index
        ])
        index += 4

    # Буферы
    vbo = ctx.buffer(np.array(vertex_data, dtype='f4'))
    ibo = ctx.buffer(np.array(indices, dtype='i4'))

    # Шейдеры
    program = ctx.program(
        vertex_shader='''
        #version 330
        in vec2 in_pos;
        in vec2 in_uv;
        out vec2 uv;
        void main() {
            gl_Position = vec4(in_pos, 0.0, 1.0);
            uv = in_uv;
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

    # VAO
    vao = ctx.vertex_array(
        program,
        [(vbo, '2f 2f', 'in_pos', 'in_uv')],
        index_buffer=ibo
    )

    # Рендеринг
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ctx.clear(0.1, 0.1, 0.1)
        texture.use(location=0)
        vao.render(moderngl.TRIANGLES)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
