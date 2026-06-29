import numpy as np
import ctypes
import os
from OpenGL.GL import *
from texture import Texture
import glm

class CenarioQuad:
    def __init__(self, lista_vertices, caminho_textura, normal=(0.0, 1.0, 0.0)):
        self.caminho = caminho_textura

        dados = []
        for v in lista_vertices:

            dados.extend([v[0], v[1], v[2], v[3], v[4], normal[0], normal[1], normal[2]])

        vertices = np.array(dados, dtype=np.float32)

        indices = np.array([0, 1, 3, 1, 2, 3], dtype=np.uint32)

        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        self.EBO = glGenBuffers(1)

        glBindVertexArray(self.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        tamanho = 8 * 4

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, tamanho, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, tamanho, ctypes.c_void_p(3 * 4))
        glEnableVertexAttribArray(1)

        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, tamanho, ctypes.c_void_p(5 * 4))
        glEnableVertexAttribArray(2)

        glBindVertexArray(0)

        if os.path.exists(self.caminho):
            self.textura = Texture(self.caminho)
        else:
            print("Erro ao achar textura:", self.caminho)
            self.textura = None

    def draw(self, id_shader):
        if self.textura:
            self.textura.bind()
        local_modelo = glGetUniformLocation(id_shader, "modelo")

        matriz = glm.mat4(1.0)
        glUniformMatrix4fv(local_modelo, 1, GL_FALSE, glm.value_ptr(matriz))
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

    def draw_em(self, id_shader, matriz_modelo):

        if self.textura:
            self.textura.bind()
        local_modelo = glGetUniformLocation(id_shader, "modelo")
        glUniformMatrix4fv(local_modelo, 1, GL_FALSE, glm.value_ptr(matriz_modelo))
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
