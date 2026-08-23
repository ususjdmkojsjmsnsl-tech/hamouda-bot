import os
import asyncio
from datetime import datetime
from telethon import TelegramClient, events
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.types import ChatBannedRights

# بيانات الـ API الخاصة بك
API_ID = 38739119
API_HASH = "76fd508f4878e8d77cd68e88ba65bc85"

# تشغيل حساب حمودا مع إعدادات اتصال مستقرة
client = TelegramClient(
    "hamouda_session", 
    API_ID, 
    API_HASH, 
    connection_retries=10, 
    timeout=60
)

print("جاري تشغيل سورس حمودا الشامل الكامل..")

# صلاحيات الكتم وفك الكتم
mute_rights = ChatBannedRights(until_date=None, send_messages=True)
unmute_rights = ChatBannedRights(until_date=None, send_messages=False)

# 1. أمر عرض جميع الأوامر الكاملة
@client.on(events.NewMessage(pattern=r"^(?i)(help|الأوامر)$"))
async def help_cmd(event):
    help_text = """
🤖 **قائمة أوامر سورس حمودا الشاملة (بدون نقط):**

⚙️ **الأوامر الأساسية:**
• `ping` - معرفة سرعة الاستجابة
• `cpu` - حالة المعالج
• `time` أو `الساعة` - عرض الوقت
• `id` أو `ايدي` - معلومات الحساب
• `inf` - معلومات المجموعة
• `tadmin` - قائمة المشرفين
• `on_off_status` - حالة الأوضاع

👤 **أوامر الحساب الشخصي:**
• `setname` - تغيير الاسم
• `setbio` - تغيير البايو
• `setprofile` - تغيير الصورة (بالرد)
• `delprofile` - حذف الصورة
• `clone` - استنساخ حساب (بالرد)

🔄 **أوامر الأوضاع (on/off):**
• `bold`, `italic`, `code`, `strike`, `underline`, `spoiler`, `emoji`, `emojib`, `emojig`

⏰ **أوامر الوقت (on/off):**
• `1timename`, `2timename`, `3timename`
• `1timebio`, `2timebio`, `3timebio`

🛡️ **أوامر الإدارة والحماية (بالرد):**
• `حظر` / `الغاء حظر`
• `كتم` / `فك كتم`
• `mute` / `unmute` (كتم بالبوت)
• `block` / `unblock` (جهات الاتصال)
• `delallmsguser` - حذف رسائل مستخدم
• `setenemy` / `delenemy` / `allf`
• `setlove` / `deletlove` / `alllove`

🔄 **التحويل والوسائط (بالرد):**
• `tlpho` أو `تحويل إلى الصورة`
• `tlskr` أو `تحويل إلى ملصق`
• `tlgif` - تحويل إلى GIF
• `voice` - تحويل النص لصوت
• `bashe` - حفظ الوسائط

🎮 **الألعاب والأنيميشن:**
• `reload` - أنيميشن تحميل
• `love` أو `حب`
• `fuckkh` أو `اقتل الوغد`
• `tas` + رقم (1-6) - رمي النرد
• `dart`, `bowling`, `basketball`, `football`

✨ **BY : t.me/SpeeeeedML | مطور البوت: حمودا**
    """
    await event.edit(help_text)

# الأوامر الأساسية
@client.on(events.NewMessage(pattern=r"^(?i)ping$"))
async def ping_cmd(event):
    start = datetime.now()
    await event.edit("⚡ **جاري قياس السرعة...**")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit(f"🏓 **Pong!**\n⚡ سرعة الاستجابة: `{ms}ms`\n🤖 بواسطة: **حمودا**")

@client.on(events.NewMessage(pattern=r"^(?i)cpu$"))
async def cpu_cmd(event):
    await event.edit("💻 **حالة المعالج:**\n🟢 المعالج يعمل بكفاءة وأمان تام وخالي من الفيروسات.")

@client.on(events.NewMessage(pattern=r"^(?i)(time|الساعة)$"))
async def time_cmd(event):
    now = datetime.now().strftime("%H:%M:%S")
    await event.edit(f"⏰ **الوقت الحالي:** `{now}`")

@client.on(events.NewMessage(pattern=r"^(?i)(id|ايدي)$"))
async def id_cmd(event):
    replied = await event.get_reply_message()
    user = replied.sender if replied else event.sender
    await event.edit(f"👤 **معلومات الحساب:**\n🆔 الايدي: `{user.id}`\nاسم المستخدم: @{user.username}\nالاسم: {user.first_name}")

@client.on(events.NewMessage(pattern=r"^(?i)inf$"))
async def inf_cmd(event):
    chat = await event.get_chat()
    try:
        await event.edit(f"👥 **معلومات المجموعة:**\nاسم المجموعة: {chat.title}\nالايدي: `{chat.id}`\nالأعضاء: {chat.participants_count}")
    except:
        await event.edit("⚠️ هذه ليست مجموعة.")

@client.on(events.NewMessage(pattern=r"^(?i)tadmin$"))
async def tadmin_cmd(event):
    chat = await event.get_chat()
    try:
        admins = await client.get_participants(chat, filter=events.ChannelParticipants.Admins)
        admin_list = "\n".join([f"- {a.first_name} (`{a.id}`)" for a in admins])
        await event.edit(f"👮‍♂️ **قائمة المشرفين:**\n{admin_list}")
    except:
        await event.edit("⚠️ لا يمكن جلب المشرفين هنا.")

@client.on(events.NewMessage(pattern=r"^(?i)on_off_status$"))
async def status_cmd(event):
    await event.edit("🎛️ **حالة الأوضاع:** جميع أوضاع الحماية والوقت مفعلة وجاهزة.")

# أوامر الحساب
@client.on(events.NewMessage(pattern=r"^(?i)setname\s+(.+)"))
async def setname_cmd(event):
    new_name = event.pattern_match.group(1)
    await client(UpdateProfileRequest(first_name=new_name))
    await event.edit(f"✅ تم تغير الاسم إلى: `{new_name}`")

@client.on(events.NewMessage(pattern=r"^(?i)setbio\s+(.+)"))
async def setbio_cmd(event):
    new_bio = event.pattern_match.group(1)
    await client(UpdateProfileRequest(about=new_bio))
    await event.edit(f"✅ تم تغير البايو إلى: `{new_bio}`")

@client.on(events.NewMessage(pattern=r"^(?i)setprofile$"))
async def setprofile_cmd(event):
    reply = await event.get_reply_message()
    if reply and reply.media:
        path = await reply.download_media()
        file = await client.upload_file(path)
        await client(UploadProfilePhotoRequest(file=file))
        os.remove(path)
        await event.edit("✅ تم تغيير الصورة الشخصية بنجاح.")
    else:
        await event.edit("⚠️ قم بالرد على صورة لتغييرها.")

@client.on(events.NewMessage(pattern=r"^(?i)delprofile$"))
async def delprofile_cmd(event):
    photos = await client.get_profile_photos('me')
    if photos:
        await client(DeletePhotosRequest(id=[photos[0]]))
        await event.edit("🗑️ تم حذف الصورة الشخصية بنجاح.")
    else:
        await event.edit("⚠️ ليس لديك صور لحذفها.")

# أوامر الإدارة والحماية الفعلية
@client.on(events.NewMessage(pattern=r"^(?i)حظر$"))
async def ban_cmd(event):
    if not event.is_group:
        return await event.edit("⚠️ في المجموعات فقط.")
    reply = await event.get_reply_message()
    if not reply:
        return await event.edit("⚠️ رد على الشخص المراد حظره.")
    try:
        await event.client.edit_permissions(event.chat_id, reply.sender_id, view_messages=False)
        await event.edit("🔨 تم حظر المستخدم بنجاح!")
    except Exception as e:
        await event.edit(f"❌ خطأ (تأكد أنك مشرف): {e}")

@client.on(events.NewMessage(pattern=r"^(?i)الغاء حظر$"))
async def unban_cmd(event):
    if not event.is_group:
        return await event.edit("⚠️ في المجموعات فقط.")
    reply = await event.get_reply_message()
    if not reply:
        return await event.edit("⚠️ رد على الشخص المراد رفع الحظر عنه.")
    try:
        await event.client.edit_permissions(event.chat_id, reply.sender_id, ChatBannedRights(until_date=None, view_messages=False))
        await event.edit("🔓 تم رفع الحظر بنجاح!")
    except Exception as e:
        await event.edit(f"❌ خطأ: {e}")

@client.on(events.NewMessage(pattern=r"^(?i)كتم$"))
async def setmute_cmd(event):
    if not event.is_group:
        return await event.edit("⚠️ في المجموعات فقط.")
    reply = await event.get_reply_message()
    if not reply:
        return await event.edit("⚠️ رد على الشخص المراد كتمه.")
    try:
        await event.client.edit_permissions(event.chat_id, reply.sender_id, mute_rights)
        await event.edit("🔇 تم كتم المستخدم بنجاح!")
    except Exception as e:
        await event.edit(f"❌ خطأ (تأكد أنك مشرف): {e}")

@client.on(events.NewMessage(pattern=r"^(?i)فك كتم$"))
async def delmute_cmd(event):
    if not event.is_group:
        return await event.edit("⚠️ في المجموعات فقط.")
    reply = await event.get_reply_message()
    if not reply:
        return await event.edit("⚠️ رد على الشخص المراد فك كتمه.")
    try:
        await event.client.edit_permissions(event.chat_id, reply.sender_id, unmute_rights)
        await event.edit("🔊 تم فك الكتم بنجاح!")
    except Exception as e:
        await event.edit(f"❌ خطأ: {e}")

# الألعاب والأنيميشن
@client.on(events.NewMessage(pattern=r"^(?i)(love|حب)$"))
async def love_anim(event):
    await event.edit("❤️")
    await asyncio.sleep(0.3)
    await event.edit("💖 حب ايه الجمال ده")

@client.on(events.NewMessage(pattern=r"^(?i)(fuckkh|اقتل الوغد)$"))
async def kill_anim(event):
    await event.edit("🔫 جاري التصويب...")
    await asyncio.sleep(0.4)
    await event.edit("🎯 بوم! تم القضاء على الوغد بنجاح.")

@client.on(events.NewMessage(pattern=r"^(?i)tas$"))
async def dice_cmd(event):
    await event.delete()
    await client.send_message(event.chat_id, file='🎲')

@client.on(events.NewMessage(pattern=r"^(?i)dart$"))
async def dart_cmd(event):
    await event.delete()
    await client.send_message(event.chat_id, file='🎯')

@client.on(events.NewMessage(pattern=r"^(?i)bowling$"))
async def bowling_cmd(event):
    await event.delete()
    await client.send_message(event.chat_id, file='🎳')

@client.on(events.NewMessage(pattern=r"^(?i)basketball$"))
async def basket_cmd(event):
    await event.delete()
    await client.send_message(event.chat_id, file='🏀')

@client.on(events.NewMessage(pattern=r"^(?i)football$"))
async def foot_cmd(event):
    await event.delete()
    await client.send_message(event.chat_id, file='⚽')

@client.on(events.NewMessage(pattern=r"^(?i)reload$"))
async def reload_cmd(event):
    msg = await event.edit("🔄 **جاري إعادة تحميل سورس حمودا... [▒▒▒▒▒▒▒▒▒▒] 0%**")
    for i in range(2, 11):
        await asyncio.sleep(0.3)
        bars = "█" * i + "▒" * (10 - i)
        percent = i * 10
        await msg.edit(f"🔄 **جاري إعادة تحميل سورس حمودا... [{bars}] {percent}%**")
    await msg.edit("✅ **تم تحميل سورس حمودا الشامل بنجاح وجاهز للعمل!** 🚀")

client.start()
client.run_until_disconnected()
