import pygame
from outils import *

pygame.init()

ecran = pygame.display.set_mode((800,600))
tdr = pygame.time.Clock()
police_puzzle = pygame.font.SysFont('Arial', 28)

taiile_x = 3
taiile_y = 3

plateau = Plateau(taiile_x,taiile_y, police_puzzle)
statue_partie = 1


def ecran_menu():
    pass


def ecran_jeu():

    coups = police_puzzle.render(f"Coups : {plateau.nbr_coups}", 1 ,'black')

    if plateau.affichage(ecran):
        print("victoire")
        enregistrer()

    ecran.blit(coups, (625, 55))
                    

def ecran_score():
    pass


en_cours = True
while en_cours:

    tdr.tick(30)
    ecran.fill((255,255,255))

    match statue_partie:
        case 0:
            ecran_menu()
        case 1:
            ecran_jeu()
        case 2:
            ecran_score()

    ecran_jeu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False
    

    pygame.display.update()

pygame.quit()