from OpenGL.GL import *
import OpenGL.GL.shaders as gls
import os

class Shader:
    def __init__(self, arquivo_vertex, arquivo_fragment):
        pasta_atual = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(pasta_atual, arquivo_vertex), 'r') as file:
            codigo_vertex = file.read()
        with open(os.path.join(pasta_atual, arquivo_fragment), 'r') as file:
            codigo_fragment = file.read()

        id_vertex   = gls.compileShader(codigo_vertex,   GL_VERTEX_SHADER)
        id_fragment = gls.compileShader(codigo_fragment, GL_FRAGMENT_SHADER)
        self.shaderId = gls.compileProgram(id_vertex, id_fragment)
