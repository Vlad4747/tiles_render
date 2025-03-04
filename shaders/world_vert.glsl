#version 330
in vec2 in_pos;  // Добавлено объявление атрибута
out vec2 opos;  // Выходные координаты

void main() {
    gl_Position = vec4(in_pos, 0.0, 1.0);  // Установка позиции вершин
    opos = in_pos;  // Передача координат в фрагментный шейдер
}