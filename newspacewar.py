#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os
import time
import math
import random
import pygame
from pygame.locals import * 
import heapq
import tkinter as tk


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


explosion_sound = pygame.mixer.Sound("explosion.wav")
laser_sound = pygame.mixer.Sound("laser.wav")
hyperspace_sound = pygame.mixer.Sound("hyperspace.wav")

font = pygame.font.SysFont(None, 24)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space War")


player_img = pygame.image.load("player.svg")
enemy_img = pygame.image.load("enemy.svg")
bullet_img = pygame.image.load("bullet2.svg")
background_img = pygame.image.load("starfield.gif")



class Node:
    def __init__(self, x, y, walkable):
        self.x = x
        self.y = y
        self.walkable = walkable
        self.g_score = float('inf')
        self.h_score = 0
        self.f_score = float('inf')
        self.parent = None      
    
       
############################

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
#######################################################################

class Player(Sprite):
    def __init__(self, image, x, y):
        super().__init__(pygame.transform.scale(image, (50, 50)), x, y)
        self.speed = 0
        self.score = 0
        self.lives = 5
        self.angle = 0
        self.original_image = pygame.transform.scale(image, (50, 50))

    def turn_left(self):
        self.angle += 45
        self.rotate_player()

    def turn_right(self):
        self.angle -= 45
        self.rotate_player()

    def accelerate(self):
        self.speed += 2

    def decelerate(self):
        self.speed -= 1

    def hyperspace(self):
        hyperspace_sound.play()
        self.rect.x = random.randint(0, SCREEN_WIDTH)
        self.rect.y = random.randint(0, SCREEN_HEIGHT)
        self.speed *= 0.5

    def rotate_player(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)

    def get_angle(self):
        return self.angle

###############
class Enemy(Sprite):
    def __init__(self, image, x, y):
        super().__init__(pygame.transform.scale(image, (50, 50)), x, y)
        self.speed = 1
        self.angle = random.randint(0, 360)  # Random initial angle
        self.shoot_timer = 0
        self.shoot_interval = 60  
        

    def update(self):
       
        self.rect.x += self.speed * -math.sin(math.radians(self.angle))
        self.rect.y += self.speed * -math.cos(math.radians(self.angle))
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0
            

    def shoot(self):
        bullet = Bullet(bullet_img, self.rect.centerx, self.rect.centery)
        bullet.angle = self.angle
        bullets.add(bullet)


################


class Bullet(Sprite):
    def __init__(self, image, x, y):
        super().__init__(pygame.transform.scale(image, (10, 30)), x, y)
        self.speed = 20
        self.angle = 0

    def update(self):
        # Calculate movement based on player's rotation
        self.rect.x += self.speed * -math.sin(math.radians(self.angle))
        self.rect.y += self.speed * -math.cos(math.radians(self.angle))
        # Keep bullet size constant
        self.rect.width = 10
        self.rect.height = 30
    def rotate_bullet(self, player_angle):
        self.angle = player_angle
        
        
#########################
class Game():
    def __init__(self):
        self.state = "splash"
        self.clock = pygame.time.Clock()
        self.level = 1
        self.lives = 3
        self.score = 0

   
    def show_status(self):
        #"""Displays the current game status."""
        font = pygame.font.Font(None, 24)
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        lives_text = font.render(f"Lives: {self.lives}", True, WHITE)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(level_text, (10, 10))
        screen.blit(lives_text, (10, 30))
        screen.blit(score_text, (10, 50))

##################################

# Define the dimensions of the game area
GAME_WIDTH = 600
GAME_HEIGHT = 500

def draw_game_interface():
    
    # Draw game area border
        pygame.draw.rect(screen, WHITE, (100, 50, GAME_WIDTH, GAME_HEIGHT), 3)
    
    
###################################
###########################################################




#############################
def game_over_screen():
    screen.fill((0, 0, 0))
    font_large = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 24)
    game_over_text = font_large.render("Game Over", True, RED)
    restart_text = font_small.render("Press R to restart", True, WHITE)
    quit_text = font_small.render("Press Q to quit", True, WHITE)

    
    game_over_x = SCREEN_WIDTH // 2 - game_over_text.get_width() // 2
    game_over_y = SCREEN_HEIGHT // 4 - game_over_text.get_height() // 2

   
    restart_x = SCREEN_WIDTH // 2 - restart_text.get_width() // 2
    restart_y = SCREEN_HEIGHT // 2 - restart_text.get_height() // 2

   
    quit_x = SCREEN_WIDTH // 2 - quit_text.get_width() // 2
    quit_y = SCREEN_HEIGHT // 2 + restart_text.get_height()

    
    screen.blit(game_over_text, (game_over_x, game_over_y))
    screen.blit(restart_text, (restart_x, restart_y))
    screen.blit(quit_text, (quit_x, quit_y))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_r:
                    return True  # Restart the game
                elif event.key == K_q:
                    pygame.quit()
                    exit()  # Quit the game

########################################3

game = Game()


draw_game_interface()


game.show_status()


player = Player(player_img, GAME_WIDTH, GAME_HEIGHT)


enemies = pygame.sprite.Group()
for _ in range(10):
    enemy = Enemy(enemy_img, random.randint(0, GAME_WIDTH), random.randint(0, GAME_HEIGHT))
    enemies.add(enemy)


bullets = pygame.sprite.Group()





#################################################################################################################
##################################################################################################################
def main():
    
    
    running = True
    game_over = False
    


    while running and not game_over: 
        screen.fill(BLACK)  

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    player.turn_left()
                elif event.key == K_RIGHT:
                    player.turn_right()
                elif event.key == K_UP:
                    player.accelerate()
                elif event.key == K_DOWN:
                    player.decelerate()
                elif event.key == K_SPACE:
                    bullet = Bullet(bullet_img, player.rect.centerx, player.rect.centery)
                    bullet.angle = player.angle
                    bullets.add(bullet)

    
        player.rotate_player()
        player.move(player.speed * -math.sin(math.radians(player.angle)), player.speed * -math.cos(math.radians(player.angle)))

        
        for enemy in enemies:
            enemy.update()
            if random.random() < 0.01:  # Probability of shooting
                enemy.shoot()

        # Update bullets
        bullets.update()

#################Collision detection between player and game borders
        if player.rect.left < 0:
            player.rect.left = 0
        elif player.rect.right > GAME_WIDTH:
            player.rect.right = GAME_WIDTH
        if player.rect.top < 0:
            player.rect.top = 0
        elif player.rect.bottom > GAME_HEIGHT:
            player.rect.bottom = GAME_HEIGHT
                
                
#############Collision detection between bullets and enemies
        enemy_hit = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for enemy in enemy_hit:
           
            new_enemy = Enemy(enemy_img, random.randint(0, GAME_WIDTH), random.randint(0, GAME_HEIGHT))
            enemies.add(new_enemy)
            
            game.score += 100

################# Collision detection between enemies and player
        enemy_player_hit = pygame.sprite.spritecollide(player, enemies, True)
        if enemy_player_hit:
            game.lives -= 1
            if game.lives <= 0:
                game_over = True  

        
        screen.blit(background_img, (0, 0))
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        bullets.draw(screen)

        
        draw_game_interface()
        game.show_status()

        pygame.display.flip()
        game.clock.tick(60)

    if game_over:
        game_over_screen()

        
    pygame.quit()


if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:




