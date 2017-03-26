import sys
from PyQt5.QtWidgets import QApplication
from hmpy.gui.main_window import MainWindow


class Application(QApplication):
    """The main hmpy application."""

    __main_window = None

    def __init__(self, args):
        """ Initialize the application.

        Args:
            args: the application arguments
        """
        super(Application, self).__init__(args)
        self.__main_window = MainWindow()


def main():
    app = Application(sys.argv)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

