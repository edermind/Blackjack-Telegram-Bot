import pytest

from cards import Card, Deck, Hand
from game import BUST, BLACKJACK, LOSE, PUSH, WIN, Game


def card(rank, suit="♥"):
    return Card(suit, rank)


def test_card():
    assert card("A").weight == 11
    assert str(card("10", "♠")) == "10♠"


def test_deck():
    deck = Deck(1)
    assert len(deck.cards) == 52
    assert len({str(c) for c in deck.cards}) == 52
    assert isinstance(deck.draw(), Card)
    assert len(deck.cards) == 51


def test_hand_total():
    hand = Hand()
    hand.add(card("A"))
    hand.add(card("K"))
    assert hand.total() == 21
    assert hand.is_blackjack()


def test_hand_ace():
    hand = Hand()
    for rank in ["A", "A", "9"]:
        hand.add(card(rank))
    assert hand.total() == 21


def test_hand_bust():
    hand = Hand()
    for rank in ["K", "Q", "2"]:
        hand.add(card(rank))
    assert hand.total() == 22
    assert hand.is_bust()


def test_hand_str():
    hand = Hand()
    hand.add(card("A"))
    hand.add(card("10", "♠"))
    assert str(hand) == "A♥ 10♠"


def game(player, dealer):
    deck = Deck(1)
    g = Game(deck)
    for rank in player:
        g.player.add(card(rank))
    for rank in dealer:
        g.dealer.add(card(rank))
    return g


def test_finish_blackjack():
    g = game(["A", "K"], ["10", "9"])
    g.finish()
    assert g.result == BLACKJACK

    g = game(["A", "K"], ["A", "K"])
    g.finish()
    assert g.result == PUSH


def test_finish_results():
    g = game(["10", "8"], ["10", "7"])
    g.finish()
    assert g.result == WIN

    g = game(["10", "7"], ["10", "8"])
    g.finish()
    assert g.result == LOSE

    g = game(["10", "8"], ["10", "8"])
    g.finish()
    assert g.result == PUSH

    g = game(["10", "K"], ["10", "10", "5"])
    g.finish()
    assert g.result == WIN


def test_start():
    deck = Deck(1)
    g = Game(deck)
    g.start()
    assert len(g.player.cards) == 2
    assert len(g.dealer.cards) == 2


def test_hit_bust():
    deck = Deck(1)
    g = Game(deck)
    g.player.add(card("K"))
    g.player.add(card("Q"))
    deck.cards = [card("2")]
    g.hit()
    assert g.result == BUST


def test_hit_21():
    deck = Deck(1)
    g = Game(deck)
    g.player.add(card("10"))
    g.player.add(card("9"))
    g.dealer.add(card("10"))
    g.dealer.add(card("8"))
    deck.cards = [card("2")]
    g.hit()
    assert g.result == WIN


def test_stand():
    deck = Deck(1)
    g = Game(deck)
    g.player.add(card("10"))
    g.player.add(card("8"))
    g.dealer.add(card("10"))
    g.dealer.add(card("6"))
    deck.cards = [card("A")]
    g.stand()
    assert g.result == WIN


def test_get_text():
    g = game(["10", "8"], ["10", "7"])
    text = g.get_text()
    assert "🂠" in text
    g.finish()
    text = g.get_text()
    assert "10♥ 7♥" in text
    assert WIN in text
