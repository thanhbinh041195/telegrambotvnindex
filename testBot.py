from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

async def sendMessage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def sendPhoto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    imgUrl = 'https://i.imgflip.com/2xc9z0.png'
    await update.message.reply_photo(imgUrl)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)

app = ApplicationBuilder().token("6142347342:AAFRf3sBShXSrjx0W3n533XfPGx7quFpAbQ").build()

app.add_handler(CommandHandler("hello", sendMessage))
app.add_handler(CommandHandler("sendPhoto", sendPhoto))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

app.run_polling()