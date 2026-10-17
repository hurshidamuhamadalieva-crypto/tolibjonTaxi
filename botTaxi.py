import re
import html
import asyncio
from telethon import TelegramClient, events

# =================== TELEGRAM API ===================
api_id = 37531523
api_hash = 'b4a9ecb2c20a09c26c1e1bdc110427c2'

# =================== TELEGRAM CLIENT ===================
client = TelegramClient(
    "taxi_session",          # session nomi
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
    # odam bor
    'odam bor','odambor','odam bor ekan','odam bor edi','odam borakan',
    'bitta odam bor','ikkita odam bor','uchta odam bor',"to'rtta odam bor",'tortta odam bor',
    'komplek odam bor','komplekt odam bor','kompilek odam bor','kampilek odam bor',
    '1ta odam bor','2ta odam bor','3ta odam bor','4ta odam bor',
    'odam bor 1','odam bor 2','odam bor 3','odam bor 4',
    'rishtonga odam bor','toshkentga odam bor',"toshkendan farg'onaga odam bor",
    'тўрта одам бор','одам бор','комплект одам бор','компилект odam бор','кампилек одам бор',
    'towga 1kishi', 'toshkentga 1kishi', "farg'onaga 1kishi", 'rishtonga 1kishi', '1kishi bor',
    'towga 2kishi', 'toshkentga 2kishi', "farg'onaga 2kishi", 'rishtonga 2kishi', '2kishi bor',
    'towga 3kishi', 'toshkentga 3kishi', "farg'onaga 3kishi", 'rishtonga 3kishi', '3kishi bor',
    'towga 4kishi', 'toshkentga 4kishi', "farg'onaga 4kishi", 'rishtonga 4kishi', '4kishi bor',
    'машина бор','одам бор эди','одам бор экан','одам бор 1','одам бор 2','одам бор 3','одам бор 4',
    'битта одам бор','иккита одам бор','учта одам бор','комплек одам бор','1та одам бор','2та одам бор',
    '3та одам бор','4та одам бор', 'toshkentdan bir kishi', 'rishtonga bir kishi', '1 ta qiz bor', 'ayol kishi bor mashina sorashyabdi',
    'Chirchiqdan 1 kishi', 'Yangiyuldan 1 kishi', 'Zangiotadan 1 kishi', 'Qibraydan 1 kishi', '1 kishi bor',
    '2-ta odam bor', '2-kishi bor', '3-ta odam bor', '3-kishi bor', '4-ta odam bor', '4-kishi bor',
    '2-ta kishi bor', '3-ta kishi bor', '4-ta kishi bor', '2-ta ayolkishi bor', '3-ta ayolkishi bor', '4-ta ayolkishi bor', "odam.bor", 
    "1 kishi bor", "2 kishi bor", "2kishi bor",
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
    
    # mashina kerak
    'mashina kerak','mashina kere','mashina kerek','mashina kera','mashina keraa',
    'bagajli mashina kerak','bosh mashina kerak','bosh mashina bormi','boshi bormi',
    'mashina izlayapman','mashina topaman','mashina kerak edi',
    'машина керак','багажли машина керак','бош машина керак','машина кере','машina кераа',

    # pochta bor
    'pochta bor','pochta kerak','pochta ketadi','pochta olib ketadi','pochta bormi',
    'почта бор','почта кетади','почта керак','почта олиб кетади',
    'тошкентга почта бор','тошкентдан почта бор','риштонга почта бор','риштондан почта бор',

    # ketadi
    'ketadi','ketvotti','ketishi kerak',
    'кетяпт','кетвотди','кетади','кетишади','кетиши керак', "1kishi ekan", "2kishi ekan", "3kishi ekan", "4kishi ekan",
    "2 kishi ekan", "3 kishi ekan", "1 kishi ekan", "toshketga 1kishi", "toshkenda odam bor",

    # dostavka
    'dastavka bor','dostavka bor','dastafka','dastafka bor',
    'доставкa бор','даставка бор','доставка бор','доставкa керак',
    "Toshkentdan Rishtonga 1odam bor", '1odam bor', '1ta kamla', 'bitta kamlarga', '1ta kamlarga',
    '1 ta kamlarga', '2kiwimiz', "bagajga yuk bor", '2kishimiz', "2 kiwimiz", "2 kishimiz", "2kiwimiz", 
    "3kiwimiz", "3 kiwimiz", "3 kishimiz", "3kishimiz", "4kishimiz", "4kiwimiz", "4 kishimiz", "4 kiwimiz",
    "Toshkentga 1kishi", "Toshkenga 1kishi", "Rishtonga 1kishi", "Rishotondan 1kiwi", "poshta  bor", "moshina kerak",
    "ayollar bor mashina kerak", "ayollar bor moshina kerak", "Toshkentga 1ta odam bor", "1 ta qiz bola bor", "qiz bola bor",
    "1ta qiz bor", "1ta qiz bola bor", 'одам бор',
    'одам бор экан','одам бор эди','битта одам бор','иккита одам бор','учта одам бор','тўртта одам бор','1та одам бор','2та одам бор','3та одам бор','4та одам бор','одам бор 1','одам бор 2','одам бор 3','одам бор 4',

    'комплек одам бор','комплект одам бор','компилек одам бор','кампилек одам бор',

    'риштонга одам бор','тошкентга одам бор','тошкентдан фарғонага одам бор','тошкентга 1 киши','риштонга 1 киши','фарғонага 1 киши','1 киши бор','2 киши бор','3 киши бор','4 киши бор',
    'чирчиқдан 1 киши', 'янгийўлдан 1 киши', 'зангиотадан 1 киши', 'қибрайдан 1 киши',

    '1 та қиз бор', '1 та қиз бола бор', 'қиз бола бор', 'аёл киши бор машина сўрашяпти', 'аёллар бор машина керак',

    # mashina
    'машина керак', 'машина кере', 'машина керeк', 'багажли машина керак', 'машина излаяпман', 'мошина керак',

    'ОДАМ БОР','ОДАМБОР','ОДАМ БОР ЭКАН','ОДАМ БОР ЭДИ','ОДАМ БОРАКАН',

    'БИТТА ОДАМ БОР','ИККИТА ОДАМ БОР','УЧТА ОДАМ БОР',"ТО'РТТА ОДАМ БОР",'ТОРТТА ОДАМ БОР',

    'КОМПЛЕК ОДАМ БОР','КОМПЛЕКТ ОДАМ БОР','КОМПИЛЕК ОДАМ БОР','КАМПИЛЕК ОДАМ БОР',

    '1ТА ОДАМ БОР','2ТА ОДАМ БОР','3ТА ОДАМ БОР','4ТА ОДАМ БОР',

    'ОДАМ БОР 1','ОДАМ БОР 2','ОДАМ БОР 3','ОДАМ БОР 4',

    'РИШТОНГА ОДАМ БОР','ТОШКЕНТГА ОДАМ БОР',"ТОШКЕНДАН ФАРҒОНАГА ОДАМ БОР",

    'ТЎРТА ОДАМ БОР','ОДАМ БОР','КОМПЛЕКТ ОДАМ БОР','КОМПИЛЕКТ ОДАМ БОР','КАМПИЛЕК ОДАМ БОР',

    'TOWГА 1КИШИ','ТОШКЕНТГА 1КИШИ',"ФАРҒОНАГА 1КИШИ",'РИШТОНГА 1КИШИ','1КИШИ БОР',

    'TOWГА 2КИШИ','ТОШКЕНТГА 2КИШИ',"ФАРҒОНАГА 2КИШИ",'РИШТОНГА 2КИШИ','2КИШИ БОР',

    'TOWГА 3КИШИ','ТОШКЕНТГА 3КИШИ',"ФАРҒОНАГА 3КИШИ",'РИШТОНГА 3КИШИ','3КИШИ БОР',

    'TOWГА 4КИШИ','ТОШКЕНТГА 4КИШИ',"ФАРҒОНАГА 4КИШИ",'РИШТОНГА 4КИШИ','4КИШИ БОР',
    "Farg'ona pochta bor", 'pochta bor', 'Rishtoni Uyratiga bita odam bor', "bita odam bor", 'toshkendan margilonga qanchekan'
]

KEYWORDS_RE = re.compile("|".join(re.escape(k) for k in KEYWORDS), re.IGNORECASE)

# =================== TELEFON ===================
# O'zbekiston operator kodlari
VALID_CODES = {
    '20', '33', '50', '55', '61', '62', '65', '66', '67', '69', '70', '71',
    '72', '73', '74', '75', '76', '77', '78', '79', '88', '90', '91', '93',
    '94', '95', '97', '98', '99'
}

# +998 90 123 45 67 / 90-123-45-67 / 901234567 / (90)1234567 / 998901234567
PHONE_RE = re.compile(
    r'(?<!\d)(?:\+?\s*998)?[\s\-\(\)\.]*'
    r'(\d{2})[\s\-\(\)\.]*(\d{3})[\s\-\(\)\.]*(\d{2})[\s\-\(\)\.]*(\d{2})(?!\d)'
)

def normalize_phone(raw):
    """Profildagi raqamni +998XXXXXXXXX ko'rinishga keltiradi."""
    if not raw:
        return None
    digits = re.sub(r'\D', '', raw)
    if digits.startswith('998') and len(digits) >= 12:
        return '+' + digits[:12]
    if len(digits) == 9:
        return '+998' + digits
    return None

def extract_phones(text):
    """Matndagi barcha to'g'ri raqamlarni qaytaradi."""
    phones = []
    for m in PHONE_RE.finditer(text):
        if m.group(1) not in VALID_CODES:
            continue
        number = '+998' + ''.join(m.groups())
        if number not in phones:
            phones.append(number)
    return phones

# =================== PROFIL ===================
def get_username(sender):
    username = getattr(sender, 'username', None)
    if username:
        return username
    # yangi Telegramda bir nechta username bo'lishi mumkin
    for u in (getattr(sender, 'usernames', None) or []):
        if getattr(u, 'active', False) and getattr(u, 'username', None):
            return u.username
    return None

def build_profile(sender):
    """(egasi_matni, profil_havolasi) qaytaradi.
    Username bor     -> t.me/username
    Username yo'q    -> tg://user?id=ID
    Ikkalasi ham yo'q -> Berkitilgan
    """
    if sender is None:
        return "Berkitilgan", "Berkitilgan"

    username = get_username(sender)
    sender_id = getattr(sender, 'id', None)

    if username:
        return (
            f"@{username}",
            f"<a href='https://t.me/{username}'>Profilga o‘tish</a>"
        )
    if sender_id:
        return (
            "Username yo‘q",
            f"<a href='tg://user?id={sender_id}'>Profilga o‘tish</a>"
        )
    return "Berkitilgan", "Berkitilgan"

# =================== HANDLER ===================
async def safe(coro):
    """Xato bo'lsa botni to'xtatmaydi, None qaytaradi."""
    try:
        return await coro
    except Exception as e:
        print("⚠️ Ma'lumot olib bo'lmadi:", e)
        return None

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
            safe(event.get_chat()),
            safe(event.get_sender())
        )

        group_name = html.escape(getattr(chat, 'title', None) or 'Nomaʼlum guruh')
        if getattr(chat, 'username', None):
            group_link = f"https://t.me/{chat.username}/{event.id}"
            group_display = f"<a href='{group_link}'>{group_name}</a>"
        else:
            group_display = group_name

        # ---- profil: username bo'lmasa id bilan ----
        owner_display, profile_link = build_profile(sender)

        # ---- telefon: avval profildan, keyin matndan ----
        phones = []
        p = normalize_phone(getattr(sender, 'phone', None))
        if p:
            phones.append(p)
        for ph in extract_phones(text):
            if ph not in phones:
                phones.append(ph)

        phone_display = (
            "\n".join(f"<code>{ph}</code>" for ph in phones)
            if phones else "Berkitilgan"
        )

        message_text = (
            f"🔈  <b>Elon topildi</b>\n\n"
            f"📝 <b></b> {html.escape(text)}\n\n"
            f"📍  <b>Guruh:</b> {group_display}\n\n"
            f"👤 <b></b> {owner_display}\n\n"
            f"📞 <b></b> {phone_display}\n\n"
            f"👉🏻 <b></b> {profile_link}"
        )

        for target_id in TARGET_CHAT_IDS:
            try:
                await client.send_message(
                    target_id,
                    message_text,
                    parse_mode='html'
                )
                print(f"📨 Yuborildi → {target_id}")
            except Exception as e:
                print(f"❌ {target_id} ga yuborib bo'lmadi:", e)

    except Exception as e:
        print("❌ Xatolik:", e)

# =================== START ===================
print("🚕 Taxi bot ishga tushdi...")
client.start()
client.run_until_disconnected()