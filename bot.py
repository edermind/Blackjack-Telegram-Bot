import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import key
from cards import Deck
from game import Game

dp = Dispatcher()

games = {}  # user_id -> текущая игра
decks = {}  # user_id -> колода игрока


def play_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🃏 Ещё", callback_data="hit"),
        InlineKeyboardButton(text="✋ Хватит", callback_data="stand"),
    ]])


def new_game_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🔄 Новая игра", callback_data="new"),
    ]])


def start_new_game(user_id):
    deck = decks.get(user_id)
    if deck is None or len(deck.cards) < 60:
        deck = Deck()
        decks[user_id] = deck

    game = Game(deck)
    game.start()
    games[user_id] = game

    if game.is_over():
        keyboard = new_game_keyboard()
    else:
        keyboard = play_keyboard()
    return game.get_text(), keyboard


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Это игра в 21 (блэкджек), дилер - я.\n"
        "Блэкджек платит 3:2, дилер берёт до 17.\n\n"
        "Чтобы начать, напиши /play"
    )


@dp.message(Command("play"))
async def cmd_play(message: Message):
    text, keyboard = start_new_game(message.from_user.id)
    await message.answer(text, reply_markup=keyboard)


@dp.message()
async def delete_user_message(message: Message):
    if message.from_user.id not in games:
        return
    try:
        await message.delete()
    except TelegramAPIError:
        pass


@dp.callback_query(F.data == "new")
async def on_new(call: CallbackQuery):
    text, keyboard = start_new_game(call.from_user.id)
    await call.message.edit_text(text, reply_markup=keyboard)
    await call.answer()


@dp.callback_query(F.data.in_(["hit", "stand"]))
async def on_move(call: CallbackQuery):
    game = games.get(call.from_user.id)
    if game is None or game.is_over():
        await call.answer("Игра не активна, напиши /play")
        return

    if call.data == "hit":
        game.hit()
    else:
        game.stand()

    if game.is_over():
        keyboard = new_game_keyboard()
    else:
        keyboard = play_keyboard()

    await call.message.edit_text(game.get_text(), reply_markup=keyboard)
    await call.answer()


async def main():
    bot = Bot(token=key)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
