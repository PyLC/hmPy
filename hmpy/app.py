import sys
from PyQt5.QtWidgets import QApplication
from hmpy.gui.main_window import MainWindow


class Application(QApplication):
    """The main hmpy application."""

    def __init__(self, args):
        """ Initialize the application.

        :param args: the application arguments
        """
        super().__init__(args)
        self.__main_window = MainWindow()


def main():
    app = Application(sys.argv)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

