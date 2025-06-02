import pygame
import sys
import random
import math
import time
import os

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
MONEY_SIZE = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 205, 50)
RED = (255, 0, 0)
BLUE = (30, 144, 255)
GOLD = (255, 215, 0)
LIGHT_BLUE = (173, 216, 230)
GAME_TIME = 30  # seconds

class MoneyGrabber:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Money Grabber")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Game state
        self.game_active = False
        self.game_over = False
        self.difficulty = "Medium"
        self.player_score = 0
        self.bot_score = 0
        self.start_time = 0
        self.time_left = GAME_TIME

        # Bot settings
        self.bot_speeds = {"Easy": 3, "Medium": 5, "Hard": 7}
        self.bot_reaction_times = {"Easy": 1.5, "Medium": 1.0, "Hard": 0.5}
        self.bot_pos = [WIDTH - 100, HEIGHT // 2]  # List for mutable position
        self.bot_target_time = 0

        # Load images
        self.load_images()

        # Create custom hand cursor
        self.default_cursor = pygame.mouse.get_cursor()
        self.hand_cursor = self.create_hand_cursor()

        # Money position and type
        self.money_pos = (0, 0)
        self.use_coin_image = True
        self.spawn_money()

        # Load sound
        try:
            self.coin_sound = pygame.mixer.Sound("coin.wav") if os.path.exists("coin.wav") else None
        except:
            self.coin_sound = None

    def load_images(self):
        """Load all game images"""
        # Create assets directory if it doesn't exist
        if not os.path.exists("assets"):
            os.makedirs("assets")

        # Define image paths
        coin_path = os.path.join("assets", "coin.png")
        money_path = os.path.join("assets", "money.png")
        player_path = os.path.join("assets", "player.png")
        bot_path = os.path.join("assets", "bot.png")

        # Load or create coin image
        try:
            if os.path.exists(coin_path):
                self.coin_img = pygame.image.load(coin_path).convert_alpha()
                self.coin_img = pygame.transform.scale(self.coin_img, (MONEY_SIZE, MONEY_SIZE))
            else:
                self.coin_img = self.create_default_coin()
        except:
            self.coin_img = self.create_default_coin()

        # Load or create money image
        try:
            if os.path.exists(money_path):
                self.money_img = pygame.image.load(money_path).convert_alpha()
                self.money_img = pygame.transform.scale(self.money_img, (MONEY_SIZE, MONEY_SIZE))
            else:
                self.money_img = self.create_default_money()
        except:
            self.money_img = self.create_default_money()

        # Load or create player image
        try:
            if os.path.exists(player_path):
                self.player_img = pygame.image.load(player_path).convert_alpha()
                self.player_img = pygame.transform.scale(self.player_img, (40, 40))
            else:
                self.player_img = self.create_default_player()
        except:
            self.player_img = self.create_default_player()

        # Load or create bot image
        try:
            if os.path.exists(bot_path):
                self.bot_img = pygame.image.load(bot_path).convert_alpha()
                self.bot_img = pygame.transform.scale(self.bot_img, (40, 40))
            else:
                self.bot_img = self.create_default_bot()
        except:
            self.bot_img = self.create_default_bot()

    def create_default_coin(self):
        """Create a default coin image"""
        coin = pygame.Surface((MONEY_SIZE, MONEY_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(coin, GOLD, (MONEY_SIZE//2, MONEY_SIZE//2), MONEY_SIZE//2)
        dollar_text = self.font.render("$", True, BLACK)
        dollar_rect = dollar_text.get_rect(center=(MONEY_SIZE//2, MONEY_SIZE//2))
        coin.blit(dollar_text, dollar_rect)
        return coin

    def create_default_money(self):
        """Create a default money image"""
        money = pygame.Surface((MONEY_SIZE, MONEY_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(money, GREEN, (0, 0, MONEY_SIZE, MONEY_SIZE//2))
        dollar_text = self.font.render("$$$", True, BLACK)
        dollar_rect = dollar_text.get_rect(center=(MONEY_SIZE//2, MONEY_SIZE//4))
        money.blit(dollar_text, dollar_rect)
        return money

    def create_default_player(self):
        """Create a default player image"""
        player = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(player, BLUE, (20, 20), 20)
        return player

    def create_default_bot(self):
        """Create a default bot image"""
        bot = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(bot, RED, (20, 20), 20)
        pygame.draw.circle(bot, WHITE, (15, 15), 5)
        pygame.draw.circle(bot, WHITE, (25, 15), 5)
        pygame.draw.circle(bot, BLACK, (15, 15), 2)
        pygame.draw.circle(bot, BLACK, (25, 15), 2)
        pygame.draw.arc(bot, WHITE, (10, 20, 20, 10), 0, math.pi, 2)
        return bot

    def create_hand_cursor(self):
        """Create a custom hand cursor for grabbing money"""
        cursor_size = 32
        cursor_surface = pygame.Surface((cursor_size, cursor_size), pygame.SRCALPHA)
        hand_color = (255, 220, 180)  # Skin tone
        pygame.draw.circle(cursor_surface, hand_color, (16, 20), 10)
        pygame.draw.ellipse(cursor_surface, hand_color, (14, 5, 6, 15))
        pygame.draw.ellipse(cursor_surface, hand_color, (20, 6, 6, 14))
        pygame.draw.ellipse(cursor_surface, hand_color, (26, 8, 6, 12))
        pygame.draw.circle(cursor_surface, BLACK, (16, 20), 10, 1)
        pygame.draw.ellipse(cursor_surface, BLACK, (14, 5, 6, 15), 1)
        pygame.draw.ellipse(cursor_surface, BLACK, (20, 6, 6, 14), 1)
        pygame.draw.ellipse(cursor_surface, BLACK, (26, 8, 6, 12), 1)
        hotspot = (16, 20)
        try:
            cursor = pygame.cursors.Cursor(hotspot, cursor_surface)
            return cursor
        except:
            return pygame.mouse.get_cursor()

    def update_cursor(self, mouse_pos):
        """Update cursor based on position"""
        if self.game_active and not self.game_over:
            distance = math.sqrt((mouse_pos[0] - self.money_pos[0])**2 +
                               (mouse_pos[1] - self.money_pos[1])**2)
            if distance <= MONEY_SIZE // 2:
                try:
                    pygame.mouse.set_cursor(self.hand_cursor)
                except:
                    pass
            else:
                pygame.mouse.set_cursor(self.default_cursor)
        else:
            pygame.mouse.set_cursor(self.default_cursor)

    def spawn_money(self):
        """Spawn money at random position"""
        margin = MONEY_SIZE
        self.money_pos = (
            random.randint(margin, WIDTH - margin),
            random.randint(margin, HEIGHT - margin))
        self.bot_target_time = time.time() + self.bot_reaction_times[self.difficulty]
        self.use_coin_image = random.choice([True, False])

    def show_snatch_animation(self, x, y):
        """Show snatching animation"""
        for i in range(5):
            self.screen.fill(LIGHT_BLUE)
            self.draw_scores()
            bot_rect = self.bot_img.get_rect(center=(int(self.bot_pos[0]), int(self.bot_pos[1])))
            self.screen.blit(self.bot_img, bot_rect)

            hand_x = x - (i * 5)
            hand_y = y - (i * 5)
            hand_color = (255, 220, 180)
            pygame.draw.circle(self.screen, hand_color, (hand_x, hand_y), 15)

            angle = math.pi / 4
            finger1_end = (hand_x + 20 * math.cos(angle - 0.3),
                          hand_y + 20 * math.sin(angle - 0.3))
            finger2_end = (hand_x + 20 * math.cos(angle + 0.3),
                          hand_y + 20 * math.sin(angle + 0.3))

            pygame.draw.line(self.screen, hand_color, (hand_x, hand_y), finger1_end, 5)
            pygame.draw.line(self.screen, hand_color, (hand_x, hand_y), finger2_end, 5)

            shrink_factor = 1.0 - (i * 0.2)
            if shrink_factor > 0:
                current_img = self.coin_img if self.use_coin_image else self.money_img
                scaled_size = int(MONEY_SIZE * shrink_factor)
                if scaled_size > 0:
                    scaled_img = pygame.transform.scale(current_img, (scaled_size, scaled_size))
                    img_rect = scaled_img.get_rect(center=self.money_pos)
                    self.screen.blit(scaled_img, img_rect)

            pygame.display.flip()
            pygame.time.delay(30)

    def update_bot(self):
        if not self.game_active or self.game_over:
            return

        if time.time() >= self.bot_target_time:
            dx = self.money_pos[0] - self.bot_pos[0]
            dy = self.money_pos[1] - self.bot_pos[1]
            distance = math.sqrt(dx**2 + dy**2)

            if distance < MONEY_SIZE // 2:
                self.bot_score += 1
                if self.coin_sound:
                    self.coin_sound.play()
                self.spawn_money()
            else:
                speed = self.bot_speeds[self.difficulty]
                if distance > 0:
                    self.bot_pos[0] += dx / distance * speed
                    self.bot_pos[1] += dy / distance * speed

    def draw_money(self):
        if self.use_coin_image:
            coin_rect = self.coin_img.get_rect(center=self.money_pos)
            self.screen.blit(self.coin_img, coin_rect)
        else:
            money_rect = self.money_img.get_rect(center=self.money_pos)
            self.screen.blit(self.money_img, money_rect)

    def draw_scores(self):
        player_text = self.font.render(f"Player: {self.player_score}", True, BLUE)
        bot_text = self.font.render(f"Bot: {self.bot_score}", True, RED)
        time_text = self.font.render(f"Time: {int(self.time_left)}", True, BLACK)
        self.screen.blit(player_text, (20, 20))
        self.screen.blit(bot_text, (WIDTH - 150, 20))
        self.screen.blit(time_text, (WIDTH // 2 - 50, 20))

    def draw_menu(self):
        self.screen.fill(LIGHT_BLUE)
        title = self.font.render("MONEY GRABBER", True, BLACK)
        self.screen.blit(title, (WIDTH // 2 - 100, 100))

        coin_rect = self.coin_img.get_rect(center=(WIDTH // 2 - 50, 170))
        money_rect = self.money_img.get_rect(center=(WIDTH // 2 + 50, 170))
        self.screen.blit(self.coin_img, coin_rect)
        self.screen.blit(self.money_img, money_rect)

        instructions = [
            "Click on the money before the bot grabs it!",
            "Game lasts for 30 seconds."
        ]

        for i, line in enumerate(instructions):
            text = self.small_font.render(line, True, BLACK)
            self.screen.blit(text, (WIDTH // 2 - 150, 220 + i * 30))

        self.screen.blit(self.small_font.render("Select difficulty:", True, BLACK), (WIDTH // 2 - 60, 300))

        difficulties = ["Easy", "Medium", "Hard"]
        button_width = 100
        button_height = 40

        for i, diff in enumerate(difficulties):
            button_x = WIDTH // 2 - 150 + i * 120
            button_y = 330
            button_color = GREEN if diff == self.difficulty else BLUE
            pygame.draw.rect(self.screen, button_color, (button_x, button_y, button_width, button_height))
            text = self.small_font.render(diff, True, WHITE)
            self.screen.blit(text, (button_x + 20, button_y + 10))

        pygame.draw.rect(self.screen, GREEN, (WIDTH // 2 - 60, 400, 120, 50))
        start_text = self.font.render("START", True, WHITE)
        self.screen.blit(start_text, (WIDTH // 2 - 40, 410))

        player_rect = self.player_img.get_rect(center=(WIDTH // 4, 500))
        bot_rect = self.bot_img.get_rect(center=(WIDTH * 3 // 4, 500))
        self.screen.blit(self.player_img, player_rect)
        self.screen.blit(self.bot_img, bot_rect)

        player_label = self.small_font.render("Player", True, BLUE)
        bot_label = self.small_font.render("Bot", True, RED)
        self.screen.blit(player_label, (WIDTH // 4 - 25, 530))
        self.screen.blit(bot_label, (WIDTH * 3 // 4 - 15, 530))

    def draw_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.font.render("GAME OVER", True, WHITE)
        self.screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 80))

        final_score = self.font.render(f"Player: {self.player_score}  Bot: {self.bot_score}", True, WHITE)
        self.screen.blit(final_score, (WIDTH // 2 - 120, HEIGHT // 2 - 30))

        if self.player_score > self.bot_score:
            winner = self.font.render("You Win!", True, BLUE)
            player_rect = self.player_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
            self.screen.blit(self.player_img, player_rect)
        elif self.bot_score > self.player_score:
            winner = self.font.render("Bot Wins!", True, RED)
            bot_rect = self.bot_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
            self.screen.blit(self.bot_img, bot_rect)
        else:
            winner = self.font.render("It's a Draw!", True, WHITE)
            player_rect = self.player_img.get_rect(center=(WIDTH // 2 - 30, HEIGHT // 2 + 30))
            bot_rect = self.bot_img.get_rect(center=(WIDTH // 2 + 30, HEIGHT // 2 + 30))
            self.screen.blit(self.player_img, player_rect)
            self.screen.blit(self.bot_img, bot_rect)

        self.screen.blit(winner, (WIDTH // 2 - 60, HEIGHT // 2 + 70))

        pygame.draw.rect(self.screen, GREEN, (WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 50))
        play_again = self.font.render("Play Again", True, WHITE)
        self.screen.blit(play_again, (WIDTH // 2 - 70, HEIGHT // 2 + 130))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if not self.game_active:
                    difficulties = ["Easy", "Medium", "Hard"]
                    button_width = 100
                    button_height = 40

                    for i, diff in enumerate(difficulties):
                        button_x = WIDTH // 2 - 150 + i * 120
                        button_y = 330

                        if (button_x <= mouse_pos[0] <= button_x + button_width and
                            button_y <= mouse_pos[1] <= button_y + button_height):
                            self.difficulty = diff

                    if (WIDTH // 2 - 60 <= mouse_pos[0] <= WIDTH // 2 + 60 and
                        400 <= mouse_pos[1] <= 450):
                        self.game_active = True
                        self.game_over = False
                        self.player_score = 0
                        self.bot_score = 0
                        self.start_time = time.time()
                        self.bot_pos = [WIDTH - 100, HEIGHT // 2]
                        self.spawn_money()

                elif self.game_over:
                    if (WIDTH // 2 - 100 <= mouse_pos[0] <= WIDTH // 2 + 100 and
                        HEIGHT // 2 + 120 <= mouse_pos[1] <= HEIGHT // 2 + 170):
                        self.game_active = False
                        self.game_over = False

                else:
                    distance = math.sqrt((mouse_pos[0] - self.money_pos[0])**2 +
                                       (mouse_pos[1] - self.money_pos[1])**2)
                    if distance <= MONEY_SIZE // 2:
                        self.show_snatch_animation(mouse_pos[0], mouse_pos[1])
                        self.player_score += 1
                        if self.coin_sound:
                            self.coin_sound.play()
                        self.spawn_money()

        return True

    def run(self):
        running = True

        while running:
            running = self.handle_events()
            mouse_pos = pygame.mouse.get_pos()
            self.update_cursor(mouse_pos)

            if self.game_active and not self.game_over:
                current_time = time.time()
                self.time_left = GAME_TIME - (current_time - self.start_time)

                if self.time_left <= 0:
                    self.game_over = True
                    self.time_left = 0

                self.update_bot()

            if not self.game_active:
                self.draw_menu()
            else:
                self.screen.fill(LIGHT_BLUE)
                self.draw_scores()

                if not self.game_over:
                    self.draw_money()
                    bot_rect = self.bot_img.get_rect(center=(int(self.bot_pos[0]), int(self.bot_pos[1])))
                    self.screen.blit(self.bot_img, bot_rect)
                else:
                    self.draw_game_over()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = MoneyGrabber()
    game.run()
