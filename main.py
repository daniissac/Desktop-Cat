import sys
import random
import math
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QMenu
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QPixmap, QCursor, QAction
import platform

if platform.system() == "Windows":
    import ctypes
elif platform.system() == "Darwin":  # macOS
    import subprocess
elif platform.system() == "Linux":
    import subprocess

class CatPet(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.prevent_sleep()

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
        self.animation_slowdown = 0

        self.is_dragging = False
        self.meow_timer = 0
        self.click_start_pos = None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(50)  # Update every 50ms for smooth animation

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def load_images(self):
        self.idle = [QPixmap(f'assets/idle{i}.png') for i in range(1, 5)]
        self.idle_to_sleeping = [QPixmap(f'assets/sleeping{i}.png') for i in range(1, 7)]
        self.sleeping = [QPixmap(f'assets/zzz{i}.png') for i in range(1, 5)]
        self.sleeping_to_idle = [QPixmap(f'assets/sleeping{i}.png') for i in range(6, 0, -1)]
        self.walking_left = [QPixmap(f'assets/walkingleft{i}.png') for i in range(1, 5)]
        self.walking_right = [QPixmap(f'assets/walkingright{i}.png') for i in range(1, 5)]
        self.meow = self.idle  # Use idle animation for meowing if no specific meow animation is available

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
        if self.is_dragging:
            cursor_pos = self.mapFromGlobal(QCursor.pos())
            self.pos = QPointF(cursor_pos.x() - self.click_start_pos.x(),
                               cursor_pos.y() - self.click_start_pos.y())
            self.frame = self.idle[0]  # Use a single frame while dragging
        elif self.meow_timer > 0:
            self.frame = self.animate(self.meow, slowdown_factor=3)
            self.meow_timer -= 1
            if self.meow_timer <= 0:
                self.state = 0
                self.i_frame = 0
        elif self.state == 0:  # Idle
            self.frame = self.animate(self.idle, slowdown_factor=6)
            self.rest_timer += 1
            if self.rest_timer > 100 and random.random() < 0.02:
                self.state = 4
                self.movement_timer = random.randint(20, 100)
                self.rest_timer = 0
            elif random.random() < 0.001:
                self.state = 1
                self.i_frame = 0
        elif self.state == 1:  # Idle to sleeping
            self.frame = self.animate(self.idle_to_sleeping, slowdown_factor=3)
            if self.i_frame == len(self.idle_to_sleeping) - 1:
                self.state = 2
                self.i_frame = 0
        elif self.state == 2:  # Sleeping
            self.frame = self.animate(self.sleeping, slowdown_factor=8)
            if random.random() < 0.005:
                self.state = 3
                self.i_frame = 0
        elif self.state == 3:  # Sleeping to idle
            self.frame = self.animate(self.sleeping_to_idle, slowdown_factor=3)
            if self.i_frame == len(self.sleeping_to_idle) - 1:
                self.state = 0
                self.i_frame = 0
        elif self.state == 4:  # Walking
            if self.direction.x() < 0:
                self.frame = self.animate(self.walking_left)
            else:
                self.frame = self.animate(self.walking_right)
            
            speed = random.uniform(0.5, 1.5)
            self.pos += self.direction * speed
            
            if self.pos.x() < 0 or self.pos.x() > self.screen_width - self.pet_width:
                self.direction = QPointF(-self.direction.x(), self.direction.y())
            if self.pos.y() < 0 or self.pos.y() > self.screen_height - self.pet_height:
                self.direction = QPointF(self.direction.x(), -self.direction.y())
            
            self.pos.setX(max(0, min(self.pos.x(), self.screen_width - self.pet_width)))
            self.pos.setY(max(0, min(self.pos.y(), self.screen_height - self.pet_height)))
            
            self.movement_timer -= 1
            if self.movement_timer <= 0:
                if random.random() < 0.7:
                    self.state = 0
                    self.i_frame = 0
                else:
                    self.direction = QPointF(random.uniform(-1, 1), random.uniform(-1, 1))
                    self.direction /= math.sqrt(self.direction.x()**2 + self.direction.y()**2)
                    self.movement_timer = random.randint(20, 100)

        self.label.setPixmap(self.frame)
        self.setGeometry(int(self.pos.x()), int(self.pos.y()), self.pet_width, self.pet_height)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = True
            self.click_start_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.is_dragging:
                self.is_dragging = False
                self.state = 0  # Return to idle state
                self.i_frame = 0
            else:
                self.meow_timer = 20  # Meow for about 1 second (20 * 50ms)
                self.i_frame = 0

    def mouseMoveEvent(self, event):
        if self.is_dragging:
            self.pos = QPointF(event.globalPosition().x() - self.click_start_pos.x(),
                               event.globalPosition().y() - self.click_start_pos.y())
            self.move(int(self.pos.x()), int(self.pos.y()))

    def show_context_menu(self, position):
        context_menu = QMenu(self)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        context_menu.addAction(exit_action)
        context_menu.exec(self.mapToGlobal(position))


    def prevent_sleep(self):
        system = platform.system()
        if system == "Windows":
            ctypes.windll.kernel32.SetThreadExecutionState(
                0x80000002  # ES_CONTINUOUS | ES_SYSTEM_REQUIRED
            )
        elif system == "Darwin":  # macOS
            subprocess.run(["caffeinate", "-d", "-i", "-m", "-u", "&"])
        elif system == "Linux":
            subprocess.run(["xdg-screensaver", "suspend", str(self.winId())])
        else:
            print(f"Unsupported operating system: {system}")

    def allow_sleep(self):
        system = platform.system()
        if system == "Windows":
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)  # ES_CONTINUOUS
        elif system == "Darwin":  # macOS
            subprocess.run(["killall", "caffeinate"])
        elif system == "Linux":
            subprocess.run(["xdg-screensaver", "resume", str(self.winId())])
        else:
            print(f"Unsupported operating system: {system}")

    def closeEvent(self, event):
        self.allow_sleep()
        super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    cat = CatPet()
    cat.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
