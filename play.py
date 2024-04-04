import pygame
import pygame_menu
import PlayerCreate

def main():
    pygame.init()
    surface = pygame.display.set_mode((800, 550))


    menu = pygame_menu.Menu('Welcome', 800, 550, theme=pygame_menu.themes.THEME_BLUE)



    menu.add.button('New Game', PlayerCreate.main)
    menu.add.button('Quit', pygame_menu.events.EXIT)


    menu.mainloop(surface)
    pass



if __name__ == "__main__":
    main()