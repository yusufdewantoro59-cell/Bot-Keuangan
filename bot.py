from telegram.ext import ApplicationBuilder, MessageHandler, filters
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import re
import os

# ================= CONFIG =================
BOT_TOKEN = os.environ["BOT_TOKEN"]
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
# =========================================

# Google Sheets Auth
import json

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

google_creds = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(
    google_creds, scope
)

client = gspread.authorize(creds)
sheet = client.open_by_key(os.environ["SPREADSHEET_ID"]).sheet1


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
