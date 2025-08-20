# Import necessary libraries
import math  # For mathematical operations like square root
import random  # For generating random numbers
import pygame  # For game development

# Constants
SCREEN_WIDTH = 800  # Width of the game window
SCREEN_HEIGHT = 500  # Height of the game window
PLAYER_START_X = 370  # Initial X position of the player
PLAYER_START_Y = 380  # Initial Y position of the player
ENEMY_START_Y_MIN = 50  # Minimum Y position for enemy spawn
ENEMY_START_Y_MAX = 150  # Maximum Y position for enemy spawn
ENEMY_SPEED_X = 4  # Horizontal speed of enemies
ENEMY_SPEED_Y = 4  # Vertical speed of enemies
BULLET_SPEED_Y = 10  # Speed of the bullet
COLLISION_DISTANCE = 27  # Distance threshold for collision detection

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Background
background = pygame.image.load('assets/bg.png')  # Load background image

# Caption and Icon
pygame.display.set_caption("Space Invader")  # Set window title
icon = pygame.image.load('assets/ufo.png')  # Load window icon
pygame.display.set_icon(icon)  # Set window icon

# Player
playerImg = pygame.image.load('assets/player.png')  # Load player image
playerX = PLAYER_START_X  # Current X position of player
playerY = PLAYER_START_Y  # Current Y position of player
playerX_change = 0  # Change in player's X position per frame

# Enemy
enemyImg = []  # List to store enemy images
enemyX = []  # List to store enemy X positions
enemyY = []  # List to store enemy Y positions
enemyX_change = []  # List to store enemy X movement values
enemyY_change = []  # List to store enemy Y movement values
num_of_enemies = 6  # Number of enemies in the game

for _ in range(num_of_enemies):
    enemyImg.append(pygame.image.load('assets/enemy.png'))  # Load enemy image
    enemyX.append(random.randint(0, SCREEN_WIDTH - 64))  # Random X position (64 is enemy size)
    enemyY.append(random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX))  # Random Y position
    enemyX_change.append(ENEMY_SPEED_X)  # Set initial X movement speed
    enemyY_change.append(ENEMY_SPEED_Y)  # Set initial Y movement speed

# Bullet
bulletImg = pygame.image.load('assets/bullet.png')  # Load bullet image
bulletX = 0  # Current X position of bullet
bulletY = PLAYER_START_Y  # Current Y position of bullet
bulletX_change = 0  # Change in bullet's X position (not used currently)
bulletY_change = BULLET_SPEED_Y  # Change in bullet's Y position
bullet_state = "ready"  # State of bullet ("ready" or "fire")

# Score
score_value = 0  # Current game score
font = pygame.font.Font('freesansbold.ttf', 32)  # Font for score display
textX = 10  # X position of score text
textY = 10  # Y position of score text

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)  # Font for game over text

def show_score(x, y):
    # Display the current score on the screen.
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))  # Create score text
    screen.blit(score, (x, y))  # Draw score text on screen

def game_over_text():
    # Display the game over text
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))  # Create game over text
    screen.blit(over_text, (200, 250))  # Draw game over text on screen

def player(x, y):
    # Draw the player on the screen
    screen.blit(playerImg, (x, y))  # Draw player image at given coordinates

def enemy(x, y, i):
    # Draw an enemy on the screen
    screen.blit(enemyImg[i], (x, y))  # Draw enemy image at given coordinates

def fire_bullet(x, y):
    # Fire a bullet from the player's position
    global bullet_state  # Access global bullet state variable
    bullet_state = "fire"  # Set bullet state to "fire"
    screen.blit(bulletImg, (x + 16, y + 10))  # Draw bullet slightly offset from player center

def isCollision(enemyX, enemyY, bulletX, bulletY):
    # Check if there is a collision between the enemy and a bullet
    distance = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)  # Calculate distance
    return distance < COLLISION_DISTANCE  # Return True if distance is less than threshold

#Game loop
running = True  # Main game loop control variable

while running:
    screen.fill((0, 0, 0))  # Fill screen with black (background)
    screen.blit(background, (0, 0))  # Draw background image

    for event in pygame.event.get():  # Process all game events
        if event.type == pygame.QUIT:  # If window close button clicked
            running = False  # Exit game loop
        if event.type == pygame.KEYDOWN:  # If key is pressed
            if event.key == pygame.K_LEFT:  # Left arrow key
                playerX_change = -5  # Move player left
            if event.key == pygame.K_RIGHT:  # Right arrow key
                playerX_change = 5  # Move player right
            if event.key == pygame.K_SPACE and bullet_state == "ready":  # Space key to fire
                bulletX = playerX  # Set bullet start position to player position
                fire_bullet(bulletX, bulletY)  # Fire bullet
        if event.type == pygame.KEYUP and event.key in [pygame.K_LEFT, pygame.K_RIGHT]:  # Key released
            playerX_change = 0  # Stop player movement

    # Player Movement
    playerX += playerX_change  # Update player position
    playerX = max(0, min(playerX, SCREEN_WIDTH - 64))  # Keep player within screen bounds (64 is player size)

    # Enemy Movement
    for i in range(num_of_enemies):
        if enemyY[i] > 340:  # Game Over Condition (enemy reached bottom)
            for j in range(num_of_enemies):
                enemyY[j] = 2000  # Move all enemies off-screen
            game_over_text()  # Show game over message
            break  # Exit loop

        enemyX[i] += enemyX_change[i]  # Move enemy horizontally
        if enemyX[i] <= 0 or enemyX[i] >= SCREEN_WIDTH - 64:  # If enemy hits screen edge
            enemyX_change[i] *= -1  # Reverse horizontal direction
            enemyY[i] += enemyY_change[i]  # Move enemy down

        # Collision Check
        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):  # If bullet hits enemy
            bulletY = PLAYER_START_Y  # Reset bullet position
            bullet_state = "ready"  # Reset bullet state
            score_value += 1  # Increase score
            enemyX[i] = random.randint(0, SCREEN_WIDTH - 64)  # Respawn enemy at random X
            enemyY[i] = random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX)  # Respawn enemy at random Y

        enemy(enemyX[i], enemyY[i], i)  # Draw enemy

    # Bullet Movement
    if bulletY <= 0:  # If bullet goes off top of screen
        bulletY = PLAYER_START_Y  # Reset bullet position
        bullet_state = "ready"  # Reset bullet state
    elif bullet_state == "fire":  # If bullet is active
        fire_bullet(bulletX, bulletY)  # Draw bullet
        bulletY -= bulletY_change  # Move bullet upward

    player(playerX, playerY)  # Draw player
    show_score(textX, textY)  # Draw score
    pygame.display.update()  # Update the display





