import os
from OpenGL.GL import *
from PIL import Image

class Texture:
    def __init__(self, nome_arquivo):
        self.id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        try:
            imagem = Image.open(nome_arquivo)

            imagem = imagem.transpose(Image.FLIP_TOP_BOTTOM)

            dados_imagem = imagem.convert("RGBA").tobytes()

            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, imagem.width, imagem.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, dados_imagem)

            glGenerateMipmap(GL_TEXTURE_2D)
        except Exception as e:
            print(f"Erro ao carregar textura {nome_arquivo}: {e}")

    def bind(self):
        glBindTexture(GL_TEXTURE_2D, self.id)
