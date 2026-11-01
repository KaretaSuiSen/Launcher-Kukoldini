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

    def generate_deck() -> list[str]:
        """Генерирует колоду из 5 стандартных мастей + спецкарты."""
        ranks = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        deck = ranks * 5  # 5 наборов базовых карт
        deck.extend(["KUKOLDINI"] * 5)  # 5 карт Куколдини
        rand.shuffle(deck)
        return deck

    def game_starter(self):
        name = input(
            "Ну что, озорник, готов сыграть по крупному в игру жизни с дилером Куколдини? "
            "Если не боишься, введи свое имя: "
        ).strip()
        print(f"Замечательно, готовься, {name}, игра начинается!\n")

        self.dealers_bank = 10000
        self.players_bank = 10000

    def game(self):
        while self.players_bank > 0 and self.dealers_bank > 0:
            deck = self.generate_deck()
            player_score = 0
            dealer_score = 0

            print("-" * 50)
            print(
                f"Баланс игрока: {self.players_bank} | Баланс дилера: {self.dealers_bank}"
            )

            # --- Ввод ставки ---
            raw_bet = input("Ставь ставки, малыш (или '/exit' для выхода): ").strip()
            if raw_bet == "/exit":
                print("Испугался? Ну бывай!")
                break

            try:
                players_bet = int(raw_bet)
            except ValueError:
                print("Эй, давай без шуточек тут! Вводи целое число.")
                continue

            if players_bet <= 0:
                print("Ставка должна быть больше нуля!")
                continue

            if players_bet > self.players_bank or players_bet > self.dealers_bank:
                print("Мы тут в долг не даем и выше банка не прыгаем!")
                continue

            # Фиксация банка раунда
            pot = players_bet * 2
            self.players_bank -= players_bet
            self.dealers_bank -= players_bet

            if self.players_bank == 0:
                print("Ну наконец-то мы повеселимся! ЭТО ИГРА ПО ВЗРОСЛОМУ (ALL-IN)!")
            elif players_bet >= 5000:
                print("Ставка сделана! Играем по крупному!")
            else:
                print("Да вы посмотрите, у нас тут дилетант!")

            # --- Стартовая раздача (по 2 карты) ---
            print("\nЯ раздаю карты, желаю удачи! Она тебе понадобится.")
            for _ in range(2):
                player_score += self.WORTH[deck.pop()]
                dealer_score += self.WORTH[deck.pop()]

            # Проверка моментального выигрыша (21 очко с раздачи)
            if dealer_score >= 21:
                print(
                    "Сегодня госпожа удача на моей стороне! Это же сам туз 'КУКОЛДИНИ'!"
                )
                self.dealers_bank += pot
                continue
            elif player_score >= 21:
                print("Невероятно, это же сам туз 'КУКОЛДИНИ'! А ты фартовый малый!")
                self.players_bank += pot
                continue

            # --- Ход игрока ---
            print(f"Твой начальный счет: {player_score}")
            while player_score < 21:
                choice = (
                    input(
                        "Добираешь карты? (нажми Enter, чтобы взять / 'нет', чтобы остановиться): "
                    )
                    .lower()
                    .strip()
                )
                if choice == "нет":
                    break

                card = deck.pop()
                player_score += self.WORTH[card]
                print(f"Выпала карта: {card} | Твой счет: {player_score}")

            # --- Ход дилера (если игрок не сгорел) ---
            if player_score <= 21:
                while dealer_score < 18:
                    card = deck.pop()
                    dealer_score += self.WORTH[card]

            # --- Подведение итогов раунда ---
            print("\n" + "=" * 20 + " ВСКРЫВАЕМСЯ " + "=" * 20)
            print(f"Дилер: {dealer_score} | {name}: {player_score}")

            if player_score > 21:
                print("Ха-Ха, перебор! Опыт не пропьешь!")
                self.dealers_bank += pot
            elif dealer_score > 21 or player_score > dealer_score:
                print("А ты не плох, этот раунд за тобой!")
                self.players_bank += pot
            elif player_score < dealer_score:
                print("Ха-Ха, дилер забирает банк!")
                self.dealers_bank += pot
            else:
                print("Ничья! Ставки возвращаются господам игрокам.")
                self.players_bank += players_bet
                self.dealers_bank += players_bet

            # Запрос на продолжение
            again = input("\nНу что, сыграем еще? ('нет' для выхода): ").lower().strip()
            if again == "нет":
                break

        print("\nИгра окончена!")
        print(
            f"Итоговый баланс: {name} — {self.players_bank}, Дилер — {self.dealers_bank}"
        )
