import pygame

class DrawingApp:
    def __init__(self):
        pygame.init()
        # setting resolution
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        # initial font size
        self.radius = 15
        # initial color
        self.mode = 'blue'
        # color mapping
        self.colors = {'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (0, 0, 255), 'yelow': (255, 255, 0)}
        self.points = []
        # starting with circle
        self.triangle = False
        self.circle = True
        self.rectangle = False
        self.square = False
        self.rhombus = False  # New attribute for rhombus mode

    def run(self):
        while True:
            # handlng quiting
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                # changing font size with keyboard
                if event.type == pygame.KEYDOWN:
                    self.handle_key_events(event.key)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_events(event.button)
                # tracking the mouse motion
                if event.type == pygame.MOUSEMOTION:
                    self.points.append(event.pos)
                    self.points = self.points[-256:]

            self.draw_frame()
            pygame.display.flip()
            self.clock.tick(60)

    def handle_key_events(self, key):
        # if pressed c - clear all
        if key == pygame.K_c:
            self.points.clear()
        # if pressed t - triangle
        elif key == pygame.K_t:
            self.triangle = True
            self.circle = False
            self.rectangle = False
            self.square = False
            self.rhombus = False
        # o - circle
        elif key == pygame.K_o:
            self.circle = True
            self.triangle = False
            self.rectangle = False
            self.square = False
            self.rhombus = False
        # p - rectangle
        elif key == pygame.K_p:
            self.circle = False
            self.triangle = False
            self.rectangle = True
            self.square = False
            self.rhombus = False
        # s - square
        elif key == pygame.K_s:
            self.circle = False
            self.triangle = False
            self.rectangle = False
            self.square = True
            self.rhombus = False
        # changing colors using color map
        elif key == pygame.K_r:
            self.mode = 'red'
        elif key == pygame.K_g:
            self.mode = 'green'
        elif key == pygame.K_b:
            self.mode = 'blue'
        elif key == pygame.K_y:
            self.mode = 'yellow'
        # rhombus
        elif key == pygame.K_h:
            self.circle = False
            self.triangle = False
            self.rectangle = False
            self.square = False
            self.rhombus = True

    def handle_mouse_events(self, button):
        key_unicode = pygame.key.name(button).lower()
        if key_unicode in self.colors:
            self.current_color = self.colors[key_unicode]
        if button == pygame.BUTTON_LEFT:
            self.start_pos = pygame.mouse.get_pos()

    def draw_frame(self):
        self.screen.fill((0, 0, 0))

        i = 0
        while i < len(self.points) - 1:
            # drawing segment between coordinates
            self.draw_line_between(i, self.points[i], self.points[i + 1])
            i += 1

        if self.rectangle:
            if hasattr(self, 'start_pos'):
                # calculating rect coordinate of current position
                mouse_pos = pygame.mouse.get_pos()
                rect_width = abs(mouse_pos[0] - self.start_pos[0])
                rect_height = abs(mouse_pos[1] - self.start_pos[1])
                rect_x = min(mouse_pos[0], self.start_pos[0])
                rect_y = min(mouse_pos[1], self.start_pos[1])
                # draw rectangle
                pygame.draw.rect(self.screen, self.current_color, pygame.Rect(rect_x, rect_y, rect_width, rect_height),
                                 2)

    def draw_line_between(self, index, start, end):
        color = self.calculate_color(index)

        dx = start[0] - end[0]
        dy = start[1] - end[1]
        iterations = max(abs(dx), abs(dy))

        for i in range(iterations):
            progress = 1.0 * i / iterations
            aprogress = 1 - progress
            # draw something on current x,y posiions (endless loop)
            x = int(aprogress * start[0] + progress * end[0])
            y = int(aprogress * start[1] + progress * end[1])
            if self.circle:
                pygame.draw.circle(self.screen, color, (x, y), self.radius)
            elif self.triangle:
                vertices = [(x, y), (x + self.radius, y + self.radius), (x - self.radius, y + self.radius)]
                pygame.draw.polygon(self.screen, color, vertices)
            elif self.rectangle:
                rect_width = 5
                rect_x, rect_y = x - 50, y - 37.5
                rect_size = (100, 75)
                pygame.draw.rect(self.screen, color, pygame.Rect(rect_x, rect_y, rect_size[0], rect_size[1]))
                pygame.draw.rect(self.screen, color, pygame.Rect(rect_x, rect_y, rect_size[0], rect_size[1]), rect_width)
            elif self.square:
                rect_width = 5
                rect_x, rect_y = x - 50, y - 50
                rect_size = (100, 100)
                pygame.draw.rect(self.screen, color, pygame.Rect(rect_x, rect_y, rect_size[0], rect_size[1]))
                pygame.draw.rect(self.screen, color, pygame.Rect(rect_x, rect_y, rect_size[0], rect_size[1]), rect_width)
            elif self.rhombus:  # Draw a rhombus
                rhombus_size = 100
                rhombus_vertices = [(x, y - rhombus_size // 2), (x + rhombus_size // 2, y),
                                    (x, y + rhombus_size // 2), (x - rhombus_size // 2, y)]
                pygame.draw.polygon(self.screen, color, rhombus_vertices)

    def calculate_color(self, index):
        # changing color using color mapping
        if self.mode == 'blue':
            return self.colors['blue']
        elif self.mode == 'red':
            return self.colors['red']
        elif self.mode == 'green':
            return self.colors['green']
        elif self.mode == 'yellow':
            return self.colors['yellow']

if __name__ == "__main__":
    app = DrawingApp()
    app.run()
