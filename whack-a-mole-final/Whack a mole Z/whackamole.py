import pygame
import sys
import random
import os
import time

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Whack-a-Mole")

# Mole parameters
mole_radius = 100
matrix_size = 3
hole_positions = [
    (i * (width // (matrix_size + 1)), j * (height // (matrix_size + 1)))
    for i in range(1, matrix_size + 1)
    for j in range(1, matrix_size + 1)
]

# Get the absolute path to the assets directory
assets_path = os.path.join(os.getcwd(), 'assets')

# Load background image
background_image = pygame.image.load(os.path.join(assets_path, 'background.png'))
background_image = pygame.transform.scale(background_image, (width, height))

# Load hole image
hole_image = pygame.image.load(os.path.join(assets_path, 'hole.png'))
hole_image = pygame.transform.scale(hole_image, (width // (matrix_size + 1), height // (matrix_size + 1)))

# Load mole images from the assets directory
mole_images = {
    'normal': pygame.image.load(os.path.join(assets_path, 'mole_image.png')),
    'hit': pygame.image.load(os.path.join(assets_path, 'mole_hit_image.png')),
}
mole_images['normal'] = pygame.transform.scale(mole_images['normal'], (2 * mole_radius, 2 * mole_radius))
mole_images['hit'] = pygame.transform.scale(mole_images['hit'], (2 * mole_radius, 2 * mole_radius))

# Load sounds
hit_sound = pygame.mixer.Sound(os.path.join(assets_path, 'hit_sound.wav'))
miss_sound = pygame.mixer.Sound(os.path.join(assets_path, 'miss_sound.wav'))

# Load background music
pygame.mixer.music.load(os.path.join(assets_path, 'background_music.mp3'))
pygame.mixer.music.set_volume(0.5)  # Adjust volume (0.0 to 1.0)

# Game parameters
font = pygame.font.Font(None, 36)
points = 0
hits = 0
misses = 0
game_duration = 74  # 60 seconds
timer_start_time = pygame.time.get_ticks()

# Initialize mole position
mole_x, mole_y = random.choice(hole_positions)
mole_state = 'normal'
mole_start_time = pygame.time.get_ticks()
mole_duration = 2000  # 2 seconds

# Initialize auto-switching timer
auto_switch_time = pygame.time.get_ticks() + 2000  # Set initial auto-switch time (2 seconds)

# Menu parameters
menu_font = pygame.font.Font(None, 50)
menu_text = menu_font.render("Whack-a-Mole", True, (255, 255, 255))
button_width = 250  # Set your desired width
button_height =150  # Set your desired height
play_button = pygame.image.load(os.path.join(assets_path, 'play_button.png'))
play_button = pygame.transform.scale(play_button, (button_width, button_height))

play_button_rect = play_button.get_rect(center=(width // 2, height // 2))

# Game states
# Đặt biến trạng thái trò chơi và biến chờ thoát ở đầu mã
MENU = 'menu'
PLAYING = 'playing'
END_GAME = 'end_game'
game_state = MENU
waiting_for_exit = False

# Define the draw_mole function
def draw_mole(x, y, state='normal'):
    screen.blit(mole_images[state], (x - mole_radius, y - mole_radius))

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_state == MENU and play_button_rect.collidepoint(event.pos):
                game_state = PLAYING
                pygame.mixer.music.play(-1)  # Resume background music
                timer_start_time = pygame.time.get_ticks()  # Reset timer

    if game_state == MENU:
        screen.blit(background_image, (0, 0))
        screen.blit(play_button, play_button_rect)
        screen.blit(menu_text, (width // 2 - menu_text.get_width() // 2, height // 4))
    elif game_state == PLAYING:
        screen.blit(background_image, (0, 0))
        # Draw holes in the matrix
        for hole_position in hole_positions:
            screen.blit(hole_image, (hole_position[0] - width // (matrix_size + 1) // 2, hole_position[1] - height // (matrix_size + 1) // 2))

        # Check if it's time to switch the mole's position
      # Check if it's time to switch the mole's position
        current_time = pygame.time.get_ticks()
        if current_time >= auto_switch_time:
            mole_x, mole_y = random.choice(hole_positions)
            mole_state = 'normal'
            misses += 1  # Increment misses because the mole moved
    
    # Decrease the interval between mole switches over time
            interval_reduction = 250  # Adjust this value based on your preference
            auto_switch_time = current_time + max(500, 2000 - (current_time - timer_start_time) // interval_reduction)


        # Draw the mole if it's within the duration
        if mole_state == 'normal' or (mole_state != 'hit' and current_time - mole_start_time < mole_duration):
            draw_mole(mole_x, mole_y, state=mole_state)

        # Check for mole hit or miss by mouse click
        if mole_state == 'normal' and pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            distance = pygame.math.Vector2(mouse_x - mole_x, mouse_y - mole_y).length()

            if distance < mole_radius:
                points += 1
                hit_sound.play()  # Play hit sound
                mole_state = 'hit'
                hits += 1
                cnt = 0
                while cnt <= 24:
                    cnt += 1
                    draw_mole(mole_x, mole_y, state='hit')
                    points_text = font.render(f"Points: {points}", True, (255, 255, 255))
                    hits_text = font.render(f"Hits: {hits}", True, (255, 255, 255))
                    misses_text = font.render(f"Misses: {misses}", True, (255, 255, 255))
                    timer_text = font.render(f"Time: {max(0, game_duration - (current_time - timer_start_time) // 1000)} s", True, (255, 255, 255))

                    screen.blit(points_text, (10, 10))
                    screen.blit(hits_text, (10, 50))
                    screen.blit(misses_text, (10, 90))
                    screen.blit(timer_text, (width - 150, 10))

                    pygame.display.flip()
                time.sleep(0.1)
                mole_state = 'normal'
                mole_x, mole_y = random.choice(hole_positions)
                mole_start_time = current_time  # Reset the start time for the new mole
                auto_switch_time = current_time + 2000
                continue
            else:
                misses += 1
                miss_sound.play()  # Play miss sound
                time.sleep(0.1)

        # Check for mole state change after hit duration
        if mole_state != 'hit' and current_time - mole_start_time >= mole_duration:
            mole_state = 'normal'
            mole_x, mole_y = random.choice(hole_positions)
            mole_start_time = current_time  # Reset the start time for the new mole
            continue

        # Draw game stats and timer
        points_text = font.render(f"Points: {points}", True, (255, 255, 255))
        hits_text = font.render(f"Hits: {hits}", True, (255, 255, 255))
        misses_text = font.render(f"Misses: {misses}", True, (255, 255, 255))
        timer_text = font.render(f"Time: {max(0, game_duration - (current_time - timer_start_time) // 1000)} s", True, (255, 255, 255))

        screen.blit(points_text, (10, 10))
        screen.blit(hits_text, (10, 50))
        screen.blit(misses_text, (10, 90))
        screen.blit(timer_text, (width - 150, 10))

    pygame.display.flip()
    clock.tick(60)

    # Check for game end
    current_time = pygame.time.get_ticks()
    if current_time - timer_start_time >= game_duration * 1000:
        running = False

# Stop background music when the game ends
pygame.mixer.music.stop()
screen.fill((0, 0, 0))  # Xóa màn hình
end_game_font = pygame.font.Font(None, 50)
end_game_text = end_game_font.render(f"Your Score: {points}", True, (255, 255, 255))
screen.blit(end_game_text, (width // 2 - end_game_text.get_width() // 2, height // 2 - end_game_text.get_height() // 2))
pygame.display.flip()

# Đợi người dùng tắt cửa sổ
waiting_for_exit = True
while waiting_for_exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting_for_exit = False
    
   