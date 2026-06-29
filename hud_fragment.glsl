#version 330 core
out vec4 FragColor;

in vec2 TexCoord;

uniform sampler2D textura;
uniform vec4 cor_hud;       
uniform bool usar_textura;  

void main()
{
    if (usar_textura) {
        vec4 t = texture(textura, TexCoord);
        if (t.a < 0.05) discard;
        FragColor = t;
    } else {
        FragColor = cor_hud;
    }
}
