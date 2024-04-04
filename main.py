import pygame
import pygame_menu
import play

pygame.init()
surface = pygame.display.set_mode((800, 550))




menu = pygame_menu.Menu('Welcome', 800, 550, theme=pygame_menu.themes.THEME_BLUE)


menu.add.text_input('Name :', default='John Doe')
menu.add.button('Play', play.main)
menu.add.button('Quit', pygame_menu.events.EXIT)


menu.mainloop(surface)
