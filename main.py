import pygame
from sys import exit
from random import randint

def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 100 
    text_surface = text_font.render(f'Score : {current_time}',False,"Black")
    text_rect = text_surface.get_rect(midbottom = (400,50))
    screen.blit(text_surface,text_rect)
    return current_time

def obstacle_movement(rect_list):
    if rect_list:
        for obstacle_rect in rect_list:
            obstacle_rect.x-=7
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface,obstacle_rect)
            else:
                screen.blit(fly_surface,obstacle_rect)
        rect_list = [rect for rect in rect_list if rect.x > -100]
        return rect_list
    else:
        return []

def collisons(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def player_animation():
    global player_index,player_surface
    if player_rect.bottom < 300:
        player_surface = player_jump
    else:
        player_index+=0.1
        if player_index >= len(players):
            player_index = 0
        player_surface = players[int(player_index)]


pygame.init()

screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
text_font = pygame.font.Font("./font/Pixeltype.ttf",50)

#background
sky_surface = pygame.image.load("./graphics/Sky.png").convert()
ground_surface = pygame.image.load("./graphics/ground.png").convert()

#villians
snail_1 = pygame.image.load("./graphics/snail/snail1.png").convert_alpha()
snail_2 = pygame.image.load("./graphics/snail/snail2.png").convert_alpha()
snails = [snail_1,snail_2]
snail_index = 0
snail_surface = snails[snail_index]

fly_1 = pygame.image.load("./graphics/Fly/Fly1.png").convert_alpha()
fly_2 = pygame.image.load("./graphics/Fly/Fly2.png").convert_alpha()
flys = [fly_1,fly_2]
fly_index = 0
fly_surface = flys[fly_index]

obstacle_rect_list = []

player_jump = pygame.image.load("./graphics/Player/jump.png").convert_alpha()
player_walk1 = pygame.image.load("./graphics/Player/player_walk_1.png").convert_alpha()
player_walk2 = pygame.image.load("./graphics/Player/player_walk_2.png").convert_alpha()
players = [player_walk1,player_walk2]
player_index = 0
player_surface = players[player_index]
player_rect = player_surface.get_rect(midbottom = (80,300))
player_gravity = 0

#for start screen
player_stand = pygame.image.load("./graphics/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))
title_surface = text_font.render("RUNNER",False,"Black")
title_rect = title_surface.get_rect(midbottom = (400,50))
instruction_surface = text_font.render("Press SPACE to start",False,"Black")
instruction_rect = title_surface.get_rect(center = (300,80))

#obstacles timing
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_timer,500)

fly_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_timer,300)

game_active = False
start_time = 0
score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                player_gravity = -25

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
            
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surface.get_rect(midbottom = (randint(900,1200),300)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(midbottom = (randint(900,1200),210)))
            if event.type == snail_timer:
                if snail_index == 0: snail_index = 1
                else: snail_index = 0
                snail_surface = snails[snail_index]

            if event.type == fly_timer:
                if fly_index == 0: fly_index = 1
                else: fly_index = 0
                fly_surface = flys[fly_index]

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = pygame.time.get_ticks()   
        

    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))

        score = display_score()
        
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        player_gravity+=1
        player_rect.y+=player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300 
        player_animation()
        screen.blit(player_surface,player_rect)

        game_active = collisons(player_rect,obstacle_rect_list)

    else:
        screen.fill((93,129,162))
        screen.blit(player_stand,player_stand_rect)
        
        score_surface = text_font.render(f'score : {score}',False,"Black")
        score_rect = score_surface.get_rect(center = (400,80))
        over_surface = text_font.render('GAME OVER',False,"Black")
        over_rect = over_surface.get_rect(midbottom = (400,50))
        if score == 0 :
            screen.blit(title_surface,title_rect)
            screen.blit(instruction_surface,instruction_rect)
        else:
            screen.blit(over_surface,over_rect)
            screen.blit(score_surface,score_rect)
            obstacle_rect_list.clear()
            player_rect.midbottom = (80,300)
            player_gravity = 0


    pygame.display.update()
    clock.tick(60)