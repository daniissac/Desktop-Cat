import sys
import random
import math
import platform
import ctypes
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QMenu
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QPixmap, QCursor, QAction


class CatPet(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.prevent_sleep()

    def initUI(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
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
            subprocess.run(['systemd-inhibit', '--what=idle', 'sleep', 'infinity'])

    def allow_sleep(self):
        if platform.system() == 'Windows':
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
        elif platform.system() in ['Darwin', 'Linux']:
            # The subprocess will automatically terminate when the script ends
            pass


def main():
    app = QApplication(sys.argv)
    cat = CatPet()
    cat.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()