import pygame
import random
import PlayerCreate
import button


Name = []
S_Role = []
AI = ['WARRIOR1', 'TANK1']



def main():
    pygame.init()

    clock = pygame.time.Clock()
    fps = 60
    #game window
    bottom_panel = 150
    screen_width = 800
    screen_height = 400 + bottom_panel

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('PSB BATTLE')

    #define game variables
    current_Warrior = 1
    total_Warrior = 6
    action_cooldown =  0
    action_wait_time = 90
    attack = False
    potion = False
    potion_effect = 15
    click = False
    game_over = 0

    #def fonts
    font = pygame.font.SysFont('Times New Roman', 26)

    #def colours
    red = (255, 0, 0)
    green = (0, 255, 0)



    #load images
    #background image
    background_img = pygame.image.load("img/Background/bg.jpeg").convert_alpha()
    #panel image
    panel_img = pygame.image.load("img/Icon/panel.png").convert_alpha()
    #sword image
    sword_img = pygame.image.load("img/Icon/sword.png").convert_alpha()
    #potion image
    potion_img = pygame.image.load("img/Icon/potion.png").convert_alpha()
    #restart image
    restart_img = pygame.image.load("img/Icon/restart.png").convert_alpha()
    #win or lose image
    victory_img = pygame.image.load("img/Icon/victory.png").convert_alpha()
    defeat_img = pygame.image.load("img/Icon/defeat.png").convert_alpha()



    #function for drawing text
    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    #function for drawing background
    def draw_bg():
        screen.blit(background_img, (0, 0))

    #function for drawing panel
    def draw_panel():
        screen.blit(panel_img, (0, screen_height - bottom_panel))
        #draw char stats
        draw_text(f'L:{Char1.rank}{Char1.name} HP:{Char1.hp}', font, red, 20, screen_height - bottom_panel + 10)
        draw_text(f'L:{Char2.rank}{Char2.name} HP:{Char2.hp}', font, red, 20, screen_height - bottom_panel + 60)
        draw_text(f'L:{Char3.rank}{Char3.name} HP:{Char3.hp}', font, red, 200, screen_height - bottom_panel + 10)


        #draw AI stats
        draw_text(f'L:{AI_1.rank}{AI_1.name} HP:{AI_1.hp}', font, red, 420, screen_height - bottom_panel + 10)
        draw_text(f'L:{AI_2.rank}{AI_2.name} HP:{AI_2.hp}', font, red, 420, screen_height - bottom_panel + 60)
        draw_text(f'L:{AI_3.rank}{AI_3.name} HP:{AI_3.hp}', font, red, 600, screen_height - bottom_panel + 10)



    #warrior class
    class warrior():
        def __init__(self, x, y, name, max_hp, atk, rank, exp, potions, role):
            self.name = name 
            self.max_hp = max_hp
            self.hp =  max_hp
            self.atk = atk
            self.df = random.randint(1,10)
            self.rank = rank
            self.exp = exp
            self.start_potions = potions
            self.potions = potions
            self.role = role
            self.alive = True
            self.animation_list = []
            self.frame_index = 0
            self.action = 0 #0: idle 1:attack 2:hurt 3:dead
            self.update_time = pygame.time.get_ticks()
            #load idle img
            temp_list = []
            for i in range (8):
                img = pygame.image.load(f'img/{self.role}/Idle/{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height()*3))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            #load attack img
            temp_list = []
            for i in range (8):
                img = pygame.image.load(f'img/{self.role}/Attack/{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height()*3))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            #load hurt img
            temp_list = []
            for i in range (3):
                img = pygame.image.load(f'img/{self.role}/Hurt/{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height()*3))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            #load dead img
            temp_list = []
            for i in range (10):
                img = pygame.image.load(f'img/{self.role}/Death/{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height()*3))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            self.image = self.animation_list[self.action][self.frame_index]
            self.rect =  self.image.get_rect()
            self.rect.center = (x, y)

        def update(self):
            animation_cooldown = 100
            #handle animation
            #update image
            self.image = self.animation_list[self.action][self.frame_index]
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            
            #reset to the start
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 3:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.idle()


        def idle(self):
            self.action = 0
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()



        def attack(self, target):
            #deal dmg to enemy
            rand_atk = random.randint(0, 15)
            damage = self.atk + rand_atk - target.df + (random.randint(-5,10))
            if damage < 0:
                damage = 0
                target.exp += target.df * 1.5
                target.hp -= damage
                target.hurt()
            elif damage > 10:
                target.exp += target.df * 1.2
                target.hp -= damage
                target.hurt()
                self.exp += damage
            else:
                target.exp += target.df
                target.hp -= damage
                self.exp+= damage
                target.hurt()

            if self.exp > 100:
                self.rank += 1
                self.exp = 0
            
            if target.exp > 100:
                target.rank += 1
                target.exp = 0

            #check if dead
            if target.hp < 1:
                target.hp = 0
                target.alive = False
                target.death()
            #Damage Text
            damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
            damage_text_group.add(damage_text)
            #atk animation
            self.action = 1
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        def hurt(self):
            #hurt animation
            self.action = 2
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        def death(self):
            #hurt animation
            self.action = 3
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        def reset(self):
            self.alive = True
            self.potions = self.start_potions
            self.hp = self.max_hp
            self.frame_index = 0
            self.action = 0
            self.update_time =  pygame.time.get_ticks()



        def draw(self):
            screen.blit(self.image, self.rect)


    class tank():
        def __init__(self, x, y, name, max_hp, atk, rank, exp, potions, role):
            self.name = name 
            self.max_hp = max_hp
            self.hp =  max_hp
            self.atk = atk
            self.df = random.randint(5,15)
            self.rank = rank
            self.exp = exp
            self.start_potions = potions
            self.potions = potions
            self.role = role
            self.alive = True
            self.animation_list = []
            self.frame_index = 0
            self.action = 0 #0:idle 1:attack 2:hurt 3:dead
            self.update_time = pygame.time.get_ticks()
            #load idle img
            temp_list = []
            for i in range(4):
                img = pygame.image.load(f'img/{self.role}/Idle/{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 3.5, img.get_height()*3.5))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            #load attack img
            temp_list = []
            for i in range(10):
                img = pygame.image.load(f'img/{self.role}/Attack/{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 3.5, img.get_height()*3.5))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            #load hurt img
            temp_list = []
            for i in range(7):
                img = pygame.image.load(f'img/{self.role}/Block/{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 3.5, img.get_height()*3.5))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            #load dead img
            temp_list = []
            for i in range(8):
                img = pygame.image.load(f'img/{self.role}/Death/{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 3.5, img.get_height()*3.5))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            self.image = self.animation_list[self.action][self.frame_index]
            self.rect =  self.image.get_rect()
            self.rect.center = (x, y)

        def update(self):
            animation_cooldown = 150
            #handle animation
            #update image
            self.image = self.animation_list[self.action][self.frame_index]
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            
            #reset to the start
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 3:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.idle()
        


        def idle(self):
            self.action = 0
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


        def attack(self, target):
            #deal dmg to enemy
            rand_atk = random.randint(0, 9)
            damage = self.atk + rand_atk - target.df + (random.randint(-5,10))
            if damage < 0:
                damage = 0
                target.exp += target.df * 1.5
                target.hp -= damage
                target.hurt()
            elif damage > 10:
                target.exp += target.df * 1.2
                target.hp -= damage
                target.hurt()
                self.exp += damage
            else:
                target.exp += target.df
                target.hp -= damage
                self.exp+= damage
                target.hurt()
            
            if self.exp > 100:
                self.rank += 1
                self.exp = 0
            
            if target.exp > 100:
                target.rank += 1
                target.exp = 0

            #check if dead
            if target.hp < 1:
                target.hp = 0
                target.alive = False
                target.death()
            damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
            damage_text_group.add(damage_text)

            #atk animation
            self.action = 1
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

            #hurt animation
        def hurt(self):
            self.action = 2
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        def death(self):
            #death animation
            self.action = 3
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        def reset(self):
            self.alive = True
            self.potions = self.start_potions
            self.hp = self.max_hp
            self.frame_index = 0
            self.action = 0
            self.update_time =  pygame.time.get_ticks()


        def draw(self):
            screen.blit(self.image, self.rect)

    class HealthBar():
        def __init__(self, x, y, hp, max_hp):
            self.x = x
            self.y = y
            self.hp = hp
            self.max_hp = max_hp

        def draw(self, hp):
            #update with new health
            self.hp = hp
            #calculate health
            ratio = self.hp / self.max_hp

            pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
            pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))

    class DamageText(pygame.sprite.Sprite):
        def __init__(self, x, y, damage, colour):
            pygame.sprite.Sprite.__init__(self)
            self.image = font.render(damage, True, colour)
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.counter = 0
           

        def update(self):
            #disappear dmg text
            self.rect.y -= 1
            self.counter += 1
            if self.counter > 30:
                self.kill()

    damage_text_group = pygame.sprite.Group()  


    Char = []

    #Character Creation
    #(x,y,name,hp,atk,def,rank,exp,potions,role)
    if S_Role[0][0][0] == 'WARRIOR':
        Char1 = warrior(300, 260, Name[0], 100, 5, 1, 0, 3, S_Role[0][0][0])
        Char.append(Char1)
    else:
        Char1 = tank(300, 260, Name[0], 100, 1, 1, 0, 3, S_Role[0][0][0])
        Char.append(Char1)

    if S_Role[1][0][0] == 'WARRIOR':
        Char2 = warrior(200, 260, Name[1], 100, 5, 1, 0, 3, S_Role[1][0][0])
        Char.append(Char2)
    else:
        Char2 = tank(200, 260, Name[1], 100, 1, 1, 0, 3, S_Role[1][0][0])
        Char.append(Char2)

    if S_Role[2][0][0] == 'WARRIOR':
        Char3 = warrior(100, 260, Name[2], 100, 5, 1, 0, 3, S_Role[2][0][0])
        Char.append(Char3)
    else:
        Char3 = tank(100, 260, Name[2], 100, 1, 1, 0, 3, S_Role[2][0][0])
        Char.append(Char3)


    Char1_health_bar = HealthBar(20, screen_height - bottom_panel + 40, Char1.hp, Char1.max_hp)
    Char2_health_bar = HealthBar(20, screen_height - bottom_panel + 90, Char2.hp, Char2.max_hp)
    Char3_health_bar = HealthBar(220, screen_height - bottom_panel + 40, Char2.hp, Char2.max_hp)

    #AI Creation
    cclass = [warrior, tank]
    AI_list = []
    RandNo_List1 = []
    RandNo_List2 = []
    AI_pos = []


    for count in range(3):

        digit1 = str(random.randint(0,9))
        RandNo_List1.append(digit1)

        digit2 = str(random.randint(0,9))
        RandNo_List2.append(digit2)

        AI_class = random.choice(cclass)
        AI_list.append(AI_class)

    #(x,y,name,hp,atk,def,rank,exp,potions,role)
    if AI_list[0] == warrior:
        AI_1 = warrior(460, 260, 'AI' + RandNo_List1[0] + RandNo_List2[0] , 100, 5, 1, 0, 3, 'Warrior1')
        AI_pos.append(AI_1)
    else:
        AI_1 = tank(460, 260, 'AI' + RandNo_List1[0] + RandNo_List2[0], 100, 1, 1, 0, 3, 'Tank1')
        AI_pos.append(AI_1)

    if AI_list[1] == warrior:
        AI_2 = warrior(600, 260, 'AI' + RandNo_List1[1] + RandNo_List2[1] , 100, 5, 1, 0, 3, 'Warrior1')
        AI_pos.append(AI_2)
    else:
        AI_2 = tank(600, 260, 'AI' + RandNo_List1[1] + RandNo_List2[1], 100, 1, 1, 0, 3, 'Tank1')
        AI_pos.append(AI_2)


    if AI_list[2] == warrior:
        AI_3 = warrior(750, 260, 'AI' + RandNo_List1[2] + RandNo_List2[2] , 100, 5, 1, 0, 3, 'Warrior1')
        AI_pos.append(AI_3)
    else:
        AI_3 = tank(750, 260, 'AI' + RandNo_List1[2] + RandNo_List2[2], 100, 1, 1, 0, 3, 'Tank1')
        AI_pos.append(AI_3)



    AI_1_health_bar = HealthBar(420, screen_height - bottom_panel + 40, AI_1.hp, AI_1.max_hp)
    AI_2_health_bar = HealthBar(420, screen_height - bottom_panel + 90, AI_2.hp, AI_2.max_hp)
    AI_3_health_bar = HealthBar(620, screen_height - bottom_panel + 40, AI_3.hp, AI_3.max_hp)

    #create button
    potion_button = button.Button(screen, 300, screen_height - bottom_panel + 70, potion_img, 64, 64)
    restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)

    
    run = True
    while run:

        clock.tick(fps)

        #draw background
        draw_bg()

        #draw_panel
        draw_panel()
        #Char Health
        Char1_health_bar.draw(Char1.hp)
        Char2_health_bar.draw(Char2.hp)
        Char3_health_bar.draw(Char3.hp)
        #AI Health
        AI_1_health_bar.draw(AI_1.hp)
        AI_2_health_bar.draw(AI_2.hp)
        AI_3_health_bar.draw(AI_3.hp)


        #draw Char
        Char1.update()
        Char1.draw()

        Char2.update()
        Char2.draw()

        Char3.update()
        Char3.draw()

        #draw AI
        AI_1.update()
        AI_1.draw()

        AI_2.update()
        AI_2.draw()

        AI_3.update()
        AI_3.draw()

        #damage text
        damage_text_group.update()
        damage_text_group.draw(screen)


        #reset action
        #control char action
        attack = False
        potion = False
        target = None
        #mouse cursor
        pygame.mouse.set_visible(True)

        pos = pygame.mouse.get_pos()
        for count, AI in enumerate(AI_pos):
            if AI.rect.collidepoint(pos):
                #hide mouse
                pygame.mouse.set_visible(False)
                #show sword
                screen.blit(sword_img, pos)
                if click == True and AI.alive == True:
                    attack = True
                    target = AI_pos[count]

        if potion_button.draw():
            potion = True
       
        



        if game_over == 0:
                #player action
            for count, Player in enumerate(Char):
                if current_Warrior == 1 + count * 2:
                    if Player.alive == True:
                        action_cooldown += 1
                        if action_cooldown >= action_wait_time:
                        #look for player action
                        # #attack
                            if attack == True and target != None:
                                Player.attack(target)
                                current_Warrior += 1
                                action_cooldown = 0
                            if potion == True:
                                if Player.potions > 0:
                                    #check if exceed 100HP
                                    if Player.max_hp - Player.hp > potion_effect:
                                        heal_amount = potion_effect
                                    else:
                                        heal_amount = Player.max_hp - Player.hp
                                    Player.hp += heal_amount
                                    Player.potions -= 1
                                    damage_text = DamageText(Player.rect.centerx, Player.rect.y, str(heal_amount), green)
                                    damage_text_group.add(damage_text)
                                    current_Warrior += 1
                                    action_cooldown = 0


                    else:
                        current_Warrior += 1
            '''if potion_button.draw():
                potion = True
                draw_text(str(Player.potions), font, red, 250, screen_height - bottom_panel + 70)'''

            #AI action
            for count, AI in enumerate(AI_pos):
                if current_Warrior == 2 + count * 2:
                    if AI.alive == True:
                        action_cooldown += 1
                        if action_cooldown >= action_wait_time:
                        #AI heal
                            if (AI.hp / AI.max_hp) < 0.5 and AI.potions > 0:
                                if AI.max_hp - AI.hp > potion_effect:
                                    heal_amount = potion_effect
                                else:
                                    heal_amount = AI.max_hp - AI.hp
                                AI.hp += heal_amount
                                AI.potions -= 1
                                damage_text = DamageText(AI.rect.centerx, AI.rect.y, str(heal_amount), green)
                                damage_text_group.add(damage_text)
                                current_Warrior += 1
                                action_cooldown = 0
                                
                            else:
                                AI.attack(random.choice(Char))
                                current_Warrior += 1
                                action_cooldown = 0

                    else:
                        current_Warrior += 1


            #if all have their turn
            if current_Warrior > total_Warrior:
                current_Warrior = 1

        #check if all Player are dead
        alive_Player = 0
        for Player in Char:
            if Player.alive == True:
                alive_Player += 1
        if alive_Player == 0:
            game_over = -1

        #check if all AI are dead
        alive_AI = 0
        for AI in AI_pos:
            if AI.alive == True:
                alive_AI += 1
        if alive_AI == 0:
            game_over = 1

        #check if game is over
        if game_over != 0:
            if game_over == 1:
                screen.blit(victory_img, (250, 50))

            if game_over == -1:
                screen.blit(defeat_img, (290, 50))
            if restart_button.draw():
                for Player in Char:
                    Player.reset()
                for AI in AI_pos:
                    AI.reset()
                current_Warrior = 1
                action_cooldown
                game_over = 0


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run =  False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            else:
                click = False

            
        pygame.display.update()

    if __name__ == "__main__":
       main()


pygame.quit()