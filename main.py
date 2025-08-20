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




