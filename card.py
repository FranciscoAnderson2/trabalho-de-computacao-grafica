import ctypes
from OpenGL.GL import *
import glm

# ------------------------------------------------------------------
# Card: representa uma carta como um retangulo 3D colorido
# Sem textura ainda - so geometria basica com VBO/VAO/EBO
# ------------------------------------------------------------------
class Card:
    # Tamanho padrao de uma carta
    LARGURA = 2.0
    ALTURA  = 3.1

    def __init__(self, cor=(0.8, 0.5, 0.1, 1.0)):
        # Cor da carta (R, G, B, A)
        self.cor = cor
        self._setup_geometry()

    def _setup_geometry(self):
        l = self.LARGURA / 2.0  # metade da largura
        h = self.ALTURA         # altura total

        # Posicoes de cada ponta do retangulo (x, y, z) - sem UV por enquanto
        vertices = np.array([
             l,  h,  0.0,   # topo-direito
             l,  0.0, 0.0,  # base-direito
            -l,  0.0, 0.0,  # base-esquerdo
            -l,  h,  0.0,   # topo-esquerdo
        ], dtype=np.float32)

        indices = np.array([
            0, 1, 3,   # triangulo 1
            1, 2, 3,   # triangulo 2
        ], dtype=np.uint32)

        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        self.EBO = glGenBuffers(1)

        glBindVertexArray(self.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        stride = 3 * vertices.itemsize
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glBindVertexArray(0)

    def draw(self, shader_id, matriz_modelo):
        # Desenha a carta usando a matriz que veio la da main
        loc_modelo = glGetUniformLocation(shader_id, "modelo")
        loc_cor    = glGetUniformLocation(shader_id, "cor")

        glUniformMatrix4fv(loc_modelo, 1, GL_FALSE, glm.value_ptr(matriz_modelo))
        glUniform4f(loc_cor, self.cor[0], self.cor[1], self.cor[2], self.cor[3])

        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
