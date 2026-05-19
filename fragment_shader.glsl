#version 330 core
out vec4 FragColor;

uniform vec4 cor;  // cor solida passada pela CPU

void main()
{
    FragColor = cor;
}
