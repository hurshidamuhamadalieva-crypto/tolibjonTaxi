import re
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# =================== TELEGRAM API ===================
api_id = 38017100
api_hash = '0d1ee14a452e04c86c4dd37709bb7a2f'

# =================== TELEGRAM CLIENT ===================
from telethon.sessions import StringSession

SESSION = "1ApWapzMBuyUtaQ9Tx72OMJ6eUUKgiv-Tck8O2B-CHWzXjh8NASk84R6_ZrudiWUVDp4PaNTP7b-jG9GJPIgz_JPrJiXmitSxWyF4JF_cDB8V1LiaFh5anqbVkP-bLK7u1ozCfo62_tFQHnA9cGNIiyE4gvCoVKiT0jjzyPAgCZoys4YIcvVytHeFPOATYfglbpVKksQE4wkguSzwHDzKY2e8v5KpwMBrgZ74V-rgcQzB9negbYoAPGofaRkMFyQqsh3X-5I8GXpZYuOE3NEaF4DTxnPvB6o8AWoKRv6c3pxyDfz1GQquXq7HEPxeSUTWWjlCTR3fNFPLDAfZeu3E39700GFgwVY="
client = TelegramClient(
    StringSession(SESSION),
    api_id,
    api_hash,
    device_model="PC 64bit",
    system_version="Windows 10",
    app_version="Telegram 9.12.1"
)
# =================== SKIP CHAT ID ===================
SKIP_CHAT_IDS = [
    -1004441188512
]

# =================== TARGET CHAT ID ===================
TARGET_CHAT_IDS = [
    -1004441188512
]

# =================== KALIT SO‘ZLAR ===================
KEYWORDS = [
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
    'toshkentdan 1 kishi bering deganga', 'toshkentdan 2 kishi bering degan',
    'toshkentdan 2 kishi bering deganga', 'toshkentdan 3 kishi bering degan',
    'toshkentdan 3 kishi bering deganga', 'toshkentdan 4 kishi bering degan',
    'toshkentdan 4 kishi bering deganga', 'toshkentdan bagdodga odam bor', 'toshkentdan bir kishi',
    'Toshkentdan Rishtonga 1odam bor', 'toshkentga 1kishi', 'toshkentga 1kishi bor',
    'Toshkentga 1ta odam bor', 'toshkentga 2kishi', 'toshkentga 3kishi', 'toshkentga 4kishi',
    'toshkentga odam bor', 'toshketga 1kishi', 'towga 1kishi', 'towga 2kishi', 'towga 3kishi',
    'towga 4kishi', 'uchkoprikda 1kishi', 'uchkoprikdan 1kishi', 'uchta odam bor',
    'yangiqorgondan 1kishi', 'Yangiyuldan 1 kishi', 'Zangiotadan 1 kishi', 'амирсойдан 1киши',
    'аёл киши бор машина сўрашяпти', 'аёллар бор машина керак', 'бағдодан 1киши бор',
    'бир қиз бир бола бор', 'битта одам бор', 'боғдоддан 2киши', 'газалкентдан 1киши',
    'газалкентдан 2киши', 'зангиотадан 1 киши', 'иккита одам бор', 'кампилек одам бор',
    'катта ёшли аёл бор', 'компилек одам бор', 'компилект odam бор', 'комплек одам бор',
    'комплект одам бор', 'одам бор', 'одам бор 1', 'одам бор 2', 'одам бор 3', 'одам бор 4',
    'одам бор эди', 'одам бор экан', 'озимиздан 1киши', 'озимиздан 2 киши', 'риштонга 1 киши',
    'риштонга одам бор', 'ташкентдан риштонга одам бор', 'тошкентга 1 киши', 'тошкентга одам бор',
    'тошкентдан бағдодга одам бор', 'тошкентдан боғдодга одам бор',
    'тошкентдан фарғонага одам бор', 'тўрта одам бор', 'тўртта одам бор', 'учкўприкда 1киши',
    'учкўприкдан 1киши', 'учта одам бор', 'фарғонага 1 киши', 'фарғонага 2киши',
    'фарғонага одам бор', 'фарғонадан 1киши', 'чирчиқдан 1 киши', 'чирчиқдан 1киши',
    'эртагага қўқонга 1киши', 'янгийўлдан 1 киши', 'янгиқўрғондан 1киши', 'ўзимиздан 1киши',
    'ғазалкентдан 1киши', 'ғазалкентдан 2 киши', 'қибрайдан 1 киши', 'қиз бола бор',
    'қўқонга 1киши', 'қўқонга одам бор', 'қўқондан одам бор', "Bitta odam Bor",
    "rishtonda bitaa odam", "Rishton dan Toshga 1ta odam bor", "pochta bor ekan", "pochta borekan",
    "pochta borakan", "bochta bor edi", "oldi mestaga odam bor", "bogdodga odam bor",
    "buvaydaga odam bor", "buvaydadan odam bor", "fargonaga 2 kishi", "toshkentdan pustoy mashina kerak",
    "toshdan 2 kishimiz", "rishtonga 3 ta odam bor", "ayollari bor mashina kerak",
    "ayol kishisi bor mashina bormi", "oldi bo'sh mashina kerak", "orqa salonga odam bor",
    "hozirga yurib turgan mashina kerak", "hozirga yuradigan moshina bormi",
]

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

# =================== HANDLER ===================
@client.on(events.NewMessage(incoming=True))
async def handler(event):
    try:
        if not (event.is_group or event.is_channel):
            return

        chat_id = event.chat_id
        if chat_id in SKIP_CHAT_IDS:
            return

        text = event.raw_text
        if not text or not KEYWORDS_RE.search(text):
            return

        chat, sender = await asyncio.gather(
            event.get_chat(),
            event.get_sender()
        )

        group_name = getattr(chat, 'title', 'Nomaʼlum guruh')
        if getattr(chat, 'username', None):
            group_link = f"https://t.me/{chat.username}/{event.id}"
            group_display = f"<a href='{group_link}'>{group_name}</a>"
        else:
            group_display = group_name

        username = getattr(sender, 'username', None)
        owner_display = f"@{username}" if username else "Berkitilgan"

        sender_id = getattr(sender, 'id', None)
        profile_link = (
            f"<a href='tg://user?id={sender_id}'>Profilga o‘tish</a>"
            if sender_id else "Berkitilgan"
        )

        phone = normalize_phone(sender.phone) if sender.phone else None
        if not phone:
            for m in PHONE_RE.finditer(text):
                phone = normalize_phone(m.group(0))
                if phone:
                    break

        phone_display = phone if phone else "Berkitilgan"

        message_text = (
            f"🔈  <b>SIGNAL BOT N1</b>\n\n"
            f"📝 <b></b> {text}\n\n"
            f"📍  <b>Guruh:</b> {group_display}\n\n"
            f"👤 <b></b> {owner_display}\n\n"
            f"📞 <b></b> {phone_display}\n\n"
            f"👉🏻 <b></b> {profile_link}"
        )

        for target_id in TARGET_CHAT_IDS:
            await client.send_message(
                target_id,
                message_text,
                parse_mode='html'
            )
            print(f"📨 Yuborildi → {target_id}")

    except Exception as e:
        print("❌ Xatolik:", e)

# =================== START ===================
print("🚕 Taxi bot ishga tushdi...")
client.start()
client.run_until_disconnected()