from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import logging
import os
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TELEGRAM_TOKEN = os.getenv('tlgtoken')

app_bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text('Hola  leyendo mi token dese env')
  
  

  

app_bot.add_handler(CommandHandler('start', start))

app_bot.run_polling()

  
@app.route('/webhook', methods=['POST'])
def webhook():
  update = request.get_json()
  app_bot.process_update(Update.de_json(update, app_bot.bot))
  return '', 200


if __name__ == '__main__':
  app.run(port=5000)


# import atexit
# @atexit.register
# def close_connection():
#   cursor.close()
#   conn.close()
  
