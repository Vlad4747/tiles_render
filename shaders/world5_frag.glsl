#version 330
uniform sampler2D atlas;  // Текстура атласа
in vec2 opos;  // Входные координаты
out vec4 f_color;  // Выходной цвет
uniform int tile_indices[400];  // Индексы тайлов
uniform int tile_heights[400];  // Высоты тайлов
uniform float elapsed;  // Время (закомментировано)
uniform vec2 res;  // Разрешение окна
const float MAXH = 7.;  // Максимальная высота
float map(float value, float min1, float max1, float min2, float max2) {
    return min2 + (value - min1) * (max2 - min2) / (max1 - min1);  // Функция для отображения значений
}
float ofract(float x){
    return fract(x+0.5);  // Функция для получения дробной части
}
vec2 mapTexture(vec2 coord,vec2 iuv){
    return vec2(
        ofract((iuv.x+coord.x)/32./2.+.5),  // Отображение текстурных координат
        ofract((iuv.y+1.)     /2./2.)+coord.y/2.
        )*2.;  // Масштабирование текстурных координат
}
float fetchID(vec2 pos){return float(tile_indices[int(pos.x) % 10 + int(pos.y) * 10]);}  // Получение ID тайла
int fetchH(vec2 pos){return tile_heights[int(pos.x) % 10 + int(pos.y) * 10];}  // Получение высоты тайла
void main() {
    tile_indices[0]; tile_heights[0]; // required to keep variables used
    float ratio = min(res.x,res.y)/max(res.x,res.y);  // Соотношение сторон
    f_color = vec4(0.);  // Инициализация цвета

    float startr = 0.9;  // Начальная высота
    int ii = -2;  // Индекс высоты
    for(float i = startr+(1.-startr)/MAXH-0.001; i <= 1.; i+=(1.-startr)/MAXH){  // Цикл по высоте
        ii++;  // Увеличение индекса высот
        //тень
        vec2 iuv = (opos+vec2(0,-0.1/ratio)+vec2(0.03*cos(elapsed/1.),0.03*cos(elapsed/1.)/ratio))*(1./i); // Внутренние текстурные координаты
        vec2 muv = (iuv+1.)*vec2(10.,10.)*vec2(1.,ratio); // Отображение текстурных координат
        if(fetchH(muv) <= ii){  // Проверка высоты тайла
            vec2 tuv = vec2(fract(muv.x),fract(muv.y)); // Текстурные координаты
            if(i > max(abs(opos.x),abs(opos.y))) {  // Проверка на границы
                f_color-=vec4(vec3(0.05),1.);
            }
        }
        //тайл
        iuv = opos*(1./i); // Внутренние текстурные координаты
        muv = (iuv+1.)*vec2(10.,10.)*vec2(1.,ratio); // Отображение текстурных координат
        if(fetchH(muv) >= ii){  // Проверка высоты тайла
            vec2 tuv = vec2(fract(muv.x),fract(muv.y)); // Текстурные координаты
            if(i > max(abs(opos.x),abs(opos.y))) {  // Проверка на границы
                f_color=texture(atlas,  // Получение цвета текстуры
                    mapTexture(vec2(fetchID(muv),0.),tuv));
            }
        }
    }
}