import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    FSInputFile,
    InputMediaPhoto
)

# ================= SOZLAMALAR (SHU YERNI O'ZGARTIRING) =================
BOT_TOKEN = "9025226513:AAEqqDwGRjwyDn-oWKUiGe6OSqhsD_s9Jo4"
ADMIN_ID = 8706773769  # @userinfobot bergan o'zingizning raqamli ID ingiz
ADMIN_USERNAME = "@sizning_username"  # Shaxsiy Telegram username ingiz
DEMO_LINK = "https://turkmin.github.io/qada-cloud/"

# PythonAnywhere bepul serveri uchun proksi (agar lokal kompyuterda ishlatsangiz None qiling)
PROXY_URL = "http://proxy.server:3128"
# =====================================================================

logging.basicConfig(level=logging.INFO)

session = AiohttpSession(proxy=PROXY_URL) if PROXY_URL else None
# Shunday holatga o'zgartiring:
bot = Bot(token="9025226513:AAEqqDwGRjwyDn-oWKUiGe6OSqhsD_s9Jo4")
dp = Dispatcher()

# Buyurtma holatlari (FSM)
class OrderForm(StatesGroup):
    tariff = State()
    family_name = State()
    device_type = State()
    phone = State()

# Asosiy menyu tugmalari
def get_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💎 Tariflar va Narxlar"), KeyboardButton(text="🎬 Namuna (Demo) ko‘rish")],
            [KeyboardButton(text="🛒 Buyurtma berish")],
            [KeyboardButton(text="👨‍💻 Admin bilan bog‘lanish")]
        ],
        resize_keyboard=True
    )

# Bekor qilish tugmasi
def get_cancel_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Bekor qilish")]],
        resize_keyboard=True
    )

# 1. /start buyrug'i (har qanday holatda ishlaydi)
@dp.message(CommandStart(), StateFilter("*"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    text = (
        f"Assalomu alaykum, <b>{message.from_user.first_name}</b>! 👋\n\n"
        "👑 <b>«Qada Daftari»</b> — to‘y va marosimlardagi qada-to‘yonalarni "
        "adashmasdan, oson va aniq hisoblab boruvchi zamonaviy ilova.\n\n"
        "Quyidagi bo‘limlardan birini tanlang:"
    )
    await message.answer(text, reply_markup=get_main_menu(), parse_mode="HTML")

# Bekor qilish (har qanday bosqichda buyurtmani to'xtatadi)
@dp.message(F.text == "❌ Bekor qilish", StateFilter("*"))
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Amal bekor qilindi. Asosiy menyudasiz:", reply_markup=get_main_menu())

# 2. Tariflar va Narxlar
@dp.message(F.text == "💎 Tariflar va Narxlar")
async def show_tariffs(message: types.Message):
    text = (
        "💎 <b>«QADA DAFTARI» TARIFLARI:</b>\n\n"
        "1️⃣ <b>OFLAYN TARIF — 150 000 so‘m</b> (bir martalik to‘lov)\n"
        "• Internetsiz ishlaydi (bitta telefon xotirasida saqlanadi)\n"
        "• Kirim-chiqim, valyuta ($), chorva va PDF hisobot\n"
        "• Oilangiz nomi yozilgan shaxsiy Android ilova (.apk)\n\n"
        "2️⃣ <b>OILAVIY BULUTLI TARIF — 250 000 so‘m</b> (bir martalik to‘lov)\n"
        "• <b>Butun oila a'zolari</b> (ota-ona, farzandlar) o‘z telefonidan bitta bazaga ulanadi\n"
        "• Bir telefonda yozilgan qada 1 soniyada boshqalarda ham ko‘rinadi\n"
        "• <b>2 xil kirish kodi:</b> Admin PIN (qo‘shish/o‘chirish) va Kuzatuvchi PIN (faqat ko‘rish)\n"
        "• Telefon yo‘qolsa yoki almashsa ham ma'lumotlar bulutda 100% saqlanadi\n"
        "• Ham <b>Android (.apk)</b>, ham <b>iPhone (iOS)</b> uchun mos!\n\n"
        "3️⃣ <b>VIP / TAYYOR BAZA TARIFI — 450 000 so‘m</b> (bir martalik to‘lov)\n"
        "• «Oilaviy Bulutli» tarifning <b>BARCHA</b> imkoniyatlari\n"
        "• <b>Eski daftar yoki Excel fayldagi barcha qadalaringizni bazaga tayyor kiritib berish</b>\n"
        "• Oila nomiga maxsus dizayndagi <b>individual ilova ikonkasi (logotip)</b>\n"
        "• Ustuvor tezkor texnik yordam\n\n"
        "👇 Buyurtma berish uchun <b>«🛒 Buyurtma berish»</b> tugmasini bosing."
    )
    await message.answer(text, parse_mode="HTML")

# 3. Namuna (Demo) ko'rish — 5 ta rasm + 1 ta video + Demo havola
@dp.message(F.text == "🎬 Namuna (Demo) ko‘rish")
async def show_demo(message: types.Message):
    await message.answer("⏳ Namuna rasmlar va video yuklanmoqda...")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 5 ta rasmni albom qilib yuborish
    media = []
    for i in range(1, 6):
        for ext in [".jpg", ".png", ".jpeg"]:
            img_path = os.path.join(base_dir, f"{i}{ext}")
            if os.path.exists(img_path):
                caption = "📸 Ilova ko‘rinishi va imkoniyatlari" if i == 1 else None
                media.append(InputMediaPhoto(media=FSInputFile(img_path), caption=caption))
                break
    
    if media:
        await message.answer_media_group(media=media)
    
    # Videoni yuborish
    video_path = os.path.join(base_dir, "demo.mp4")
    if os.path.exists(video_path):
        await message.answer_video(
            video=FSInputFile(video_path),
            caption="🎥 Ilovaning ishlash jarayoni (video qo‘llanma)"
        )
    
    demo_text = (
        "🌐 <b>Jonli sinab ko‘rish (Demo versiya):</b>\n"
        f"👉 {DEMO_LINK}\n\n"
        "🔑 <i>Sinov uchun kirish ma'lumotlari:</i>\n"
        "• Email: <code>karimov@qada.uz</code>\n"
        "• Parol: <code>123456</code>\n"
        "• Admin PIN: <code>7777</code> | Kuzatuvchi PIN: <code>1111</code>"
    )
    await message.answer(demo_text, parse_mode="HTML")

# 4. Admin bilan bog'lanish
@dp.message(F.text == "👨‍💻 Admin bilan bog‘lanish")
async def contact_admin(message: types.Message):
    text = (
        "👨‍💻 Savollaringiz bo‘lsa yoki maxsus talablar asosida buyurtma bermoqchi bo‘lsangiz, "
        f"to‘g‘ridan-to‘g‘ri adminga yozing:\n\n👉 {ADMIN_USERNAME}"
    )
    await message.answer(text)

# 5. Buyurtma berish jarayoni (4 qadamli so'rovnoma)
@dp.message(F.text == "🛒 Buyurtma berish")
async def start_order(message: types.Message, state: FSMContext):
    await state.set_state(OrderForm.tariff)
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="1️⃣ Oflayn tarif (150 000 so‘m)")],
            [KeyboardButton(text="2️⃣ Oilaviy Bulutli tarif (250 000 so‘m)")],
            [KeyboardButton(text="3️⃣ VIP / Tayyor baza tarifi (450 000 so‘m)")],
            [KeyboardButton(text="❌ Bekor qilish")]
        ],
        resize_keyboard=True
    )
    await message.answer("1/4. Qaysi tarifni tanlaysiz?", reply_markup=kb)

@dp.message(OrderForm.tariff)
async def process_tariff(message: types.Message, state: FSMContext):
    await state.update_data(tariff=message.text)
    await state.set_state(OrderForm.family_name)
    await message.answer(
        "2/4. Ilova sarlavhasiga qaysi <b>Oila nomi</b> yozilsin?\n"
        "<i>(Masalan: Alimovlar oilasi qada daftari)</i>",
        reply_markup=get_cancel_kb(),
        parse_mode="HTML"
    )

@dp.message(OrderForm.family_name)
async def process_family(message: types.Message, state: FSMContext):
    await state.update_data(family_name=message.text)
    await state.set_state(OrderForm.device_type)
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Android telefon (APK)")],
            [KeyboardButton(text="🍏 iPhone (iOS)"), KeyboardButton(text="📱+🍏 Ikkalasi ham")],
            [KeyboardButton(text="❌ Bekor qilish")]
        ],
        resize_keyboard=True
    )
    await message.answer("3/4. Qanday telefonlarda ishlatasiz?", reply_markup=kb)

@dp.message(OrderForm.device_type)
async def process_device(message: types.Message, state: FSMContext):
    await state.update_data(device_type=message.text)
    await state.set_state(OrderForm.phone)
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 Telefon raqamimni yuborish", request_contact=True)],
            [KeyboardButton(text="❌ Bekor qilish")]
        ],
        resize_keyboard=True
    )
    await message.answer(
        "4/4. Siz bilan bog‘lanishimiz va tayyor ilovani yuborishimiz uchun "
        "<b>telefon raqamingizni</b> yuboring (yoki yozing):",
        reply_markup=kb,
        parse_mode="HTML"
    )

@dp.message(OrderForm.phone)
async def process_phone(message: types.Message, state: FSMContext):
    phone_val = message.contact.phone_number if message.contact else message.text
    data = await state.get_data()
    await state.clear()

    user = message.from_user
    username_str = f"@{user.username}" if user.username else "Username yo‘q"

    # Adminga boradigan tayyor buyurtma varaqasi
    admin_msg = (
        "🚨 <b>YANGI BUYURTMA KELDI!</b>\n\n"
        f"👤 <b>Mijoz:</b> {user.full_name} ({username_str})\n"
        f"📞 <b>Telefon:</b> <code>{phone_val}</code>\n"
        f"💎 <b>Tarif:</b> {data['tariff']}\n"
        f"👑 <b>Oila sarlavhasi:</b> <code>{data['family_name']}</code>\n"
        f"📱 <b>Qurilma:</b> {data['device_type']}\n"
        f"🆔 <b>User ID:</b> <code>{user.id}</code>"
    )

    try:
        await bot.send_message(chat_id=ADMIN_ID, text=admin_msg, parse_mode="HTML")
    except Exception as e:
        logging.error(f"Adminga yuborishda xato: {e}")

    await message.answer(
        "✅ <b>Buyurtmangiz qabul qilindi!</b>\n\n"
        "Tez orada admin siz bilan bog‘lanib, oilangiz uchun maxsus tayyorlangan "
        "ilova va kirish kodlarini yuboradi.",
        reply_markup=get_main_menu(),
        parse_mode="HTML"
    )

async def main():
    while True:
        try:
            print("Qada Daftari buyurtma boti ishga tushdi...")
            await dp.start_polling(bot)
        except Exception as e:
            logging.error(f"Ulanishda xato: {e}. 5 soniyadan keyin qayta urinilmoqda...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
