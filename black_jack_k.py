import random as rand


class BlackJackKukoldini:
    # Словарь номиналов карт
    WORTH = {
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 10,
        "Q": 10,
        "K": 10,
        "A": 11,
        "KUKOLDINI": 21,
    }

    @staticmethod
    def generate_deck() -> list[str]:
        """Генерирует колоду из 5 стандартных мастей + спецкарты."""
        ranks = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        deck = ranks * 5  # 5 наборов базовых карт
        deck.extend(["KUKOLDINI"] * 5)  # 5 карт Куколдини
        rand.shuffle(deck)
        return deck

    def game_starter(self, name):
        self.player_name = name
        self.deck = self.generate_deck()
        self.players_bank = 10000
        self.dealers_bank = 10000
        self.pot = 0
        self.over = False

    def round_starter(self):
        if len(self.deck) < 15:
            self.deck = self.generate_deck()

        self.players_deck = []
        self.dealers_deck = []
        self.over = False
        self.pot = 0

        self.starter_deal()

    def starter_deal(self):
        for _ in range(2):
            self.players_deck.append(self.deck.pop())
            self.dealers_deck.append(self.deck.pop())

    def player_grabbing(self):
        if self.over:
            return False
        
        self.players_deck.append(self.deck.pop())

        if self.conver(self.players_deck) > 21:
            self.over = True
            return False
        
        return True

    def dealer_grabbing(self):
        while self.conver(self.dealers_deck) < 18:
            self.dealers_deck.append(self.deck.pop())

    def stand(self):
        self.over = True
        self.dealer_grabbing()
        return self.validation()

    def conver(self, deck):
        score = 0
        for card in deck:
            score += self.WORTH[card]

        print(score)
        return score

    def validation(self):
        p_score = self.conver(self.players_deck)
        d_score = self.conver(self.dealers_deck)

        if 'KUKOLDINI' in self.players_deck:
            return f"Победа {self.player_name}!"
        
        if 'KUKOLDINI' in self.dealers_deck:
            return "Куколдини выиграл эту партию!"

        if p_score > 21:
            self.dealers_bank += self.pot
            return "Перебор! Куколдини забирает банк."

        if d_score > 21:
            self.players_bank += self.pot
            return f"{self.player_name} победил! Куколдини перебрал."

        if p_score > d_score:
            self.players_bank += self.pot
            return f"Победа {self.player_name}!"

        if d_score > p_score:
            self.dealers_bank += self.pot
            return "Куколдини выиграл эту партию."

        self.dealers_bank += self.pot // 2
        self.players_bank += self.pot // 2
        return "Ничья! Банк возвращается."
    
    def round_restart(self):
        if self.players_bank <= 0:
            return 'player'
        
        elif self.dealers_bank <= 0:
            return 'dealer'
        
        self.dealers_deck = []
        self.players_deck = []
        self.pot = 0
        self.over = False
    
    def betting(self, bet=500):
        bet = min(bet, self.players_bank, self.dealers_bank)
        
        if self.players_bank == 0:
            return 'player'
        
        elif self.dealers_bank == 0:
            return 'dealer'
        
        self.players_bank -= bet
        self.dealers_bank -= bet
        self.pot = bet * 2
