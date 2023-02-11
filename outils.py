import pygame
import random
import string
import json
import time


class Puzzle():

    def __init__(self, x, y, police):
        self.position = {'x': 0, 'y': 0}
        self.contenu, (self.position['x']), (self.position['y']) = gen_plateau(x,y, police)
        self.nbr_coups = 0
    
    def affichage(self, surface):

        #Affichage du puzzle
        for i,ligne in enumerate(self.contenu):
            for j,case in enumerate(ligne):

                if case != 0:
                    case.affichage(surface, 25+j*80, 25+i*80)
                    
        x = self.position['x']
        y = self.position['y']

        touche = pygame.key.get_pressed()
        action = False

        #Deplacement avec les fleches
        if touche[pygame.K_RIGHT]:
            action = True
            self.contenu, self.position['x'], self.position['y'] = deplacer(self.contenu, x, y, 'Droite')

        if touche[pygame.K_LEFT]:
            action = True
            self.contenu, self.position['x'], self.position['y']= deplacer(self.contenu, x, y, 'Gauche')

        if touche[pygame.K_UP]:
            action = True
            self.contenu, self.position['x'], self.position['y'] = deplacer(self.contenu, x, y, 'Haut')           

        if touche[pygame.K_DOWN]:
            action = True
            self.contenu, self.position['x'], self.position['y'] = deplacer(self.contenu, x, y, 'Bas')

        
        if action:
            time.sleep(.2)

            if self.position['x'] != x or self.position['y'] != y:
                self.nbr_coups += 1

            action = False
            return victoire(self.contenu)
            
        return False

              
class Piece():

    def __init__(self, num, x, y, police):
        self.num = str(num)
        self.texte = police.render(self.num, 1, 'black')
        self.rect = pygame.Rect(x, y, 70, 70)
        

    def affichage(self, surface, x, y):

        self.rect.x = x
        self.rect.y = y

        pygame.draw.rect(surface, 'blue', self.rect, 2)
        #Affiche le numero au centre de la piece
        surface.blit(self.texte, ((self.rect.x + 35) - self.texte.get_rect().width/2, (self.rect.y + 35) - self.texte.get_rect().height/2))     
        

class Bouton():
    def __init__(self, message, x, y, police):
        self.texte = police.render(message, 1, 'black')
        self.rect = self.texte.get_rect()
        self.rect.topleft = (x, y)
        self.rect.w = self.texte.get_width()+20
        self.rect.h = self.texte.get_height()+20

    #Affiche le bouton retourne True lorsque l'on clique a l'interieur
    def affichage(self, surface):
        
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):

            if (pygame.mouse.get_pressed()[0] == 1):
                action = True

        pygame.draw.rect(surface, 'red', self.rect, 2)
        surface.blit(self.texte, ( self.rect.x+10, self.rect.y+10))

        return action


class Entree():

    def __init__(self, x, y, police):
        self.num = ''
        self.rect = pygame.Rect(x, y, 100, 40)
        self.surface = police.render(self.num, 1, 'black')
        self.rect.h = self.surface.get_height()+20

    #Affiche l'entrée utilisateur permet d'écrire lorsque la souris est a l'interieur
    def affichage(self, surface, police):

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):

            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_BACKSPACE:
                        self.num = self.num[:-1]

                    elif pygame.key.name(event.key) in string.digits:
                        self.num += pygame.key.name(event.key)

                self.surface = police.render(self.num, 1, 'black')
                self.rect.w = max(100 ,self.surface.get_width()+20)
        
        pygame.draw.rect(surface, 'lightblue', self.rect, 2)
        surface.blit(self.surface, (self.rect.x+10, self.rect.y+10))

#Genere le puzzle de taille donné en placant les pieces au hasard, retourne aussi les coordonnés de la case vide
def gen_plateau(x, y, police):

    nombres = []
    for a in range((x*y)):
        nombres += [a]

    plateau = []

    for i in range(x):

        ligne = []

        for j in range(y):

            n = random.choice(nombres)
            nombres.remove(n)

            if n == 0:
                pos_x = i
                pos_y = j
                ligne += [0]
            else:
                ligne += [Piece(n, (250 + i*80), (150 + j*80), police)]
            

        plateau += [ligne]
  

    return (plateau, pos_x, pos_y)

#Deplace la case vide en echangeant la valeur des deux cases correspondant a la direction
def deplacer(plateau, x, y, direction):

    if direction == 'Gauche':
        if y-1 >= 0:
            plateau[x][y] ,plateau[x][y-1] = plateau[x][y-1], plateau[x][y]
            y -= 1

    if direction == 'Droite':
        if y+1 < len(plateau[x]):
            plateau[x][y] ,plateau[x][y+1] = plateau[x][y+1], plateau[x][y]
            y += 1

    if direction == 'Bas':    
        if x+1 < len(plateau):
            plateau[x][y], plateau[x+1][y] = plateau[x+1][y], plateau[x][y]
            x += 1

    if direction == 'Haut':
        if x-1 >= 0:
            plateau[x][y], plateau[x-1][y] = plateau[x-1][y], plateau[x][y]
            x -= 1
    
    return (plateau, x, y)

#Teste si les pieces du puzzle sont dans l'ordre croissant
def victoire(plateau):

    precedent = 0

    for x in range(len(plateau)):
        for y in range(len(plateau[x])):
            
            if plateau[x][y] == 0 :
                continue
            if int(plateau[x][y].num) < precedent:
                return False

            precedent = int(plateau[x][y].num)
    
    return True

#Ajoute le score dans la categorie correspondant a la taille du puzzle
def enregistrer(score,x,y):

    f = open("scores.json", "r+")
    scores = json.load(f)

    if f"{x}:{y}" not in scores:
        scores[f"{x}:{y}"] = []

    if score > 0:
        scores[f"{x}:{y}"].append(score)

    f.seek(0)
    json.dump(scores, f, indent=4)

    f.close()

#Recupere le Meilleur score de la categorie choisie
def recuperer(x,y):

    f = open("scores.json", "r+")
    scores = json.load(f)

    f.close()
    return sorted(scores[f"{x}:{y}"])[0]