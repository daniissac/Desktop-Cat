import random
import math
import platform
import ctypes
import subprocess
import os
import sys
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QLabel, QMenu

class CatPet(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.prevent_sleep()

    def initUI(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.label = QLabel(self)
        self.setCentralWidget(self.label)

        screen = QApplication.primaryScreen().geometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()

        self.pet_width = 72
        self.pet_height = 64

        self.pos = QPointF(
            random.randint(0, self.screen_width - self.pet_width),
            random.randint(0, self.screen_height - self.pet_height)
        )

        self.setGeometry(
            int(self.pos.x()), int(self.pos.y()),
            self.pet_width, self.pet_height
        )

        self.load_images()

        self.i_frame = 0
        self.state = 0  # Start in idle state
        self.direction = QPointF(random.uniform(-1, 1), random.uniform(-1, 1))
        self.direction /= math.sqrt(
            self.direction.x()**2 + self.direction.y()**2
        )  # Normalize

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
        self.idle_to_sleeping = [
            QPixmap(f'assets/sleeping{i}.png') for i in range(1, 7)
        ]
        self.sleeping = [QPixmap(f'assets/zzz{i}.png') for i in range(1, 5)]

    def prevent_sleep(self):
        if platform.system() == 'Windows':
            ctypes.windll.kernel32.SetThreadExecutionState(
                0x80000002
            )
        elif platform.system() == 'Darwin':  # macOS
            subprocess.run(['caffeinate', '-d', '-w', str(os.getpid())])
        elif platform.system() == 'Linux':
            subprocess.run([
                'systemd-inhibit', '--what=idle', 'sleep', 'infinity'
            ])

    def allow_sleep(self):
        if platform.system() == 'Windows':
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
        elif platform.system() in ['Darwin', 'Linux']:
            # The subprocess will automatically terminate when the script ends
            pass

    def show_context_menu(self, position):
        context_menu = QMenu(self)
        exit_action = context_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        
        # You can add more menu items here if needed
        # For example:
        # toggle_action = context_menu.addAction("Toggle Animation")
        # toggle_action.triggered.connect(self.toggle_animation)

        context_menu.exec_(self.mapToGlobal(position))

    def update(self):
        if not self.is_dragging and self.state == 0:  # Only move if not being dragged and in idle state
            new_pos = self.pos + self.direction * self.movement_speed
            if self.is_within_screen(new_pos):
                self.pos = new_pos
                self.setGeometry(int(self.pos.x()), int(self.pos.y()), self.pet_width, self.pet_height)
            else:
                self.direction = QPointF(random.uniform(-1, 1), random.uniform(-1, 1))
                self.direction /= math.sqrt(self.direction.x()**2 + self.direction.y()**2)

        if self.meow_timer > 0:
            self.meow_timer -= 1

    def update_animation(self):
        if self.state == 0:  # Idle
            self.i_frame = (self.i_frame + 1) % len(self.idle)
            self.frame = self.idle[self.i_frame]
        elif self.state == 1:  # Transition to sleeping
            if self.i_frame < len(self.idle_to_sleeping) - 1:
                self.i_frame += 1
            self.frame = self.idle_to_sleeping[self.i_frame]
        elif self.state == 2:  # Sleeping
            self.i_frame = (self.i_frame + 1) % len(self.sleeping)
            self.frame = self.sleeping[self.i_frame]
        
        self.label.setPixmap(self.frame)

    def change_state(self):
        if self.state == 0:
            self.state = 1  # Start transition to sleeping
            self.i_frame = 0
        elif self.state == 1:
            self.state = 2  # Start sleeping
            self.i_frame = 0
        else:
            self.state = 0  # Back to idle
            self.i_frame = 0
        
        self.state_timer.start(random.randint(5000, 10000))

    def is_within_screen(self, pos):
        return (0 <= pos.x() <= self.screen_width - self.pet_width and
                0 <= pos.y() <= self.screen_height - self.pet_height)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = True
            self.click_start_pos = event.pos()
            self.window_start_pos = self.pos()
            if self.meow_timer == 0:
                print("Meow!")  # Replace with actual sound playing logic
                self.meow_timer = 50  # Set cooldown for meowing

    def mouseMoveEvent(self, event):
        if self.is_dragging:
            delta = event.pos() - self.click_start_pos
            new_pos = self.window_start_pos + delta
            if self.is_within_screen(new_pos):
                self.pos = new_pos
                self.setGeometry(int(self.pos.x()), int(self.pos.y()), self.pet_width, self.pet_height)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = False

    def closeEvent(self, event):
        self.allow_sleep()
        super().closeEvent(event)



def main():
    app = QApplication(sys.argv)
    cat = CatPet()
    cat.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()