#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoord;

out vec2 TexCoord;

uniform mat4 modelo;
uniform mat4 projecao_hud;

void main()
{
    gl_Position = projecao_hud * modelo * vec4(aPos, 1.0);
    TexCoord = aTexCoord;
}
