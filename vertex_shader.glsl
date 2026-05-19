#version 330 core
layout (location = 0) in vec3 aPos;

uniform mat4 modelo;
uniform mat4 camera;
uniform mat4 projecao;

void main()
{
    gl_Position = projecao * camera * modelo * vec4(aPos, 1.0);
}
