#!usr/bin/python3
#-*- coding: UTF-8 -*-

import random
import pygame

'''
Jogo da Vida - Conway
by Daniel Augusto
18/08/2019

# Controles:
R - Randomiza o Tabuleiro
H - Reset
Click Esquerdo - Altera o tile para "vivo" ou "morto"
________________________
|Click Direito - Começar|
------------------------
'''

# Configs
#|-Janela
largura = 800
altura = 600
#|-Tiles
cores = {"morto": (255,255,255), "vivo": (200,200,0), "reset": (0,0,0)}
tilesSize = 10 # !!! Deve ser divisor tanto da largura quanto da altura, simultaneamente para que nao sobre espaços. Sugiro 4 ou mais!
chancesDoModoAleatorio = 40 # porcento
#|-Game
alreadyDraw = False
inGame = False
clock = pygame.time.Clock()
fps = 25 # Aumente para jogar mais rápido e Diminua para jogar mais lentamente.
running = True



pygame.init()
screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Game of Life")


def startGame(): # Executado após as operações iniciais
    findNeiboors()

class tile: # Cada quadrado é um tile
    def __init__(self, x , y):
        self.posX = x*tilesSize
        self.posY = y*tilesSize
        self.tilesConfig = [self.posX, self.posY, tilesSize, tilesSize] # Posição e tamanho
        self.status = False # Vivo(true) ou Morto(False)
        self.rect = None # Elemento do retangulo
        self.neighboors = 0 # Quantidade de Vizinhos
        self.draw()

    ''' Desenhar a cor do quadrado, dependedo do status do tile '''
    def draw(self):
        if self.status:
            self.rect = pygame.draw.rect(screen, cores['vivo'], self.tilesConfig, 0)
        else:
            self.rect = pygame.draw.rect(screen, cores['reset'], self.tilesConfig, 0)
            self.rect = pygame.draw.rect(screen, cores['morto'], self.tilesConfig, 1)

    ''' Define o status apos contar o numero de vizinhos!'''
    def Life_or_Death(self):
        if self.neighboors <= 1 or self.neighboors > 3:
            self.status = False
        elif self.neighboors == 3:
            self.status = True
        self.draw()

# Cria o tabuleiro, gerando uma matriz. Cada elemento da matriz é um objeto da classe tile
def set_board():
    board = []
    for i in range(int(largura/tilesSize)):
        board.append([])
        for j in range(int(altura/tilesSize)):
            board[i].append(tile(i, j))
    return board

# Após cada tile ter sua quantidade de vizinhos setada, esssa função manda redesenha-lo.
def reDraw():
    for x in range(len(board)):
        for y in range(len(board[x])):
            board[x][y].Life_or_Death()

# Encontra o numero de vizinhos que cada tile tem.
def findNeiboors():
    for x in range(len(board)):
        for y in range(len(board[x])):

            # posição dos vizinhos. Ordem: SupEsquerda, Cima, SupDireita, Esqueda, Direita, InfEsquerda, baixo, InfDireita
            neighboor = [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]
            neighboorAlive = 0

            for z in neighboor:
                try: # Caso esteja na borda, os indices sairao da matriz, entao se for indexErro apenas desconsidere, pois nao há vizinho 
                    if board[z[0]][z[1]].status:
                        neighboorAlive += 1
                except IndexError:
                    pass

            # Seta quantos vizinhos essa peça possui
            board[x][y].neighboors = neighboorAlive
    
    reDraw()

while running:
    clock.tick(fps)
    # Cria o tabuleiro apenas uma vez
    if not alreadyDraw:
        alreadyDraw = True
        board = set_board()

    
    for event in pygame.event.get():
        # Sair
        if event.type == pygame.QUIT:
            running = False 
            break
        # Desenhar o primeiros padroes
        if event.type == pygame.MOUSEBUTTONUP and event.button ==1 and not inGame:
            mousePos = pygame.mouse.get_pos()
            for x in range(len(board)):
                for y in range(len(board[x])):
                    ''' Para achar o tile a qual está clicando, pegasse a posição atual do mouse
                    e para cada tile no tabuleiro verifica seus limites, tantos horizontais quanto verticais.
                    Se a posição do mouse estiver, estritamente dentro dos limites, entao muda o status do tile.'''
                    # Extremos
                    posMinX = board[x][y].posX
                    posMinY = board[x][y].posY
                    posMaxX = posMinX+tilesSize
                    posMaxY = posMinY+tilesSize
                    # Conferindo
                    if (posMinX <= mousePos[0] <= posMaxX) and (posMinY <= mousePos[1] <= posMaxY):
                        board[x][y].status = not board[x][y].status
                        board[x][y].draw()
                    
        if event.type == pygame.KEYDOWN:
            # Randomiza o primeiro Padrao
            if event.key == pygame.K_r:
                for x in range(len(board)):
                    for y in range(len(board[x])):
                        chance = [x+1 for x in range(10)]
                        z = random.choice(chance)
                        if z <= chancesDoModoAleatorio/10:
                            board[x][y].status = True
                        else:
                            board[x][y].status = False
                        board[x][y].draw()
            if event.key == pygame.K_h:
                inGame = False
                set_board()
                        
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            inGame = True
    if inGame:
        startGame()

    pygame.display.update()



# Thanks
