import chess


class Kukoldini_Pawns:
    @staticmethod
    def board_maker():
        return chess.Board()

    def game_starter(self):
        self.board = self.board_maker()
        self.current_piece = None
        self.playing = True

    def game_validate(self):
        if self.board.is_checkmate():
            self.playing = False
            return f"Шах и Мат. Победа {['белых', 'черных'][self.board.turn]}"

        if self.board.is_check():
            return "Шах"

        if self.board.is_insufficient_material():
            self.playing = False
            return "Недостаточно фигур"

        if self.board.can_claim_threefold_repetition():
            self.playing = False
            return "Троекратное повторение хода"

        if self.board.is_game_over():
            self.playing = False
            return "Игра окончена "

    def step_validation(self, was, will):
        i, n = chess.square_name(was), chess.square_name(will)
        uci = i + n
        move = chess.Move.from_uci(uci)

        piece = self.board.piece_at(was)
        if piece and "18"[self.board.turn] in n and piece.piece_type == chess.PAWN:
            move = chess.Move.from_uci(uci + "q")

        if move in self.board.legal_moves:
            self.board.push(move)
            self.reset_selection()
            return True

        self.reset_selection()
        return False

    def possible_steps(self, index):
        piece = self.board.piece_at(index)
        if piece is None:
            return []

        if piece.color == self.board.turn:
            self.current_piece = index
            return [
                move for move in self.board.legal_moves if move.from_square == index
            ]

        return []

    def reset_selection(self):
        self.current_piece = None
