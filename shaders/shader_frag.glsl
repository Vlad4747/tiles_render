#version 330 core

//in vec2 uv; // Входные текстурные координаты
out vec4 fragColor; // Цвет фрагмента


uniform vec2 u_resolution;
uniform sampler2D tex; // Текстура

void main() {
    vec2 uv = gl_FragCoord.xy / u_resolution.xy;
    uv.y=1.-uv.y;
    vec3 color = texture(tex,uv).xyz;
    fragColor = vec4(color,1.0); // Получение цвета из текстуры
}