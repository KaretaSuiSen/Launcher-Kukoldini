import os
import sys

from black_jack_k import BlackJackKukoldini
from database import DataBaseManager
from kukoldini_chess import Kukoldini_Pawns
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenuBar,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class Launcher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1024, 1024)
        self.menu = QTabWidget()
        self.db_manager = DataBaseManager("stats.sqlite3")
        self.name = "???"
        self.setCentralWidget(self.menu)
        self.setWindowTitle("Лаунчер Куколдини")
        need_dir = os.path.dirname(os.path.abspath(__file__))
        icon = os.path.join(need_dir, "imgs\\launcher_kukoldini.png").replace("\\", "/")
        self.setWindowIcon(QIcon(icon))

        self.black_jack = BlackJackKukoldini()
        self.blackjack_tab = QWidget()
        self.black_jack_layout = QGridLayout(self.blackjack_tab)
        self.start_the_gamed = QPushButton("Начать игру", self.blackjack_tab)
        self.start_the_gamed.clicked.connect(self.kukoldini_game)
        self.start_the_gamed.setStyleSheet("""QPushButton {padding: 100px; font-size: 40px; border: 2px solid rgb(190, 150, 4); border-radius: 8px}
                                           QPushButton:hover {background-color: rgba(50, 108, 104, 0.8); border: 2px solid rgb(190, 150, 4); border-radius: 8px}""")
        self.black_jack_layout.addWidget(
            self.start_the_gamed, 1, 1, Qt.AlignmentFlag.AlignCenter
        )

        self.checkmates = Kukoldini_Pawns()
        self.checkmates_tab = QWidget()
        self.checkmates_layout = QGridLayout(self.checkmates_tab)
        self.start_the_gamec = QPushButton("Начать игру", self.checkmates_tab)
        self.start_the_gamec.clicked.connect(self.chess_game)
        self.start_the_gamec.setStyleSheet("""QPushButton {padding: 100px; font-size: 40px; border: 2px solid rgb(190, 150, 4); border-radius: 8px}
                                           QPushButton:hover {background-color: rgba(50, 108, 104, 0.8); border: 2px solid rgb(190, 150, 4); border-radius: 8px}""")
        self.checkmates_layout.addWidget(
            self.start_the_gamec, 1, 1, Qt.AlignmentFlag.AlignCenter
        )
        self.board_buttons = {}

        stats_tab = QWidget()
        self.stats_layout = QVBoxLayout(stats_tab)
        self.game_stats = QMenuBar()
        self.stats_custom()

        self.menu.addTab(self.blackjack_tab, "БлекДжек Куколдини")
        self.menu.addTab(self.checkmates_tab, "Пешки Куколдини")
        self.menu.addTab(stats_tab, "Статистика игрока")

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
        self.pass_grabbing.setStyleSheet("""QPushButton {padding: 40px; font-size: 24px; background-color: rgba(50, 108, 104, 0.5)}
                                        QPushButton:hover {background-color: rgba(50, 108, 104, 0.8); border: 2px solid rgb(190, 150, 4); border-radius: 8px}""")
        self.pass_grabbing.clicked.connect(self.standing)
        self.add_cards_to_deck = QPushButton("Добрать карты")
        self.add_cards_to_deck.setStyleSheet("""QPushButton {padding: 40px; font-size: 24px; background-color: rgba(50, 108, 104, 0.5)}
                                        QPushButton:hover {background-color: rgba(50, 108, 104, 0.8); border: 2px solid rgb(190, 150, 4); border-radius: 8px}""")
        self.add_cards_to_deck.clicked.connect(self.player_grabbing)
        self.start_the_game = QPushButton("Начать игру")
        self.start_the_game.setStyleSheet("""QPushButton {padding: 40px; font-size: 24px; background-color: rgba(50, 108, 104, 0.5)}
                                        QPushButton:hover {background-color: rgba(50, 108, 104, 0.8); border: 2px solid rgb(190, 150, 4); border-radius: 8px}""")
        self.start_the_game.clicked.connect(self.kukoldini_game)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(base_dir, "imgs\\diler.jpg").replace("\\", "/")

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

    def kukoldini_game(self):
        name = self.get_players_name()
        self.name = name
        self.black_jack.game_starter(self.name)
        if not hasattr(self, "pot"):
            self.blackjack_custom()

        if hasattr(self, "pot"):
            self.reset()

        self.name = name

        self.vsblty_toogler(self.black_jack_layout, True)
        self.start_the_gamed.hide()

        if hasattr(self, "pot"):
            self.update_ui()

        self.start_the_game.setEnabled(False)
        self.play_round()

    def play_round(self):
        if self.stop:
            return

        self.kukoldinis_speech.setText("")
        self.start_the_game.setEnabled(False)
        self.start_the_game.setText("Игра в самом разгаре!")
        self.start_the_game.setStyleSheet("""QPushButton {padding: 40px; font-size: 24px; background-color: rgba(50, 108, 104, 0.5); color: rgba(0, 0, 0, 0.8)}
                                          QPushButton:hover {background-color: rgba(50, 108, 104, 0.8); border: 2px solid rgb(190, 150, 4); border-radius: 8px}""")
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
            self.new_game_question_bj()

        elif verdict == "dealer":
            self.kukoldinis_speech.setText("Куколдини разорен! Ты сорвал весь куш!")
            self.stop = True
            self.add_cards_to_deck.setEnabled(False)
            self.pass_grabbing.setEnabled(False)
            self.new_game_question_bj()

        self.update_ui()

    def standing(self):
        res = self.black_jack.stand()
        self.update_ui()
        self.kukoldinis_speech.setText(res)
        self.kukoldinis_hand.setText(
            "\n".join(f"[{i}]" for i in self.black_jack.dealers_deck)
        )
        self.db_manager.add_res(self.name, "black_jack", self.name in res)
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

        self.db_manager.register_or_get_player(name.strip())
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
        self.name = "???"
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
        self.start_the_game.setStyleSheet("""QPushButton {padding: 40px; font-size: 24px; background-color: rgba(50, 108, 104, 0.5)}
                                          QPushButton:hover {background-color: rgba(50, 108, 104, 0.8); border: 2px solid rgb(190, 150, 4); border-radius: 8px}""")
        self.start_the_game.setText("Сыграем еще один раунд?")
        self.start_the_game.setEnabled(True)
        self.start_the_game.clicked.disconnect()
        self.start_the_game.clicked.connect(self.play_round)

    def new_game_question_bj(self):
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
        self.vsblty_toogler(self.black_jack_layout, False)
        self.start_the_gamed.show()

    @staticmethod
    def vsblty_toogler(
        layout: QGridLayout | QHBoxLayout | QVBoxLayout, visibility: bool
    ):
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
                    Launcher.vsblty_toogler(layout_s, visibility)

    def checkmates_custom(self):
        layout = self.checkmates_layout

        for i in range(64):
            btn = QPushButton("")
            btn.clicked.connect(lambda _, square=i: self.cell_clicked(square))
            row, col = i // 8, i % 8
            color = ["white", "black"][(row + col) % 2]
            ss = f"background-color: {color}; color: rgb(190, 150, 4)"
            btn.setFixedSize(70, 70)
            btn.setStyleSheet(ss)
            self.board_buttons[i] = btn
            layout.addWidget(btn, 7 - row + 1, col + 1)

        self.game_dialog = QLabel("")
        self.game_dialog.setStyleSheet("color: rgb(190, 150, 4); font-size: 40px;")
        self.back = QPushButton("БЭК")
        self.back.setStyleSheet("""QPushButton {font-size: 24px; background-color: rgba(50, 108, 104, 0.5)}
                                    QPushButton:hover {background-color: rgba(50, 108, 104, 0.8); border: 2px solid rgb(190, 150, 4); border-radius: 8px}""")
        self.back.setFixedSize(400, 60)
        self.back.clicked.connect(self.backing)
        self.current_player_lbl = QLabel(self.name)

        layout.addWidget(self.game_dialog, 0, 11)
        layout.addWidget(self.back, 1, 11)
        layout.addWidget(self.current_player_lbl, 2, 11)
        layout.setRowStretch(9, 1)
        layout.setColumnStretch(9, 1)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(base_dir, "imgs\\kukoldinis_pawns.jpg").replace(
            "\\", "/"
        )

        self.checkmates_tab.setObjectName("checkmates_tab")

        self.checkmates_tab.setStyleSheet(f"""
            QWidget#checkmates_tab {{
                border-image: url("{img_path}") 0 0 0 0 stretch stretch;
            }}
        """)

    def cell_clicked(self, cell_id):
        if not self.checkmates.playing:
            return

        self.board_update_ui()

        if self.checkmates.current_piece is None:
            possible_steps = self.checkmates.possible_steps(cell_id)
            for move in possible_steps:
                id = move.to_square
                self.board_buttons[id].setStyleSheet(
                    "QPushButton {color: rgb(190, 150, 4);"
                    + " background-color: rgba(73, 209, 0, 0.3);"
                    + " font-size: 36px; font-weight: bold;} QPushButton:hover {border: 2px solid rgb(190, 150, 4)}"
                )
            return

        if self.board.color_at(self.checkmates.current_piece) == self.board.color_at(
            cell_id
        ):
            possible_steps = self.checkmates.possible_steps(cell_id)
            for move in possible_steps:
                id = move.to_square
                self.board_buttons[id].setStyleSheet(
                    "QPushButton {color: rgb(190, 150, 4);"
                    + " background-color: rgba(73, 209, 0, 0.3);"
                    + " font-size: 36px; font-weight: bold;} QPushButton:hover {border: 2px solid rgb(190, 150, 4)}"
                )
            return

        core = self.checkmates.step_validation(self.checkmates.current_piece, cell_id)
        if not core:
            return

        self.board_update_ui()
        res = self.checkmates.game_validate()
        if res:
            self.game_dialog.setText(res)
            if res != "Шах":
                self.new_game_question_chess()

    def chess_game(self):
        self.vsblty_toogler(self.checkmates_layout, True)
        self.checkmates.game_starter()
        self.board = self.checkmates.board
        self.start_the_gamec.hide()
        if self.name == "???":
            self.name = self.get_players_name()

        if not self.board_buttons:
            self.checkmates_custom()
        self.current_player_lbl.setText(self.name)
        self.board_update_ui()

    def backing(self):
        if not self.checkmates.playing:
            return

        if self.board.move_stack:
            self.board.pop()
        self.board_update_ui()

    def board_update_ui(self):
        self.game_dialog.setText(
            f"Сейчас ходят: {['Черные', 'Белые'][self.board.turn]}"
        )
        for square, button in self.board_buttons.items():
            piece = self.board.piece_at(square)
            colorr = ["white", "black"][(square // 8 + square % 8) % 2]
            ss = (
                "QPushButton {"
                + f"background-color: {colorr}; color: rgb(190, 150, 4);"
                + " font-size: 36px; font-weight: bold;} QPushButton:hover {border: 2px solid rgb(190, 150, 4)}"
            )
            if piece:
                button.setText(piece.unicode_symbol())

                button.setStyleSheet(ss)
            else:
                button.setText("")
                button.setStyleSheet(ss)

    def new_game_question_chess(self):
        self.db_manager.add_res(
            self.name, "chess", "Белые" in self.game_dialog.text()
        )
        answer = QMessageBox.question(
            self,
            "Повторная игра",
            "Сыграем еще?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if answer == QMessageBox.StandardButton.Yes:
            self.chess_game()
            return

        self.name = "???"
        self.board_buttons.clear()
        self.vsblty_toogler(self.checkmates_layout, False)
        self.start_the_gamec.show()

    def database_unwraping(self):
        self.stats_table.clearContents()
        self.stats_table.setRowCount(0)

        database = ["chess", "black_jack"][self.sender().text() == "БлэкДжек Куколдини"]
        res = self.db_manager.get_stats(database)
        rows, cols = len(res), 3

        self.stats_table.setRowCount(rows)

        for row in range(rows):
            for col in range(cols):
                item = QTableWidgetItem(str(res[row][col]))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.stats_table.setItem(row, col, item)

    def stats_custom(self):
        games = self.game_stats.addMenu("Игры Куколдини")
        self.bj_data = games.addAction("БлэкДжек Куколдини")
        self.chess_data = games.addAction("Пешки Куколдини")
        self.bj_data.triggered.connect(self.database_unwraping)
        self.chess_data.triggered.connect(self.database_unwraping)
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(3)
        self.stats_table.setHorizontalHeaderLabels(self.db_manager.headers)
        self.stats_table.horizontalHeader().setStretchLastSection(True)
        self.stats_layout.addWidget(self.game_stats)
        self.stats_layout.addWidget(self.stats_table)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Launcher()
    ex.show()
    sys.exit(app.exec())
