import pygame, sys, random

pygame.init()
w_width = 512
w_height = 942

screen = pygame.display.set_mode((w_width, w_height))
clock = pygame.time.Clock()
pygame.display.set_caption("PyGame Test")

'''
*****************************  Game variables ****************************
'''
game_active = True
gravity = .25
bird_movement = 0


bg_surface = pygame.image.load('flappy_assets/assets/background-day.png').convert()
#Convert converts file to be best format, helps for consistency
bg_surface = pygame.transform.smoothscale(bg_surface, (w_width, w_height))

floor_surface = pygame.image.load('flappy_assets/assets/base.png').convert()
floor_surface = pygame.transform.smoothscale(floor_surface, (w_width, w_height//5))
floor_x = 0

#Bird import, slightly diff from surface
bird_surface = pygame.image.load('flappy_assets/assets/bluebird-midflap.png').convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center = (w_width//10, w_height//2))

pipe_surface = pygame.image.load('flappy_assets/assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_rect = pipe_surface.get_rect(center = (w_width//8, w_height-1))
pipe_list = []
pipe_height = [400,600,800]

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1400) #ms, 1sec = 1,000ms

def draw_floor():
    screen.blit(floor_surface, (floor_x, w_height-(w_height//8)))
    screen.blit(floor_surface, (floor_x + w_width, w_height-(w_height//8)))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (w_width*2, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (w_width*2, random_pipe_pos-(w_height//3)))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 4
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if(pipe.bottom >= 1024):
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True) #Surface, flipX?, flipY?
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if(bird_rect.colliderect(pipe)):
            return False
        if(bird_rect.top <= -100 or bird_rect.bottom >= w_height-(w_height//8)):
            return False

    return True
            
        
running = True
while running:

    #### Event Handler
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            pygame.quit()
            sys.exit()
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_q):
                pygame.quit()
                sys.exit()
            if (event.key == pygame.K_SPACE and game_active):
                bird_movement = 0
                bird_movement -= 8
            if (event.key == pygame.K_SPACE and game_active==False):
                game_active = True
                pipe_list.clear()
                bird_rect.center = w_width//10, w_height//2
                bird_movement = 0
                
        if (event.type == SPAWNPIPE):
            pipe_list.extend(create_pipe())

    screen.blit(bg_surface,(0,0)) #bg

    #Floor
    floor_x -= 2
    draw_floor()
    if(floor_x <= -w_width):
        floor_x = 0
    screen.blit(floor_surface,(floor_x,w_height-(w_height//8)))

    if(game_active):
        #Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        if(len(pipe_list)>=10):
            pipe_list.pop(0)
            pipe_list.pop(0)
        
        #Bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird_surface, bird_rect)
        game_active = check_collision(pipe_list)
        
        pygame.display.update() #Stops game active
        clock.tick(80)
