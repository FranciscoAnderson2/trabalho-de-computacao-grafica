import numpy as np
import ctypes
from OpenGL.GL import *
import glm

class HUD:

    def __init__(self):

        vertices = np.array([
            1.0, 1.0, 0.0,  1.0, 1.0,
            1.0, 0.0, 0.0,  1.0, 0.0,
            0.0, 0.0, 0.0,  0.0, 0.0,
            0.0, 1.0, 0.0,  0.0, 1.0,
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

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(3 * 4))
        glEnableVertexAttribArray(1)
        glBindVertexArray(0)

    def _aplicar(self, shader_id, x, y, larg, alt):
        local_modelo = glGetUniformLocation(shader_id, "modelo")

        m = glm.translate(glm.mat4(1.0), glm.vec3(x, y, 0.0))
        m = glm.scale(m, glm.vec3(larg, alt, 1.0))
        glUniformMatrix4fv(local_modelo, 1, GL_FALSE, glm.value_ptr(m))

    def ret(self, shader_id, x, y, larg, alt, cor=(1,1,1,1)):

        self._aplicar(shader_id, x, y, larg, alt)
        glUniform4f(glGetUniformLocation(shader_id, "cor_hud"), *cor)
        glUniform1i(glGetUniformLocation(shader_id, "usar_textura"), 0)
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

    def imagem(self, shader_id, x, y, larg, alt, id_tex):

        self._aplicar(shader_id, x, y, larg, alt)
        glUniform4f(glGetUniformLocation(shader_id, "cor_hud"), 1,1,1,1)
        glUniform1i(glGetUniformLocation(shader_id, "usar_textura"), 1)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, id_tex)
        glUniform1i(glGetUniformLocation(shader_id, "textura"), 0)
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

    def borda(self, shader_id, x, y, larg, alt, espessura, cor):

        e = espessura
        self.ret(shader_id, x,       y,           larg, e,    cor)
        self.ret(shader_id, x,       y+alt-e,     larg, e,    cor)
        self.ret(shader_id, x,       y,           e,    alt,  cor)
        self.ret(shader_id, x+larg-e, y,          e,    alt,  cor)
