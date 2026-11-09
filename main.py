import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

BOT_TOKEN = "9207194444:AAFbuZLm_iH6Cn-oaosmsuCW8gAujDgdazI"
ADMIN_ID = 1872175086

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Tortlar katalogi
CAKES_MENU = {
    "red_velvet": {
        "name": "🔴 Red Velvet (Qizil Barsxat)",
        "price": "150,000 so'm",
        "description": "Mayin biskvit va pishloqli (cream cheese) krem aralashmasi."
    },
    "medovik": {
        "name": "🍯 Medovik (Asalli tort)",
        "price": "120,000 so'm",
        "description": "Tabiiy asal va sariyog'li krem bilan tayyorlangan klassik tort."
    },
    "napoleon": {
        "name": "🥐 Napoleon",
        "price": "130,000 so'm",
        "description": "Qat-qat xamir va zavarnoy (pishirilgan) krem uyg'unligi."
    },
    "snickers": {
        "name": "🥜 Snickers Tort",
        "price": "160,000 so'm",
        "description": "Shokoladli biskvit, arab yong'og'i va karamel bilan."
    },
    "tiramisu": {
        "name": "☕ Tiramisu",
        "price": "170,000 so'm",
        "description": "Italiya uslubidagi maskarpone pishlog'i va kofe ta'mli desert."
    },
    "fruity": {
        "name": "🍓 Mevali Tort",
        "price": "140,000 so'm",
        "description": "Yengil biskvit, qaymoqli krem va yangi uzilgan mevalar bilan."
    }
}

def get_menu_keyboard():
    buttons = []
    for cake_id, cake_info in CAKES_MENU.items():
        buttons.append([InlineKeyboardButton(text=cake_info["name"], callback_data=f"cake_{cake_id}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        f"Assalomu alaykum, {message.from_user.first_name}! 👋\n\n"
        "Shirinliklar va tortlar menyusiga xush kelibsiz. Qaysi tort haqida ma'lumot olmoqchisiz?",
        reply_markup=get_menu_keyboard()
    )

@dp.callback_query(F.data.startswith("cake_"))
async def show_cake_info(callback: CallbackQuery):
    cake_id = callback.data.split("_")[1]
    cake = CAKES_MENU.get(cake_id)
    if cake:
        text = (
            f"<b>{cake['name']}</b>\n\n"
            f"📝 <b>Tavsif:</b> {cake['description']}\n"
            f"💰 <b>Narxi:</b> {cake['price']}"
        )
        back_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Menyuga qaytish", callback_data="back_to_menu")]
        ])
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_kb)
    await callback.answer()

@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "Tortlar menyusi:",
        reply_markup=get_menu_keyboard()
    )
    await callback.answer()

async def main():
    print(f"Bot ishga tushdi... Admin ID: {ADMIN_ID}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
