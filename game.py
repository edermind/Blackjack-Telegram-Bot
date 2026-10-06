from cards import Hand

# результаты раунда
BLACKJACK = "Блэкджек! 🎉"
WIN = "Вы выиграли! ✅"
LOSE = "Вы проиграли ❌"
PUSH = "Ничья 🤝"
BUST = "Перебор! ❌"


class Game:
    def __init__(self, deck):
        self.deck = deck
        self.player = Hand()
        self.dealer = Hand()
        self.result = None

    def is_over(self):
        return self.result is not None

    def start(self):
        for _ in range(2):
            self.player.add(self.deck.draw())
            self.dealer.add(self.deck.draw())
        if self.player.is_blackjack() or self.dealer.is_blackjack():
            self.finish()

    def hit(self):
        if self.is_over():
            return
        self.player.add(self.deck.draw())
        if self.player.is_bust():
            self.result = BUST
        elif self.player.total() == 21:
            self.stand()

    def stand(self):
        if self.is_over():
            return
        while self.dealer.total() < 17:
            self.dealer.add(self.deck.draw())
        self.finish()

    def finish(self):
        player_total = self.player.total()
        dealer_total = self.dealer.total()

        if self.player.is_blackjack() and self.dealer.is_blackjack():
            self.result = PUSH
        elif self.player.is_blackjack():
            self.result = BLACKJACK
        elif self.dealer.is_blackjack():
            self.result = LOSE
        elif self.dealer.is_bust():
            self.result = WIN
        elif player_total > dealer_total:
            self.result = WIN
        elif player_total < dealer_total:
            self.result = LOSE
        else:
            self.result = PUSH

    def get_text(self):
        if self.is_over():
            dealer_cards = str(self.dealer)
            dealer_points = self.dealer.total()
        else:
            first_card = self.dealer.cards[0]
            dealer_cards = str(first_card) + " 🂠"
            dealer_points = first_card.weight

        text = "🎩 Дилер: " + dealer_cards + "\n"
        text += "Очки дилера: " + str(dealer_points) + "\n\n"
        text += "👤 Ваши карты:\n"
        for card in self.player.cards:
            text += str(card) + "\n"
        text += "Ваши очки: " + str(self.player.total())

        if self.is_over():
            text += "\n\n" + self.result
        return text
