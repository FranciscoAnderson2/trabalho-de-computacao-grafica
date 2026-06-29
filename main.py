import glfw
from OpenGL.GL import *
import glm
import os
import math
import random

from shader  import Shader
from cenario import CenarioQuad
from card    import Card
from hud     import HUD
from texture import Texture

NINJAS = [
    ("choji_akimichi.png",  4, 4, 6), ("dosu_kinuta.png",    5, 6, 5), ("gaara.png",          5, 4, 7),
    ("hinata_hyuga.png",    2, 2, 3), ("ino_yamanaka.png",   4, 3, 5), ("kankuro.png",         5, 5, 6),
    ("kiba_inuzuka.png",    2, 3, 2), ("kin_tsuchi.png",     2, 2, 3), ("naruto_uzumaki.png",  3, 4, 4),
    ("neji_hyuga.png",      4, 4, 5), ("rock_lee.png",       3, 6, 2), ("sakura_haruno.png",   3, 2, 5),
    ("sasuke_uchiha.png",   4, 5, 4), ("shikamaru_nara.png", 3, 2, 5), ("shino_aburame.png",   2, 2, 2),
    ("temari.png",          4, 5, 4), ("tenten.png",         3, 3, 4), ("zaku_abumi.png",      3, 5, 2),
]

def desenhar_carta(carta, shader_id, x, y, z, rotacao_x=0.0, rotacao_z=0.0, escala=0.85):

    matriz_modelo = glm.translate(glm.mat4(1.0), glm.vec3(x, y, z))
    matriz_modelo = glm.rotate(matriz_modelo, glm.radians(rotacao_x), glm.vec3(1, 0, 0))
    if rotacao_z != 0:
        matriz_modelo = glm.rotate(matriz_modelo, glm.radians(rotacao_z), glm.vec3(0, 0, 1))
    matriz_modelo = glm.scale(matriz_modelo, glm.vec3(escala, escala, escala))

    carta.draw(shader_id, matriz_modelo)

def main():

    if not glfw.init(): return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    janela = glfw.create_window(1200, 700, "Naruto Card Game", None, None)
    if not janela:
        glfw.terminate()
        return
    glfw.make_context_current(janela)

    shader3d = Shader("vertex_shader.glsl", "fragment_shader.glsl")
    shader_hud = Shader("hud_vertex.glsl", "hud_fragment.glsl")

    pasta_base = os.path.dirname(os.path.abspath(__file__))
    pasta_cenario = os.path.join(pasta_base, "assets", "cenario")
    pasta_cartas = os.path.join(pasta_base, "assets", "cartas", "ninjas")
    pasta_hud_img = os.path.join(pasta_base, "assets", "hud")

    chao = CenarioQuad([
        ( 30, -10,  0,  8, 0), ( 30,  25,  0,  8, 6),
        (-30,  25,  0,  0, 6), (-30, -10,  0,  0, 0),
    ], os.path.join(pasta_cenario, "textura_chao.jpg"), normal=(0.0, 0.0, 1.0))

    fundo = CenarioQuad([
        ( 30, -10,  0, 1, 0), ( 30, -10, 20, 1, 1),
        (-30, -10, 20, 0, 1), (-30, -10,  0, 0, 0),
    ], os.path.join(pasta_cenario, "textura_parede_fundo.png"), normal=(0.0, 1.0, 0.0))

    parede_esquerda = CenarioQuad([
        (-10, -10,  0, 0, 0), (-10, -10, 15, 0, 1),
        (-10,  25, 15, 1, 1), (-10,  25,  0, 1, 0),
    ], os.path.join(pasta_cenario, "textura_parede_lateral.png"), normal=(1.0, 0.0, 0.0))

    parede_direita = CenarioQuad([
        (10,  25,  0, 0, 0), (10,  25, 15, 0, 1),
        (10, -10, 15, 1, 1), (10, -10,  0, 1, 0),
    ], os.path.join(pasta_cenario, "textura_parede_lateral.png"), normal=(-1.0, 0.0, 0.0))

    mao_cenario = CenarioQuad([
        ( 12, -9.9, -1, 1, 0), ( 12, -9.9, 10, 1, 1),
        (-12, -9.9, 10, 0, 1), (-12, -9.9, -1, 0, 0),
    ], os.path.join(pasta_cenario, "textura_mao_jutsu.png"), normal=(0.0, 1.0, 0.0))

    objetos_cartas = {}
    for nome, custo, ataque, vida in NINJAS:
        objetos_cartas[nome] = Card(os.path.join(pasta_cartas, nome))

    def criar_baralho():
        baralho = [(objetos_cartas[n], c, a, v) for n, c, a, v in NINJAS]
        random.shuffle(baralho)
        return baralho

    baralho_jogador_1 = criar_baralho()
    baralho_jogador_2 = criar_baralho()

    VIDA_MAXIMA = 15
    CHAKRA_MAXIMO = 10

    vida_jogadores = [VIDA_MAXIMA, VIDA_MAXIMA]
    chakra_jogadores = [3, 3]           
    turno_atual = [0]              
    mao_jogadores = [[], []]         
    campo_jogadores = [[], []]         
    selecao_mao = [0, 0]           
    selecao_campo = [None, None]   
    comprou_carta = [False, False]   
    animacao_ataque = [-1, -1, 0.0]  

    def controle_teclado(janela_jogo, tecla, scancode, acao, mods):

        if acao != glfw.PRESS:
            return

        jogador = turno_atual[0]
        baralhos = [baralho_jogador_1, baralho_jogador_2]

        if glfw.KEY_1 <= tecla <= glfw.KEY_6:
            indice = tecla - glfw.KEY_1
            if indice < len(mao_jogadores[jogador]):
                selecao_mao[jogador] = indice

        elif tecla == glfw.KEY_C:
            if not comprou_carta[jogador] and len(mao_jogadores[jogador]) < 6 and baralhos[jogador]:
                mao_jogadores[jogador].append(baralhos[jogador].pop(0))
                selecao_mao[jogador] = len(mao_jogadores[jogador]) - 1
                comprou_carta[jogador] = True

        elif tecla == glfw.KEY_ENTER:
            if mao_jogadores[jogador] and len(campo_jogadores[jogador]) < 2:
                indice = min(selecao_mao[jogador], len(mao_jogadores[jogador]) - 1)
                carta_selecionada, custo_carta, ataque_carta, vida_carta = mao_jogadores[jogador][indice]

                if chakra_jogadores[jogador] >= custo_carta:
                    chakra_jogadores[jogador] -= custo_carta
                    campo_jogadores[jogador].append((carta_selecionada, custo_carta, ataque_carta, vida_carta, False))
                    mao_jogadores[jogador].pop(indice)
                    selecao_mao[jogador] = max(0, min(selecao_mao[jogador], len(mao_jogadores[jogador]) - 1))

        elif tecla == glfw.KEY_Q: selecao_campo[jogador] = 0 if len(campo_jogadores[jogador]) > 0 else None
        elif tecla == glfw.KEY_W: selecao_campo[jogador] = 1 if len(campo_jogadores[jogador]) > 1 else None
        elif tecla == glfw.KEY_E: selecao_campo[jogador] = 2 if len(campo_jogadores[jogador]) > 2 else None
        elif tecla == glfw.KEY_R: selecao_campo[jogador] = 3 if len(campo_jogadores[jogador]) > 3 else None

        elif tecla == glfw.KEY_A:
            indice_ataque = selecao_campo[jogador]
            if indice_ataque is not None and indice_ataque < len(campo_jogadores[jogador]):
                carta_ataque, custo_ataque, ataque_real, vida_atk, ja_atacou = campo_jogadores[jogador][indice_ataque]
                if not ja_atacou:

                    animacao_ataque[0] = jogador
                    animacao_ataque[1] = indice_ataque
                    animacao_ataque[2] = glfw.get_time()

                    dano_ataque = ataque_real
                    inimigo = 1 - jogador

                    if campo_jogadores[inimigo]:

                        carta_def, custo_def, atk_def, vida_def, atacou_def = campo_jogadores[inimigo][0]
                        vida_def -= dano_ataque

                        if vida_def <= 0:

                            dano_perfurou = abs(vida_def)
                            if dano_perfurou > 0:
                                vida_jogadores[inimigo] = max(0, vida_jogadores[inimigo] - dano_perfurou)
                            campo_jogadores[inimigo].pop(0)
                        else:
                            campo_jogadores[inimigo][0] = (carta_def, custo_def, atk_def, vida_def, atacou_def)
                    else:

                        vida_jogadores[inimigo] = max(0, vida_jogadores[inimigo] - dano_ataque)

                    campo_jogadores[jogador][indice_ataque] = (carta_ataque, custo_ataque, ataque_real, vida_atk, True)
                    selecao_campo[jogador] = None

        elif tecla == glfw.KEY_SPACE:
            pode_comprar = (len(baralhos[jogador]) > 0 and len(mao_jogadores[jogador]) < 6)

            if not comprou_carta[jogador] and pode_comprar:
                print("AVISO: Voce precisa puxar uma carta (tecla C) antes de passar a vez!")
            else:
                proximo_jogador = 1 - jogador
                turno_atual[0] = proximo_jogador
                comprou_carta[proximo_jogador] = False
                chakra_jogadores[proximo_jogador] = min(CHAKRA_MAXIMO, chakra_jogadores[proximo_jogador] + 1)

                campo_jogadores[proximo_jogador] = [(c, custo, atk, vida, False) for c, custo, atk, vida, atacou in campo_jogadores[proximo_jogador]]
                selecao_campo[proximo_jogador] = None

    glfw.set_key_callback(janela, controle_teclado)

    textura_naruto = Texture(os.path.join(pasta_hud_img, "naruto player1.png"))
    textura_sasuke = Texture(os.path.join(pasta_hud_img, "sasuke player2.png"))
    interface_hud = HUD()

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    local_camera = glGetUniformLocation(shader3d.shaderId, "camera")
    local_projecao = glGetUniformLocation(shader3d.shaderId, "projecao")
    local_luz = glGetUniformLocation(shader3d.shaderId, "luzPos")
    local_posicao_camera = glGetUniformLocation(shader3d.shaderId, "cameraPos")

    while not glfw.window_should_close(janela):
        glfw.poll_events()

        largura_tela, altura_tela = glfw.get_framebuffer_size(janela)
        glViewport(0, 0, largura_tela, altura_tela)

        glClearColor(0.08, 0.08, 0.12, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glEnable(GL_DEPTH_TEST)
        glUseProgram(shader3d.shaderId)

        proporcao_tela = largura_tela / altura_tela if altura_tela > 0 else 1.0
        matriz_projecao = glm.perspective(glm.radians(45.0), proporcao_tela, 0.1, 100.0)

        posicao_camera = glm.vec3(0, 22, 8)
        matriz_camera = glm.lookAt(posicao_camera, glm.vec3(0, 0, 0), glm.vec3(0, 0, 1))

        glUniformMatrix4fv(local_projecao, 1, GL_FALSE, glm.value_ptr(matriz_projecao))
        glUniformMatrix4fv(local_camera, 1, GL_FALSE, glm.value_ptr(matriz_camera))

        tempo_atual = glfw.get_time()

        glUniform3f(local_luz, 0.0, 4.0, 5.0)
        glUniform3f(local_posicao_camera, posicao_camera.x, posicao_camera.y, posicao_camera.z)

        chao.draw(shader3d.shaderId)
        fundo.draw(shader3d.shaderId)
        parede_esquerda.draw(shader3d.shaderId)
        parede_direita.draw(shader3d.shaderId)
        mao_cenario.draw(shader3d.shaderId)

        for indice_carta, (carta, custo, atk, vida, atacou) in enumerate(campo_jogadores[0]):
            carta_selecionada = (turno_atual[0] == 0 and selecao_campo[0] == indice_carta)
            escala_carta = 1.45 if carta_selecionada else 1.25
            altura_z = 0.4 if carta_selecionada else 0.1 

            offset_x = 0.0
            if animacao_ataque[0] == 0 and animacao_ataque[1] == indice_carta:
                progresso = (tempo_atual - animacao_ataque[2]) / 0.8
                if progresso < 1.0:
                    offset_x = math.sin(progresso * math.pi) * -3.0

            posicao_x = 5.5 + (indice_carta * 4.0)
            desenhar_carta(carta, shader3d.shaderId,
                           x=posicao_x + offset_x, y=6.0, z=altura_z,
                           rotacao_x=0.0, rotacao_z=90.0, escala=escala_carta)

        for indice_carta, (carta, custo, atk, vida, atacou) in enumerate(campo_jogadores[1]):
            carta_selecionada = (turno_atual[0] == 1 and selecao_campo[1] == indice_carta)
            escala_carta = 1.45 if carta_selecionada else 1.25
            altura_z = 0.4 if carta_selecionada else 0.1

            offset_x = 0.0
            if animacao_ataque[0] == 1 and animacao_ataque[1] == indice_carta:
                progresso = (tempo_atual - animacao_ataque[2]) / 0.8
                if progresso < 1.0:
                    offset_x = math.sin(progresso * math.pi) * 3.0

            posicao_x = -5.5 - (indice_carta * 4.0)
            desenhar_carta(carta, shader3d.shaderId,
                           x=posicao_x + offset_x, y=6.0, z=altura_z,
                           rotacao_x=0.0, rotacao_z=-90.0, escala=escala_carta)

        jogador = turno_atual[0]
        mao_do_jogador = mao_jogadores[jogador]
        quantidade_cartas = len(mao_do_jogador)

        if quantidade_cartas > 0:
            espaco_entre_cartas = min(2.2, 18.0 / quantidade_cartas)
            posicao_inicial_x = (quantidade_cartas - 1) * espaco_entre_cartas / 2.0

            for indice_carta, (carta, custo, atk, vida) in enumerate(mao_do_jogador):
                posicao_x = posicao_inicial_x - (indice_carta * espaco_entre_cartas)
                posicao_z = 1.6 if indice_carta == selecao_mao[jogador] else 1.0  
                posicao_y = 15.0  

                desenhar_carta(carta, shader3d.shaderId,
                               x=posicao_x, y=posicao_y, z=posicao_z,
                               rotacao_x=-60.0, rotacao_z=180.0, escala=0.75)

        glDisable(GL_DEPTH_TEST)
        glUseProgram(shader_hud.shaderId)

        matriz_ortografica = glm.ortho(0.0, float(largura_tela), 0.0, float(altura_tela), -1.0, 1.0)
        glUniformMatrix4fv(glGetUniformLocation(shader_hud.shaderId, "projecao_hud"), 1, GL_FALSE, glm.value_ptr(matriz_ortografica))

        tamanho_avatar = 90    
        tamanho_borda = 6     
        margem_tela = 15    
        largura_barra = 120   
        altura_barra = 10    
        espaco_entre_barras = 4     

        posicao_x_j1 = margem_tela
        posicao_y_j1 = margem_tela
        interface_hud.imagem(shader_hud.shaderId, posicao_x_j1, posicao_y_j1, tamanho_avatar, tamanho_avatar, textura_naruto.id)

        barra_x_j1 = posicao_x_j1
        barra_y_vida_j1 = posicao_y_j1 + tamanho_avatar + espaco_entre_barras
        barra_y_chakra_j1 = barra_y_vida_j1 + altura_barra + espaco_entre_barras

        interface_hud.ret(shader_hud.shaderId, barra_x_j1, barra_y_vida_j1, largura_barra, altura_barra, (0.15, 0.15, 0.15, 0.9))
        interface_hud.ret(shader_hud.shaderId, barra_x_j1, barra_y_vida_j1, largura_barra * (vida_jogadores[0]/VIDA_MAXIMA), altura_barra, (0.2, 0.8, 0.2, 1.0))

        interface_hud.ret(shader_hud.shaderId, barra_x_j1, barra_y_chakra_j1, largura_barra, altura_barra, (0.15, 0.15, 0.15, 0.9))
        interface_hud.ret(shader_hud.shaderId, barra_x_j1, barra_y_chakra_j1, largura_barra * (chakra_jogadores[0]/CHAKRA_MAXIMO), altura_barra, (0.15, 0.5, 0.9, 1.0))

        posicao_x_j2 = largura_tela - margem_tela - tamanho_avatar
        posicao_y_j2 = altura_tela - margem_tela - tamanho_avatar
        interface_hud.imagem(shader_hud.shaderId, posicao_x_j2, posicao_y_j2, tamanho_avatar, tamanho_avatar, textura_sasuke.id)

        barra_x_j2 = posicao_x_j2 - (largura_barra - tamanho_avatar)   
        barra_y_vida_j2 = posicao_y_j2 - altura_barra - espaco_entre_barras
        barra_y_chakra_j2 = barra_y_vida_j2 - altura_barra - espaco_entre_barras

        interface_hud.ret(shader_hud.shaderId, barra_x_j2, barra_y_vida_j2, largura_barra, altura_barra, (0.15, 0.15, 0.15, 0.9))
        interface_hud.ret(shader_hud.shaderId, barra_x_j2, barra_y_vida_j2, largura_barra * (vida_jogadores[1]/VIDA_MAXIMA), altura_barra, (0.2, 0.8, 0.2, 1.0))

        interface_hud.ret(shader_hud.shaderId, barra_x_j2, barra_y_chakra_j2, largura_barra, altura_barra, (0.15, 0.15, 0.15, 0.9))
        interface_hud.ret(shader_hud.shaderId, barra_x_j2, barra_y_chakra_j2, largura_barra * (chakra_jogadores[1]/CHAKRA_MAXIMO), altura_barra, (0.15, 0.5, 0.9, 1.0))

        COR_AMARELA = (1.0, 0.85, 0.0, 1.0)
        if turno_atual[0] == 0:
            interface_hud.borda(shader_hud.shaderId, posicao_x_j1 - tamanho_borda, posicao_y_j1 - tamanho_borda, 
                                tamanho_avatar + tamanho_borda*2, tamanho_avatar + tamanho_borda*2, tamanho_borda, COR_AMARELA)
        else:
            interface_hud.borda(shader_hud.shaderId, posicao_x_j2 - tamanho_borda, posicao_y_j2 - tamanho_borda, 
                                tamanho_avatar + tamanho_borda*2, tamanho_avatar + tamanho_borda*2, tamanho_borda, COR_AMARELA)

        if vida_jogadores[0] <= 0 or vida_jogadores[1] <= 0:
            textura_vencedor = textura_sasuke if vida_jogadores[0] <= 0 else textura_naruto

            tamanho_vitoria = 400
            x_vitoria = (largura_tela - tamanho_vitoria) / 2
            y_vitoria = (altura_tela - tamanho_vitoria) / 2

            interface_hud.ret(shader_hud.shaderId, x_vitoria - 20, y_vitoria - 20,
                              tamanho_vitoria + 40, tamanho_vitoria + 40, (0.0, 0.0, 0.0, 0.7))

            brilho = abs(math.sin(glfw.get_time() * 3.0))
            interface_hud.borda(shader_hud.shaderId, x_vitoria - 20, y_vitoria - 20,
                                tamanho_vitoria + 40, tamanho_vitoria + 40, 8,
                                (1.0, 0.85, 0.0, brilho))

            interface_hud.imagem(shader_hud.shaderId, x_vitoria, y_vitoria,
                                 tamanho_vitoria, tamanho_vitoria, textura_vencedor.id)

        glfw.swap_buffers(janela)

    glfw.terminate()

if __name__ == "__main__":
    main()
