import logging
import random
from datetime import datetime
from telethon import TelegramClient, events
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.types import ChatBannedRights

# ===== بيانات الـ API الخاصة بك =====
API_ID = 38739119
API_HASH = '76fd508f4878e8d77cd68e88ba65bc85'
SESSION_NAME = 'hamoda_userbot_session'

# إنشاء عميل تيليجرام لحسابك الشخصي
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
bot_name = 'حمودا'

# ===== إعدادات التسجيل =====
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("UserBot with custom features has started.")


# ============================================================
# === دالة التحقق من المشرفين في المجموعات ===
# ============================================================
async def is_user_admin(event):
    # السماح بالتنفيذ فوراً في الرسائل المحفوظة أو الدردشات الخاصة للاختبار
    if not event.is_group:
        return True
    try:
        chat = await event.get_chat()
        sender_id = event.sender_id
        # إذا كان الحساب هو مالك البوت أو المشرف
        if sender_id == (await client.get_me()).id:
            return True
        async for admin in client.iter_participants(chat, filter=events.ChannelParticipants.ADMINISTRATORS):
            if admin.id == sender_id:
                return True
        return False
    except Exception:
        return True # لتسهيل التجربة في حال القيود


# ============================================================
# === 1. تغيير بروفايل الحساب عند الرد بـ setprofile ===
# ============================================================
@client.on(events.NewMessage(pattern=r'(?i)^setprofile$'))
async def set_profile_picture(event):
    if not event.is_reply:
        await event.reply("⚠️ يرجى الرد على صورة لاستخدام هذا الأمر.")
        return

    reply_msg = await event.get_reply_message()
    if not reply_msg.photo:
        await event.reply("⚠️ الرسالة التي رددت عليها ليست صورة.")
        return

    try:
        photo_path = await reply_msg.download_media()
        file = await client.upload_file(photo_path)
        await client(UploadProfilePhotoRequest(file=file))
        await event.edit("✅ تم تغير الصوره بنجاح!")
    except Exception as e:
        await event.edit(f"❌ حدث خطأ أثناء تغيير الصورة: {str(e)}")


# ============================================================
# === 2. الرد على كلمة (بوت) ===
# ============================================================
@client.on(events.NewMessage(pattern=r'(?i)^بوت$'))
async def reply_to_bot_word(event):
    await event.reply("اسمي حمودا يا معلم 🌟")


# ============================================================
# === 3. قائمة الأوامر الكاملة عند كتابة (الاوامر) ===
# ============================================================
@client.on(events.NewMessage(pattern=r'(?i)^الاوامر$'))
async def show_all_commands(event):
    commands_text = (
        "<b>📋 قائمة أوامر مساعدك الشخصي (حمودا):</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "🛠️ <b>أوامر الحساب والملف الشخصي:</b>\n"
        "🔹 <code>setprofile</code> (بالرد على صورة) - لتغيير بروفايلك الشخصي وتحديثه.\n"
        "🔹 <code>الاوامر</code> - لعرض هذه القائمة.\n"
        "🔹 <code>حمودا ايدي</code> - لمعرفة الأيدي الخاص بك أو الشخص المردود عليه.\n"
        "🔹 <code>حمودا الوقت</code> - لمعرفة الوقت والتاريخ الحالي.\n\n"
        "🛡️ <b>أوامر الإدارة والحماية (في الجروبات):</b>\n"
        "🔹 <code>كتم</code> (بالرد) - لكتم عضو في المجموعة.\n"
        "🔹 <code>فك كتم</code> (بالرد) - لفك الكتم عن عضو.\n"
        "🔹 <code>حظر</code> (بالرد) - لحظر مستخدم نهائياً.\n"
        "🔹 <code>طرد</code> (بالرد) - لطرد مستخدم.\n\n"
        "🎮 <b>الألعاب والترفيه:</b>\n"
        "🔹 <code>لعبة الحظ</code> أو <code>حجر ورق مقص</code>\n"
        "🔹 <code>نسبة الحب [اسم الشخص]</code>\n"
        "🔹 <code>نكتة</code> أو <code>حكمة</code>"
    )
    await event.reply(commands_text, parse_mode='html')


# ============================================================
# === 4. معلومات الحساب والوقت ===
# ============================================================
@client.on(events.NewMessage(pattern=r'(?i)^حمودا ايدي$'))
async def get_my_id(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        await event.reply(f"👤 أيدي المستخدم: <code>{reply.sender_id}</code>", parse_mode='html')
    else:
        user = await client.get_me()
        await event.reply(f"🆔 أيدي الخاص بك: <code>{user.id}</code>", parse_mode='html')


@client.on(events.NewMessage(pattern=r'(?i)^حمودا الوقت$'))
async def get_current_time(event):
    now = datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
    await event.reply(f"⏰ الوقت والتاريخ الحالي: <code>{now}</code>", parse_mode='html')


# ============================================================
# === 5. أوامر الإدارة الفعالة (كتم، فك كتم، حظر، طرد) ===
# ============================================================
@client.on(events.NewMessage(pattern=r'(?i)^كتم$'))
async def mute_user(event):
    if not event.is_group:
        await event.reply("⚠️ هذا الأمر يعمل داخل المجموعات فقط.")
        return
    if await is_user_admin(event):
        if event.is_reply:
            reply = await event.get_reply_message()
            if not reply.sender_id:
                await event.reply("❌ لا يمكن تحديد المستخدم.")
                return
            try:
                # حقوق تقييد الكتم (منع إرسال الرسائل)
                rights = ChatBannedRights(until_date=None, send_messages=True)
                await client.edit_permissions(event.chat_id, reply.sender_id, rights)
                await event.reply("🔇 تم كتم المستخدم بنجاح.")
            except Exception as e:
                await event.reply(f"❌ خطأ: {e}")
        else:
            await event.reply("⚠️ يجب الرد على رسالة الشخص المراد كتمه.")


@client.on(events.NewMessage(pattern=r'(?i)^فك كتم$'))
async def unmute_user(event):
    if not event.is_group:
        await event.reply("⚠️ هذا الأمر يعمل داخل المجموعات فقط.")
        return
    if await is_user_admin(event):
        if event.is_reply:
            reply = await event.get_reply_message()
            if not reply.sender_id:
                await event.reply("❌ لا يمكن تحديد المستخدم.")
                return
            try:
                # إلغاء كافة القيود لفك الكتم
                rights = ChatBannedRights(until_date=None, send_messages=False)
                await client.edit_permissions(event.chat_id, reply.sender_id, rights)
                await event.reply("🔊 تم فك الكتم عن المستخدم.")
            except Exception as e:
                await event.reply(f"❌ خطأ: {e}")
        else:
            await event.reply("⚠️ يجب الرد على رسالة الشخص المراد فك كتمه.")


@client.on(events.NewMessage(pattern=r'(?i)^حظر$'))
async def ban_user(event):
    if not event.is_group:
        await event.reply("⚠️ هذا الأمر يعمل داخل المجموعات فقط.")
        return
    if await is_user_admin(event):
        if event.is_reply:
            reply = await event.get_reply_message()
            if not reply.sender_id:
                await event.reply("❌ لا يمكن تحديد المستخدم.")
                return
            try:
                # حظر نهائي من المجموعة
                rights = ChatBannedRights(until_date=None, view_messages=True)
                await client.edit_permissions(event.chat_id, reply.sender_id, rights)
                await event.reply("🚷 تم حظر المستخدم من المجموعة.")
            except Exception as e:
                await event.reply(f"❌ خطأ: {e}")
        else:
            await event.reply("⚠️ يجب الرد على رسالة الشخص المراد حظره.")


@client.on(events.NewMessage(pattern=r'(?i)^طرد$'))
async def kick_user(event):
    if not event.is_group:
        await event.reply("⚠️ هذا الأمر يعمل داخل المجموعات فقط.")
        return
    if await is_user_admin(event):
        if event.is_reply:
            reply = await event.get_reply_message()
            if not reply.sender_id:
                await event.reply("❌ لا يمكن تحديد المستخدم.")
                return
            try:
                await client.kick_participant(event.chat_id, reply.sender_id)
                await event.reply("👢 تم طرد المستخدم.")
            except Exception as e:
                await event.reply(f"❌ خطأ: {e}")
        else:
            await event.reply("⚠️ يجب الرد على رسالة الشخص المراد طرده.")


# ============================================================
# === 6. الألعاب والترفيه (مفعلة بالكامل) ===
# ============================================================
@client.on(events.NewMessage(pattern=r'(?i)^(حجر ورق مقص|لعبة الحظ)$'))
async def rps_game(event):
    options = ["✂️ مقص", "🪨 حجر", "📄 ورقة"]
    bot_choice = random.choice(options)
    await event.reply(f"اختياري هو: <b>{bot_choice}</b> 🎮", parse_mode='html')


@client.on(events.NewMessage(pattern=r'(?i)^نسبة الحب\s+(.+)'))
async def love_calculator(event):
    target = event.pattern_match.group(1)
    percentage = random.randint(30, 100)
    await event.reply(f"❤️ نسبة الحب بينك وبين <b>{target}</b> هي: <b>{percentage}%</b> 😍", parse_mode='html')


@client.on(events.NewMessage(pattern=r'(?i)^(نكتة|نكت)$'))
async def send_joke(event):
    jokes = [
        "مرة واحد محشش بيسال محشش تفتكر الجمعة يوافق آخر الشهر؟ قاله لو استنى عليه ممكن يوافق! 😂",
        "واحد بيقول لمراته: أنا بحب فيكي عقلك الراقي.. قالتله: بعيد الشر عن عقلي! 🤭",
        "واحد كريم جوز بنتة لواحد كريم، تقابلوا الصبح، حمّاه بيقوله: صباح الخير يا صهري العزيز، إيه رأيك في العروسة؟ قاله: والله العروسة على عيني وراسي، بس الباب اللي قفلته ورايا وأنا جاي هو اللي مصعبها عليّا! 🤣"
    ]
    await event.reply(random.choice(jokes))


@client.on(events.NewMessage(pattern=r'(?i)^حكمة$'))
async def send_wisdom(event):
    wisdoms = [
        "من طال لسانه كثرت خطاياه، ومن كثر كلامه كثر سقطه. 📜",
        "الوقت كالسيف إن لم تقطعه قطعك. ⏳",
        "الصمت حكمة وقليل فاعله. 🌙"
    ]
    await event.reply(random.choice(wisdoms))


# ============================================================
# === التشغيل الأساسي للـ UserBot ===
# ============================================================
def main():
    print("جاري تشغيل حسابك الشخصي عبر Telethon وتفعيل جميع الأوامر...")
    client.start()
    print("تم تسجيل الدخول بنجاح والحساب الشخصي يعمل الآن!")
    client.run_until_disconnected()

if __name__ == '__main__':
    main()
    
