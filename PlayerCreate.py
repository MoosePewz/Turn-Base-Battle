import pygame
import pygame_menu
import play
import PSB_Game




Roles = [['WARRIOR'], ['TANK']]



   
def get_name(name):
    PSB_Game.Name.append(name)
    print("my name is", name)
    print(PSB_Game.Name)
def get_role(role):
    PSB_Game.S_Role.append(role)
    print('role is',role)
    print(PSB_Game.S_Role)





def main():
    pygame.init()
    surface = pygame.display.set_mode((800, 550))


    menu = pygame_menu.Menu('Welcome', 800, 550, theme=pygame_menu.themes.THEME_BLUE)



    menu.add.text_input('Character 1 Name:', onreturn= get_name)
    menu.add.dropselect('Role:', Roles, onchange= get_role)
    menu.add.text_input('Character 2 Name:', onreturn= get_name)
    menu.add.dropselect('Role:', Roles, onchange= get_role)
    menu.add.text_input('Character 3 Name:', onreturn= get_name)
    menu.add.dropselect('Role:', Roles, onchange= get_role)
    menu.add.button('Start', PSB_Game.main)
    menu.add.button('Back', play.main)

    



    menu.mainloop(surface)
    pass
    




if __name__ == "__main__":
    main()