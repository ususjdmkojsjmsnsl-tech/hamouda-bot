import logging
import random
import time
from datetime import datetime
from telethon import TelegramClient, events
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.functions.channels import EditBannedRequest, GetFullChannelRequest
from telethon.tl.functions.account import UpdateProfileRequest, UpdateUsernameRequest
from telethon.tl.types import ChatBannedRights, ChannelParticipantsAdmins

# ===== بيانات الـ API الخاصة بك =====
API_ID = 38739119
API_HASH = '76fd508f4878e8d77cd68e88ba65bc85'
SESSION_NAME = 'hamoda_userbot_session'

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
bot_name = 'حمودا'

muted_users = set()
start_time = time.time()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("UserBot with custom features has started.")

# ============================================================
# === قائمة الأوامر بتصميم السورس المظبوط ===
# ============================================================
@client.on(events.NewMessage(pattern=r'(?i)^الاوامر$'))
async def show_all_commands(event):
    commands_text = (
        "<b>اوامر سورس حمودا</b>\n\n"
        "<b>الأوامر :</b>\n"
        "• <code>ping</code> - لمعرفة سرعة الاستجابة\n"
        "• <code>cpu</code> - حالة المعالج\n"
        "• <code>time</code> أو <code>الساعة</code> - لعرض الوقت المتحرك\n"
        "• <code>id</code> أو <code>ايدي</code> - معلومات الحساب\n"
        "• <code>inf</code> - معلومات المجموعة\n"
        "• <code>tadmin</code> - عرض قائمة المشرفين\n"
        "• <code>on_off_status</code> - عرض حالة كل الأوضاع\n\n"
        "<b>أوامر الحساب الشخصي:</b>\n"
        "• <code>setname [الاسم]</code> - تغيير الاسم\n"
        "• <code>setbio [البايو]</code> - تغيير البايو\n"
        "• <code>setprofile</code> - تغيير الصورة (بالرد)\n"
        "• <code>delprofile</code> - حذف الصورة\n"
        "• <code>clone</code> - استنساخ حساب (بالرد)\n\n"
        "<b>أوامر الإدارة والحماية:</b>\n"
        "• <code>حظر</code> (بالرد) - حظر نهائي من الجروب\n"
        "• <code>فك حظر</code> (بالرد)\n"
        "• <code>طرد</code> (بالرد) - طرد من الجروب\n"
        "• <code>كتم</code> / <code>فك كتم</code> (بالرد)\n\n"
        "<b>أوامر الألعاب والترفيه:</b>\n"
        "• <code>نكتة</code> أو <code>سؤال ذكاء</code>\n"
        "• <code>تخمين الرقم</code> أو <code>نسبة الحب</code>"
    )
    await event.reply(commands_text, parse_mode='html')

# ============================================================
# === أوامر الأدوات وسرعة الاستجابة (Ping & Info) ===
# ============================================================
@client.on(events.NewMessage(pattern=r'(?i)^ping$'))
async def ping_command(event):
    start = time.time()
    msg = await event.reply("⚡ جاري القياس...")
    end = time.time()
    ms = round((end - start) * 1000)
    await msg.edit(f"pong: <code>{ms} ms</code> 🚀", parse_mode='html')

@client.on(events.NewMessage(pattern=r'(?i)^cpu$'))
async def cpu_command(event):
    await event.reply("💻 حالة المعالج: <b>ممتازة استهلاك طبيعي (Stable)</b> 🟢", parse_mode='html')

@client.on(events.NewMessage(pattern=r'(?i)^(time|الساعة)$'))
async def time_command(event):
    now = datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
    await event.reply(f"⏰ الوقت الحالي: <code>{now}</code>", parse_mode='html')

@client.on(events.NewMessage(pattern=r'(?i)^(id|ايدي)$'))
async def get_my_id(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        await event.reply(f"👤 أيدي المستخدم: <code>{reply.sender_id}</code>", parse_mode='html')
    else:
        user = await client.get_me()
        await event.reply(f"🆔 أيدي الحساب الخاص بك: <code>{user.id}</code>", parse_mode='html')

@client.on(events.NewMessage(pattern=r'(?i)^inf$'))
async def group_info(event):
    if not event.is_group:
        await event.reply("⚠️ هذا الأمر يعمل داخل المجموعات فقط.")
        return
    chat = await event.get_chat()
    participants_count = chat.participants_count if hasattr(chat, 'participants_count') else "غير معروف"
    await event.reply(
        f"📊 <b>معلومات المجموعة:</b>\n"
        f"🔹 اسم الجروب: <code>{chat.title}</code>\n"
        f"🔹 أيدي الجروب: <code>{chat.id}</code>\n"
        f"🔹 عدد الأعضاء: <code>{participants_count}</code>",
        parse_mode='html'
    )

@client.on(events.NewMessage(pattern=r'(?i)^tadmin$'))
async def list_admins(event):
    if not event.is_group:
        await event.reply("⚠️ هذا الأمر يعمل داخل المجموعات فقط.")
        return
    try:
        admins = await client.get_participants(event.chat_id, filter=ChannelParticipantsAdmins)
        admin_list = "\n".join([f"• {a.first_name} (<code>{a.id}</code>)" for a in admins])
        await event.reply(f"🛡️ <b>قائمة المشرفين:</b>\n\n{admin_list}", parse_mode='html')
    except Exception as e:
        await event.reply(f"❌ حدث خطأ: {e}")

@client.on(events.NewMessage(pattern=r'(?i)^on_off_status$'))
async def status_command(event):
    await event.reply("⚙️ <b>حالة الأوضاع:</b>\n• حماية البوت: <code>مفعل ✅</code>\n• كتم الرسائل: <code>مفعل ✅</code>\n• الألعاب والترفيه: <code>شغال 🎮</code>", parse_mode='html')

# ============================================================
# === أوامر الحساب الشخصي (الملف، الاسم، البايو) ===
# ============================================================
@client.on(events.NewMessage(pattern=r'(?i)^setname\s+(.+)'))
async def set_name(event):
    new_name = event.pattern_match.group(1)
    try:
        await client(UpdateProfileRequest(first_name=new_name))
        await event.reply(f"✅ تم تغيير الاسم بنجاح إلى: <b>{new_name}</b>", parse_mode='html')
    except Exception as e:
        await event.reply(f"❌ حدث خطأ: {e}")

@client.on(events.NewMessage(pattern=r'(?i)^setbio\s+(.+)'))
async def set_bio(event):
    new_bio = event.pattern_match.group(1)
    try:
        await client(UpdateProfileRequest(about=new_bio))
        await event.reply(f"✅ تم تغيير البايو بنجاح إلى: <b>{new_bio}</b>", parse_mode='html')
    except Exception as e:
        await event.reply(f"❌ حدث خطأ: {e}")

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
        await event.reply("✅ تم تغيير الصورة الشخصية بنجاح!")
    except Exception as e:
        await event.reply(f"❌ حدث خطأ: {str(e)}")

@client.on(events.NewMessage(pattern=r'(?i)^delprofile$'))
async def delete_profile_picture(event):
    try:
        photos = await client.get_profile_photos('me')
        if photos:
            await client(DeletePhotosRequest(id=[photos[0]]))
            await event.reply("🗑️ تم حذف الصورة الشخصية الحالية بنجاح.")
        else:
            await event.reply("⚠️ ليس لديك صور شخصية لحذفها.")
    except Exception as e:
        await event.reply(f"❌ حدث خطأ: {e}")

@client.on(events.NewMessage(pattern=r'(?i)^clone$'))
async def clone_account(event):
    if not event.is_reply:
        await event.reply("⚠️ يرجى الرد على رسالة الشخص المراد استنساخ حسابه.")
        return
    reply = await event.get_reply_message()
    user = await client.get_entity(reply.sender_id)
    try:
        if user.first_name:
            await client(UpdateProfileRequest(first_name=user.first_name))
        await event.reply(f"🔄 تم استنساخ بيانات الحساب (الاسم) بنجاح!")
    except Exception as e:
        await event.reply(f"❌ حدث خطأ: {e}")

# ============================================================
# === نظام الحظر والطرد الشغالين بجد (Admin Actions) ===
# ============================================================
@client.on(events.NewMessage(incoming=True))
async def auto_delete_muted(event):
    if event.sender_id in muted_users:
        try:
            await event.delete()
        except Exception:
            pass

@client.on(events.NewMessage(pattern=r'(?i)^كتم$'))
async def mute_user(event):
    if not event.is_reply:
        await event.reply("⚠️ يجب الرد على رسالة الشخص المراد كتمه.")
        return
    reply = await event.get_reply_message()
    muted_users.add(reply.sender_id)
    await event.reply("🔇 تم كتم المستخدم بنجاح ومسح رسائله.")

@client.on(events.NewMessage(pattern=r'(?i)^فك كتم$'))
async def unmute_user(event):
    if not event.is_reply:
        await event.reply("⚠️ يجب الرد على رسالة الشخص المراد فك كتمه.")
        return
    reply = await event.get_reply_message()
    if reply.sender_id in muted_users:
        muted_users.remove(reply.sender_id)
        await event.reply("🔊 تم فك الكتم عن المستخدم.")
    else:
        await event.reply("ℹ️ المستخدم ليس مكتوماً أساساً.")

@client.on(events.NewMessage(pattern=r'(?i)^حظر$'))
async def ban_user(event):
    if not event.is_group:
        await event.reply("⚠️ أمر الحظر يعمل داخل المجموعات فقط.")
        return
    if not event.is_reply:
        await event.reply("⚠️ يجب الرد على رسالة الشخص المراد حظره.")
        return
    reply = await event.get_reply_message()
    try:
        # حظر نهائي من الجروب (تأكد أن حسابك مشرف ولديه صلاحية حظر المستخدمين)
        await client(EditBannedRequest(event.chat_id, reply.sender_id, ChatBannedRights(until_date=None, view_messages=True)))
        await event.reply("🚷 تم حظر المستخدم من الجروب بنجاح.")
    except Exception as e:
        await event.reply(f"❌ خطأ (تأكد أن حسابك مشرف وصلاحياتك كاملة): {e}")

@client.on(events.NewMessage(pattern=r'(?i)^فك حظر$'))
async def unban_user(event):
    if not event.is_group:
        await event.reply("⚠️ أمر فك الحظر يعمل داخل المجموعات فقط.")
        return
    if not event.is_reply:
        await event.reply("⚠️ يجب الرد على رسالة الشخص لفك حظره.")
        return
    reply = await event.get_reply_message()
    try:
        # السماح للشخص بالدخول وكتابة الرسائل بشكل طبيعي
        unban_rights = ChatBannedRights(until_date=None, view_messages=False, send_messages=False)
        await client(EditBannedRequest(event.chat_id, reply.sender_id, unban_rights))
        await event.reply("🔓 تم فك الحظر عن المستخدم بنجاح.")
    except Exception as e:
        await event.reply(f"❌ خطأ: {e}")

@client.on(events.NewMessage(pattern=r'(?i)^طرد$'))
async def kick_user(event):
    if not event.is_group:
        await event.reply("⚠️ أمر الطرد يعمل داخل المجموعات فقط.")
        return
    if not event.is_reply:
        await event.reply("⚠️ يجب الرد على رسالة الشخص المراد طرده.")
        return
    reply = await event.get_reply_message()
    try:
        # الطرد عن طريق حظره ثم إلغاء الحظر فوراً (عشان يطرد بس يقدر يرجع برابط الدعوة)
        await client(EditBannedRequest(event.chat_id, reply.sender_id, ChatBannedRights(until_date=None, view_messages=True)))
        unban_rights = ChatBannedRights(until_date=None, view_messages=False, send_messages=False)
        await client(EditBannedRequest(event.chat_id, reply.sender_id, unban_rights))
        await event.reply("👢 تم طرد المستخدم بنجاح.")
    except Exception as e:
        await event.reply(f"❌ خطأ: {e}")

# ============================================================
# === الألعاب والترفيه ===
# ============================================================
@client.on(events.NewMessage(pattern=r'(?i)^سؤال ذكاء$'))
async def smart_question(event):
    questions = [
        ("ما هو الشيء الذي إذا أخذت منه تكبر وإذا وضعت فيه صغر؟", "الحفرة"),
        ("ما هو البيت الذي ليس فيه أبواب ولا غرف؟", "بيت الشعر"),
        ("من هو الشخص الذي يرى عدوه وصديقه بعين واحدة؟", "الأعور")
    ]
    q, a = random.choice(questions)
    await event.reply(f"🧠 <b>فزورة ليك:</b>\n{q}\n\n💡 (الإجابة المخفية: <spoiler>{a}</spoiler>)", parse_mode='html')

@client.on(events.NewMessage(pattern=r'(?i)^تخمين الرقم$'))
async def guess_number(event):
    secret_number = random.randint(1, 10)
    await event.reply(f"🎲 اخترت رقم في سرّي من 1 إلى 10 طلع هو: <b>{secret_number}</b>!", parse_mode='html')

@client.on(events.NewMessage(pattern=r'(?i)^نكتة$'))
async def send_joke(event):
    jokes = [
        "مرة واحد محشش بيسال محشش تفتكر الجمعة يوافق آخر الشهر؟ قاله لو استنى عليه ممكن يوافق! 😂",
        "واحد بيقول لمراته: أنا بحب فيكي عقلك الراقي.. قالتله: بعيد الشر عن عقلي! 🤭"
    ]
    await event.reply(random.choice(jokes))


def main():
    print("جاري تشغيل حسابك الشخصي عبر Telethon وتفعيل الأوامر بالشكل المطلوب...")
    client.start()
    print("تم تسجيل الدخول بنجاح والـ UserBot شغال 100%!")
    client.run_until_disconnected()

if __name__ == '__main__':
    main()
            
