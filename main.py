from PyQt5.QtWidgets import QApplication
from ui import MusicPlayerUI
import sys

app = QApplication(sys.argv)
window = MusicPlayerUI()
window.show()
sys.exit(app.exec_())
