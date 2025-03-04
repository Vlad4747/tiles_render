#version 330 core


out vec4 fragColor; // Цвет фрагмента
in vec2 v_texcoord; // Получаем текстурные координаты




uniform vec2 u_resolution;
uniform sampler2D tex; // Текстура

void main() {
    vec2 uv = gl_FragCoord.xy / u_resolution.xy;
    uv.y=1.-uv.y;
    uv.x = uv.x * u_resolution.x/u_resolution.y;
    uv.x = uv.x / 32;
    uv.y = uv.y / 2;
    uv = uv / 0.1;

    uv.x = mod(uv.x,1./32.);
    uv.y = mod(uv.y,1./2.);

    vec3 color = texture(tex,v_texcoord.xy/vec2(32.,2.)).xyz;
    fragColor = vec4(color,1.0); // Получение цвета из текстуры
    if (uv.x > 1./32. || uv.y >  1./2.){
         fragColor = vec4(vec3(0.),1.0);
    }
}