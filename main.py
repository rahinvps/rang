import requests
import time
import telebot
import threading
import random
import html

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ============================================
# CONFIG
# ============================================

BOT_TOKEN = "8620237186:AAF11ibRkQTO-lFKLnlr39prFZEVf_fxiIQ"
CHAT_ID = "-1003644188907"
API_KEY = "MRKVD1UFXWP"

BASE_URL = "https://2oo9.cloud/api/MXS47FLFX0U/project/tetragonexvoltxsms/@public/api"

HEADERS = {
    "mauthapi": API_KEY
}

# ============================================
# BUTTON LINKS
# ============================================

CHANNEL_LINK = "https://t.me/rmmethodzone"
NUMBER_BOT_LINK = "https://t.me/rmxel_bot"

# ============================================
# SERVICES & EMOJIS
# ============================================

SERVICES = ["facebook", "whatsapp", "telegram", "instagram"]

SERVICE_MAP = {
    "facebook": {"short": "FB", "emoji": "🔵"},
    "whatsapp": {"short": "WA", "emoji": "🟢"},
    "telegram": {"short": "TG", "emoji": "🔷"},
    "instagram": {"short": "IG", "emoji": "📸"}
}

# ============================================
# SETTINGS
# ============================================

DELETE_AFTER = 180

bot = telebot.TeleBot(BOT_TOKEN)

sent_hits = set()

# ============================================
# COUNTRY DETECT (ALL COUNTRIES UPDATED)
# ============================================

COUNTRY_CODES = {
    "1": "🇺🇸/🇨🇦 USA/Canada", "7": "🇷🇺/🇰🇿 Russia/Kazakhstan", "20": "🇪🇬 Egypt", 
    "27": "🇿🇦 South Africa", "30": "🇬🇷 Greece", "31": "🇳🇱 Netherlands", "32": "🇧🇪 Belgium", 
    "33": "🇫🇷 France", "34": "🇪🇸 Spain", "36": "🇭🇺 Hungary", "39": "🇮🇹 Italy", 
    "40": "🇷🇴 Romania", "41": "🇨🇭 Switzerland", "43": "🇦🇹 Austria", "44": "🇬🇧 United Kingdom", 
    "45": "🇩🇰 Denmark", "46": "🇸🇪 Sweden", "47": "🇳🇴 Norway", "48": "🇵🇱 Poland", 
    "49": "🇩🇪 Germany", "51": "🇵🇪 Peru", "52": "🇲🇽 Mexico", "53": "🇨🇺 Cuba", 
    "54": "🇦🇷 Argentina", "55": "🇧🇷 Brazil", "56": "🇨🇱 Chile", "57": "🇨🇴 Colombia", 
    "58": "🇻🇪 Venezuela", "60": "🇲🇾 Malaysia", "61": "🇦🇺 Australia", "62": "🇮🇩 Indonesia", 
    "63": "🇵🇭 Philippines", "64": "🇳🇿 New Zealand", "65": "🇸🇬 Singapore", "66": "🇹🇭 Thailand", 
    "81": "🇯🇵 Japan", "82": "🇰🇷 South Korea", "84": "🇻🇳 Vietnam", "86": "🇨🇳 China", 
    "90": "🇹🇷 Turkey", "91": "🇮🇳 India", "92": "🇵🇰 Pakistan", "93": "🇦🇫 Afghanistan", 
    "94": "🇱🇰 Sri Lanka", "95": "🇲🇲 Myanmar", "98": "🇮🇷 Iran", "211": "🇸🇸 South Sudan", 
    "212": "🇲🇦 Morocco", "213": "🇩🇿 Algeria", "216": "🇹🇳 Tunisia", "218": "🇱🇾 Libya", 
    "220": "🇬🇲 Gambia", "221": "🇸🇳 Senegal", "222": "🇲🇷 Mauritania", "223": "🇲🇱 Mali", 
    "224": "🇬🇳 Guinea", "225": "🇨🇮 Ivory Coast", "226": "🇧🇫 Burkina Faso", "227": "🇳🇪 Niger", 
    "228": "🇹🇬 Togo", "229": "🇧🇯 Benin", "230": "🇲🇺 Mauritius", "231": "🇱🇷 Liberia", 
    "232": "🇸🇱 Sierra Leone", "233": "🇬🇭 Ghana", "234": "🇳🇬 Nigeria", "235": "🇹🇩 Chad", 
    "236": "🇨🇫 Central African Republic", "237": "🇨🇲 Cameroon", "238": "🇨🇻 Cape Verde", 
    "239": "🇸🇹 Sao Tome and Principe", "240": "🇬🇶 Equatorial Guinea", "241": "🇬🇦 Gabon", 
    "242": "🇨🇬 Congo", "243": "🇨🇩 DR Congo", "244": "🇦🇴 Angola", "245": "🇬🇼 Guinea-Bissau", 
    "246": "🇮🇴 Diego Garcia", "247": "🇦🇨 Ascension Island", "248": "🇸🇨 Seychelles", 
    "249": "🇸🇩 Sudan", "250": "🇷🇼 Rwanda", "251": "🇪🇹 Ethiopia", "252": "🇸🇴 Somalia", 
    "253": "🇩🇯 Djibouti", "254": "🇰🇪 Kenya", "255": "🇹🇿 Tanzania", "256": "🇺🇬 Uganda", 
    "257": "🇧🇮 Burundi", "258": "🇲🇿 Mozambique", "260": "🇿🇲 Zambia", "261": "🇲🇬 Madagascar", 
    "262": "🇷🇪 Reunion", "263": "🇿🇼 Zimbabwe", "264": "🇳🇦 Namibia", "265": "🇲🇼 Malawi", 
    "266": "🇱🇸 Lesotho", "267": "🇧🇼 Botswana", "268": "🇸🇿 Eswatini", "269": "🇰🇲 Comoros", 
    "290": "🇸🇭 Saint Helena", "291": "🇪🇷 Eritrea", "297": "🇦🇼 Aruba", "298": "🇫🇴 Faroe Islands", 
    "299": "🇬🇱 Greenland", "350": "🇬🇮 Gibraltar", "351": "🇵🇹 Portugal", "352": "🇱🇺 Luxembourg", 
    "353": "🇮🇪 Ireland", "354": "🇮🇸 Iceland", "355": "🇦🇱 Albania", "356": "🇲🇹 Malta", 
    "357": "🇨🇾 Cyprus", "358": "🇫🇮 Finland", "359": "🇧🇬 Bulgaria", "370": "🇱🇹 Lithuania", 
    "371": "🇱🇻 Latvia", "372": "🇪🇪 Estonia", "373": "🇲🇩 Moldova", "374": "🇦🇲 Armenia", 
    "375": "🇧🇾 Belarus", "376": "🇦🇩 Andorra", "377": "🇲🇨 Monaco", "378": "🇸🇲 San Marino", 
    "380": "🇺🇦 Ukraine", "381": "🇷🇸 Serbia", "382": "🇲🇪 Montenegro", "383": "🇽🇰 Kosovo", 
    "385": "🇭🇷 Croatia", "386": "🇸🇮 Slovenia", "387": "🇧🇦 Bosnia and Herzegovina", 
    "389": "🇲🇰 North Macedonia", "420": "🇨🇿 Czech Republic", "421": "🇸🇰 Slovakia", 
    "423": "🇱🇮 Liechtenstein", "500": "🇫🇰 Falkland Islands", "501": "🇧🇿 Belize", 
    "502": "🇬🇹 Guatemala", "503": "🇸🇻 El Salvador", "504": "🇭🇳 Honduras", "505": "🇳🇮 Nicaragua", 
    "506": "🇨🇷 Costa Rica", "507": "🇵🇦 Panama", "508": "🇵🇲 Saint Pierre and Miquelon", 
    "509": "🇭🇹 Haiti", "590": "🇬🇵 Guadeloupe", "591": "🇧🇴 Bolivia", "592": "🇬🇾 Guyana", 
    "593": "🇪🇨 Ecuador", "594": "🇬🇫 French Guiana", "595": "🇵🇾 Paraguay", "596": "🇲🇶 Martinique", 
    "597": "🇸🇷 Suriname", "598": "🇺🇾 Uruguay", "599": "🇨🇼 Curacao", "670": "🇹🇱 East Timor", 
    "672": "🇦🇶 Antarctica", "673": "🇧🇳 Brunei", "674": "🇳🇷 Nauru", "675": "🇵🇬 Papua New Guinea", 
    "676": "🇹🇴 Tonga", "677": "🇸🇧 Solomon Islands", "678": "🇻🇺 Vanuatu", "679": "🇫يج Fiji", 
    "680": "🇵🇼 Palau", "681": "🇼🇫 Wallis and Futuna", "682": "🇨🇰 Cook Islands", "683": "🇳🇺 Niue", 
    "685": "🇼🇸 Samoa", "686": "🇰🇮 Kiribati", "687": "🇳🇨 New Caledonia", "688": "🇹🇻 Tuvalu", 
    "689": "🇵🇫 French Polynesia", "690": "🇹🇰 Tokelau", "691": "🇫🇲 Micronesia", "692": "🇲🇭 Marshall Islands", 
    "850": "🇰🇵 North Korea", "852": "🇭🇰 Hong Kong", "853": "🇲🇴 Macau", "855": "🇰🇭 Cambodia", 
    "856": "🇱🇦 Laos", "880": "🇧🇩 Bangladesh", "886": "🇹🇼 Taiwan", "960": "🇲🇻 Maldives", 
    "961": "🇱🇧 Lebanon", "962": "🇯🇴 Jordan", "963": "🇸🇾 Syria", "964": "🇮🇶 Iraq", 
    "965": "🇰🇼 Kuwait", "966": "🇸🇦 Saudi Arabia", "967": "🇾🇪 Yemen", "968": "🇴🇲 Oman", 
    "970": "🇵🇸 Palestine", "971": "🇦🇪 UAE", "972": "🇮🇱 Israel", "973": "🇧🇭 Bahrain", 
    "974": "🇶🇦 Qatar", "975": "🇧🇹 Bhutan", "976": "🇲🇳 Mongolia", "977": "🇳🇵 Nepal", 
    "992": "🇹🇯 Tajikistan", "993": "🇹🇲 Turkmenistan", "994": "🇦🇿 Azerbaijan", "995": "🇬🇪 Georgia", 
    "996": "🇰🇬 Kyrgyzstan", "998": "🇺🇿 Uzbekistan"
}

def get_country_info(rang):
    rang = str(rang)
    for code in sorted(COUNTRY_CODES.keys(), key=len, reverse=True):
        if rang.startswith(code):
            text_data = COUNTRY_CODES[code]
            # ফ্ল্যাগ এবং শর্ট নেম আলাদা করা
            parts = text_data.split(" ")
            flag = parts[0]
            name = " ".join(parts[1:])
            
            # শর্ট কোডের জন্য কাস্টম লজিক (যেমন: USA/Canada -> US)
            short = name.split("/")[0][:2].upper()
            return {"name": name, "flag": flag, "short": short}, code
            
    return {"name": "Global", "flag": "🌍", "short": "GL"}, ""

# ============================================
# FAKE REALISTIC NUMBER GENERATOR
# ============================================

def generate_fake_number(rang):
    country_info, code = get_country_info(rang)
    if not code:
        return f"+{random.randint(1000000000, 9999999999)}"
    fake_digits = "".join([str(random.randint(0, 9)) for _ in range(8)])
    return f"+{code}{fake_digits}"

# ============================================
# BUTTONS GENERATOR (TELEBOT COMPATIBLE)
# ============================================

def make_buttons(otp_code):
    markup = InlineKeyboardMarkup(row_width=2)
    
    # প্রথম সারির বাটন (ওটিপি এবং ফুল এসএমএস কপি টাইপ অ্যালার্ট)
    markup.add(
        InlineKeyboardButton(f"🔑 {otp_code}", callback_data=f"copy_otp_{otp_code}"),
        InlineKeyboardButton("💬 Full SMS", callback_data="copy_full_sms")
    )
    
    # দ্বিতীয় সারির বাটন (বট এবং চ্যানেল লিংক)
    markup.add(
        InlineKeyboardButton("🤖 NUMBER BOT", url=NUMBER_BOT_LINK),
        InlineKeyboardButton("📢 MAIN CHANNEL", url=CHANNEL_LINK)
    )
    return markup

# ============================================
# REALISTIC OTP TEXT GENERATOR
# ============================================

def get_real_sms_text(app, otp_code):
    if "telegram" in app:
        return f"Telegram code: {otp_code}. You can also use this link to log in:\nhttps://t.me/login/{otp_code}\n\nDon't give this code to anyone, even if they say they're from Telegram!"
    elif "whatsapp" in app:
        return f"Your WhatsApp code is {otp_code}. You can also tap on this link to verify your phone:\nv.whatsapp.com/{otp_code}\n\nDon't share this code with others."
    elif "facebook" in app:
        return f"{otp_code} is your Facebook confirmation code. For your security, do not share this code."
    elif "instagram" in app:
        return f"{otp_code} is your Instagram code. Sharing this code can give others access to your account."
    else:
        return f"Your verification code is: {otp_code}. Valid for 5 minutes. Do not share this OTP."

# ============================================
# NON-BLOCKING AUTO DELETE
# ============================================

def auto_delete(chat_id, message_id):
    def worker():
        time.sleep(DELETE_AFTER)
        try:
            bot.delete_message(chat_id, message_id)
        except:
            pass
    threading.Thread(target=worker, daemon=True).start()

# ============================================
# SEND RANGE WITH YOUR FORMAT
# ============================================

def send_range(service, hit):
    rang = hit["range"]
    country_info, _ = get_country_info(rang)
    
    premium_flag = country_info["flag"]
    srv_data = SERVICE_MAP.get(service, {"short": service.upper(), "emoji": "🔥"})
    
    short_code = f"{country_info['short']}_{srv_data['short']}"
    srv_emoji = srv_data["emoji"]
    
    masked = generate_fake_number(rang)
    otp_code = str(random.randint(100000, 999999)) if service != "telegram" else str(random.randint(10000, 99999))
    full_sms = get_real_sms_text(service, otp_code)

    # আপনার পাঠানো ডিজাইন অনুযায়ী হুবহু গ্রুপ মেসেজ ফরম্যাট
    group_msg = (
        f"{premium_flag} <b>#{short_code} {srv_emoji} OTP SUCCESS</b>\n\n"
        f"<b>Number:</b> <code>{masked}</code>\n"
        f"<b>OTP Code:</b> <code>{html.escape(otp_code)}</code>\n"
        f"<b>Full SMS:</b> <code>{html.escape(full_sms)}</code>"
    )

    try:
        sent = bot.send_message(
            CHAT_ID,
            group_msg,
            parse_mode="HTML",
            reply_markup=make_buttons(otp_code)
        )
        auto_delete(CHAT_ID, sent.message_id)
    except Exception as e:
        print("Telegram Send Error:", e)

# ============================================
# CALLBACK HANDLING FOR ALERT
# ============================================

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith("copy_otp_"):
        otp = call.data.replace("copy_otp_", "")
        bot.answer_callback_query(call.id, text=f"🔑 Code: {otp} (Tap hold message text to copy)", show_alert=False)
    elif call.data == "copy_full_sms":
        bot.answer_callback_query(call.id, text="💬 Copy full text box directly from the chat!", show_alert=False)

# ============================================
# CONSOLE LOOP
# ============================================

def check_console():
    while True:
        try:
            url = f"{BASE_URL}/console"
            res = requests.get(url, headers=HEADERS, timeout=40)
            data = res.json()

            if data["meta"]["code"] == 200:
                for hit in data["data"]["hits"]:
                    service = hit["sid"].lower()

                    if service not in SERVICES:
                        continue

                    uid = f"{hit['range']}_{hit['time']}"

                    if uid in sent_hits:
                        continue

                    sent_hits.add(uid)
                    send_range(service, hit)
                    time.sleep(40)

        except Exception as e:
            print("ERROR:", e)

        time.sleep(55)

# ============================================
# START
# ============================================

if __name__ == "__main__":
    print("LIVE RANG FORWARDER RUNNING...")
    threading.Thread(target=check_console, daemon=True).start()
    bot.infinity_polling()
