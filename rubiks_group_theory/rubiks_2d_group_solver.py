import pygame
import sys

# Colors
COLORS = {
    'W': (255, 255, 255), 'Y': (255, 255, 0),
    'R': (255, 0, 0),     'O': (255, 165, 0),
    'B': (0, 0, 255),     'G': (0, 255, 0),
    'BLACK': (0, 0, 0)
}

class Rubiks2D:
    def __init__(self):
        # Initialize a solved cube: 6 faces, each 3x3
        self.faces = {
            'top': [['W']*3 for _ in range(3)],
            'bottom': [['Y']*3 for _ in range(3)],
            'front': [['G']*3 for _ in range(3)],
            'back': [['B']*3 for _ in range(3)],
            'left': [['O']*3 for _ in range(3)],
            'right': [['R']*3 for _ in range(3)],
        }
        self.size = 40  # size of each sticker

    def rotate_face_clockwise(self, face):
        self.faces[face] = [list(r) for r in zip(*self.faces[face][::-1])]

    def move_U(self):
        """Rotate Top face clockwise and shift adjacent edges."""
        self.rotate_face_clockwise('top')
        # Temporary storage for the row being shifted
        row_f = [self.faces['front'][0][i] for i in range(3)]
        row_r = [self.faces['right'][0][i] for i in range(3)]
        row_b = [self.faces['back'][0][i] for i in range(3)]
        row_l = [self.faces['left'][0][i] for i in range(3)]
        
        for i in range(3):
            self.faces['front'][0][i] = row_r[i]
            self.faces['right'][0][i] = row_b[i]
            self.faces['back'][0][i] = row_l[i]
            self.faces['left'][0][i] = row_f[i]

    def draw(self, screen):
        # Map faces to grid positions (x, y)
        layout = {
            'top': (1, 0), 'left': (0, 1), 'front': (1, 1),
            'right': (2, 1), 'back': (3, 1), 'bottom': (1, 2)
        }
        for face, (grid_x, grid_y) in layout.items():
            for r in range(3):
                for c in range(3):
                    color = COLORS[self.faces[face][r][c]]
                    rect = (grid_x*3*self.size + c*self.size + 50, 
                            grid_y*3*self.size + r*self.size + 50, 
                            self.size-2, self.size-2)
                    pygame.draw.rect(screen, color, rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((700, 500))
    clock = pygame.time.Clock()
    cube = Rubiks2D()

    while True:
        screen.fill(COLORS['BLACK'])
        cube.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u: # Press 'U' to rotate top face
                    cube.move_U()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()