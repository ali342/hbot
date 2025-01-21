from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.ext import CallbackContext

from google.oauth2 import service_account
from googleapiclient.discovery import build


TOKEN: Final = '7931945288:AAEftUNVrtYZV-pjp3a1r17VhSd5F2mM6Fs'
BOT_USERNAME: Final = '@DrHabibBot'



# getting google sheets data


# Load credentials from the JSON file
creds = service_account.Credentials.from_service_account_file('cred2.json')

# Build the service
service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()

# get 11 grade info
result11 = sheet.values().get(spreadsheetId='1SyhaZNLxX60qzOAOsBYHCgR5iEqLaHHuQO1jJ4ziphk', range='send11!A1:k10').execute()
values_send11 = result11.get('values', [])

# tiding the data
ind11 = {}                          # getting names of coloumns   not used actually
id_ind11 = -1                        # getting the index of the id coloumn not used also
ids11 = {}
pid_ind11 = -1
for i in range(len(values_send11[0])) :
    if 'id' in values_send11[0][i].lower():
        id_ind11 = i
    elif 'parent' in values_send11[0][i].lower():
        pid_ind11 = i
    ind11[values_send11[0][i]] = i

for row in values_send11 :
    ids11[row[id_ind11]] = {}
    if pid_ind11 != -1 :
        for id in row[pid_ind11].strip().split() :
            ids11[id] = {}

    for i in range(len(row)) :
        ids11[row[id_ind11]][values_send11[0][i]] = row[i]

        if pid_ind11 != -1 :
            for id in row[pid_ind11].strip().split() :
                ids11[id][values_send11[0][i]] = row[i]

print(ids11)
ind11k = list(ind11.keys())
inf11 = """"""   # preparing the names to be shown
for info in ind11k :
    inf11 += info + "\n"

# get 12 grade info
result12 = sheet.values().get(spreadsheetId='1SyhaZNLxX60qzOAOsBYHCgR5iEqLaHHuQO1jJ4ziphk', range='send12!A1:k10').execute()
values_send12 = result12.get('values', [])

# tiding the data
ind12 = {}     # getting names of coloumns
id_ind12 = -1    # getting the index of the id coloumn
ids12 = {}
pid_ind12 = -1
for i in range(len(values_send12[0])) :
    if 'id' in values_send12[0][i].lower():
        id_ind12 = i
    elif 'parent' in values_send12[0][i].lower():
        pid_ind12 = i
    ind12[values_send12[0][i]] = i

for row in values_send12 :
    ids12[row[id_ind12]] = {}

    if pid_ind12 != -1 :
        for id in row[pid_ind12].strip().split() :
            ids12[id] = {}

    for i in range(len(row)) :
        ids12[row[id_ind12]][values_send12[0][i]] = row[i]

        if pid_ind12 != -1 :
            for id in row[pid_ind12].strip().split() :
                ids12[id][values_send12[0][i]] = row[i]
print(ids12)

ind12k = list(ind12.keys())
inf12 = """"""    # preparing the names to be shown
for info in ind12k :
    inf12 += info + "\n"


# this to make the bot answer to normal messages




async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type = update.message.chat.type
    if chat_type == 'private' :
        if str(update.message.chat.id) in ids11 :
            context.user_data['data'] = ids11[str(update.message.chat.id)]
            context.user_data['age'] = 11
            
        elif str(update.message.chat.id) in ids12 :
            context.user_data['data'] = ids12[str(update.message.chat.id)]
            context.user_data['age'] = 12
    print(context.user_data)
    await update.message.reply_text("""    مرحبا, انا الروبوت الخاص بالدكتور حبيب عيسى    """)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type = update.message.chat.type
    if chat_type == 'private' :
        await update.message.reply_text('اذا كنت بتعاني من مشاكل رجاء تواصل معي على الخاص @Habib_issa2003' )

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type = update.message.chat.type
    if chat_type == 'private' :
        if context.user_data['age'] == 11 :
            await update.message.reply_text(f"""المعلومات التالية متوفرة عنك :
            {inf11}""")
            await update.message.reply_text("""  الرجاء كتابة الاختيار """)

        elif context.user_data['age'] == 12 :
            await update.message.reply_text(f"""المعلومات التالية متوفرة عنك :
            {inf12}""")
            await update.message.reply_text("""  الرجاء كتابة الاختيار """)
        else :
            await update.message.reply_text("""  ما الك اسم عندي """)



        
        

# Responses

def handle_response(text:str, context: CallbackContext) -> str:
    processed : str = text.lower().strip()
    print(context.user_data['data'])
    try :
        ans = context.user_data['data'][processed]
        return ans
    except :
        return "هناك خطأ املائي الرجاء إعادة الاختيار"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    message_type: str = update.message.chat.type      # thie tells us what type is the chat (group, private,..)
    text:str = update.message.text 
    print( f'user{update.message.chat.id} : {text} {message_type}' )

    if message_type != 'group' :
        response: str = handle_response(text, context)

    print('bot:' , response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'update {update} caused error {context.error} ')


if __name__ == '__main__' :
    print('starting...')
    app = Application.builder().token(TOKEN).build()

    # commmands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('info', info_command))


    # messages 
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)
    print('polling..')
    app.run_polling(poll_interval=5)






