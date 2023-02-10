from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import requests
from bs4 import BeautifulSoup

def getSymbolPrice(symbol:str):
    url = 'https://www.fireant.vn/api/Data/Markets/Quotes?symbols=' + symbol.upper()

    #request and parse json data
    data = requests.get(url).json()

    #parse data
    companyName = data[0]['Name']
    currentPrice = "{:,.0f}".format(data[0]['PriceCurrent'])
    currentPercent = round(data[0]['PricePercentChange'] * 100, 2)
    volume = "{:,.0f}".format(data[0]['TotalVolume'])

    #symbol infor
    infor = '🗂 ' + companyName + '\n' + '🔎 Gía cổ phiếu #{}: {} ({}%)'.format(symbol.upper(), currentPrice, currentPercent) + '\n📊 ' 'Khối lượng: {}'.format(volume)
    return infor

def getSymbolInfor(symbol:str):
    url = 'https://www.fireant.vn/api/Data/Companies/CompanyInfo?symbol=' + symbol.upper()

    #request and parse json data
    data = requests.get(url).json()

    #parse data
    companyName = data['CompanyName']
    companyHistory = BeautifulSoup(data['History']) #companyHistory.get_text()
    companyOverView = data['Overview']

    infor = '🗂 Thông tin {}:'.format(companyName) + '\n' + '{}'.format(companyOverView)

    return infor

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #Echo a message from any user
    await update.message.reply_text(update.message.text)

async def symbolPrice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    symbolName = update.effective_message.text[7:10]
    r = getSymbolPrice(symbolName)
    #print(update)
    await update.message.reply_text(r)

async def symbolInfor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    symbolName = update.effective_message.text[6:9]
    r = getSymbolInfor(symbolName)
    #print(update)
    await update.message.reply_text(r)    

app = ApplicationBuilder().token("5873449023:AAFp-mOXtxEN1OfDgck2MCKNs2qAaBpOKQc").build()

app.add_handler(CommandHandler("price", symbolPrice))
app.add_handler(CommandHandler("info", symbolInfor))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

app.run_polling()