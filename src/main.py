from PyQt5.QtWidgets import QApplication, QWidget
import sys


def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Clinical Sabah")
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
