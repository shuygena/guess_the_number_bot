import random

from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from aiogram.dispatcher.filters import Text


# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather
BOT_TOKEN : str = 'BOT TOKEN HERE'

bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher(bot)

ATTEMPTS : int = 7

user : dict = {'in_game': False,
               'secret_number': None,
               'attempts': None,
               'total_games': 0,
               'wins': 0}

def get_random_number() -> int:
    return random.randint(1, 100)


\async def process_start_command(message: Message):
    await message.answer('Привет!\nДавай сыграем в игру "Угадай число"?\n\nЧтобы получить правила игры и список доступных команд - отправьте команду /help')


async def process_help_command(message: Message):
    await message.answer(f'Правила игры:\n\nЯ загадываю число от 1 до 100, а вам нужно его угадать\nУ вас есть {ATTEMPTS} попыток\n\nДоступные команды:\n/help - правила игры и список команд\n/cancel - выйти из игры\n/stat - посмотреть статистику\n\nДавай сыграем?')

async def process_stat_command(message: Message):
    await message.answer(f'Всего игр сыграно: {user["total_games"]}\nИгр выиграно: {user["wins"]}')

async def process_cancel_command(message: Message):
    if user['in_game']:
        await message.answer('Вы вышли из игры. Если захотите сыграть снова - напишите об этом')
        user['in_game'] = False
    else:
        await message.answer('А мы итак с вами не играем. Может, сыграем разок?')

async def process_positive_answer(message: Message):
    if not user['in_game']:
        await message.answer('Ура!\n\nЯ загадал число от 1 до 100, попробуй угадать!')
        user['in_game'] = True
        user['secret_number'] = get_random_number()
        user['attempts'] = ATTEMPTS
    else:
        await message.answer('Пока мы играем в игру я могу реагировать только на числа от 1 до 100 и команды /cancel и /stat')

async def process_negative_answer(message: Message):
    if not user['in_game']:
        await message.answer('Жаль :(\n\nЕсли захотите поиграть - просто напишите об этом')
    else:
        await message.answer('Мы же сейчас с вами играем. Присылайте, пожалуйста, числа от 1 до 100')

async def process_numbers_answer(message: Message):
    if user['in_game']:
        if int(message.text) == user['secret_number']:
            await message.answer('Ура!!! Вы угадали число!\n\nМожет, сыграем еще?')
            user['in_game'] = False
            user['total_games'] += 1
            user['wins'] += 1
        elif int(message.text) > user['secret_number']:
            await message.answer('Мое число меньше')
            user['attempts'] -= 1
        elif int(message.text) < user['secret_number']:
            await message.answer('Мое число больше')
            user['attempts'] -= 1
        
        if user['attempts'] == 0:
            await message.answer(f'К сожалению, у вас больше не осталось попыток. Вы проиграли :(\n\nМое число было {user["secret_number"]}\n\nДавайте сыграем еще?')
            user['in_game'] = False
            user['total_games'] += 1
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')

async def process_other_text_answers(message: Message):
    if user['in_game']:
        await message.answer('Мы же сейчас с вами играем. Присылайте, пожалуйста, числа от 1 до 100')
    else:
        await message.answer('Я довольно ограниченный бот, давайте просто сыграем в игру?')

dp.register_message_handler(process_start_command, commands='start')
dp.register_message_handler(process_help_command, commands='help')
dp.register_message_handler(process_stat_command, commands='stat')
dp.register_message_handler(process_cancel_command, commands='cancel')
dp.register_message_handler(process_positive_answer, Text(equals=['Да', 'Давай', 'Сыграем', 'Игра', 'Играть', 'Хочу играть'], ignore_case=True))
dp.register_message_handler(process_negative_answer, Text(equals=['Нет', 'Не', 'Не хочу'], ignore_case=True))
dp.register_message_handler(process_numbers_answer, lambda x: x.text.isdigit() and 1 <= int(x.text) <= 100)
dp.register_message_handler(process_other_text_answers)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)