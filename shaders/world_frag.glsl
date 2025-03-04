#version 330
uniform sampler2D atlas;  // Текстура атласа
in vec2 opos;  // Входные координаты
out vec4 f_color;  // Выходной цвет
uniform vec2 res;  // Разрешение окна

float ofract(float x){
    return fract(x+0.5);  // Функция для получения дробной части
}
vec2 mapTexture(vec2 coord,vec2 iuv){
    return vec2(
        ofract((iuv.x+coord.x)/32./2.+.5),  // Отображение текстурных координат
        ofract((iuv.y+1.)     /2./2.)+coord.y/2.
        )*2.;  // Масштабирование текстурных координат
}
void main() {
    float ratio = min(res.x,res.y)/max(res.x,res.y);
    vec2 uv = opos*10.*vec2(1,ratio);
    vec2 tuv = vec2(fract(uv.x+0.5),fract(uv.y+0.5));
    f_color = texture(atlas,mapTexture(vec2(float(int((2.+sin(opos.x*10.)+sin(opos.y*10.)+0.5)*2.)-2.),0.),tuv));

}