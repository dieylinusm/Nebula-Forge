import asyncio
import platform
import pygame
import random
import math

# Game constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 10
CELL_SIZE = 60
GRID_OFFSET_X = (WIDTH - GRID_SIZE * CELL_SIZE) // 2
GRID_OFFSET_Y = (HEIGHT - GRID_SIZE * CELL_SIZE) // 2
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)

# Game objects
PLAYER = "P"
RESOURCE = "R"
HAZARD = "H"

class NebulaForge:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Nebula Forge")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.player_pos = (GRID_SIZE // 2, GRID_SIZE // 2)
        self.resources = {"Quark": 0, "Plasma": 0, "Neutrino": 0}
        self.tools = {"Shield": 0, "Pulse": 0}
        self.score = 0
        self.game_over = False
        self.setup_level()

    def setup_level(self):
        # Clear grid
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.grid[self.player_pos[1]][self.player_pos[0]] = PLAYER

        # Place resources and hazards
        for _ in range(8):
            while True:
                x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
                if self.grid[y][x] is None:
                    self.grid[y][x] = RESOURCE if random.random() < 0.7 else HAZARD
                    break

    def craft_tool(self, tool):
        if tool == "Shield" and self.resources["Quark"] >= 2 and self.resources["Plasma"] >= 1:
            self.resources["Quark"] -= 2
            self.resources["Plasma"] -= 1
            self.tools["Shield"] += 1
            self.score += 50
            return True
        elif tool == "Pulse" and self.resources["Plasma"] >= 2 and self.resources["Neutrino"] >= 1:
            self.resources["Plasma"] -= 2
            self.resources["Neutrino"] -= 1
            self.tools["Pulse"] += 1
            self.score += 50
            return True
        return False

    def use_tool(self, tool):
        if self.tools[tool] > 0:
            self.tools[tool] -= 1
            if tool == "Pulse":
                # Clear adjacent hazards
                x, y = self.player_pos
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and self.grid[ny][nx] == HAZARD:
                            self.grid[ny][nx] = None
                            self.score += 20
            return True
        return False

    def move_player(self, dx, dy):
        new_x, new_y = self.player_pos[0] + dx, self.player_pos[1] + dy
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            if self.grid[new_y][new_x] == RESOURCE:
                self.resources[random.choice(["Quark", "Plasma", "Neutrino"])] += 1
                self.score += 10
                self.grid[new_y][new_x] = None
            elif self.grid[new_y][new_x] == HAZARD and not self.tools["Shield"]:
                self.game_over = True
                return
            elif self.grid[new_y][new_x] == HAZARD and self.tools["Shield"]:
                self.tools["Shield"] -= 1
                self.grid[new_y][new_x] = None
                self.score += 30

            self.grid[self.player_pos[1]][self.player_pos[0]] = None
            self.player_pos = (new_x, new_y)
            self.grid[new_y][new_x] = PLAYER

            # Respawn resources/hazards if grid is sparse
            if sum(row.count(RESOURCE) + row.count(HAZARD) for row in self.grid) < 4:
                self.setup_level()

    def draw(self):
        self.screen.fill(BLACK)

        # Draw grid
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(
                    GRID_OFFSET_X + x * CELL_SIZE,
                    GRID_OFFSET_Y + y * CELL_SIZE,
                    CELL_SIZE - 5,
                    CELL_SIZE - 5
                )
                pygame.draw.rect(self.screen, WHITE, rect, 1)

                if self.grid[y][x] == PLAYER:
                    pygame.draw.circle(self.screen, CYAN, rect.center, CELL_SIZE // 3)
                elif self.grid[y][x] == RESOURCE:
                    pygame.draw.rect(self.screen, PURPLE, rect, 2)
                elif self.grid[y][x] == HAZARD:
                    pygame.draw.rect(self.screen, RED, rect)

        # Draw resources, tools, and score
        y_offset = 10
        for resource, count in self.resources.items():
            text = self.font.render(f"{resource}: {count}", True, WHITE)
            self.screen.blit(text, (10, y_offset))
            y_offset += 30
        for tool, count in self.tools.items():
            text = self.font.render(f"{tool}: {count}", True, WHITE)
            self.screen.blit(text, (10, y_offset))
            y_offset += 30
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, y_offset))

        if self.game_over:
            game_over_text = self.font.render("Game Over! Press R to Restart", True, WHITE)
            self.screen.blit(game_over_text, (WIDTH//2 - 150, HEIGHT//2))

        pygame.display.flip()

    def update_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.KEYDOWN:
                if self.game_over and event.key == pygame.K_r:
                    self.__init__()
                elif not self.game_over:
                    if event.key == pygame.K_UP:
                        self.move_player(0, -1)
                    elif event.key == pygame.K_DOWN:
                        self.move_player(0, 1)
                    elif event.key == pygame.K_LEFT:
                        self.move_player(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move_player(1, 0)
                    elif event.key == pygame.K_s:
                        self.craft_tool("Shield")
                    elif event.key == pygame.K_p:
                        self.craft_tool("Pulse")
                    elif event.key == pygame.K_u:
                        self.use_tool("Pulse")

        self.draw()

async def main():
    game = NebulaForge()
    while not game.game_over:
        game.update_loop()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
