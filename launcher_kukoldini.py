import os
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class Launcher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1024, 1024)
        self.menu = QTabWidget()
        self.name = "???"
        self.setCentralWidget(self.menu)

        self.blackjack_tab = QWidget()
        self.black_jack_layout = QGridLayout(self.blackjack_tab)
        self.start_the_game = QPushButton("Начать игру", self.blackjack_tab)
        self.start_the_game.clicked.connect(self.kukoldini_game)
        self.start_the_game.setStyleSheet("padding: 100px")
        self.black_jack_layout.addWidget(
            self.start_the_game, 1, 1, Qt.AlignmentFlag.AlignCenter
        )

        checkmates_tab = QWidget()
        self.checkmates_layout = QGridLayout(checkmates_tab)

        self.menu.addTab(self.blackjack_tab, "БлекДжек Куколдини")
        self.menu.addTab(checkmates_tab, "Пешки Куколдини")

    def blackjack_custom(self):
        layout = self.black_jack_layout

        p_lo = QVBoxLayout()
        pot = QLabel("Общая ставка")
        pot.setStyleSheet("font-size: 20px")
        pot.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.pot = QLineEdit()
        self.pot.setReadOnly(True)
        p_lo.addWidget(pot)
        p_lo.addWidget(self.pot)
        p_lo.setContentsMargins(10, 10, 10, 50)

        pl_lo = QVBoxLayout()
        players_bet = QLabel(self.name)
        players_bet.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.players_bet = QLineEdit()
        self.players_bet.setReadOnly(True)
        players_hand = QLabel(f"Рука {self.name}")
        players_hand.setStyleSheet("font-size: 20px")
        players_hand.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.players_hand = QHBoxLayout()
        pl_lo.addWidget(players_bet)
        pl_lo.addWidget(self.players_bet)
        pl_lo.setContentsMargins(10, 10, 10, 50)

        k_lo = QVBoxLayout()
        kukoldini = QLabel("ОТЕК КУКОЛДИНИ")
        kukoldini.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.kukoldinis_bet = QLineEdit()
        self.kukoldinis_bet.setReadOnly(True)
        kukoldinis_hand = QLabel("Рука Куколдини")
        kukoldinis_hand.setStyleSheet("font-size: 20px")
        kukoldinis_hand.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.kukoldinis_speech = QLabel("")
        self.kukoldinis_hand = QHBoxLayout()
        k_lo.addWidget(kukoldini)
        k_lo.addWidget(self.kukoldinis_bet)
        k_lo.setContentsMargins(10, 10, 10, 50)

        self.place_a_bet = QPushButton("Поставить ставку")
        self.add_cards_to_deck = QPushButton("Добрать карты")
        self.start_the_game = QPushButton("Начать игру")
        self.start_the_game.clicked.connect(self.kukoldini_game)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(base_dir, "diler.jpg").replace("\\", "/")

        self.blackjack_tab.setObjectName("blackjack_tab")

        self.blackjack_tab.setStyleSheet(f"""
            QWidget#blackjack_tab {{
                border-image: url("{img_path}") 0 0 0 0 stretch stretch;
            }}
        """)

        layout.addLayout(pl_lo, 0, 0, Qt.AlignmentFlag.AlignTop)
        layout.addLayout(p_lo, 0, 1, Qt.AlignmentFlag.AlignTop)
        layout.addLayout(k_lo, 0, 2, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(players_hand, 1, 0)
        layout.addWidget(kukoldinis_hand, 1, 2)
        layout.addWidget(self.kukoldinis_speech, 1, 1)
        layout.addLayout(self.players_hand, 2, 0)
        layout.addLayout(self.kukoldinis_hand, 2, 2)
        layout.addWidget(self.place_a_bet, 4, 0)
        layout.addWidget(self.add_cards_to_deck, 4, 2)
        layout.addWidget(self.start_the_game, 5, 1)
        layout.setRowStretch(3, 1)

    def chackmates_custom(self):
        pass

    def kukoldini_game(self):
        self.start_the_game.deleteLater()
        self.name = self.get_players_name()
        self.blackjack_custom()
        self.start_the_game.setText("Игра в самом разгаре!")

    def get_players_name(self):
        name = QInputDialog.getText(
            self, "Введите имя игрока", "Новый Маргинал вступает в игру..."
        )[0].strip()
        if not name:
            self.kukoldinis_speech.setText("Назовись, чужак!")
            self.get_players_name()

        if hasattr(self, "kukoldinis_speech"):
            self.kukoldinis_speech.clear()
        return name


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Launcher()
    ex.show()
    sys.exit(app.exec())
