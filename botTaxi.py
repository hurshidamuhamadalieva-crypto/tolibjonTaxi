import re
import time
import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import Channel, Chat, User

# =================== TELEGRAM API ===================
api_id = 37531523
api_hash = 'b4a9ecb2c20a09c26c1e1bdc110427c2'

# sequential_updates=False -> Telethon bir nechta kelgan xabarni ketma-ket emas,
# balki bir vaqtda (parallel) qayta ishlaydi. Bu botni sezilarli tezlashtiradi,
# chunki guruhlar ko'p bo'lganda xabarlar navbatda kutib turmaydi.
client = TelegramClient(
    'taxi_session',
    api_id,
    api_hash,
    sequential_updates=False,
)

# =================== SKIP CHAT ID ===================
# Ushbu guruh/kanallardagi xabarlar hech qachon tekshirilmaydi.
SKIP_CHAT_IDS = [
    -1004441188512
]

# =================== TARGET CHAT ID ===================
TARGET_CHAT_IDS = [
    -1004441188512
]

# =================== KALIT SO'ZLAR (LOTIN + KIRILL) ===================
# Har bir kategoriya ostida avval qo'lda yozilgan so'zlar, keyin esa
# ularning lotin->kirill (o'zbekcha-kirill) avtomatik yozilishi keladi.

# --- ODAM / KISHI / QIZ / AYOL BOR ---
KEYWORDS_BASE_ODAM_BOR = [
    '1 kishi bor', '1 kishi bor edi', '1 kishi bor ekan', '1 kishi ekan', '1 ta qiz bola bor',
    '1 ta qiz bor', '1 киши бор', '1 та қиз бола бор', '1 та қиз бор',
    '1kishi ayol kishili mashina kerak', '1kishi bor', '1kishi ekan', '1odam bor', '1ta odam bor',
    '1ta qiz bola bor', '1ta qiz bor', '1киши аёл кишили машина керак', '1та одам бор',
    '2 kishi bor edi', '2 kishi bor ekan', '2 kishi ekan', '2 kishimiz', '2 киши бор',
    '2-kishi bor', '2-ta ayolkishi bor', '2-ta kishi bor', '2-ta odam bor', '2kishi bor',
    '2kishi ekan', '2kishimiz', '2ta ayol bor', '2ta odam bor', '2та аёл бор', '2та одам бор',
    '3 kishi bor edi', '3 kishi bor ekan', '3 kishi ekan', '3 kishimiz', '3 киши бор',
    '3-kishi bor', '3-ta ayolkishi bor', '3-ta kishi bor', '3-ta odam bor', '3kishi bor',
    '3kishi ekan', '3kishimiz', '3ta odam bor', '3та одам бор', '4 kishi bor edi',
    '4 kishi bor ekan', '4 kishimiz', '4 odam bor', '4 киши бор', '4 одам бор', '4-kishi bor',
    '4-ta ayolkishi bor', '4-ta kishi bor', '4-ta odam bor', '4kishi bor', '4kishi ekan',
    '4kishimiz', '4ta odam bor', '4та одам бор', 'amirsoydan 1kishi',
    'ayol kishi bor mashina sorashyabdi', 'ayollar bor mashina kerak', 'ayollar bor moshina kerak',
    'bagdodan 1kishi bor', 'bir qiz bir bola bor', 'bitta odam bor', "bog'doddan 2kishi",
    'Chirchiqdan 1 kishi', 'chirchiqdan 1kishi', 'ertagaga qoqonga 1kishi', "farg'onaga 1kishi",
    "farg'onaga 2kishi", "farg'onaga 3kishi", "farg'onaga 4kishi", 'fargonadan 1kishi',
    'fargonaga 2kishi', 'fargonaga odam bor', "g'azalkantdan 2 kishi", "g'azalkentdan 1kishi",
    'gazalkentdan 1kishi', 'gazalkentdan 2kishi', 'ikkita odam bor', 'kampilek odam bor',
    'katta yoshli ayol bor', 'kompilek odam bor', 'komplek odam bor', 'komplekt odam bor',
    "o'zimizdan 1kishi", 'odam bor', 'odam bor 1', 'odam bor 2', 'odam bor 3', 'odam bor 4',
    'odam bor edi', 'odam bor ekan', 'odam borakan', 'odam.bor', 'odambor', 'ozimizdan 1kishi',
    'ozimizdan 2 kishi', 'Qibraydan 1 kishi', 'qiz bola bor', 'qoqondan odam bor',
    'qoqonga 1kishi', 'qoqonga odam bor', 'rishtonga 1kishi', 'rishtonga 1kishi bor',
    'rishtonga 2kishi', 'rishtonga 3kishi', 'rishtonga 4kishi', 'rishtonga bir kishi',
    'rishtonga odam bor', 'tashkentdan rishtonga odam bor', "to'rtta odam bor", 'tortta odam bor',
    'toshkenda odam bor', "toshkendan bog'dodga odam bor", "toshkendan farg'onaga odam bor",
    'Toshkenga 1kishi', 'toshkenga 1kishi bor', 'toshkentdan 1 kishi bering degan',
    
]

# --- MASHINA / MOSHINA KERAK ---
KEYWORDS_BASE_MASHINA_KERAK = [
    'bagajli mashina kerak', 'bosh mashina bormi', 'bosh mashina kerak', 'jentra kerak',
    'kobalt kerak', 'mashina izlayapman', 'mashina kera', 'mashina keraa', 'mashina kerak',
    'mashina kerak edi', 'mashina kere', 'mashina kerek', 'mashina topaman', 'moshina kerak',
    'pustoy mashina kerak', 'yengil mashina kerak', 'багажли машина керак', 'бош машина борми',
    'бош машина керак', 'джентра керак', 'енгил машина керак', 'машина бор', 'машина излаяпман',
    'машина керeк', 'машина керак', 'машина кере', 'мошина керак', 'пустой машина керак',
]

# --- POCHTA / DOSTAVKA ---
KEYWORDS_BASE_POCHTA_DOSTAVKA = [
    'dastafka', 'dastafka bor', 'dastavka bor', 'dostavka bor', 'pochta bor', 'pochta bormi',
    'pochta kerak', 'pochta ketadi', 'pochta olib ketadi', 'даставка бор', 'доставка бор',
    'почта бор', 'почта керак', 'почта кетади', 'почта олиб кет', 'почта олиб кетади', 'пошта бор',
    'риштонга почта бор', 'риштондан почта бор', 'тошкентга почта бор', 'тошкентдан почта бор',
]

# --- KETADI / KETMOQCHI ---
KEYWORDS_BASE_KETADI_BOSHQA = [
    'bagdodga ketishi kerak', 'ketadi', 'ketishi kerak', 'ketvotti', 'toshkentga ketaman',
    'бағдодга кетиши керак', 'кетади', 'кетвотти', 'кетиши керак', 'тошкентга кетаман',
]

KEYWORDS_BASE = (
    KEYWORDS_BASE_ODAM_BOR +
    KEYWORDS_BASE_MASHINA_KERAK +
    KEYWORDS_BASE_POCHTA_DOSTAVKA +
    KEYWORDS_BASE_KETADI_BOSHQA 
)
# Quyidagilar - yuqoridagi lotincha so'zlarning kirillcha (o'zbek-kirill)
# ko'rinishi, avtomatik harf-ma-harf o'giril(transliteratsiya qilin)gan va
# faqat mavjud bo'lmagan (hali ro'yxatda yo'q) so'zlargina qo'shilgan.

# --- MASHINA / MOSHINA KERAK — kirillcha ---
KEYWORDS_TRANSLIT_MASHINA_KERAK = [
    'жентра керак', 'йенгил машина керак', 'кобалт керак', 'машина кера', 'машина кераа',
    'машина керак еди', 'машина керек', 'машина топаман',
]

# --- POCHTA / DOSTAVKA — kirillcha ---
KEYWORDS_TRANSLIT_POCHTA_DOSTAVKA = [
    'дастафка', 'дастафка бор', 'почта борми',
]

# --- KETADI / KETMOQCHI — kirillcha ---
KEYWORDS_TRANSLIT_KETADI_BOSHQA = [
    'багдодга кетиши керак',
]



KEYWORDS_TRANSLIT = (
    KEYWORDS_TRANSLIT_MASHINA_KERAK +
    KEYWORDS_TRANSLIT_POCHTA_DOSTAVKA +
    KEYWORDS_TRANSLIT_KETADI_BOSHQA 
)

# Ikkala ro'yxatni (lotincha + kirillcha) birlashtiramiz va aniq takrorlarni olib tashlaymiz.
KEYWORDS = list(dict.fromkeys(KEYWORDS_BASE + KEYWORDS_TRANSLIT))

KEYWORDS_RE = re.compile("|".join(re.escape(k) for k in KEYWORDS), re.IGNORECASE)

# =================== TELEFON REGEX ===================
PHONE_RE = re.compile(r'(\+?998[\d\-\s\(\)]{9,15}|9\d{8})')


def normalize_phone(raw):
    digits = re.sub(r'\D', '', raw)
    if digits.startswith('998') and len(digits) >= 12:
        return '+' + digits[:12]
    if len(digits) == 9:
        return '+998' + digits
    return None


def get_username(user):
    """Foydalanuvchi username'ini qaytaradi.

    Telegram endi bitta akkauntda bir nechta username bo'lishiga ruxsat beradi.
    Bunday hollarda eski `.username` maydoni bo'sh (None) bo'lib qolishi mumkin,
    lekin haqiqiy username `.usernames` ro'yxatida turadi. Aynan shu sabab
    ba'zida username bor bo'lsa ham bot uni "Berkitilgan" deb ko'rsatgan.
    """
    uname = getattr(user, 'username', None)
    if uname:
        return uname
    usernames = getattr(user, 'usernames', None)
    if usernames:
        for u in usernames:
            if getattr(u, 'username', None):
                return u.username
    return None


def build_message_link(chat_id, chat_username, msg_id):
    """Xabarga to'g'ridan-to'g'ri o'tadigan havolani tuzadi.

    - Ochiq (username'li) guruh/kanal bo'lsa -> https://t.me/username/msg_id
    - Yopiq (username'siz) super-guruh/kanal bo'lsa -> https://t.me/c/ID/msg_id
      (bu havola faqat shu guruh a'zosi bo'lgan akkauntlarda ochiladi)
    - Oddiy (eski turdagi) guruhlarda xabarga to'g'ridan-to'g'ri havola bo'lmaydi.
    """
    if chat_username:
        return f"https://t.me/{chat_username}/{msg_id}"
    chat_id_str = str(chat_id)
    if chat_id_str.startswith('-100'):
        internal_id = chat_id_str[4:]
        return f"https://t.me/c/{internal_id}/{msg_id}"
    return None


# =================== KESH (TEZLIK UCHUN) ===================
# Har bir xabar uchun guruh va yuboruvchi ma'lumotini qaytadan so'rab
# o'tirmaslik uchun keshlab qo'yamiz - bu botni sezilarli tezlashtiradi.
CHAT_CACHE = {}
CHAT_CACHE_TIME = {}
SENDER_CACHE = {}
SENDER_CACHE_TIME = {}
CACHE_TTL = 1800  # 30 daqiqa - shundan keyin ma'lumot qayta yangilanadi
MAX_SENDER_CACHE = 8000  # xotira shishib ketmasligi uchun chegara


async def get_chat_info(event):
    chat_id = event.chat_id
    now = time.time()
    cached = CHAT_CACHE.get(chat_id)
    if cached and now - CHAT_CACHE_TIME.get(chat_id, 0) < CACHE_TTL:
        return cached

    chat = await event.get_chat()
    info = {
        'title': getattr(chat, 'title', 'Nomaʼlum guruh'),
        'username': getattr(chat, 'username', None),
    }
    CHAT_CACHE[chat_id] = info
    CHAT_CACHE_TIME[chat_id] = now
    return info


async def get_sender_info(event):
    sender_id = event.sender_id
    if sender_id is None:
        return None

    now = time.time()
    cached = SENDER_CACHE.get(sender_id)
    if cached and now - SENDER_CACHE_TIME.get(sender_id, 0) < CACHE_TTL:
        return cached

    sender = await event.get_sender()
    if sender is None:
        return None

    if len(SENDER_CACHE) > MAX_SENDER_CACHE:
        SENDER_CACHE.clear()
        SENDER_CACHE_TIME.clear()

    info = {
        'id': sender_id,
        'is_user': isinstance(sender, User),
        'username': get_username(sender),
        'phone': getattr(sender, 'phone', None),
    }
    SENDER_CACHE[sender_id] = info
    SENDER_CACHE_TIME[sender_id] = now
    return info


# =================== HANDLER ===================
@client.on(events.NewMessage(incoming=True))
async def handler(event):
    try:
        # 🔥 ULANGAN SESSIYA A'ZO BO'LGAN BARCHA GURUH VA KANALLAR TEKSHIRILADI
        # (shaxsiy chatlar bundan mustasno)
        if not (event.is_group or event.is_channel):
            return

        chat_id = event.chat_id
        if chat_id in SKIP_CHAT_IDS:
            return

        text = event.raw_text
        if not text or not KEYWORDS_RE.search(text):
            return

        chat_info, sender_info = await asyncio.gather(
            get_chat_info(event),
            get_sender_info(event),
        )

        group_name = chat_info['title']

        if sender_info:
            username = sender_info['username']
            owner_display = f"@{username}" if username else "Berkitilgan"

            if sender_info['is_user']:
                profile_link = f"<a href='tg://user?id={sender_info['id']}'>Profilga o'tish</a>"
            elif username:
                profile_link = f"<a href='https://t.me/{username}'>Profilga o'tish</a>"
            else:
                profile_link = None

            phone = normalize_phone(sender_info['phone']) if sender_info['phone'] else None
        else:
            # Anonim admin nomidan yozilgan xabar (guruh nomidan yuborilgan)
            post_author = getattr(event.message, 'post_author', None)
            owner_display = post_author if post_author else "Anonim (guruh nomidan)"
            profile_link = None
            phone = None

        if not phone:
            for m in PHONE_RE.finditer(text):
                phone = normalize_phone(m.group(0))
                if phone:
                    break

        phone_display = phone if phone else "Berkitilgan"

        msg_link = build_message_link(chat_id, chat_info['username'], event.id)

        lines = [
            "",
            f"📝  <b>Elon:</b> {text}",
            "",
            f"📍  <b>Guruh:</b> {group_name}",
            "",
            f"  <b>User:</b> {owner_display}",
            "",
            f"  <b>Raqam:</b> {phone_display}",
            "",
        ]
        if msg_link:
            lines.append(f" <a href='{msg_link}'>Xabarga o'tish</a>")
        if profile_link:
            lines.append(f" {profile_link}")

        message_text = "\n".join(lines)

        # Barcha manzillarga bir vaqtning o'zida (parallel) yuboriladi - tezroq.
        await asyncio.gather(*[
            client.send_message(target_id, message_text, parse_mode='html', link_preview=False)
            for target_id in TARGET_CHAT_IDS
        ])
        print(f"📨 Yuborildi -> {len(TARGET_CHAT_IDS)} ta manzil")

    except Exception as e:
        print("❌ Xatolik:", e)


# =================== KESHNI ISHGA TUSHIRISHDA TO'LDIRISH ===================
async def warm_up_cache():
    """Sessiya a'zo bo'lgan barcha guruh/kanallarni oldindan keshga oladi.

    Shu tufayli birinchi mos xabar kelganda ham guruh nomini/username'ini
    qayta so'rab o'tirmay, darhol javob beradi - bu tezlikni oshiradi va
    ayni paytda barcha ulangan guruh/kanallar nazoratda ekanini kafolatlaydi.
    """
    count = 0
    async for dialog in client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, (Channel, Chat)):
            CHAT_CACHE[dialog.id] = {
                'title': getattr(entity, 'title', 'Nomaʼlum guruh'),
                'username': getattr(entity, 'username', None),
            }
            CHAT_CACHE_TIME[dialog.id] = time.time()
            count += 1
    return count


async def cache_refresher():
    """Guruh nomi/username o'zgarishi yoki yangi guruhga qo'shilish holatlarini
    hisobga olish uchun keshni har 15 daqiqada yangilab turadi."""
    while True:
        await asyncio.sleep(900)
        try:
            count = await warm_up_cache()
            print(f"🔄 Kesh yangilandi: {count} ta guruh/kanal")
        except Exception as e:
            print("⚠️ Kesh yangilashda xatolik:", e)


# =================== START ===================
async def main():
    await client.start()
    count = await warm_up_cache()
    print(f"🚕 Taxi bot ishga tushdi... {count} ta guruh/kanal nazoratga olindi.")
    asyncio.create_task(cache_refresher())
    await client.run_until_disconnected()


client.loop.run_until_complete(main())
