import numpy as np
import ctypes
import os
from OpenGL.GL import *
from texture import Texture
import glm

class Card:
    def __init__(self, caminho_textura):

        meia_larg = 1.0
        alt = 3.1

        vertices = np.array([
             meia_larg,  alt, 0.0,   1.0, 1.0,   0.0, 0.0, 1.0,
             meia_larg,  0.0, 0.0,   1.0, 0.0,   0.0, 0.0, 1.0,
            -meia_larg,  0.0, 0.0,   0.0, 0.0,   0.0, 0.0, 1.0,
            -meia_larg,  alt, 0.0,   0.0, 1.0,   0.0, 0.0, 1.0,
        ], dtype=np.float32)

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

        if os.path.exists(caminho_textura):
            self.textura = Texture(caminho_textura)
        else:
            print("Nao achou imagem da carta:", caminho_textura)
            self.textura = None

    def draw(self, id_shader, matriz_modelo):
        if self.textura:
            self.textura.bind()

        local_modelo = glGetUniformLocation(id_shader, "modelo")
        glUniformMatrix4fv(local_modelo, 1, GL_FALSE, glm.value_ptr(matriz_modelo))

        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
