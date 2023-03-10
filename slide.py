import pygame
from outils import *

pygame.init()

ecran = pygame.display.set_mode((800,600))
pygame.display.set_caption("Slide Puzzle")
tdr = pygame.time.Clock()
police_puzzle = pygame.font.SysFont('Arial', 28)

taiile_x = Entree(275, 280, police_puzzle)
taiile_y = Entree(425, 280, police_puzzle)
lbl_x = police_puzzle.render('Lignes', 1, 'black')
lbl_y = police_puzzle.render('Colonnes', 1, 'black')

statut_partie = 0


def ecran_menu():

    global statut_partie, puzzle
    
    taiile_x.affichage(ecran, police_puzzle)
    taiile_y.affichage(ecran, police_puzzle)

    ecran.blit(lbl_x, (275,240))
    ecran.blit(lbl_y, (425,240))

    if Bouton("COMMENCER", 315, 350, police_puzzle).affichage(ecran):

        x = int(taiile_x.num)
        y = int(taiile_y.num)

        #Demarre la partie si la largeur et la longueur du puzzle sont entre 2 et 7
        if (2 <= x <= 7) and (2 <= y <= 7):

            puzzle = Puzzle(x, y, police_puzzle)
            statut_partie = 1


def ecran_jeu():
    global statut_partie

    coups = police_puzzle.render(f"Coups : {puzzle.nbr_coups}", 1 ,'black')

    if puzzle.affichage(ecran):
        enregistrer(puzzle.nbr_coups, taiile_x.num, taiile_y.num)
        statut_partie = 2

    ecran.blit(coups, (625, 55))
                    
#Affiche le score de la partie et le meilleur score du puzzle joué
def ecran_score():
    global statut_partie

    if Bouton("Retour Menu", 600, 500, police_puzzle).affichage(ecran):
        statut_partie = 0

    lbl_score = police_puzzle.render(f"Puzzle completé en: {puzzle.nbr_coups} coups", 1, 'black')
    lbl_meilleur_score = police_puzzle.render(f"Meilleur score : {recuperer(taiile_x.num, taiile_y.num)} coups", 1, "black")
    ecran.blit(lbl_score,(250,200))
    ecran.blit(lbl_meilleur_score,(250, 300))


en_cours = True
while en_cours:

    tdr.tick(30)
    ecran.fill((255,255,255))

    match statut_partie:
        case 0:
            ecran_menu()
        case 1:
            ecran_jeu()
        case 2:
            ecran_score()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False
    

    pygame.display.update()

pygame.quit()