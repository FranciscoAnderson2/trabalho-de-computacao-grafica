#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoord;
layout (location = 2) in vec3 aNormal;

out vec2 TexCoord;
out vec3 Normal;
out vec3 FragPos;

uniform mat4 modelo;
uniform mat4 camera;
uniform mat4 projecao;

void main()
{

    FragPos = vec3(modelo * vec4(aPos, 1.0));

    Normal = mat3(transpose(inverse(modelo))) * aNormal;

    TexCoord = aTexCoord;

    gl_Position = projecao * camera * modelo * vec4(aPos, 1.0);
}
