import pygame as pg
import sys
import random as rdm

pg.init()

def collisionDetection(rect1,rect2):
    return rect1.colliderect(rect2)

# screen settings
screen_width=800
screen_height=600
screen=pg.display.set_mode((screen_width,screen_height))
pg.display.set_caption("First Shooting Game")

# player settings
screen_width,screen_height=screen.get_size()
player_width=25
player_height=30
player_x=screen_width//2-player_width//2
player_y=screen_height-player_height-10
player_speed=5.25

# bullet settings
bullet_width=2
bullet_height=10
bullet_speed=7
bullets=[]

# enemy settings
enemy_width=25
enemy_height=30
enemy_speed=2.75
enemies=[]
enemy_timer=0
spawn_time=2000

clock=pg.time.Clock()

# game over screen
def game_over_screen(screen):
    font1=pg.font.Font(None,125)
    font2=pg.font.Font(None,25)
    text1=font1.render("Game Over!!!",True,(124,10,2))
    text2=font2.render("Press 'R' to Restart",True,(0,255,0))
    text1_rect=text1.get_rect(center=screen.get_rect().center)
    text2_rect=text2.get_rect(midtop=(text1_rect.centerx,text1_rect.bottom+10))
    screen.blit(text1,text1_rect.topleft)
    screen.blit(text2,text2_rect.bottomleft)
    pg.display.update()
    while True:
        for event in pg.event.get():
            if event.type==pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type==pg.KEYDOWN and event.key==pg.K_r:
                enemies.clear()
                bullets.clear()
                return

running=True

while running:
    for event in pg.event.get():
        if event.type==pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type==pg.KEYDOWN:
                if event.key==pg.K_SPACE:
                    # create bullet
                    bullet_x=player_x+player_width//2-bullet_width//2
                    bullet_y=player_y
                    bullets.append(pg.Rect(bullet_x,bullet_y,bullet_width,bullet_height))

    # player movement
    keys=pg.key.get_pressed()
    if keys[pg.K_LEFT] and player_x>0:
        player_x-=player_speed
    if keys[pg.K_RIGHT] and player_x<screen_width-player_width:
        player_x+=player_speed

    # bullet movement
    for bullet in bullets:
        bullet.y-=bullet_speed
    
    # remove out of screen bullets from list
    bullets=[bullet for bullet in bullets if bullet.y>0]

    # create enemy
    current_time=pg.time.get_ticks()
    if current_time-enemy_timer>spawn_time:
        enemy_x=rdm.randint(0,screen_width-screen_height)
        enemy_y=-enemy_height
        enemies.append(pg.Rect(enemy_x,enemy_y,enemy_width,enemy_height))
        enemy_timer=current_time

    # enemy movement
    for enemy in enemies:
        enemy.y+=enemy_speed
    
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if collisionDetection(bullet,enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                break 
    
    # remove out of screen enemies from list
    enemies=[enemy for enemy in enemies if enemy.y<screen_height] 

    # dead zone
    danger_zone=pg.Rect(0,player_y,screen_width,player_height)

    for enemy in enemies[:]:
        if collisionDetection(enemy,danger_zone):
            game_over_screen(screen)

    # screen color
    screen.fill((0,0,0))

    # draw dead zone
    pg.draw.rect(screen,(124,10,2),danger_zone)

    # drwa player//in this case a rectangle
    pg.draw.rect(screen,(0,128,255),(player_x,player_y,player_width,player_height))

    # draw bullets
    for bullet in bullets:
        pg.draw.rect(screen,(255,255,255),bullet)

    # draw enemy
    for enemy in enemies:
        pg.draw.rect(screen,(100,100,100),enemy)

    # update the screen
    pg.display.flip()

    # fps cap
    clock.tick(60)

#    barn red (124,10,2)
# british green (0,66,37)