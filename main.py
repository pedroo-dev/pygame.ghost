# # Executavel
# #pip install pyinstaller
# pyinstaller -F main.py
# pyinstaller main.spec
import os, sys

dirpath = os.getcwd()
sys.path.append(dirpath)

if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)


# 1. IMPORT ------------------------------------------------------------------------

import random
import pygame
# Importando o módulo de Sistema para finalizar o jogo corretamente
from sys import exit
from ghost import Ghost
from bat import Bat
from shoot import Shoot


# 2. INICIALIZAÇÃO -----------------------------------------------------------------

# Inicialização do pygame dentro do meu módulo
pygame.init()

# Criar uma janela com uma configuração (resolução) de 840x480
WIDTH_SCREEN = 840  # Largura
HEIGHT_SCREEN = 480  # Altura

display = pygame.display.set_mode([WIDTH_SCREEN, HEIGHT_SCREEN])

# Mudar o títlo da janela
pygame.display.set_caption("SENAI Jogos")

# Carregando a imagem para criar o icone
icone = pygame.image.load("data/icone.png")

# Converter a imagem para o formato de ícone
pygame.display.set_icon(icone)


# 3.1 ELEMENTOS DE TELA ------------------------------------------------------------

# Criando um grupo de imagens para carregar na tela todos de uma unica vez
objectGroup = pygame.sprite.Group()
batGroup = pygame.sprite.Group()
shootGroup = pygame.sprite.Group()

# Background
bg = pygame.sprite.Sprite(objectGroup)
bg.image = pygame.image.load("data/background.jpg")
bg.image = pygame.transform.scale(bg.image, [840, 480])
bg.rect = bg.image.get_rect()


# Criar o objeto Ghost
ghost = Ghost(objectGroup)


# 3.2 Música -----------------------------------------------------------------------

# pygame.mixer.music.load("data/alienblues.wav")
# pygame.mixer.music.play(-1)


# 3.3 Som --------------------------------------------------------------------------

# attack = pygame.mixer.Sound("data/magic1.wav")

# 3.4 Fonte -------------------------------------------------------------------------
score_font = pygame.font.Font("font/Pixeltype.ttf", 50)

# 4. VARIAVEIS GLOBAIS -------------------------------------------------------------

# variavel para controlar o loop
gameLoop = True
gameOver = False

timer = 20
Pontos = 0

# Criando uma variavel de tempo para ajustar os frames por segundo (FPS)
clock = pygame.time.Clock()


# 5. GAME LOOP ---------------------------------------------------------------------

def main():
    global timer
    global gameLoop
    global gameOver
    global Pontos
    # Criando nosso Game Loop
    while gameLoop:
        clock.tick(60)
        # Criando nosso Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # O evento QUIT é usando para clicar no X da tela
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not gameOver:
                    # attack.play()
                    newShoot = Shoot(objectGroup, shootGroup)
                    newShoot.rect.center = ghost.rect.center

        if not gameOver:
            # # Colocar a cor de fundo da janela
            # display.fill([252, 165, 3])

            # Criar varios morcegos
            timer += 1
            if timer > 30:
                timer = 0
                if random.random() < 0.3:
                    newBat = Bat(objectGroup, batGroup)

                # Colisão
                collisions = pygame.sprite.spritecollide(ghost,
                                                         batGroup,
                                                         False,
                                                         pygame.sprite.collide_mask
                                                         )
                if collisions:
                    print("GAME OVER !!!")
                    gameOver = True

                tiros = pygame.sprite.groupcollide(shootGroup,
                                                   batGroup,
                                                   True,
                                                   True,
                                                   pygame.sprite.collide_mask
                                                   )

                if tiros:
                    Pontos += 1

            # Atualizar a posicao dos meu objetos
            objectGroup.update()

        # Desenhando os elementos do Grupo no Display
        objectGroup.draw(display)

        # Inserindo a pontuação na tela
        score_render = score_font.render(f'Score: {Pontos}', False, '  White')
        display.blit(score_render, (650, 50))

        # Continuo desenhando os elementos na tela
        pygame.display.update()


if __name__ == "__main__":
    main()
