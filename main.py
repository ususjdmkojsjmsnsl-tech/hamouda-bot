import logging
import random
from datetime import datetime
from telethon import TelegramClient, events
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

# ===== بيانات الـ API الخاصة بك =====
API_ID = 38739119
API_HASH = '76fd508f4878e8d77cd68e88ba65bc85'
SESSION_NAME = 'hamoda_userbot_session'

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
bot_name = 'حمودا'

# قاموس لتخزين الأشخاص المكتومين (لكل شات أو عامة)
muted_users = set()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("UserBot with custom features has started.")

async def is_user_admin(event):
    return True

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

@client.on(events.NewMessage(pattern=r'(?i)^بوت$'))
async def reply_to_bot_word(event):
    await event.reply("اسمي حمودا يا كسمك 😂")

@client.on(events.NewMessage(pattern=r'(?i)^الاوامر$'))
async def show_all_commands(event):
    commands_text = (
        "<b>📋 قائمة أوامر مساعدك الشخصي (حمودا):</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "🛠️ <b>أوامر الحساب والملف الشخصي:</b>\n"
        "🔹 <code>setprofile</code> (بالرد على صورة)\n"
        "🔹 <code>الاوامر</code>\n"
        "🔹 <code>ايدي</code>\n"
        "🔹 <code>الوقت</code>\n\n"
        "🛡️ <b>أوامر الإدارة (تعمل في كل مكان):</b>\n"
        "🔹 <code>كتم</code> (بالرد) - مسح رسائله تلقائياً\n"
        "🔹 <code>فك كتم</code> (بالرد)\n"
        "🔹 <code>حظر</code> (بالرد)\n"
        "🔹 <code>طرد</code> (بالرد)\n\n"
        "🎮 <b>الألعاب والترفيه الجديدة:</b>\n"
        "🔹 <code>حجر ورق مقص</code> أو <code>لعبة الحظ</code>\n"
        "🔹 <code>نسبة الحب [اسم الشخص]</code>\n"
        "🔹 <code>تخمين الرقم</code> (لعبة تخمين من 1 لـ 10)\n"
        "🔹 <code>سؤال ذكاء</code> (فوازير)\n"
        "🔹 <code>نكتة</code> أو <code>نكت</code>\n"
        "🔹 <code>حكمة</code>"
    )
    await event.reply(commands_text, parse_mode='html')

@client.on(events.NewMessage(pattern=r'(?i)^ايدي$'))
async def get_my_id(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        await event.reply(f"👤 أيدي المستخدم: <code>{reply.sender_id}</code>", parse_mode='html')
    else:
        user = await client.get_me()
        await event.reply(f"🆔 أيدي الخاص بك: <code>{user.id}</code>", parse_mode='html')

@client.on(events.NewMessage(pattern=r'(?i)^الوقت$'))
async def get_current_time(event):
    now = datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
    await event.reply(f"⏰ الوقت والتاريخ الحالي: <code>{now}</code>", parse_mode='html')

# ============================================================
# === نظام مسح رسائل المكتومين تلقائياً (في أي مكان) ===
# ============================================================
@client.on(events.NewMessage(incoming=True))
async def auto_delete_muted(event):
    if event.sender_id in muted_users:
        try:
            await event.delete()
        except Exception:
            pass

# ============================================================
# === أوامر الإدارة ===
# ============================================================
@client.on(events.NewMessage(pattern=r'(?i)^كتم$'))
async def mute_user(event):
    if not event.is_reply:
        await event.reply("⚠️ يجب الرد على رسالة الشخص المراد كتمه.")
        return
    
    reply = await event.get_reply_message()
    if not reply.sender_id:
        await event.reply("❌ لا يمكن تحديد المستخدم.")
        return

    muted_users.add(reply.sender_id)
    await event.reply("🔇 تم كتم المستخدم بنجاح (سيتم حذف رسائله تلقائياً).")


@client.on(events.NewMessage(pattern=r'(?i)^فك كتم$'))
async def unmute_user(event):
    if not event.is_reply:
        await event.reply("⚠️ يجب الرد على رسالة الشخص المراد فك كتمه.")
        return
    
    reply = await event.get_reply_message()
    if not reply.sender_id:
        await event.reply("❌ لا يمكن تحديد المستخدم.")
        return

    if reply.sender_id in muted_users:
        muted_users.remove(reply.sender_id)
        await event.reply("🔊 تم فك الكتم عن المستخدم.")
    else:
        await event.reply("ℹ️ هذا المستخدم ليس مكتوماً أساساً.")


@client.on(events.NewMessage(pattern=r'(?i)^حظر$'))
async def ban_user(event):
    if not event.is_group:
        await event.reply("⚠️ أمر الحظر يعمل داخل المجموعات فقط.")
        return
    if not event.is_reply:
        await event.reply("⚠️ يجب الرد على رسالة الشخص المراد حظره.")
        return
    
    reply = await event.get_reply_message()
    if not reply.sender_id:
        await event.reply("❌ لا يمكن تحديد المستخدم.")
        return

    try:
        await client(EditBannedRequest(event.chat_id, reply.sender_id, ChatBannedRights(until_date=None, view_messages=True)))
        await event.reply("🚷 تم حظر المستخدم من الجروب بنجاح.")
    except Exception as e:
        await event.reply(f"❌ خطأ (تأكد أن حسابك مشرف ولديه صلاحية الحظر): {e}")


@client.on(events.NewMessage(pattern=r'(?i)^طرد$'))
async def kick_user(event):
    if not event.is_group:
        await event.reply("⚠️ أمر الطرد يعمل داخل المجموعات فقط.")
        return
    if not event.is_reply:
        await event.reply("⚠️ يجب الرد على رسالة الشخص المراد طرده.")
        return
    
    reply = await event.get_reply_message()
    if not reply.sender_id:
        await event.reply("❌ لا يمكن تحديد المستخدم.")
        return
        
    try:
        await client(EditBannedRequest(event.chat_id, reply.sender_id, ChatBannedRights(until_date=None, view_messages=True)))
        await client(EditBannedRequest(event.chat_id, reply.sender_id, ChatBannedRights(until_date=None, view_messages=False)))
        await event.reply("👢 تم طرد المستخدم بنجاح.")
    except Exception as e:
        await event.reply(f"❌ خطأ (تأكد أن حسابك مشرف): {e}")


# ============================================================
# === الألعاب والترفيه (محدثة وكثيرة) ===
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


@client.on(events.NewMessage(pattern=r'(?i)^تخمين الرقم$'))
async def guess_number(event):
    secret_number = random.randint(1, 10)
    user_guess = random.randint(1, 10) # كمحاكاة سريعة أو لعبة حظ تفاعلية
    await event.reply(f"🎲 اخترت رقم في سرّي من 1 إلى 10 طلع هو: <b>{secret_number}</b>!\nلو حظك حلو هتكسب المرة الجاية 😉", parse_mode='html')


@client.on(events.NewMessage(pattern=r'(?i)^سؤال ذكاء$'))
async def smart_question(event):
    questions = [
        ("ما هي الشيء الذي أذا أخذت منه تكبر وإذا وضعت فيه صغر؟", "الحفرة"),
        ("ما هو البيت الذي ليس فيه أبواب ولا غرف؟", "بيت الشعر"),
        ("من هو الشخص الذي يرى عدوه وصديقه بعين واحدة؟", "الأعور"),
        ("ما هو الشيء الذي يسير أمامك ولا تراه؟", "المستقبل"),
        ("ما هو الشئ الذي كلما كبر صغر؟", "العمر")
    ]
    q, a = random.choice(questions)
    await event.reply(f"🧠 <b>فزورة ليك:</b>\n{q}\n\n💡 (الإجابة المخفية: <spoiler>{a}</spoiler>)", parse_mode='html')


@client.on(events.NewMessage(pattern=r'(?i)^(نكتة|نكت)$'))
async def send_joke(event):
    jokes = [
        "مرة واحد محشش بيسال محشش تفتكر الجمعة يوافق آخر الشهر؟ قاله لو استنى عليه ممكن يوافق! 😂",
        "واحد بيقول لمراته: أنا بحب فيكي عقلك الراقي.. قالتله: بعيد الشر عن عقلي! 🤭",
        "واحد كريم جوز بنتة لواحد كريم، تقابلوا الصبح، حمّاه بيقوله: صباح الخير يا صهري العزيز، إيه رأيك في العروسة؟ قاله: والله العروسة على عيني وراسي، بس الباب اللي قفلته ورايا وأنا جاي هو اللي مصعبها عليّا! 🤣",
        "واحد صعيدي راح يعمل اختبار قيادة، الظابط سأله: لو ظهر قدامك شخص وحمار تدوس مين الأول؟ الصعيدي قاله: الحمار طبعا! الظابط قاله: غلط، تدوس الفرامل! الصعيدي قاله: أصل العبقرية إن الحمار هو اللي بيظهر مفاجأة! 😆",
        "اتنين محششين ماشيين في الشارع واحد بيقول للتاني: هو احنا ليه مش ماشيين على الرصيف التاني؟ قاله: عشان الناحية دي أطول! 🚶‍♂️",
        "واحد بخيل ابنه جه قاله: يا بابا أنا نجحت وعايز هدية! أبوه قاله: شايف الشارع العريض اللي هناك ده؟ قاله: أه يا بابا، قاله: نجح السنة الجاية هخلیک تعبره! 💸",
        "مرة واحد غبي دخل سينما لقى الفيلم بيبتدي من آخرة، طلع قال للناس برا: الحقوا, البطل بيعيش في الآخر! 🎬"
    ]
    await event.reply(random.choice(jokes))


@client.on(events.NewMessage(pattern=r'(?i)^حكمة$'))
async def send_wisdom(event):
    wisdoms = [
        "من طال لسانه كثرت خطاياه، ومن كثر كلامه كثر سقطه. 📜",
        "الوقت كالسيف إن لم تقطعه قطعك. ⏳",
        "الصمت حكمة وقليل فاعله. 🌙",
        "من ترقب الناس مات هماً، ولم تخلُ من حاسدٍ لم يعش. 🌟",
        "توقع الخير تجده، وتفائل بالخير تدركه. 🎯"
    ]
    await event.reply(random.choice(wisdoms))


def main():
    print("جاري تشغيل حسابك الشخصي عبر Telethon وتفعيل جميع الأوامر...")
    client.start()
    print("تم تسجيل الدخول بنجاح والحساب الشخصي يعمل الآن!")
    client.run_until_disconnected()

if __name__ == '__main__':
    main()
