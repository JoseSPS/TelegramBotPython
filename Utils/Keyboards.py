from telebot import types

def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    markup.add(types.KeyboardButton('Buscar equipo de computo por marca'))
    markup.add(types.KeyboardButton('Quitar teclado'))
    return markup
def get_clear_keyboard():
    return types.ReplyKeyboardRemove(selective=False)