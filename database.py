import sqlite3


class DataBaseManager:
    def __init__(self, name):
        self.db_name = name
        self.headers = ["Имя игрока", "Победы игрока", "Победы Куколдини"]
        with sqlite3.connect(name) as con:
            cur = con.cursor()

            pattern = """
                CREATE TABLE IF NOT EXISTS players_data (
                player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name  TEXT NOT NULL UNIQUE
                );
                CREATE TABLE IF NOT EXISTS black_jack_stats (
                player_id INTEGER PRIMARY KEY,
                player_wins INTEGER DEFAULT 0,
                dealer_wins INTEGER DEFAULT 0,
                FOREIGN KEY (player_id) REFERENCES players_data(player_id)
                );
                CREATE TABLE IF NOT EXISTS chess_stats (
                player_id INTEGER PRIMARY KEY,
                player_wins INTEGER DEFAULT 0,
                dealer_wins INTEGER DEFAULT 0,
                FOREIGN KEY (player_id) REFERENCES players_data(player_id)
                );
            """
            cur.executescript(pattern)

    def register_or_get_player(self, name):
        with sqlite3.connect(self.db_name) as con:
            cur = con.cursor()
            pattern = """
                INSERT OR IGNORE INTO players_data (player_name) VALUES (?)
            """
            cur.execute(pattern, (name,))
            con.commit()

            ptrn = """
                SELECT player_id FROM players_data
                WHERE player_name = ?"""
            row = cur.execute(ptrn, (name,)).fetchone()
            if not row:
                return
            pl_id = row[0]

            cur.execute(
                "INSERT OR IGNORE INTO black_jack_stats (player_id) VALUES (?)",
                (pl_id,),
            )
            cur.execute(
                "INSERT OR IGNORE INTO chess_stats (player_id) VALUES (?)",
                (pl_id,),
            )

    def add_res(self, name, game_type, is_win=True):
        with sqlite3.connect(self.db_name) as con:
            cur = con.cursor()

            tablet_name = ["black_jack_stats", "chess_stats"][game_type == "chess"]
            column_name = ["dealer_wins", "player_wins"][is_win]

            pattern = f"""
                UPDATE {tablet_name}
                SET {column_name} = {column_name} + 1
                WHERE player_id = (SELECT player_id FROM players_data WHERE player_name = ?)
            """

            cur.execute(pattern, (name,))

    def get_stats(self, game_type):
        with sqlite3.connect(self.db_name) as con:
            cur = con.cursor()
            tablet_name = ["black_jack_stats", "chess_stats"][game_type == "chess"]
            pattern = f"""
                SELECT players_data.player_name, {tablet_name}.player_wins, {tablet_name}.dealer_wins FROM {tablet_name}
                LEFT JOIN players_data ON players_data.player_id = {tablet_name}.player_id
            """
            return cur.execute(pattern).fetchall()
