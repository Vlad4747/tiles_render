import pygame
import moderngl
import numpy as np
from PIL import Image


def create_tile_map(width, height):
    return np.random.randint(0, 3, (height, width), dtype=np.uint8)


def main():
    pygame.init()
    width, height = 800, 600
    pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
    ctx = moderngl.create_context()
    ctx.viewport = (0, 0, width, height)

    # Загрузка текстуры атласа
    try:
        img = Image.open("atlas.png").transpose(Image.FLIP_TOP_BOTTOM).convert("RGBA")
    except FileNotFoundError:
        raise SystemExit("Файл atlas.png не найден")

    texture = ctx.texture(img.size, 4, img.tobytes())
    texture.build_mipmaps()

    # Параметры сетки и атласа
    grid_size = 10
    atlas_cols = 32
    atlas_rows = 2
    tile_map = create_tile_map(grid_size, grid_size)
    tile_size = 2.0 / grid_size

    # Сбор данных вершин и UV
    vertex_data = []
    indices = []
    for y in range(grid_size):
        for x in range(grid_size):
            tile_id = tile_map[y, x]
            tex_x = tile_id % atlas_cols
            tex_y = tile_id // atlas_cols

            # Корректные UV-координаты
            u0 = tex_x / atlas_cols
            u1 = (tex_x + 1) / atlas_cols
            v0 = 1.0 - (tex_y + 1) / atlas_rows  # Инвертируем Y
            v1 = 1.0 - tex_y / atlas_rows

            # Координаты вершин
            x0 = x * tile_size - 1.0
            y0 = y * tile_size - 1.0
            x1 = x0 + tile_size
            y1 = y0 + tile_size

            # Вершины и UV
            vertex_data.extend([
                x0, y0, u0, v1,  # Левый нижний
                x1, y0, u1, v1,  # Правый нижний
                x1, y1, u1, v0,  # Правый верхний
                x0, y1, u0, v0  # Левый верхний
            ])

            # Индексы
            base_index = (y * grid_size + x) * 4
            indices.extend([
                base_index, base_index + 1, base_index + 2,
                            base_index + 2, base_index + 3, base_index
            ])

    # Создание буферов
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
        uniform sampler2D texture_atlas;
        in vec2 uv;
        out vec4 f_color;
        void main() {
            f_color = texture(texture_atlas, uv);
        }
        '''
    )

    # Настройка VAO
    vao = ctx.vertex_array(
        program,
        [
            (vbo, '2f 2f', 'in_pos', 'in_uv')
        ],
        index_buffer=ibo
    )

    # Основной цикл
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ctx.clear(0.0, 0.0, 0.0)  # Явная очистка
        texture.use(location=0)  # Активируем текстуру
        vao.render(moderngl.TRIANGLES)
        pygame.display.flip()
        clock.tick(6000)
        pygame.display.set_caption(f"FPS: {clock.get_fps():.2f}")

    pygame.quit()



if __name__ == "__main__":
    main()