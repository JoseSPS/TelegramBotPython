import telebot
from flask import Flask, request
import os
from Utils.keyboards import get_main_keyboard,get_clear_keyboard

API_TOKEN = 'api-token'

bot = telebot.TeleBot(API_TOKEN)
server = Flask(__name__)

# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bienvenido a FullPcPrinter, elige la opcion '/teclado' para mostrarte ayuda que puedo ofrecerte")

@bot.message_handler(commands=['hola'])
def send_welcome(message):
    bot.reply_to(message, "Hola, esto es un bot de prueba, bienvenido")

@bot.message_handler(commands=['teclado'])
def send_keyboard(message):
    markup = get_main_keyboard()
    bot.send_message(message.chat.id, "Elige una opción: ", reply_markup=markup)

@bot.message_handler(commands=["ayuda"])
def send_help(message):
    mensaje = "/teclado <mostrar acciones> \n /buscar <realizarBusqueda> \nPara mas ayuda contacta al administrador"
    bot.reply_to(message, mensaje)

@bot.message_handler(commands=['buscar'])
def send_message(message):
    consulta = message.text[8:] # POKEMON a buscar
    busqueda = 'https://fullpcprinter.web.app/buscar/%s' %consulta
    bot.reply_to(message,"Checa el siguiente link con tu busqueda \n" + busqueda)

# MENSAJES DEL KEYBOARD
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    text = message.text
    # Busca componente por marca
    if text == "Buscar equipo de computo por marca":
        bot.send_message(message.chat.id, "Ingresa la marca del producto que deseas buscar usando el comando /buscar <marcaProducto>")
    # QUITAR TECLADO
    elif text == "Quitar teclado":
        markup = get_clear_keyboard()
        bot.send_message(message.chat.id,"Escribe /teclado para mostrarlo.", reply_markup=markup)
    else:
        bot.reply_to(message, "No entiendo tu mensaje, escribe /ayuda")

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.send_message(message.chat, id, message.text)
    #bot.reply_to(message, message.text)

@server.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://fullpcprinter.herokuapp.com/' + API_TOKEN)
    return "!", 200

if __name__ == "__main__":
    #bot.polling(True)
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))