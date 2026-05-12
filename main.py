import glfw
from OpenGL.GL import *
import glm

from shader  import Shader
from cenario import CenarioQuad
from card    import Card

# ------------------------------------------------------------------
# Aqui a gente aplica a translacao, rotacao e escala
# pra colocar a carta no lugar certo
# ------------------------------------------------------------------
def desenhar_carta(carta, shader_id, x, y, z, rot_x=0.0, rot_z=0.0, escala=0.85):
    matriz_modelo = glm.translate(glm.mat4(1.0), glm.vec3(x, y, z))
    matriz_modelo = glm.rotate(matriz_modelo, glm.radians(rot_x), glm.vec3(1, 0, 0))
    if rot_z != 0:
        matriz_modelo = glm.rotate(matriz_modelo, glm.radians(rot_z), glm.vec3(0, 0, 1))
    matriz_modelo = glm.scale(matriz_modelo, glm.vec3(escala, escala, escala))
    carta.draw(shader_id, matriz_modelo)

# ------------------------------------------------------------------
# main
# ------------------------------------------------------------------
def main():
    if not glfw.init():
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    janela = glfw.create_window(1200, 700, "Naruto Card Game", None, None)
    if not janela:
        glfw.terminate()
        return

    glfw.make_context_current(janela)

    # Carrega o shader
    meuShader = Shader("vertex_shader.glsl", "fragment_shader.glsl")

    # ------------------------------------------------------------------
    # Cenario: chao, paredes - so cores solidas por enquanto
    # Cada ponto tem 3 numeros: X, Y, Z
    # ------------------------------------------------------------------
    # Chao verde escuro
    chao  = CenarioQuad([
        ( 10, 0,  10),  # A - frente direita
        ( 10, 0, -10),  # B - fundo direita
        (-10, 0, -10),  # C - fundo esquerda
        (-10, 0,  10),  # D - frente esquerda
    ], cor=(0.15, 0.35, 0.15, 1.0))

    # Parede de fundo cinza azulado
    fundo = CenarioQuad([
        ( 10, 0,  -10),
        ( 10, 10, -10),
        (-10, 10, -10),
        (-10, 0,  -10),
    ], cor=(0.2, 0.2, 0.35, 1.0))

    # Parede esquerda
    pesq = CenarioQuad([
        (-10, 0,  -10),
        (-10, 10, -10),
        (-10, 10,  10),
        (-10, 0,   10),
    ], cor=(0.25, 0.25, 0.4, 1.0))

    # Parede direita
    pdir = CenarioQuad([
        (10, 0,   10),
        (10, 10,  10),
        (10, 10, -10),
        (10, 0,  -10),
    ], cor=(0.25, 0.25, 0.4, 1.0))

    # ------------------------------------------------------------------
    # Cartas: retangulos coloridos representando os ninjas
    # Jogador 1 (esquerda) = laranja
    # Jogador 2 (direita)  = azul
    # ------------------------------------------------------------------
    carta_j1 = Card(cor=(0.9, 0.5, 0.1, 1.0))  # laranja (Naruto)
    carta_j2 = Card(cor=(0.1, 0.3, 0.8, 1.0))  # azul (Sasuke)

    # Pega os locais dos uniforms do shader
    loc_camera  = glGetUniformLocation(meuShader.shaderId, "camera")
    loc_projecao = glGetUniformLocation(meuShader.shaderId, "projecao")

    glEnable(GL_DEPTH_TEST)

    # ------------------------------------------------------------------
    # Loop principal de renderizacao
    # ------------------------------------------------------------------
    while not glfw.window_should_close(janela):
        glfw.poll_events()

        largura, altura = glfw.get_framebuffer_size(janela)
        glViewport(0, 0, largura, altura)

        # Limpa a tela
        glClearColor(0.08, 0.08, 0.12, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(meuShader.shaderId)

        proporcao_tela = largura / altura if altura > 0 else 1.0
        # Configura a perspectiva pra dar o efeito 3D
        matriz_projecao = glm.perspective(glm.radians(45.0), proporcao_tela, 0.1, 100.0)
        # Posiciona a camera meio no alto olhando pro centro da mesa
        matriz_camera = glm.lookAt(glm.vec3(0, 8, 22), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))

        # Manda as matrizes la pro shader desenhar
        glUniformMatrix4fv(loc_projecao, 1, GL_FALSE, glm.value_ptr(matriz_projecao))
        glUniformMatrix4fv(loc_camera,   1, GL_FALSE, glm.value_ptr(matriz_camera))

        # ---- Desenha Cenario ----
        chao.draw(meuShader.shaderId)
        fundo.draw(meuShader.shaderId)
        pesq.draw(meuShader.shaderId)
        pdir.draw(meuShader.shaderId)

        # ---- Desenha Cartas no Campo ----
        # Jogador 1: esquerda da mesa, deitada com rotacao
        desenhar_carta(carta_j1, meuShader.shaderId,
                       x=-4.0, y=0.1, z=1.5, rot_x=-90.0, rot_z=-90.0, escala=1.1)
        desenhar_carta(carta_j1, meuShader.shaderId,
                       x=-4.0, y=0.1, z=-1.5, rot_x=-90.0, rot_z=-90.0, escala=1.1)

        # Jogador 2: direita da mesa
        desenhar_carta(carta_j2, meuShader.shaderId,
                       x=4.0, y=0.1, z=1.5, rot_x=-90.0, rot_z=90.0, escala=1.1)
        desenhar_carta(carta_j2, meuShader.shaderId,
                       x=4.0, y=0.1, z=-1.5, rot_x=-90.0, rot_z=90.0, escala=1.1)

        glfw.swap_buffers(janela)

    glfw.terminate()

if __name__ == "__main__":
    main()
