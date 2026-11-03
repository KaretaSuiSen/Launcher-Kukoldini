import os
import sys
from black_jack_k import BlackJackKukoldini

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
    QMessageBox,
)


class Launcher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1024, 1024)
        self.menu = QTabWidget()
        self.name = "???"
        self.setCentralWidget(self.menu)

        self.black_jack = BlackJackKukoldini()
        self.blackjack_tab = QWidget()
        self.black_jack_layout = QGridLayout(self.blackjack_tab)
        self.start_the_gamed = QPushButton("Начать игру", self.blackjack_tab)
        self.start_the_gamed.clicked.connect(self.kukoldini_game)
        self.start_the_gamed.setStyleSheet("padding: 100px")
        self.black_jack_layout.addWidget(
            self.start_the_gamed, 1, 1, Qt.AlignmentFlag.AlignCenter
        )

        checkmates_tab = QWidget()
        self.checkmates_layout = QGridLayout(checkmates_tab)

        self.menu.addTab(self.blackjack_tab, "БлекДжек Куколдини")
        self.menu.addTab(checkmates_tab, "Пешки Куколдини")

    def blackjack_custom(self):
        self.stop = False
        layout = self.black_jack_layout

        p_lo = QVBoxLayout()
        pot = QLabel("Общая ставка")
        pot.setStyleSheet("font-size: 30px")
        pot.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.pot = QLineEdit()
        self.pot.setReadOnly(True)
        p_lo.addWidget(pot)
        p_lo.addWidget(self.pot)
        p_lo.setContentsMargins(10, 10, 10, 50)

        pl_lo = QVBoxLayout()
        self.players_bet_l = QLabel("Баланс ???:")
        self.players_bet_l.setStyleSheet("font-size: 20px")
        self.players_bet_l.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.players_bet = QLineEdit()
        self.players_bet.setReadOnly(True)
        self.players_hand_l = QLabel("Рука ???:")
        self.players_hand_l.setStyleSheet("font-size: 20px")
        self.players_hand_l.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.players_hand = QLabel("")
        self.players_hand.setStyleSheet("font-size: 24px;")
        pl_lo.addWidget(self.players_bet_l)
        pl_lo.addWidget(self.players_bet)
        pl_lo.setContentsMargins(10, 10, 10, 50)

        k_lo = QVBoxLayout()
        kukoldini = QLabel("Баланс ОТЕКА КУКОЛДИНИ:")
        kukoldini.setStyleSheet("font-size: 20px")
        kukoldini.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.kukoldinis_bet = QLineEdit()
        self.kukoldinis_bet.setReadOnly(True)
        self.kukoldinis_hand_l = QLabel("Рука Куколдини")
        self.kukoldinis_hand_l.setStyleSheet("font-size: 20px")
        self.kukoldinis_hand_l.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.kukoldinis_speech = QLabel("")
        self.kukoldinis_speech.setStyleSheet("font-size: 24px;")
        self.kukoldinis_hand = QLabel("")
        self.kukoldinis_hand.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.kukoldinis_hand.setStyleSheet("font-size: 24px;")
        k_lo.addWidget(kukoldini)
        k_lo.addWidget(self.kukoldinis_bet)
        k_lo.setContentsMargins(10, 10, 10, 50)

        self.pass_grabbing = QPushButton("Спасовать")
        self.pass_grabbing.setStyleSheet("padding: 40px; font-size: 24px;")
        self.pass_grabbing.clicked.connect(self.standing)
        self.add_cards_to_deck = QPushButton("Добрать карты")
        self.add_cards_to_deck.setStyleSheet("padding: 40px; font-size: 24px;")
        self.add_cards_to_deck.clicked.connect(self.player_grabbing)
        self.start_the_game = QPushButton("Начать игру")
        self.start_the_game.setStyleSheet("padding: 40px; font-size: 24px;")
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
        layout.addWidget(self.players_hand_l, 1, 0)
        layout.addWidget(self.kukoldinis_hand_l, 1, 2)
        layout.addWidget(self.kukoldinis_speech, 1, 1)
        layout.addWidget(self.players_hand, 2, 0)
        layout.addWidget(self.kukoldinis_hand, 2, 2)
        layout.addWidget(self.pass_grabbing, 4, 0)
        layout.addWidget(self.add_cards_to_deck, 4, 2)
        layout.addWidget(self.start_the_game, 5, 1)
        layout.setRowStretch(3, 1)

    def chackmates_custom(self):
        pass

    def kukoldini_game(self):
        self.name = self.get_players_name()
        self.black_jack.game_starter(self.name)
        if not hasattr(self, "pot"):
            self.blackjack_custom()

        if hasattr(self, "pot"):
            self.reset()

        self.bj_toogler(self.black_jack_layout, True)
        self.start_the_gamed.hide()

        if hasattr(self, "pot"):
            self.update_ui()

        self.start_the_game.setText("Игра в самом разгаре!")
        self.start_the_game.setEnabled(False)
        self.play_round()

    def play_round(self):
        if self.stop:
            return

        self.kukoldinis_speech.setText("")
        self.start_the_game.setEnabled(False)
        self.start_the_game.setText("Игра в самом разгаре!")
        self.add_cards_to_deck.setEnabled(True)
        self.pass_grabbing.setEnabled(True)

        self.black_jack.round_restart()
        self.black_jack.round_starter()

        bet = (-1, True)
        while bet[0] < 100 or not bet[1]:
            bet = QInputDialog.getInt(
                self,
                "Ставки",
                "Ставлю душу своей...",
                500,
                100,
            )
        bet = bet[0]

        verdict = self.black_jack.betting(bet)
        if verdict == "player":
            self.kukoldinis_speech.setText("Ты банкрот! Игра окончена.")
            self.stop = True
            self.add_cards_to_deck.setEnabled(False)
            self.pass_grabbing.setEnabled(False)
            self.new_game_question()

        elif verdict == "dealer":
            self.kukoldinis_speech.setText("Куколдини разорен! Ты сорвал весь куш!")
            self.stop = True
            self.add_cards_to_deck.setEnabled(False)
            self.pass_grabbing.setEnabled(False)
            self.new_game_question()

        self.update_ui()

    def standing(self):
        res = self.black_jack.stand()
        self.update_ui()
        self.kukoldinis_speech.setText(res)
        self.kukoldinis_hand.setText(
            "\n".join(f"[{i}]" for i in self.black_jack.dealers_deck)
        )
        self.round_ending()

    def get_players_name(self):
        name, validation = QInputDialog.getText(
            self, "Введите имя игрока", "Новый Маргинал вступает в игру..."
        )
        if not name or not validation:
            if hasattr(self, "kukoldinis_speech"):
                self.kukoldinis_speech.setText("Назовись, чужак!")
            self.get_players_name()

        if hasattr(self, "kukoldinis_speech"):
            self.kukoldinis_speech.clear()
        return name.strip()

    def player_grabbing(self):
        self.black_jack.player_grabbing()
        self.update_ui()

    def update_ui(self):
        self.players_bet.setText(str(self.black_jack.players_bank))
        self.kukoldinis_bet.setText(str(self.black_jack.dealers_bank))

        self.players_hand.setText(
            "\n".join(f"[{i}]" for i in self.black_jack.players_deck)
        )
        self.kukoldinis_hand.setText(
            "\n".join("[?]" for i in self.black_jack.dealers_deck)
        )

        self.pot.setText(str(self.black_jack.pot))
        self.players_bet_l.setText(f"Баланс {self.name}:")
        self.players_hand_l.setText(f"Рука {self.name}:")

    def reset(self):
        self.kukoldinis_speech.clear()
        self.kukoldinis_bet.clear()
        self.players_bet.clear()
        self.players_hand_l.setText(f"Рука {self.name}")
        self.kukoldinis_hand.clear()
        self.players_hand.clear()
        self.players_bet_l.setText(f"Баланс: {self.name}")
        self.pot.clear()
        self.black_jack.round_restart()
        self.add_cards_to_deck.setEnabled(True)
        self.pass_grabbing.setEnabled(True)
        self.stop = False

    def round_ending(self):
        self.add_cards_to_deck.setEnabled(False)
        self.pass_grabbing.setEnabled(False)
        self.start_the_game.setText("Сыграем еще один раунд?")
        self.start_the_game.setEnabled(True)
        self.start_the_game.clicked.disconnect()
        self.start_the_game.clicked.connect(self.play_round)

    def new_game_question(self):
        answer = QMessageBox.question(
            self,
            "Повторная игра",
            "Сыграем еще?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if answer == QMessageBox.StandardButton.Yes:
            self.reset()
            self.kukoldini_game()
            return

        self.reset()
        self.bj_toogler(self.black_jack_layout, False)
        self.start_the_gamed.show()

    @staticmethod
    def bj_toogler(layout: QGridLayout | QHBoxLayout | QVBoxLayout, visibility: bool):
        if layout is None:
            return

        for widget in range(layout.count()):
            item = layout.itemAt(widget)
            widget = item.widget()

            if widget is not None:
                widget.setVisible(visibility)

            else:
                layout_s = item.layout()
                if layout_s is not None:
                    Launcher.bj_toogler(layout_s, visibility)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Launcher()
    ex.show()
    sys.exit(app.exec())
