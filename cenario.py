import numpy as np
import ctypes
from OpenGL.GL import *
import glm

# ------------------------------------------------------------------
# CenarioQuad: desenha um quadrilateral (chao, parede) com cor solida
# Sem textura - so geometria basica com VBO/VAO/EBO
# ------------------------------------------------------------------
class CenarioQuad:
    def __init__(self, lista_vertices, cor):
        # cor é uma tupla (R, G, B, A) de 0.0 a 1.0
        self.cor = cor
        self._setup_geometry(lista_vertices)

    def _setup_geometry(self, lista_vertices):
        # Prepara os pontos do cenario na placa de video
        vertices = np.array(lista_vertices, dtype=np.float32).flatten()
        # Liga os pontos formando dois triangulos (o famoso desenho indexado)
        indices = np.array([0, 1, 3, 1, 2, 3], dtype=np.uint32)

        self.VAO = glGenVertexArrays(1)  # Cria VAO
        self.VBO = glGenBuffers(1)       # Cria VBO para os vertices
        self.EBO = glGenBuffers(1)       # Cria EBO para os indices

        glBindVertexArray(self.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        # Cada vertice tem so 3 numeros (X, Y, Z) - sem UV
        stride = 3 * vertices.itemsize
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glBindVertexArray(0)

    def draw(self, shader_id):
        loc_modelo = glGetUniformLocation(shader_id, "modelo")
        loc_cor    = glGetUniformLocation(shader_id, "cor")

        # Deixa a matriz salva aqui pra nao dar ruim na memoria do python depois
        matriz_identidade = glm.mat4(1.0)
        glUniformMatrix4fv(loc_modelo, 1, GL_FALSE, glm.value_ptr(matriz_identidade))

        # Manda a cor para o shader
        glUniform4f(loc_cor, self.cor[0], self.cor[1], self.cor[2], self.cor[3])

        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
