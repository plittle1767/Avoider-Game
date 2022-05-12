import sys
import pygame

# Starter code for an avoider game. Written by David Johnson for CS 1400 University of Utah.

# Finished game authors: Inder Singh and Preston Little

def pixel_collision(mask1, rect1, mask2, rect2):
    """
    Check if the non-transparent pixels of one contacts the other.
    """
    offset_x = rect2[0] - rect1[0]
    offset_y = rect2[1] - rect1[1]
    # See if the two masks at the offset are overlapping.
    overlap = mask1.overlap(mask2, (offset_x, offset_y))
    return overlap


def ghost_rider_v_mephisto():
    """
    This is our first level. Once we've completed this level, we will automatically jump to the second level. Failing
    starts you back at the beginning of the level.
    """
    level_1 = pygame.image.load("level_1.png")
    # Store window width and height in different forms for easy access
    level_1_size = level_1.get_size()
    level_1_rect = level_1.get_rect()

    # create the window based on the level_1 size
    screen = pygame.display.set_mode(level_1_size)
    level_1 = level_1.convert_alpha()
    level_1.set_colorkey((255, 255, 255))
    level_1_mask = pygame.mask.from_surface(level_1)

    # Create the start button data
    start_button = pygame.image.load("start_button.png").convert_alpha()
    start_button = pygame.transform.smoothscale(start_button, (30, 30))
    start_button_rect = start_button.get_rect()
    start_button_rect.center = (248, 12)
    start_button_mask = pygame.mask.from_surface(start_button)
    pygame.mouse.set_pos(248, 12)

    # Create the GhostRider data
    GhostRider = pygame.image.load("GhostRider.png").convert_alpha()
    GhostRider = pygame.transform.smoothscale(GhostRider, (20, 20))
    GhostRider_rect = GhostRider.get_rect()
    GhostRider_rect.center = (248, 12)
    GhostRider_mask = pygame.mask.from_surface(GhostRider)

    #  Create the fireball data
    fireball = pygame.image.load("fireball.png").convert_alpha()
    fireball = pygame.transform.smoothscale(fireball, (20, 20))
    fireball_rect = fireball.get_rect()
    fireball_rect.center = (26, 257)
    fireball_mask = pygame.mask.from_surface(fireball)

    #  Create the villain data
    mephisto = pygame.image.load("mephisto.png").convert_alpha()
    mephisto = pygame.transform.smoothscale(mephisto, (40, 40))
    mephisto_rect = mephisto.get_rect()
    mephisto_rect.center = (187, 466)
    mephisto_mask = pygame.mask.from_surface(mephisto)

    #  Create the level transition portal
    portal = pygame.image.load("portal.png").convert_alpha()
    portal = pygame.transform.smoothscale(portal, (40, 40))
    portal_rect = portal.get_rect()
    portal_rect.center = (305, 540)
    portal_mask = pygame.mask.from_surface(portal)

    # The frame tells which sprite frame to draw
    frame_count = 0

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # Get a font - there is some problem on my Mac that makes this pause for 10s of seconds sometimes.
    # I will see if I can find a fix.
    myfont = pygame.font.SysFont('comicsans', 14)

    # The started variable records if the start color has been clicked and the level started
    started = False

    # The is_alive variable records if anything bad has happened (off the path, touch guard, etc.)
    is_alive = True

    # This state variable shows whether the fireball is found yet or not
    found_fireball = False

    # Hide the arrow cursor and replace it with a sprite.
    pygame.mouse.set_visible(False)

    # This is the main game loop. In it we must:
    # - check for events
    # - update the scene
    # - draw the scene
    while is_alive:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_alive = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pixel_collision(GhostRider_mask, GhostRider_rect, start_button_mask, start_button_rect):
                    started = True

        # Position the GhostRider to the mouse location
        pos = pygame.mouse.get_pos()
        GhostRider_rect.center = pos
        # print(pos)

        # See if we touch the maze walls
        if pixel_collision(GhostRider_mask, GhostRider_rect, level_1_mask, level_1_rect):
            print("GAME OVER")
            game_over()
            ghost_rider_v_mephisto()
            # is_alive = False

        # See if we touch the villain
        if pixel_collision(GhostRider_mask, GhostRider_rect, mephisto_mask, mephisto_rect):
            print("GAME OVER")
            game_over()
            ghost_rider_v_mephisto()
            # is_alive = False

        # Check if we contact the fireball
        if pixel_collision(GhostRider_mask, GhostRider_rect, fireball_mask, fireball_rect):
            found_fireball = True

        # Draw the background
        screen.fill((250, 250, 250))
        screen.blit(level_1, level_1_rect)

        # Only draw the fireball and mephisto if the fireball is not collected
        if not found_fireball:
            screen.blit(fireball, fireball_rect)
            screen.blit(mephisto, mephisto_rect)

        #  Draw the portal once the fireball is collected
        if found_fireball:
            screen.blit(portal, portal_rect)
            pygame.mask.Mask.clear(mephisto_mask)

        #  When we collide with the portal, we transition to the next level
        if pixel_collision(GhostRider_mask, GhostRider_rect, portal_mask, portal_rect):
            spider_man_v_symbiotes()

        #  Draw the start button
        screen.blit(start_button, start_button_rect)

        # Draw the GhostRider character
        screen.blit(GhostRider, GhostRider_rect)

        # Write some text to the screen. You can do something like this to show some hints or whatever you want.
        label = myfont.render("Collect the fireball clear a path to the exit!", True, (0, 0, 0))
        screen.blit(label, (20, 20))

        # Every time through the loop, increase the frame count.
        frame_count += 1

        #  When the character collides with the portal, load the next level

        # Bring drawn changes to the front
        pygame.display.update()

        # This tries to force the loop to run at 30 fps
        clock.tick(30)

    pygame.quit()
    sys.exit()


def spider_man_v_symbiotes():
    """
    This is our second level. Once we've completed this level, we will automatically jump to the third level. Failing
    starts you back at the beginning of the level.
    """
    level_2 = pygame.image.load("level_2.png")
    # Store window width and height in different forms for easy access
    level_2_size = level_2.get_size()
    level_2_rect = level_2.get_rect()

    # create the window based on the level_2 size
    screen = pygame.display.set_mode(level_2_size)
    level_2 = level_2.convert_alpha()
    level_2.set_colorkey((255, 255, 255))
    level_2_mask = pygame.mask.from_surface(level_2)

    # Create the start button data
    start_button = pygame.image.load("start_button.png").convert_alpha()
    start_button = pygame.transform.smoothscale(start_button, (30, 30))
    start_button_rect = start_button.get_rect()
    start_button_rect.center = (278, 14)
    start_button_mask = pygame.mask.from_surface(start_button)
    pygame.mouse.set_pos(278, 14)

    # Create the spider_man data
    spider_man = pygame.image.load("spider_man.png").convert_alpha()
    spider_man = pygame.transform.smoothscale(spider_man, (20, 20))
    spider_man_rect = spider_man.get_rect()
    spider_man_rect.center = (278, 14)
    spider_man_mask = pygame.mask.from_surface(spider_man)

    #  Create the bell data
    goldBell = pygame.image.load("goldBell.png").convert_alpha()
    goldBell = pygame.transform.smoothscale(goldBell, (20, 20))
    goldBell_rect = goldBell.get_rect()
    goldBell_rect.center = (538, 531)
    goldBell_mask = pygame.mask.from_surface(goldBell)

    #  Create the second bell data
    goldBell2 = pygame.image.load("goldBell.png").convert_alpha()
    goldBell2 = pygame.transform.smoothscale(goldBell2, (20, 20))
    goldBell2_rect = goldBell.get_rect()
    goldBell2_rect.center = (20, 175)
    goldBell2_mask = pygame.mask.from_surface(goldBell2)

    #  Create the villain data
    venom = pygame.image.load("venom.png").convert_alpha()
    venom = pygame.transform.smoothscale(venom, (45, 45))
    venom_rect = venom.get_rect()
    venom_rect.center = (280, 243)
    venom_mask = pygame.mask.from_surface(venom)

    #  Create the second villain data
    carnage = pygame.image.load("carnage.png").convert_alpha()
    carnage = pygame.transform.smoothscale(carnage, (45, 45))
    carnage_rect = carnage.get_rect()
    carnage_rect.center = (244, 461)
    carnage_mask = pygame.mask.from_surface(carnage)

    #  Create the level transition portal
    portal = pygame.image.load("portal.png").convert_alpha()
    portal = pygame.transform.smoothscale(portal, (40, 40))
    portal_rect = portal.get_rect()
    portal_rect.center = (278, 539)
    portal_mask = pygame.mask.from_surface(portal)

    # The frame tells which sprite frame to draw
    frame_count = 0

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # Get a font - there is some problem on my Mac that makes this pause for 10s of seconds sometimes.
    # I will see if I can find a fix.
    myfont = pygame.font.SysFont('comicsans', 14)

    # The started variable records if the start color has been clicked and the level started
    started = False

    # The is_alive variable records if anything bad has happened (off the path, touch guard, etc.)
    is_alive = True

    # This state variable shows whether the gold bell is found yet or not
    found_goldBell = False
    found_goldBell2 = False

    # Hide the arrow cursor and replace it with a sprite.
    pygame.mouse.set_visible(False)

    # This is the main game loop. In it we must:
    # - check for events
    # - update the scene
    # - draw the scene
    while is_alive:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_alive = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pixel_collision(spider_man_mask, spider_man_rect, start_button_mask, start_button_rect):
                    if started:
                        started = True

        # Position the player to the mouse location
        pos = pygame.mouse.get_pos()
        spider_man_rect.center = pos
        # print(pos)

        # See if we touch the maze walls
        if pixel_collision(spider_man_mask, spider_man_rect, level_2_mask, level_2_rect):
            print("GAME OVER")
            game_over()
            spider_man_v_symbiotes()
            # is_alive = False

        # See if we touch the first villain
        if pixel_collision(spider_man_mask, spider_man_rect, venom_mask, venom_rect):
            print("GAME OVER")
            game_over()
            spider_man_v_symbiotes()
            # is_alive = False

        # See if we touch the second villain
        if pixel_collision(spider_man_mask, spider_man_rect, carnage_mask, carnage_rect):
            print("GAME OVER")
            game_over()
            spider_man_v_symbiotes()
            # is_alive = False

        # Check if we contact the bell
        if not found_goldBell and pixel_collision(spider_man_mask, spider_man_rect, goldBell_mask, goldBell_rect):
            found_goldBell = True

        # Check if we contact the second bell
        if not found_goldBell2 and pixel_collision(spider_man_mask, spider_man_rect, goldBell2_mask, goldBell2_rect):
            found_goldBell2 = True

        # Draw the background
        screen.fill((250, 250, 250))
        screen.blit(level_2, level_2_rect)

        # Only draw the gold bell and venom if the gold bell is not collected
        if not found_goldBell:
            screen.blit(goldBell, goldBell_rect)
            screen.blit(venom, venom_rect)

        # Only draw the gold bell and carnage if the second gold bell is not collected
        if not found_goldBell2:
            screen.blit(goldBell2, goldBell2_rect)
            screen.blit(carnage, carnage_rect)

        #  Draw the portal once the second gold bell is collected
        if found_goldBell and found_goldBell2:
            screen.blit(portal, portal_rect)
            pygame.mask.Mask.clear(venom_mask)
            pygame.mask.Mask.clear(carnage_mask)

        #  When we collide with the portal, we transition to the next level
        if pixel_collision(spider_man_mask, spider_man_rect, portal_mask, portal_rect):
            thor_v_destroyer()

        #  Draw the start button
        screen.blit(start_button, start_button_rect)

        # Draw the player character
        screen.blit(spider_man, spider_man_rect)

        # Write some text to the screen. You can do something like this to show some hints or whatever you want.
        label = myfont.render("Collect the gold bells to clear a path to the exit!", True, (255, 0, 0))
        screen.blit(label, (10, 15))

        # Every time through the loop, increase the frame count.
        frame_count += 1

        # Bring drawn changes to the front
        pygame.display.update()

        # This tries to force the loop to run at 30 fps
        clock.tick(30)

    pygame.quit()
    sys.exit()


def thor_v_destroyer():
    """
    This is our third and final level. Once we've completed this level, we will win the game. Failing starts you back at
    the beginning of the level.
    """
    level_3 = pygame.image.load("level_3.png")
    # Store window width and height in different forms for easy access
    level_3_size = level_3.get_size()
    level_3_rect = level_3.get_rect()

    # create the window based on the level_3 size
    screen = pygame.display.set_mode(level_3_size)
    level_3 = level_3.convert_alpha()
    level_3.set_colorkey((255, 255, 255))
    level_3_mask = pygame.mask.from_surface(level_3)

    # Create the start button data
    start_button = pygame.image.load("start_button.png").convert_alpha()
    start_button = pygame.transform.smoothscale(start_button, (30, 30))
    start_button_rect = start_button.get_rect()
    start_button_rect.center = (274, 535)
    start_button_mask = pygame.mask.from_surface(start_button)
    pygame.mouse.set_pos(274, 535)

    # Create the GhostRider data
    thor = pygame.image.load("thor.png").convert_alpha()
    thor = pygame.transform.smoothscale(thor, (20, 20))
    thor_rect = thor.get_rect()
    thor_rect.center = (248, 12)
    thor_mask = pygame.mask.from_surface(thor)

    #  Create the thors_hammer data
    thors_hammer = pygame.image.load("thors_hammer.png").convert_alpha()
    thors_hammer = pygame.transform.smoothscale(thors_hammer, (30, 30))
    thors_hammer_rect = thors_hammer.get_rect()
    thors_hammer_rect.center = (94, 105)
    thors_hammer_mask = pygame.mask.from_surface(thors_hammer)

    #  Create the villain data
    destroyer = pygame.image.load("destroyer.png").convert_alpha()
    destroyer = pygame.transform.smoothscale(destroyer, (40, 40))
    destroyer_rect = destroyer.get_rect()
    destroyer_rect.center = (400, 200)
    destoyer_mask = pygame.mask.from_surface(destroyer)

    #  Create the level transition bridge
    bridge = pygame.image.load("Bridge.png").convert_alpha()
    bridge = pygame.transform.smoothscale(bridge, (40, 40))
    bridge_rect = bridge.get_rect()
    bridge_rect.center = (275, 23)
    bridge_mask = pygame.mask.from_surface(bridge)

    # The frame tells which sprite frame to draw
    frame_count = 0

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # Get a font
    myfont = pygame.font.SysFont('monospace', 14)

    # The started variable records if the start color has been clicked and the level started
    started = False

    # The is_alive variable records if anything bad has happened (off the path, touch guard, etc.)
    is_alive = True

    # This state variable shows whether the thors_hammer is found yet or not
    found_thors_hammer = False

    # Hide the arrow cursor and replace it with a sprite.
    pygame.mouse.set_visible(False)

    # This is the main game loop. In it we must:
    # - check for events
    # - update the scene
    # - draw the scene
    while is_alive:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pixel_collision(thor_mask, thor_rect, start_button_mask, start_button_rect):
                    if started:
                        started = True

        # Position Thor to the mouse location
        pos = pygame.mouse.get_pos()
        thor_rect.center = pos
        print(pos)

        # See if we touch the maze walls
        if pixel_collision(thor_mask, thor_rect, level_3_mask, level_3_rect):
            print("GAME OVER")
            game_over()
            thor_v_destroyer()
            # is_alive = False

        # If thor touches the villain game over
        if pixel_collision(thor_mask, thor_rect, destoyer_mask, destroyer_rect):
            print("GAME OVER")
            game_over()
            thor_v_destroyer()
            # is_alive = False

        # Check if we contact with thors_hammer
        if not found_thors_hammer and pixel_collision(thor_mask, thor_rect, thors_hammer_mask, thors_hammer_rect):
            found_thors_hammer = True

        # Draw the background
        screen.fill((250, 250, 250))
        screen.blit(level_3, level_3_rect)

        # Only draw the hammer and Destroyer if the thors_hammer is not collected
        if not found_thors_hammer:
            screen.blit(thors_hammer, thors_hammer_rect)
            screen.blit(destroyer, destroyer_rect)

        #  Draw the bridge once the hammer is collected
        if found_thors_hammer:
            screen.blit(bridge, bridge_rect)
            pygame.mask.Mask.clear(destoyer_mask)

        #  When the character collides with the bridge, the game is over and they've won
        if pixel_collision(thor_mask, thor_rect, bridge_mask, bridge_rect):
            winner_screen()

        #  Draw the start button
        screen.blit(start_button, start_button_rect)

        # Draw the Thor character
        screen.blit(thor, thor_rect)

        # Write some text to the screen. You can do something like this to show some hints or whatever you want.
        label = myfont.render("Collect the hammer to clear a path to the exit!", True, (0, 0, 0))
        screen.blit(label, (20, 20))

        # Every time through the loop, increase the frame count.
        frame_count += 1

        # Bring drawn changes to the front
        pygame.display.update()

        # This tries to force the loop to run at 30 fps
        clock.tick(30)

    pygame.quit()
    sys.exit()


def game_over():
    """
    This function displays game over when you collide with a wall or a villain.
    """
    gameover = pygame.image.load("game_over.png")
    # Store window width and height in different forms for easy access
    gameover_size = gameover.get_size()
    gameover_rect = gameover.get_rect()

    # create the window based on the gameover size
    screen = pygame.display.set_mode(gameover_size)
    gameover = gameover.convert_alpha()
    gameover.set_colorkey((255, 255, 255))
    gameover_mask = pygame.mask.from_surface(gameover)

    # Draw the background
    screen.fill((250, 250, 250))
    screen.blit(gameover, gameover_rect)

    # Bring drawn changes to the front
    pygame.display.update()


def winner_screen():
    """
    This function displays the screen telling you that you've won the game.
    """
    winner = pygame.image.load("winner.png")
    # Store window width and height in different forms for easy access
    winner_size = winner.get_size()
    winner_rect = winner.get_rect()

    # create the window based on the winner size
    screen = pygame.display.set_mode(winner_size)
    winner = winner.convert_alpha()
    winner.set_colorkey((255, 255, 255))
    winner_mask = pygame.mask.from_surface(winner)

    # Draw the background
    screen.fill((250, 250, 250))
    screen.blit(winner, winner_rect)

    # Bring drawn changes to the front
    pygame.display.update()


def main():
    # Initialize pygame
    pygame.init()
    ghost_rider_v_mephisto()


# Start the program
main()
