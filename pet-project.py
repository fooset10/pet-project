


import pygame
import random
import sys


pygame.init()


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
FPS = 60


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 150, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 100, 255)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
LIGHT_BLUE = (173, 216, 230)
GOLD = (255, 215, 0)
DARK_RED = (200, 0, 0)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Футбольный пенальти ! ⚽")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)
medium_font = pygame.font.Font(None, 48)
huge_font = pygame.font.Font(None, 96)


GOAL_LEFT = SCREEN_WIDTH // 2 - 200
GOAL_RIGHT = SCREEN_WIDTH // 2 + 200
GOAL_TOP = 55
GOAL_BOTTOM = 250


class Goalkeeper:


    def __init__(self):
        self.width = 95
        self.height = 165
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT // 2 - self.height // 2 + 10
        self.jump_direction = None
        self.jump_progress = 0
        self.jump_speed = 0.12
        self.defend_center = False

    def jump(self):


        rand = random.random()
        if rand < 0.4:
            self.jump_direction = "left"
            self.defend_center = False
        elif rand < 0.8:
            self.jump_direction = "right"
            self.defend_center = False
        else:
            self.jump_direction = None
            self.defend_center = True

        self.jump_progress = 0

    def update(self):

        if self.jump_progress < 1.0 and self.jump_direction:
            self.jump_progress += self.jump_speed

            if self.jump_direction == "left":
                self.x = SCREEN_WIDTH // 2 - self.width // 2 - 100 * self.jump_progress
            elif self.jump_direction == "right":
                self.x = SCREEN_WIDTH // 2 - self.width // 2 + 100 * self.jump_progress
        else:
            if self.jump_direction:
                self.jump_direction = None
                self.jump_progress = 0
                self.x = SCREEN_WIDTH // 2 - self.width // 2

    def catch_ball(self, ball_x, ball_y, shot_direction):

        keeper_rect = pygame.Rect(self.x, self.y, self.width, self.height)


        extended_rect = keeper_rect.inflate(25, 25)

        if extended_rect.collidepoint(ball_x, ball_y):


            if self.jump_direction == shot_direction:

                return random.random() < 0.8
            elif shot_direction == "center" and self.defend_center:

                return random.random() < 0.75
            else:

                return random.random() < 0.5
        else:

            return random.random() < 0.2

    def draw(self, screen):


        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))


        head_x = self.x + self.width // 2
        head_y = self.y - 24
        pygame.draw.circle(screen, BLUE, (head_x, head_y), 24)


        pygame.draw.circle(screen, WHITE, (head_x - 9, head_y - 7), 7)
        pygame.draw.circle(screen, WHITE, (head_x + 9, head_y - 7), 7)
        pygame.draw.circle(screen, BLACK, (head_x - 9, head_y - 7), 4)
        pygame.draw.circle(screen, BLACK, (head_x + 9, head_y - 7), 4)


        if self.jump_direction:
            pygame.draw.line(screen, BLACK, (head_x - 15, head_y - 12), (head_x - 6, head_y - 8), 3)
            pygame.draw.line(screen, BLACK, (head_x + 15, head_y - 12), (head_x + 6, head_y - 8), 3)


        if self.jump_direction == "left":
            pygame.draw.circle(screen, DARK_RED, (self.x - 22, self.y + 75), 20)
        elif self.jump_direction == "right":
            pygame.draw.circle(screen, DARK_RED, (self.x + self.width + 22, self.y + 75), 20)
        else:
            pygame.draw.circle(screen, RED, (self.x - 18, self.y + 75), 18)
            pygame.draw.circle(screen, RED, (self.x + self.width + 18, self.y + 75), 18)


        for i in range(4):
            pygame.draw.line(screen, WHITE,
                             (self.x + 15, self.y + 35 + i * 30),
                             (self.x + self.width - 15, self.y + 35 + i * 30), 3)


        number = font.render("1", True, GOLD)
        screen.blit(number, (self.x + self.width // 2 - 10, self.y + self.height // 2 - 10))


class Ball:


    def __init__(self):
        self.radius = 14
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 120
        self.is_kicking = False
        self.target_x = 0
        self.target_y = 0
        self.progress = 0
        self.deflected = False

    def kick(self, direction):

        if not self.is_kicking:
            self.is_kicking = True
            self.progress = 0
            self.deflected = False


            if direction == "left":
                self.target_x = GOAL_LEFT + 40
                self.target_y = GOAL_TOP + random.randint(30, 80)
            elif direction == "center":
                self.target_x = SCREEN_WIDTH // 2 + random.randint(-30, 30)
                self.target_y = GOAL_TOP + random.randint(50, 100)
            else:  # right
                self.target_x = GOAL_RIGHT - 40
                self.target_y = GOAL_TOP + random.randint(30, 80)

    def deflect(self):

        self.deflected = True

    def update(self):

        if self.is_kicking:
            self.progress += 0.12

            if self.progress >= 1.0:
                self.is_kicking = False
                return (self.target_x, self.target_y)
            else:
                self.x = SCREEN_WIDTH // 2 + (self.target_x - SCREEN_WIDTH // 2) * self.progress
                self.y = SCREEN_HEIGHT - 120 + (self.target_y - (SCREEN_HEIGHT - 120)) * self.progress

        return None

    def draw(self, screen):

        color = ORANGE if self.deflected else WHITE
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius, 3)
        pygame.draw.line(screen, BLACK, (self.x - 11, self.y), (self.x + 11, self.y), 3)
        pygame.draw.line(screen, BLACK, (self.x, self.y - 11), (self.x, self.y + 11), 3)


class Game:


    def __init__(self):
        self.goalkeeper = Goalkeeper()
        self.ball = Ball()
        self.score = 0
        self.attempts = 0
        self.max_attempts = 10
        self.game_over = False
        self.waiting_for_kick = True
        self.result_text = ""
        self.result_timer = 0
        self.last_direction = None
        self.save_count = 0

    def shoot(self, direction):

        if (self.waiting_for_kick and
                not self.game_over and
                self.attempts < self.max_attempts):
            self.last_direction = direction
            self.goalkeeper.jump()
            self.ball.kick(direction)
            self.waiting_for_kick = False
            self.result_timer = pygame.time.get_ticks()

    def check_result(self, ball_x, ball_y, shot_direction):



        in_goal = (GOAL_LEFT <= ball_x <= GOAL_RIGHT and
                   GOAL_TOP <= ball_y <= GOAL_BOTTOM)

        if not in_goal:
            return False, "МИМО ВОРОТ! 😅"


        caught = self.goalkeeper.catch_ball(ball_x, ball_y, shot_direction)

        if caught:
            self.save_count += 1
            # Разные фразы для сэйвов
            save_phrases = ["СЭЙВ! 🧤", "ВРАТАРЬ ПОЙМАЛ! 🧤", "ОТБИЛ! 🧤", "НЕ ЗАБИЛ! 🧤"]
            return False, random.choice(save_phrases)
        else:

            goal_phrases = ["ГОООЛ! 🎉⚽", "МОЛОДЕЦ! 🎉", "ЗАБИЛ! 🎉", "ГОЛ! 🎉"]
            return True, random.choice(goal_phrases)

    def update(self):

        if not self.waiting_for_kick and not self.game_over:
            result = self.ball.update()

            if result is not None:
                ball_x, ball_y = result


                is_goal, message = self.check_result(ball_x, ball_y, self.last_direction)

                if is_goal:
                    self.score += 1
                    self.result_text = message
                else:
                    self.result_text = message
                    self.ball.deflect()

                self.attempts += 1
                self.result_timer = pygame.time.get_ticks()

                if self.attempts >= self.max_attempts:
                    self.game_over = True
                    self.waiting_for_kick = False

        if self.result_timer > 0 and pygame.time.get_ticks() - self.result_timer > 1200:
            self.result_timer = 0
            if not self.game_over:
                self.waiting_for_kick = True

        self.goalkeeper.update()

    def draw(self, screen):


        screen.fill(GREEN)


        pygame.draw.rect(screen, WHITE, (30, 40, SCREEN_WIDTH - 60, SCREEN_HEIGHT - 110), 5)
        pygame.draw.line(screen, WHITE, (SCREEN_WIDTH // 2, 40), (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70), 5)
        pygame.draw.circle(screen, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50), 60, 5)


        pygame.draw.line(screen, WHITE, (GOAL_LEFT, GOAL_TOP), (GOAL_LEFT, GOAL_BOTTOM), 12)
        pygame.draw.line(screen, WHITE, (GOAL_RIGHT, GOAL_TOP), (GOAL_RIGHT, GOAL_BOTTOM), 12)
        pygame.draw.line(screen, WHITE, (GOAL_LEFT, GOAL_TOP), (GOAL_RIGHT, GOAL_TOP), 12)


        for i in range(15):
            y = GOAL_TOP + 8 + i * 13
            if y < GOAL_BOTTOM:
                pygame.draw.line(screen, WHITE, (GOAL_LEFT + 8, y), (GOAL_RIGHT - 8, y), 2)

        for i in range(12):
            x = GOAL_LEFT + 20 + i * 38
            if x < GOAL_RIGHT:
                pygame.draw.line(screen, WHITE, (x, GOAL_TOP + 8), (x, GOAL_BOTTOM - 8), 2)


        pygame.draw.rect(screen, WHITE,
                         (SCREEN_WIDTH // 2 - 260, 45, 520, 120), 4)


        pygame.draw.circle(screen, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 190), 10)


        self.goalkeeper.draw(screen)
        self.ball.draw(screen)


        score_text = huge_font.render(f"{self.score}", True, GOLD)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - 40, 5))

        score_label = font.render("ГОЛЫ", True, WHITE)
        screen.blit(score_label, (SCREEN_WIDTH // 2 - 35, -8))


        saves_text = font.render(f"Сэйвы: {self.save_count}", True, LIGHT_BLUE)
        screen.blit(saves_text, (SCREEN_WIDTH - 150, 15))


        remaining = self.max_attempts - self.attempts
        attempts_text = font.render(f"Осталось: {remaining}/{self.max_attempts}", True, WHITE)
        screen.blit(attempts_text, (20, 15))


        bar_width = 250
        bar_height = 20
        bar_x = 20
        bar_y = 50
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height), 0, 5)
        progress = (self.attempts / self.max_attempts) * bar_width
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, progress, bar_height), 0, 5)


        if self.waiting_for_kick and not self.game_over and self.attempts < self.max_attempts:
            btn_y = SCREEN_HEIGHT - 80
            btn_width = 100
            btn_height = 70


            left_btn = (SCREEN_WIDTH // 4 - btn_width // 2, btn_y)
            pygame.draw.rect(screen, ORANGE, (*left_btn, btn_width, btn_height), 0, 10)
            pygame.draw.rect(screen, YELLOW, (*left_btn, btn_width, btn_height), 3, 10)
            left_text = big_font.render("1", True, BLACK)
            screen.blit(left_text, (left_btn[0] + btn_width // 2 - 20, left_btn[1] + 20))

            center_btn = (SCREEN_WIDTH // 2 - btn_width // 2, btn_y)
            pygame.draw.rect(screen, ORANGE, (*center_btn, btn_width, btn_height), 0, 10)
            pygame.draw.rect(screen, YELLOW, (*center_btn, btn_width, btn_height), 3, 10)
            center_text = big_font.render("2", True, BLACK)
            screen.blit(center_text, (center_btn[0] + btn_width // 2 - 20, center_btn[1] + 20))

            right_btn = (3 * SCREEN_WIDTH // 4 - btn_width // 2, btn_y)
            pygame.draw.rect(screen, ORANGE, (*right_btn, btn_width, btn_height), 0, 10)
            pygame.draw.rect(screen, YELLOW, (*right_btn, btn_width, btn_height), 3, 10)
            right_text = big_font.render("3", True, BLACK)
            screen.blit(right_text, (right_btn[0] + btn_width // 2 - 20, right_btn[1] + 20))


            left_label = font.render("ЛЕВЫЙ", True, WHITE)
            center_label = font.render("ЦЕНТР", True, WHITE)
            right_label = font.render("ПРАВЫЙ", True, WHITE)
            screen.blit(left_label, (left_btn[0] + 25, left_btn[1] - 30))
            screen.blit(center_label, (center_btn[0] + 30, center_btn[1] - 30))
            screen.blit(right_label, (right_btn[0] + 25, right_btn[1] - 30))


            hint_text = medium_font.render("Вратарь отбивает удары! Бей точно в угол!", True, YELLOW)
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150))
            screen.blit(hint_text, hint_rect)


        if self.result_text and not self.game_over:
            color = GREEN if "ГОООЛ" in self.result_text else RED
            result_surface = medium_font.render(self.result_text, True, color)
            text_rect = result_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
            screen.blit(result_surface, text_rect)


        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))

            if self.score == self.max_attempts:
                end_text = huge_font.render("ИДЕАЛЬНО! 10/10! 🏆", True, GOLD)
            elif self.score >= 7:
                end_text = huge_font.render(f"СУПЕР! {self.score}/10 🎉", True, GREEN)
            elif self.score >= 5:
                end_text = big_font.render(f"ХОРОШО! {self.score}/10 👍", True, ORANGE)
            elif self.score >= 3:
                end_text = big_font.render(f"НОРМАЛЬНО! {self.score}/10 👌", True, WHITE)
            else:
                end_text = big_font.render(f"{self.score}/10 💪", True, RED)

            text_rect = end_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
            screen.blit(end_text, text_rect)

            percent = (self.score / self.max_attempts) * 100
            percent_text = font.render(f"Реализация: {percent:.0f}% | Сэйвы: {self.save_count}", True, YELLOW)
            percent_rect = percent_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            screen.blit(percent_text, percent_rect)

            # Оценка игры
            if self.score >= 7:
                rating = "🌟 ВЕЛИКОЛЕПНАЯ ИГРА! 🌟"
            elif self.score >= 5:
                rating = "⚡ НЕПЛОХО! ТЫ ПРОБИЛ ВРАТАРЯ! ⚡"
            elif self.score >= 3:
                rating = "💪 НОРМАЛЬНО, НО МОЖНО ЛУЧШЕ! 💪"
            else:
                rating = "🎯 ВРАТАРЬ СЕГОДНЯ БЫЛ СИЛЁН! 🎯"

            rating_text = medium_font.render(rating, True, LIGHT_BLUE)
            rating_rect = rating_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
            screen.blit(rating_text, rating_rect)

            restart_text = big_font.render("R - ИГРАТЬ СНОВА", True, GREEN)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            screen.blit(restart_text, restart_rect)

    def restart(self):

        self.goalkeeper = Goalkeeper()
        self.ball = Ball()
        self.score = 0
        self.attempts = 0
        self.game_over = False
        self.waiting_for_kick = True
        self.result_text = ""
        self.result_timer = 0
        self.last_direction = None
        self.save_count = 0


def main():
    game = Game()
    running = True

    print("⚽⚽⚽ ФУТБОЛЬНЫЙ ПЕНАЛЬТИ ⚽⚽⚽")
    print("🧤 Вратарь отбивает удары !")
    print("🎯 1 - левый угол | 2 - центр | 3 - правый угол")
    print("💡 СОВЕТ: БЕЙТЕ ТОЧНО В УГОЛ, ЧТОБЫ ЗАБИТЬ!")
    print("")
    print("👉 ГОТОВ? НАЖИМАЙ 1, 2 ИЛИ 3!")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r and game.game_over:
                    game.restart()
                elif (event.key == pygame.K_1 and
                      game.waiting_for_kick and
                      not game.game_over and
                      game.attempts < game.max_attempts):
                    game.shoot("left")
                elif (event.key == pygame.K_2 and
                      game.waiting_for_kick and
                      not game.game_over and
                      game.attempts < game.max_attempts):
                    game.shoot("center")
                elif (event.key == pygame.K_3 and
                      game.waiting_for_kick and
                      not game.game_over and
                      game.attempts < game.max_attempts):
                    game.shoot("right")

        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()