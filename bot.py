from telegram.ext import ApplicationBuilder, MessageHandler, filters
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import re
import os

# ================= CONFIG =================
BOT_TOKEN = os.getenv("8525931178:AAEWtI15q0sCQektc8-vZNmlmI58gWiXSr4")
SPREADSHEET_ID = os.getenv("1a2Pl4rDePzjT-9igq_7F0xRVY2-uI8sSIyh53PoRqds")
# =========================================

# Google Sheets Auth
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

def parse_message(text):
    text = text.lower()

    angka = re.findall(r"\d+", text)
    nominal = int(angka[-1]) if angka else 0

    if "makan" in text:
        kategori = "Makan"
    elif "bensin" in text:
        kategori = "Transport"
    elif "kopi" in text:
        kategori = "Minuman"
    else:
        kategori = "Lainnya"

    return kategori, nominal, text

async def handle_message(update, context):
    text = update.message.text

    kategori, nominal, deskripsi = parse_message(text)
    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M")

    sheet.append_row([tanggal, kategori, nominal, deskripsi])

    await update.message.reply_text(
        f"✅ Dicatat\n"
        f"Kategori: {kategori}\n"
        f"Nominal: Rp{nominal:,}"
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("Bot berjalan & siap mencatat pengeluaran...")
    app.run_polling()

if __name__ == "__main__":
    main()
