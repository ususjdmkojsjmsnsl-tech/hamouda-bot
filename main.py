import logging
import random
from datetime import datetime
from telethon import TelegramClient, events
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.types import ReplyInlineMarkup, KeyboardButtonRow, KeyboardButtonCallback

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
    if not event.is_group:
        return False
    try:
        chat = await event.get_chat()
        sender_id = event.sender_id
        async for admin in client.iter_participants(chat, filter=events.ChannelParticipants.ADMINISTRATORS):
            if admin.id == sender_id:
                return True
        return False
    except Exception:
        return False


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
        await event.reply("⚠️ الرسالة التي ردرت عليها ليست صورة.")
        return

    try:
        # تحميل الصورة المؤقتة
        photo_path = await reply_msg.download_media()
        
        # رفع الصورة وتعيينها كبروفايل للحساب الشخصي
        file = await client.upload_file(photo_path)
        await client(UploadProfilePhotoRequest(file=file))
        
        # تعديل نفس الرسالة لتأكيد النجاح
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
        "🔹 <code>حمودا ايدي</code> - لمعرفة الأيدي الخاص بك.\n"
        "🔹 <code>حمودا الوقت</code> - لمعرفة الوقت والتاريخ.\n\n"
        "🛡️ <b>أوامر الإدارة والحماية (في الجروبات):</b>\n"
        "🔹 <code>حمودا كتم</code> (بالرد) - لكتم عضو في المجموعة.\n"
        "🔹 <code>حمودا فك كتم</code> (بالرد) - لفك الكتم عن عضو.\n"
        "🔹 <code>حمودا حظر</code> (بالرد) - لحظر مستخدم نهائياً.\n"
        "🔹 <code>حمودا طرد</code> (بالرد) - لطرد مستخدم.\n\n"
        "🎮 <b>الألعاب والترفيه:</b>\n"
        "🔹 <code>لعبة الحظ</code> أو <code>حجر ورق مقص</code>\n"
        "🔹 <code>نسبة الحب [اسم الشخص]</code>\n"
        "🔹 <code>نكتة</code> أو <code>حكمة</code>"
    )
    await event.reply(commands_text, parse_mode='html')


# ============================================================
# === 4. أوامر الإدارة (كتم، فك كتم، حظر، طرد) ===
# ============================================================
@client.on(events.NewMessage(pattern=r'حمودا كتم'))
async def mute_user(event):
    if not event.is_group:
        return
    if await is_user_admin(event) or event.sender_id == (await client.get_me()).id:
        if event.is_reply:
            reply = await event.get_reply_message()
            try:
                # تقييد المستخدم من إرسال الرسائل
                await client.edit_permissions(event.chat_id, reply.sender_id, send_messages=False)
                await event.reply("🔇 تم كتم المستخدم بنجاح.")
            except Exception as e:
                await event.reply(f"❌ خطأ: {e}")


@client.on(events.NewMessage(pattern=r'حمودا فك كتم'))
async def unmute_user(event):
    if not event.is_group:
        return
    if await is_user_admin(event) or event.sender_id == (await client.get_me()).id:
        if event.is_reply:
            reply = await event.get_reply_message()
            try:
                await client.edit_permissions(event.chat_id, reply.sender_id, send_messages=True)
                await event.reply("🔊 تم فك الكتم عن المستخدم.")
            except Exception as e:
                await event.reply(f"❌ خطأ: {e}")


@client.on(events.NewMessage(pattern=r'حمودا حظر'))
async def ban_user(event):
    if not event.is_group:
        return
    if await is_user_admin(event) or event.sender_id == (await client.get_me()).id:
        if event.is_reply:
            reply = await event.get_reply_message()
            try:
                await client.edit_permissions(event.chat_id, reply.sender_id, view_messages=False)
                await event.reply("🚷 تم حظر المستخدم من المجموعة.")
            except Exception as e:
                await event.reply(f"❌ خطأ: {e}")


@client.on(events.NewMessage(pattern=r'حمودا طرد'))
async def kick_user(event):
    if not event.is_group:
        return
    if await is_user_admin(event) or event.sender_id == (await client.get_me()).id:
        if event.is_reply:
            reply = await event.get_reply_message()
            try:
                await client.kick_participant(event.chat_id, reply.sender_id)
                await event.reply("👢 تم طرد المستخدم.")
            except Exception as e:
                await event.reply(f"❌ خطأ: {e}")


# ============================================================
# === 5. الألعاب والترفيه (حجر ورق مقص، نسبة الحب، نكت) ===
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


# ============================================================
# === التشغيل الأساسي للـ UserBot ===
# ============================================================
def main():
    print("جاري تشغيل حسابك الشخصي عبر Telethon مع الأوامر الجديدة...")
    client.start()
    print("تم تسجيل الدخول بنجاح والحساب الشخصي يعمل الآن!")
    client.run_until_disconnected()

if __name__ == '__main__':
    main()
        
