import random
import pygame
pygame.init()

WIDTH = 800
HEIGHT = 600
SCORE = [0, 0]
PLAYING = False
START = True
MAX_SCORE = 3
ALL_SCORE = (3, 5, 8, 15)
WINNER = ""

white = (255, 255, 255)
lightgray = (200, 200, 200)
blue = (50, 50, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface((15, 175))
        self.image.fill("blue")
        self.rect = self.image.get_rect()
        self.speed = 5

        self.rect.x = pos_x
        self.rect.y = pos_y

        self._maxY = HEIGHT - self.image.get_height()

    def move(self, direction):
        if direction == "up":
            if self.rect.y != 0: self.rect.y -= self.speed

        if direction == "down":
            if self.rect.y != self._maxY : self.rect.y += self.speed

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH//2 - self.image.get_width()//2
        self.rect.y = HEIGHT//2 - self.image.get_height()//2
        pygame.draw.circle(self.image, "red", (self.image.get_width()//2, self.image.get_height()//2), 25)
        self.speed = [4, 0]

        self.screen_center = (WIDTH//2 - self.image.get_width()//2, HEIGHT//2 - self.image.get_height()//2)

    def start(self):
        global PLAYING
        self.speed = [5, random.randint(-6, 6)]
        PLAYING = True

    def stop(self):
        global PLAYING
        self.rect.x, self.rect.y = self.screen_center
        self.speed = [0, 0]
        PLAYING = False

    def bounce(self):
        self.speed[1] = random.randint(3, 8) * random.choice([-1, 1])
        self.speed[0] *= -1

    def move(self):

        if self.rect.x <= 0:
            SCORE[1] += 1
            self.stop()
        elif self.rect.x >= WIDTH - self.image.get_width():
            SCORE[0] += 1
            self.stop()

        if self.rect.y <= 0 or self.rect.y >= HEIGHT - self.image.get_height(): self.speed[1] *= -1

        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("Font.TTF", 48)

        self.sp_grp = pygame.sprite.Group()

        self.firstPlayer = Player(25, 50)
        self.secondPlayer = Player(WIDTH - 45, 50)
        self.ball = Ball()

        self.sp_grp.add(self.firstPlayer)
        self.sp_grp.add(self.secondPlayer)
        self.sp_grp.add(self.ball)

        self.middle = pygame.Surface((2, HEIGHT))
        self.middle.fill(lightgray)
        self.oneScore = self.font.render(str(SCORE[0]), True, white)
        self.twoScore = self.font.render(str(SCORE[1]), True, white)
        self.splash = self.font.render("Press [SPACE] to start", True, (255, 50, 50))

        self.middle_rect = self.middle.get_rect()
        self.middle_rect.x = WIDTH // 2 - self.middle.get_width()//2

        self.oneScoreRect = self.oneScore.get_rect()
        self.oneScoreRect.x = WIDTH // 4 - self.oneScore.get_width() // 2

        self.twoScoreRect = self.twoScore.get_rect()
        self.twoScoreRect.x = WIDTH // 2 + WIDTH // 4 - self.twoScore.get_width() // 2

        self.splashRect = self.splash.get_rect()
        self.splashRect.x = WIDTH // 2 - self.splash.get_width() // 2
        self.splashRect.y = 500

        """ --- MENU --- """
        self.menuFont = pygame.font.Font("Font.TTF", 32)
        self.textScore = self.menuFont.render("Score Maximum : ", True, white)
        self.maxScoreText = self.menuFont.render(str(MAX_SCORE), True, white)
        self.winnerText = self.menuFont.render("Gangnant : ", True, white)
        self.winner = self.menuFont.render(WINNER, True, white)
        self.commandLeft = self.menuFont.render("Use [Z] and [S] to move left pallet", True, blue)
        self.commandRight = self.menuFont.render("Use [UP] and [DOWN] to move right pallet", True, blue)

        self.textRect = self.textScore.get_rect()
        self.textRect.x = WIDTH//4 - self.textScore.get_width() // 2
        self.textRect.y = 100

        self.maxScoreTextRect = self.maxScoreText.get_rect()
        self.maxScoreTextRect.x = WIDTH//2 - self.maxScoreText.get_width()//2
        self.maxScoreTextRect.y = 100

        self.winnerTextRect = self.winnerText.get_rect()
        self.winnerTextRect.x = WIDTH//4 - self.winnerText.get_width()//2
        self.winnerTextRect.y = 150

        self.winnerRect = self.winner.get_rect()
        self.winnerRect.x = WIDTH//2 - self.winner.get_width()//2
        self.winnerRect.y = 150

        self.commandLeftRect = self.commandLeft.get_rect()
        self.commandLeftRect.x = 50
        self.commandLeftRect.y = 300

        self.commandRightRect = self.commandRight.get_rect()
        self.commandRightRect.x = 50
        self.commandRightRect.y = 350

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_z]: self.firstPlayer.move("up")
        elif keys[pygame.K_s]: self.firstPlayer.move("down")

        if keys[pygame.K_UP]: self.secondPlayer.move("up")
        elif keys[pygame.K_DOWN]: self.secondPlayer.move("down")

    def run(self):
        global START, SCORE, MAX_SCORE, WINNER
        running = True
        while running:
            self.screen.fill("black")

            if SCORE[0] == MAX_SCORE:
                WINNER = "Left Player"
                START = True
            elif SCORE[1] == MAX_SCORE:
                WINNER = "Right Player"
                START = True

            if START:
                SCORE = [0, 0]
                self.ball.stop()
                self.maxScoreText = self.menuFont.render(str(MAX_SCORE), True, white)
                self.winner = self.menuFont.render(WINNER, True, white)

                if WINNER != "":
                    self.screen.blit(self.winner, self.winnerRect)

                self.screen.blit(self.textScore, self.textRect)
                self.screen.blit(self.maxScoreText, self.maxScoreTextRect)
                self.screen.blit(self.winnerText, self.winnerTextRect)
                self.screen.blit(self.commandLeft, self.commandLeftRect)
                self.screen.blit(self.commandRight, self.commandRightRect)
                self.screen.blit(self.splash, self.splashRect)
            else:
                self.oneScore = self.font.render(str(SCORE[0]), True, (255, 255, 255))
                self.twoScore = self.font.render(str(SCORE[1]), True, (255, 255, 255))

                self.sp_grp.update()
                self.sp_grp.draw(self.screen)

                self.screen.blit(self.middle, self.middle_rect)
                self.screen.blit(self.ball.image, self.ball.rect)
                self.screen.blit(self.oneScore, self.oneScoreRect)
                self.screen.blit(self.twoScore, self.twoScoreRect)

                if PLAYING:

                    self.move()
                    self.ball.move()
                    if self.ball.rect.colliderect(self.firstPlayer.rect) or self.ball.rect.colliderect(self.secondPlayer.rect):
                        self.ball.bounce()

                else:
                    self.screen.blit(self.splash, self.splashRect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.ball.start()
                        START = False

                    if event.key == pygame.K_BACKSPACE:
                        START = True
                        self.firstPlayer.rect.x, self.firstPlayer.rect.y = 25, 50
                        self.secondPlayer.rect.x, self.secondPlayer.rect.y = WIDTH - 45, 50

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.maxScoreTextRect.collidepoint(event.pos):
                        if MAX_SCORE in ALL_SCORE:
                            i = ALL_SCORE.index(MAX_SCORE)
                            try: MAX_SCORE = ALL_SCORE[i+1]
                            except IndexError: MAX_SCORE = ALL_SCORE[0]

            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()