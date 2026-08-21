import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import base64
from datetime import datetime, timedelta
import time
import qrcode
from io import BytesIO
import logging
import re
import random

# ===== إعدادات البوت =====
TOKEN = '8903649310:AAHb4tpn8fe1oHAr4nKeAARG7KRbyIkMOJM'
bot = telebot.TeleBot(TOKEN)
bot_name = 'حمودا'

# ===== إعدادات =====
reports = []
user_requests = {}
muted_users = set()
restricted_users = set()
link_protection_active = False
forward_protection_active = False

# ===== صورة البوت =====
BOT_PHOTO = "https://i.ibb.co/LDGhhTc2/c1f084494e03899880eae0101b2965a0.jpg"

# ===== إعدادات التسجيل =====
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Bot has started.")


# ============================================================
# === دوال التحقق من الصلاحيات (مع حماية من الأخطاء) ===
# ============================================================
def is_group_owner(user_
, chat_id):
    try:
        admins = bot.get_chat_administrators(chat_id)
        for admin in admins:
            if admin.user.id == user_id and admin.status == 'creator':
                return True
        return False
    except:
        return False


def is_user_admin(user_id, chat_id):
    try:
        admins = [admin.user.id for admin in bot.get_chat_administrators(chat_id)]
        return user_id in admins
    except:
        return False


def is_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['administrator', 'creator']
    except:
        return False


# ============================================================
# === الأمر start (مع رسالة ترحيب HTML واقتباس) ===
# ============================================================
@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup(row_width=2)

    # أزرار القسم الرئيسي
    btn_admin = InlineKeyboardButton("👑 قسم المشرفين", callback_data="admin_section")
    btn_admin.style = "primary"
    btn_groups = InlineKeyboardButton("📁 قسم الجروبات", callback_data="groups_section")
    btn_groups.style = "primary"
    btn_protection = InlineKeyboardButton("🛡️ لوحة الحماية", callback_data="protection_section")
    btn_protection.style = "primary"
    btn_info = InlineKeyboardButton("📋 أوامر إضافية", callback_data="info_section")
    btn_info.style = "primary"

    # الأزرار السفلية الجديدة
    btn_quran = InlineKeyboardButton("📖 قرآن", callback_data="quran")
    btn_quran.style = "success"
    btn_news = InlineKeyboardButton("📰 اخبار", callback_data="news")
    btn_news.style = "success"
    btn_poetry = InlineKeyboardButton("📝 شعر", callback_data="poetry")
    btn_poetry.style = "success"
    btn_quotes = InlineKeyboardButton("💬 اقتباسات", callback_data="quotes")
    btn_quotes.style = "success"
    btn_books = InlineKeyboardButton("📚 كتب", callback_data="books")
    btn_books.style = "success"
    btn_wallpapers = InlineKeyboardButton("🎨 جداريات", callback_data="wallpapers")
    btn_wallpapers.style = "success"

    # أزرار إضافية
    btn_about = InlineKeyboardButton("ℹ️ حول", callback_data="about")
    btn_about.style = "primary"
    btn_stats = InlineKeyboardButton("📊 إحصائياتي", callback_data="stats")
    btn_stats.style = "primary"
    btn_source = InlineKeyboardButton("📢 قناة السورس", url="https://t.me/MIDO_x12")
    btn_source.style = "primary"
    btn_dev = InlineKeyboardButton("👨‍💻 المطور", url="https://t.me/MIDO_x12")
    btn_dev.style = "primary"
    btn_add = InlineKeyboardButton("➕ اضف البوت لجروبك", url=f"https://t.me/{bot.get_me().username}?startgroup")
    btn_add.style = "success"

    markup.add(btn_admin, btn_groups)
    markup.add(btn_protection, btn_info)
    markup.add(btn_quran, btn_news, btn_poetry)
    markup.add(btn_quotes, btn_books, btn_wallpapers)
    markup.add(btn_about, btn_stats)
    markup.add(btn_source, btn_dev)
    markup.add(btn_add)

    # الوقت
    current_time = datetime.now().strftime("%I:%M %p")

    # ===== رسالة ترحيب جديدة مع اقتباس =====
    welcome_text = (
        f"<b>🎀 أهلاً بك في بوت حمودا</b>\n\n"
        f"<b>👤 مرحباً {message.from_user.first_name}</b>\n"
        f"<b>🆔 ايديك:</b> <code>{message.from_user.id}</code>\n"
        f"<b>🕐 الوقت:</b> {current_time}\n\n"
        f"<blockquote>✨ {bot_name} بوت حماية وإدارة متكامل\n"
        f"📌 يوفر لك جميع أدوات الحماية والإدارة\n"
        f"🎯 اختر القسم المناسب من الأزرار أدناه</blockquote>"
    )

    bot.send_photo(
        message.chat.id,
        photo=BOT_PHOTO,
        caption=welcome_text,
        parse_mode="HTML",
        reply_markup=markup
    )


# ============================================================
# === أزرار الأقسام (جميع أزرار الرجوع باللون الأحمر) ===
# ============================================================

@bot.callback_query_handler(func=lambda call: call.data == "admin_section")
def admin_section(call):
    markup = InlineKeyboardMarkup(row_width=1)
    btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")
    btn_back.style = "danger"
    markup.add(btn_back)

    bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption=(
            "**👑 قسم المشرفين**\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "🛡️ **أوامر الحماية:**\n"
            "🔹 `حمودا حظر` (رد) - حظر مستخدم\n"
            "🔹 `حمودا طرد` (رد) - طرد مستخدم\n"
            "🔹 `حمودا كتم` (رد) - كتم مستخدم\n"
            "🔹 `حمودا فك كتم` (رد) - فك الكتم\n"
            "🔹 `حمودا تقييد` (رد) - تقييد مستخدم\n"
            "🔹 `حمودا فك تقييد` (رد) - فك التقييد\n"
            "🔹 `حمودا كشف` (رد) - عرض معلومات المستخدم\n"
            "🔹 `حمودا ارفع مشرف` (رد) - رفع مشرف\n"
            "🔹 `حمودا ازاله مشرف` (رد) - ازاله مشرف"
        ),
        parse_mode="Markdown",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data == "groups_section")
def groups_section(call):
    markup = InlineKeyboardMarkup(row_width=1)
    btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")
    btn_back.style = "danger"
    markup.add(btn_back)

    bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption=(
            "**📁 قسم الجروبات**\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "📋 **أوامر المعلومات:**\n"
            "🔹 `حمودا ايدي` - عرض الايدي الخاص بك\n"
            "🔹 `حمودا معرفي` - عرض يوزرك\n"
            "🔹 `حمودا معلومات المجموعه` - معلومات المجموعة\n"
            "🔹 `حمودا رابط مجموعه` - رابط المجموعة\n\n"
            "🛠️ **أوامر إضافية:**\n"
            "🔹 `حمودا قول` - تكرار النص\n"
            "🔹 `حمودا الوقت` - الوقت والتاريخ"
        ),
        parse_mode="Markdown",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data == "protection_section")
def protection_section(call):
    markup = InlineKeyboardMarkup(row_width=1)
    btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")
    btn_back.style = "danger"
    markup.add(btn_back)

    link_status = "🟢 **مفعلة**" if link_protection_active else "🔴 **معطلة**"
    forward_status = "🟢 **مفعلة**" if forward_protection_active else "🔴 **معطلة**"

    bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption=(
            "**🛡️ لوحة الحماية**\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            f"🔗 **حماية الروابط:** {link_status}\n"
            f"🔄 **حماية التوجيه:** {forward_status}\n\n"
            "📋 **الأوامر:**\n"
            "🔹 `حمودا تفعيل حمايه الروابط` - تفعيل حماية الروابط\n"
            "🔹 `حمودا قفل حمايه الروابط` - قفل حماية الروابط\n"
            "🔹 `حمودا تفعيل حمايه التوجيه` - تفعيل حماية التوجيه\n"
            "🔹 `حمودا قفل حمايه التوجيه` - قفل حماية التوجيه"
        ),
        parse_mode="Markdown",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data == "info_section")
def info_section(call):
    markup = InlineKeyboardMarkup(row_width=1)
    btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")
    btn_back.style = "danger"
    markup.add(btn_back)

    bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption=(
            "**📋 أوامر إضافية**\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "🔹 `حمودا انشا qr` - صنع رمز QR\n"
            "🔹 `حمودا افتاري` - عرض صورتك\n"
            "🔹 `حمودا عرض صوره` (رد) - عرض صورة مستخدم\n"
            "🔹 `حمودا بلاغ` (رد) - إبلاغ عن عضو\n"
            "🔹 `حمودا شفر` + نص - تشفير نص\n"
            "🔹 `حمودا فك تشفير` + نص - فك تشفير نص\n"
            "🔹 `حمودا اضافه رد` - إضافة رد تلقائي"
        ),
        parse_mode="Markdown",
        reply_markup=markup
    )


# ============================================================
# === الأقسام الترفيهية (عشوائية مع أزرار رجوع حمراء) ===
# ============================================================

@bot.callback_query_handler(func=lambda call: call.data == "quran")
def quran_section(call):
    verses = [
        "﴿ إِنَّ اللَّهَ مَعَ الصَّابِرِينَ ﴾ [البقرة: 153]",
        "﴿ وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مَخْرَجًا ﴾ [الطلاق: 2]",
        "﴿ وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مِنْ أَمْرِهِ يُسْرًا ﴾ [الطلاق: 4]",
        "﴿ وَرَحْمَتِي وَسِعَتْ كُلَّ شَيْءٍ ﴾ [الأعراف: 156]",
        "﴿ فَإِنَّ مَعَ الْعُسْرِ يُسْرًا ﴾ [الشرح: 5]",
        "﴿ إِنَّ مَعَ الْعُسْرِ يُسْرًا ﴾ [الشرح: 6]",
        "﴿ وَتَوَكَّلْ عَلَى اللَّهِ وَكَفَى بِاللَّهِ وَكِيلًا ﴾ [الأحزاب: 3]",
        "﴿ وَلَا تَيْأَسُوا مِن رَّوْحِ اللَّهِ ﴾ [يوسف: 87]",
        "﴿ وَاسْتَعِينُوا بِالصَّبْرِ وَالصَّلَاةِ ﴾ [البقرة: 45]",
        "﴿ وَإِذَا سَأَلَكَ عِبَادِي عَنِّي فَإِنِّي قَرِيبٌ ﴾ [البقرة: 186]",
        "﴿ رَبَّنَا لَا تُزِغْ قُلُوبَنَا بَعْدَ إِذْ هَدَيْتَنَا ﴾ [آل عمران: 8]",
        "﴿ رَبَّنَا اغْفِرْ لَنَا ذُنُوبَنَا وَإِسْرَافَنَا فِي أَمْرِنَا ﴾ [آل عمران: 147]",
        "﴿ رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً ﴾ [البقرة: 201]",
        "﴿ إِنَّ اللَّهَ لَا يُضِيعُ أَجْرَ الْمُحْسِنِينَ ﴾ [هود: 115]",
        "﴿ وَمَن يَعْمَلْ سُوءًا أَوْ يَظْلِمْ نَفْسَهُ ثُمَّ يَسْتَغْفِرِ اللَّهَ يَجِدِ اللَّهَ غَفُورًا رَّحِيمًا ﴾ [النساء: 110]",
        "﴿ وَإِن تَعُدُّوا نِعْمَةَ اللَّهِ لَا تُحْصُوهَا ﴾ [إبراهيم: 34]",
        "﴿ وَأَنفِقُوا فِي سَبِيلِ اللَّهِ وَلَا تُلْقُوا بِأَيْدِيكُمْ إِلَى التَّهْلُكَةِ ﴾ [البقرة: 195]",
        "﴿ وَلَا تَهِنُوا وَلَا تَحْزَنُوا وَأَنتُمُ الْأَعْلَوْنَ إِن كُنتُم مُّؤْمِنِينَ ﴾ [آل عمران: 139]",
        "﴿ وَمَا الْحَيَاةُ الدُّنْيَا إِلَّا مَتَاعُ الْغُرُورِ ﴾ [آل عمران: 185]",
        "﴿ إِنَّ اللَّهَ لَا يُغَيِّرُ مَا بِقَوْمٍ حَتَّى يُغَيِّرُوا مَا بِأَنفُسِهِمْ ﴾ [الرعد: 11]",
        "﴿ وَأَنَّ سَعْيَهُ سَوْفَ يُرَى ﴾ [النجم: 40]",
        "﴿ فَإِذَا عَزَمْتَ فَتَوَكَّلْ عَلَى اللَّهِ ﴾ [آل عمران: 159]",
        "﴿ إِنَّا لِلَّهِ وَإِنَّا إِلَيْهِ رَاجِعُونَ ﴾ [البقرة: 156]",
        "﴿ وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ ﴾ [الطلاق: 3]",
        "﴿ وَاللَّهُ يَهْدِي مَن يَشَاءُ إِلَى صِرَاطٍ مُّسْتَقِيمٍ ﴾ [البقرة: 213]",
        "﴿ إِنَّ مَعِي رَبِّي سَيَهْدِينِي ﴾ [الشعراء: 62]",
        "﴿ وَأَنزَلْنَا إِلَيْكَ الذِّكْرَ لِتُبَيِّنَ لِلنَّاسِ مَا نُزِّلَ إِلَيْهِمْ ﴾ [النحل: 44]",
        "﴿ وَالَّذِينَ جَاهَدُوا فِينَا لَنَهْدِيَنَّهُمْ سُبُلَنَا ﴾ [العنكبوت: 69]",
        "﴿ سَلَامٌ قَوْلًا مِّن رَّبٍّ رَّحِيمٍ ﴾ [يس: 58]",
        "﴿ وَأَمَّا مَنْ خَافَ مَقَامَ رَبِّهِ وَنَهَى النَّفْسَ عَنِ الْهَوَى ﴾ [النازعات: 40]",
        "﴿ إِنَّ الْحَسَنَاتِ يُذْهِبْنَ السَّيِّئَاتِ ﴾ [هود: 114]",
        "﴿ وَالَّذِينَ آمَنُوا وَعَمِلُوا الصَّالِحَاتِ سَنُدْخِلُهُمْ جَنَّاتٍ تَجْرِي مِن تَحْتِهَا الْأَنْهَارُ ﴾ [النساء: 57]",
        "﴿ وَإِنَّ رَبَّكَ هُوَ الْعَزِيزُ الرَّحِيمُ ﴾ [الشعراء: 9]",
        "﴿ قُلْ إِنَّ صَلَاتِي وَنُسُكِي وَمَحْيَايَ وَمَمَاتِي لِلَّهِ رَبِّ الْعَالَمِينَ ﴾ [الأنعام: 162]"
    ]
    verse = random.choice(verses)

    markup = InlineKeyboardMarkup(row_width=1)
    btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")
    btn_back.style = "danger"
    btn_new = InlineKeyboardButton("🔄 آية أخرى", callback_data="quran")
    btn_new.style = "success"
    markup.add(btn_new, btn_back)

    bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption=f"**📖 آية قرآنية**\n━━━━━━━━━━━━━━━━━━\n\n{verse}",
        parse_mode="Markdown",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data == "news")
def news_section(call):
    news_list = [
        "📰 تم افتتاح مشروع جديد في المنطقة.",
        "📰 فوز الفريق الوطني في المباراة النهائية.",
        "📰 إصدار تحديث جديد لتطبيق التواصل.",
        "📰 اكتشاف جديد في مجال الطب.",
        "📰 ارتفاع مؤشرات البورصة اليوم.",
        "📰 توقيع اتفاقية سلام بين دولتين.",
        "📰 إطلاق مبادرة جديدة لدعم التعليم.",
        "📰 إنخفاض درجة الحرارة غداً."
    ]
    news = random.choice(news_list)

    markup = InlineKeyboardMarkup(row_width=1)
    btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")
    btn_back.style = "danger"
    btn_new = InlineKeyboardButton("🔄 خبر آخر", callback_data="news")
    btn_new.style = "success"
    markup.add(btn_new, btn_back)

    bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption=f"**📰 أخبار**\n━━━━━━━━━━━━━━━━━━\n\n{news}",
        parse_mode="Markdown",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data == "poetry")
def poetry_section(call):
    poems = [
        "**قال المتنبي:**\nوَإِذَا أَتَاكَ عَدُوُّكَ فِي ثَوْبِ صَدِيقٍ، فَلَا تَكُنْ صَدِيقًا لِنَفْسِكَ.",
        "**قال الشافعي:**\nدَعِ الأَيَّامَ تَفْعَلُ مَا تَشَاءُ، وَطِبْ نَفْسًا إِذَا حَكَمَ الْقَضَاءُ.",
        "**قال أحمد شوقي:**\nوَمَا نَيْلُ الْمُنَى إِلَّا بِصَبْرٍ، وَمَا صَبْرُ الْفَتَى إِلَّا بِعَزْمٍ.",
        "**قال نزار قباني:**\nحِينَ تَحِبُّ امْرَأَةً، فَإِنَّكَ تَصِيرُ شَاعِرًا.",
        "**قال المتنبي:**\nالخَيْلُ وَاللَّيْلُ وَالْبَيْدَاءُ تَعْرِفُنِي، وَالسَّيْفُ وَالرُّمْحُ وَالْقِرْطَاسُ وَالْقَلَمُ.",
        "**قال أحمد شوقي:**\nوَمَا الْإِنْسَانُ إِلَّا مَا أَرَادَ، وَمَا الْأَيَّامُ إِلَّا مَا تَجِدُ."
    ]
    poem = random.choice(poems)

    markup = InlineKeyboardMarkup(row_width=1)
    btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")
    btn_back.style = "danger"
    btn_new = InlineKeyboardButton("🔄 قصيدة أخرى", callback_data="poetry")
    btn_new.style = "success"
    markup.add(btn_new, btn_back)

    bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption=f"**📝 شعر**\n━━━━━━━━━━━━━━━━━━\n\n{poem}",
        parse_mode="Markdown",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data == "quotes")
def quotes_section(call):
    quotes = [
        {"text": "«الحياة ليست أن تنتظر العاصفة تمر، بل أن تتعلم الرقص تحت المطر.»", "author": "🕊️ حكيم مجهول"},
        {"text": "«النجاح ليس نهائيًا، والفشل ليس قاتلاً، بل الشجاعة للاستمرار هي ما يهم.»", "author": "✍️ كاتب غامض"},
        {"text": "«لا تحكم على يومك من حصادك، بل من البذور التي زرعتها.»", "author": "🌱 فيلسوف الظل"},
        {"text": "«أفضل طريقة لبدء شيء ما هي التوقف عن الكلام والبدء في الفعل.»", "author": "💫 صاحب الحكمة"},
        {"text": "«لا شيء مستحيل، حتى لو كان ذلك يعني أن تسير على الماء.»", "author": "🌟 راوي الأسرار"},
        {"text": "«الورود لا تسأل لماذا تذبل، بل تذبل لأنها أعطت كل ما لديها.»", "author": "🌹 قلب نابض"},
        {"text": "«الصمت هو أبلغ رد على الغباء.»", "author": "📖 كتاب الصمت"},
        {"text": "«من يبحث عن صديق بلا عيب، يبقى بلا صديق.»", "author": "🤝 حكيم القلوب"},
        {"text": "«الغضب هو ريح تُطفئ نور العقل.»", "author": "🕯️ نور الحكمة"},
        {"text": "«السعادة ليست وجهة، بل طريقة للسفر.»", "author": "🚀 مسافر الروح"},
        {"text": "«إن كان الفشل هو الأم، فالصبر هو الأب.»", "author": "🌳 جذور الصبر"},
        {"text": "«الأيدي التي تمد يد العون، لا تنتظر المقابل.»", "author": "🤲 روح العطاء"},
        {"text": "«الفرص لا تأتي بالصدفة، بل هي نتاج الإعداد والعمل.»", "author": "⚡ طاقة الإنجاز"},
        {"text": "«عندما تتغير اتجاه الريح، يبني البعض جدراناً، والبعض الآخر يبني طواحين هواء.»", "author": "🌀 حكيم الرياح"},
        {"text": "«الجمال ليس في الوجه، بل هو نور في القلب.»", "author": "✨ نور الروح"},
        {"text": "«الحب هو الإجابة الوحيدة التي لا تحتاج إلى سؤال.»", "author": "❤️ قلب عاشق"},
        {"text": "«الصديق الحقيقي هو من يدخل قلبك عندما يكون العالم كله خارجاً.»", "author": "🤝 صديق الوفاء"},
        {"text": "«الكلمات الجيدة كالنوافذ المفتوحة، تسمح للضوء بالدخول.»", "author": "🪟 كاتب النور"},
        {"text": "«كل نهاية هي بداية جديدة.»", "author": "🌅 بزوغ الفجر"},
        {"text": "«الغروب ليس نهاية اليوم، بل هو مقدمه لقمر جميل.»", "author": "🌙 راوي الليل"},
        {"text": "«في قلب كل إنسان حديقة، وأجمل ما فيها ما يزرعه من حب.»", "author": "🌺 بستاني الروح"},
        {"text": "«الصبر مفتاح الفرج، والصلاة مفتاح النجاح.»", "author": "🕌 تاج الإيمان"},
        {"text": "«الذكريات هي الجسر الذي يربط الماضي بالحاضر.»", "author": "🌉 حارس الذاكرة"},
        {"text": "«ليس المهم أن تكون الأول، بل المهم أن تكون الأفضل في ما تفعل.»", "author": "🏆 روح التميز"},
        {"text": "«الابتسامة هي أقصر مسافة بين قلبين.»", "author": "😊 سعادة القلوب"},
        {"text": "«الحياة رحلة، فاختر رفيقك جيداً.»", "author": "🧭 مرشد الطريق"},
        {"text": "«الجاهل يكرر أخطائه، والعاقل يتعلم منها.»", "author": "📚 حكيم المعرفة"},
        {"text": "«الأمل هو الشيء الوحيد الذي لا يموت في الإنسان.»", "author": "🌟 مشعل الأمل"},
        {"text": "«لا قيمة للكلمات بدون أفعال تثبتها.»", "author": "💪 رجل الإنجاز"},
        {"text": "«الجمال الحقيقي هو ما يبقى في القلب بعد الرحيل.»", "author": "💖 روح الجمال"}
    ]

    quote = random.choice(quotes)

    markup = InlineKeyboardMarkup(row_width=1)
    btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")
    btn_back.style = "danger"
    btn_new = InlineKeyboardButton("🔄 اقتباس آخر", callback_data="quotes")
    btn_new.style = "success"
    markup.add(btn_new, btn_back)

    caption = (
        f"**💬 اقتباس**\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"{quote['text']}\n\n"
        f"— {quote['author']}"
    )

    bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption=caption,
        parse_mode="Markdown",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data == "books")
def books_section(call):
    books = [
        "📚 «الأيام» - طه حسين",
        "📚 «مئة عام من العزلة» - غابرييل غارسيا ماركيز",
        "📚 «الجريمة والعقاب» - دوستويفسكي",
        "📚 «الغريب» - ألبير كامو",
        "📚 «الآلة الزمنية» - هربرت جورج ويلز",
        "📚 «أرض زيكولا» - عمرو عبد الحميد"
    ]
    book = random.choice(books)

    markup = InlineKeyboardMarkup(row_width=1)
    btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")
    btn_back.style = "danger"
    btn_new = InlineKeyboardButton("🔄 كتاب آخر", callback_data="books")
    btn_new.style = "success"
    markup.add(btn_new, btn_back)

    bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption=f"**📚 كتب**\n━━━━━━━━━━━━━━━━━━\n\n{book}",
        parse_mode="Markdown",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data == "wallpapers")
def wallpapers_section(call):
    markup = InlineKeyboardMarkup(row_width=1)
    btn_back = InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")
    btn_back.style = "danger"
    markup.add(btn_back)

    bo
