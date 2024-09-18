import sys
import random
import math
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QPixmap

class CatPet(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.label = QLabel(self)
        self.setCentralWidget(self.label)

        screen = QApplication.primaryScreen().geometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()

        self.pet_width = 72
        self.pet_height = 64

        self.pos = QPointF(random.randint(0, self.screen_width - self.pet_width),
                           random.randint(0, self.screen_height - self.pet_height))

        self.setGeometry(int(self.pos.x()), int(self.pos.y()), self.pet_width, self.pet_height)

        self.load_images()

        self.i_frame = 0
        self.state = 0  # Start in idle state
        self.direction = QPointF(random.uniform(-1, 1), random.uniform(-1, 1))
        self.direction /= math.sqrt(self.direction.x()**2 + self.direction.y()**2)  # Normalize

        self.frame = self.idle[0]
        self.label.setPixmap(self.frame)

        self.movement_timer = 0
        self.rest_timer = 0
        self.animation_slowdown = 0  # New variable to slow down certain animations

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(50)  # Update every 50ms for smooth animation

    def load_images(self):
        self.idle = [QPixmap(f'assets/idle{i}.png') for i in range(1, 5)]
        self.idle_to_sleeping = [QPixmap(f'assets/sleeping{i}.png') for i in range(1, 7)]
        self.sleeping = [QPixmap(f'assets/zzz{i}.png') for i in range(1, 5)]
        self.sleeping_to_idle = [QPixmap(f'assets/sleeping{i}.png') for i in range(6, 0, -1)]
        self.walking_left = [QPixmap(f'assets/walkingleft{i}.png') for i in range(1, 5)]
        self.walking_right = [QPixmap(f'assets/walkingright{i}.png') for i in range(1, 5)]

    def animate(self, array, slowdown_factor=1):
        self.animation_slowdown += 1
        if self.animation_slowdown >= slowdown_factor:
            self.animation_slowdown = 0
            if self.i_frame < len(array) - 1:
                self.i_frame += 1
            else:
                self.i_frame = 0
        return array[self.i_frame]

    def update(self):
        if self.state == 0:  # Idle
            self.frame = self.animate(self.idle, slowdown_factor=6)  # Slower blinking and tail movement
            self.rest_timer += 1
            if self.rest_timer > 100 and random.random() < 0.02:  # 2% chance to start walking after resting
                self.state = 4
                self.movement_timer = random.randint(20, 100)  # Random movement duration
                self.rest_timer = 0
            elif random.random() < 0.001:  # 0.1% chance to start sleeping
                self.state = 1
                self.i_frame = 0  # Reset frame index for smooth transition
        elif self.state == 1:  # Idle to sleeping
            self.frame = self.animate(self.idle_to_sleeping, slowdown_factor=3)  # Slightly slower transition
            if self.i_frame == len(self.idle_to_sleeping) - 1:
                self.state = 2
                self.i_frame = 0
        elif self.state == 2:  # Sleeping
            self.frame = self.animate(self.sleeping, slowdown_factor=8)  # Slower sleeping animation
            if random.random() < 0.005:  # 0.5% chance to wake up
                self.state = 3
                self.i_frame = 0
        elif self.state == 3:  # Sleeping to idle
            self.frame = self.animate(self.sleeping_to_idle, slowdown_factor=3)  # Slightly slower transition
            if self.i_frame == len(self.sleeping_to_idle) - 1:
                self.state = 0
                self.i_frame = 0
        elif self.state == 4:  # Walking
            if self.direction.x() < 0:
                self.frame = self.animate(self.walking_left)  # Keep walking animation at normal speed
            else:
                self.frame = self.animate(self.walking_right)  # Keep walking animation at normal speed
            
            # Move the pet
            speed = random.uniform(0.5, 1.5)  # Variable speed
            self.pos += self.direction * speed
            
            # Check boundaries and change direction if necessary
            if self.pos.x() < 0 or self.pos.x() > self.screen_width - self.pet_width:
                self.direction = QPointF(-self.direction.x(), self.direction.y())
            if self.pos.y() < 0 or self.pos.y() > self.screen_height - self.pet_height:
                self.direction = QPointF(self.direction.x(), -self.direction.y())
            
            # Clamp position to screen boundaries
            self.pos.setX(max(0, min(self.pos.x(), self.screen_width - self.pet_width)))
            self.pos.setY(max(0, min(self.pos.y(), self.screen_height - self.pet_height)))
            
            self.movement_timer -= 1
            if self.movement_timer <= 0:
                if random.random() < 0.7:  # 70% chance to stop and go idle
                    self.state = 0
                    self.i_frame = 0
                else:
                    # Change to a new random direction
                    self.direction = QPointF(random.uniform(-1, 1), random.uniform(-1, 1))
                    self.direction /= math.sqrt(self.direction.x()**2 + self.direction.y()**2)  # Normalize
                    self.movement_timer = random.randint(20, 100)  # Set a new movement duration

        self.label.setPixmap(self.frame)
        self.setGeometry(int(self.pos.x()), int(self.pos.y()), self.pet_width, self.pet_height)

def main():
    app = QApplication(sys.argv)
    cat = CatPet()
    cat.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
