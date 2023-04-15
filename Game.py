import pygame
from pygame.locals import *
import time
import random
import moviepy.editor as mp
def game_loop():
    pygame.init()
    pygame.mixer.music.load("Sounds/background_music.mp3")
    eat_sound = pygame.mixer.Sound("Sounds/eat_sound.mp3")
    fenetere = pygame.display.set_mode((1280, 720))
    background = pygame.image.load("Images/background.png").convert()
    player1_image = pygame.image.load("Images/player1.png").convert_alpha()
    player2_image = pygame.image.load("Images/player2.png").convert_alpha()
    food = pygame.image.load("Images/food.png").convert_alpha()
    player1_rect = player1_image.get_rect()
    player2_rect = player2_image.get_rect()
    player1_rect.topleft = (200, 200)
    player2_rect.topleft = (600, 400)
    food_rect = food.get_rect()
    score1 = 0
    score2 = 0
    pygame.mixer.music.play(-1)
    RED = (13, 104, 190)
    BLUE = (232, 76, 61)
    score_font = pygame.font.Font("Fonts/font.ttf", 90)
    
    def start_screen():
        pygame.init()
        fenetere = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Start Screen")

        gif = mp.VideoFileClip("Videos/video.mp4").resize((1280, 720))
        gif_duration = gif.duration
        button_img = pygame.image.load("Images/startbtn.png")
        button_rect = button_img.get_rect(center=fenetere.get_rect().center)
        settings_img = pygame.image.load("Images/settings.png")
        settings_rect = settings_img.get_rect(x=30, y=650)
        name_image = pygame.image.load("Images/name.png")


        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        return
                    elif settings_rect.collidepoint(event.pos):
                        # Open a new window for settings
                        settings_window = pygame.display.set_mode((1280, 720))
                        pygame.display.set_caption("Settings")
                        settings_image = pygame.image.load("Images/commands.png")
                        settings_window.blit(settings_image, (0, 0))
                        
                        # Load and display home.png in center of settings_window
                        home_image = pygame.image.load("Images/home.png")
                        home_rect = home_image.get_rect(center=settings_window.get_rect().center)
                        settings_window.blit(home_image, home_rect)
                        pygame.display.update()
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    game_loop()   
                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                    if home_rect.collidepoint(event.pos): 
                                       game_loop()      
                            pygame.display.update()
            current_time = pygame.time.get_ticks() / 2000.0
            gif_frame = gif.get_frame(current_time % gif_duration)
            gif_surface = pygame.surfarray.make_surface(gif_frame.swapaxes(0, 1))
            fenetere.blit(gif_surface, (0, 0))
            fenetere.blit(button_img, button_rect)
            fenetere.blit(settings_img, settings_rect)
            fenetere.blit(name_image, (350,120))
            pygame.display.update()

    start_screen()

    eat_sound = pygame.mixer.Sound('Sounds/eat_sound.mp3')
    winner = None
    while not winner:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        # Player 1 movement
        keys1 = pygame.key.get_pressed()
        if keys1[K_z]:
            player1_rect.move_ip(0, -6)
        if keys1[K_s]:
            player1_rect.move_ip(0, 6)
        if keys1[K_q]:
            player1_rect.move_ip(-6, 0)
        if keys1[K_d]:
            player1_rect.move_ip(6, 0)

        # Player 2 movement
        keys2 = pygame.key.get_pressed()
        if keys2[K_UP]:
            player2_rect.move_ip(0, -6)
        if keys2[K_DOWN]:
            player2_rect.move_ip(0, 6)
        if keys2[K_LEFT]:
            player2_rect.move_ip(-6, 0)
        if keys2[K_RIGHT]:
            player2_rect.move_ip(6, 0)

        # check if player1_rect has gone out of bounds and wrap it around to the opposite side
        if player1_rect.right < 0:
            player1_rect.left = fenetere.get_width()
        elif player1_rect.left > fenetere.get_width():
            player1_rect.right = 0
        elif player1_rect.bottom < 0:
            player1_rect.top = fenetere.get_height()
        elif player1_rect.top > fenetere.get_height():
            player1_rect.bottom = 0

        # check if player2_rect has gone out of bounds and wrap it around to the opposite side
        if player2_rect.right < 0:
            player2_rect.left = fenetere.get_width()
        elif player2_rect.left > fenetere.get_width():
            player2_rect.right = 0
        elif player2_rect.bottom < 0:
            player2_rect.top = fenetere.get_height()
        elif player2_rect.top > fenetere.get_height():
            player2_rect.bottom = 0

        # check if player1_rect or player2_rect collides with food_rect and increment score if they do
        if player1_rect.colliderect(food_rect):
            score1 += 1
            food_rect.x = random.randint(0, fenetere.get_width() - food_rect.width)
            food_rect.y = random.randint(0, fenetere.get_height() - food_rect.height)
            player1_rect.width += 10
            player1_rect.height += 10
            player1_image = pygame.transform.smoothscale(player1_image, (player1_rect.width, player1_rect.height))
            eat_sound.play()

        if player2_rect.colliderect(food_rect):
            score2 += 1
            food_rect.x = random.randint(0, fenetere.get_width() - food_rect.width)
            food_rect.y = random.randint(0, fenetere.get_height() - food_rect.height)
            player2_rect.width += 10
            player2_rect.height += 10
            player2_image = pygame.transform.smoothscale(player2_image, (player2_rect.width, player2_rect.height))
            eat_sound.play()

        # check if either player has won and set the winner variable accordingly
        if score1 >= 7:
            winner = "Player 1"
        elif score2 >= 7:
            winner = "Player 2"

        # Draw the game screen
        fenetere.blit(background, (0, 0))
        fenetere.blit(food, food_rect)
        fenetere.blit(player1_image, player1_rect)
        fenetere.blit(player2_image, player2_rect)


        bar_width1 = score1 * 80 # Increase the multiplication factor to create larger score bars
        bar_width2 = score2 * 80
        pygame.draw.rect(fenetere, RED, pygame.Rect(20, 20, bar_width1, 40))  # Increase the height of the bars to match
        pygame.draw.rect(fenetere, BLUE, pygame.Rect(fenetere.get_width() - 20 - bar_width2, 20, bar_width2, 40))

        # Render the scores
        player1_label = pygame.image.load("Images/label1.png")
        player2_label = pygame.image.load("Images/label2.png")
        
      


        score1_surface = score_font.render(str(score1), True, (13, 104, 190))
        score2_surface = score_font.render(str(score2), True, (232, 76, 61))

        fenetere.blit(player1_label, (50, 80))
        fenetere.blit(player2_label, (fenetere.get_width() - player2_label.get_width() +170, 80))

        fenetere.blit(score1_surface, (player1_label.get_width() + 150, 80))
        fenetere.blit(score2_surface, (fenetere.get_width() - score2_surface.get_width() - player2_label.get_width() -150, 80))

        pygame.display.update()
        
        if winner:
            while True:
                for event in pygame.event.get():
                    restart_screen()
        time.sleep(0.01) # add a delay of

        def restart_screen():
            score_font = pygame.font.Font("Fonts/font.ttf", 60)
            winner_text = score_font.render(f"{winner} wins!", True, RED)
            winner_rect = winner_text.get_rect(center=fenetere.get_rect().center)
            fenetere.blit(winner_text, winner_rect)

            # Play music
            pygame.mixer.music.load("Sounds/Winnermusic.mp3")
            pygame.mixer.music.play()

            button_img = pygame.image.load("Images/restart.png")
            button_rect = button_img.get_rect(center=(fenetere.get_width() // 2, fenetere.get_height() * 3 // 4))

            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                            game_loop()
                    fenetere.blit(button_img, button_rect)
                    pygame.display.update()

game_loop()
pygame.quit()
