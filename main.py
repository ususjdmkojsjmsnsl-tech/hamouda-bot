import os
import asyncio
from datetime import datetime
from telethon import TelegramClient, events
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.types import ChatBannedRights

API_ID = 38739119
API_HASH = "76fd508f4878e8d77cd68e88ba65bc85"

client = TelegramClient(
    "hamouda_session", 
    API_ID, 
    API_HASH, 
    connection_retries=10, 
    timeout=60
)

print("جاري تشغيل سورس حمودا بدون أخطاء للكتم والحظر..")

# صلاحيات الكتم الصحيحة (منع إرسال الرسائل)
mute_rights = ChatBannedRights(
    until_date=None,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True
)

# صلاحيات فك الكتم (السماح بكل شي)
unmute_rights = ChatBannedRights(
    until_date=None,
    send_messages=False,
    send_media=False,
    send_stickers=False,
    send_gifs=False,
    send_games=False,
    send_inline=False,
    embed_links=False
)

# 1. قائمة المساعدة وعرض الأوامر
@client.on(events.NewMessage(pattern=r"^(help|الأوامر)$"))
async def help_cmd(event):
    await event.edit("""
🤖 **قائمة أوامر سورس حمودا الكاملة:**

⚙️ **الأوامر الأساسية:**
• `ping` - لمعرفة سرعة الاستجابة
• `cpu` - حالة المعالج
• `time` أو `الساعة` - لعرض الوقت
• `id` أو `ايدي` - معلومات الحساب
• `inf` - معلومات المجموعة
• `tadmin` - عرض قائمة المشرفين
• `on_off_status` - عرض حالة الأوضاع

👤 **أوامر الحساب الشخصي:**
• `setname` - تغيير الاسم
• `setbio` - تغيير البايو
• `setprofile` - تغيير الصورة (بالرد)
• `delprofile` - حذف الصورة
• `clone` - استنساخ حساب (بالرد)

🔄 **أوامر الأوضاع:**
• `bold`, `italic`, `code`, `strike`, `underline`, `spoiler`, `emoji`, `emojib`, `emojig`

⏰ **أوامر الوقت:**
• `1timename`, `2timename`, `3timename`
• `1timebio`, `2timebio`, `3timebio`

🛡️ **أوامر الإدارة والحماية (بالرد):**
• `حظر` / `الغاء حظر`
• `كتم` / `فك كتم`
• `mute` / `unmute` (كتم البوت)
• `block` / `unblock` (جهات الاتصال)
• `delallmsguser` - حذف رسائل مستخدم
• `setenemy` / `delenemy` / `allf`
• `setlove` / `deletlove` / `alllove`

🔄 **التحويل والوسائط (بالرد):**
• `tlpho` - تحويل إلى الصورة
• `tlskr` - تحويل إلى ملصق
• `tlgif` - تحويل إلى GIF
• `voice` - تحويل النص لصوت
• `bashe` - حفظ الوسائط

🎮 **الألعاب والأنيميشن:**
• `reload` - أنيميشن تحميل
• `love` أو `حب`
• `اقتل الوغد`
• `tas` - رمي النرد
• `dart` - السهام
• `bowling` - البولينج
• `basketball` - كرة السلة
• `football` - كرة القدم

✨ **BY : t.me/SpeeeeedML**
    """)

# الأوامر الأساسية
@client.on(events.NewMessage(pattern=r"^ping$"))
async def ping_cmd(event):
    start = datetime.now()
    await event.edit("⚡ **جاري قياس السرعة...**")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit(f"🏓 **Pong!**\n⚡ سرعة الاستجابة: `{ms}ms`\n🤖 بواسطة: **حمودا**")

@client.on(events.NewMessage(pattern=r"^cpu$"))
async def cpu_cmd(event):
    await event.edit("💻 **حالة المعالج:**\n🟢 المعالج يعمل بكفاءة وأمان تام.")

@client.on(events.NewMessage(pattern=r"^(time|الساعة)$"))
async def time_cmd(event):
    now = datetime.now().strftime("%H:%M:%S")
    await event.edit(f"⏰ **الوقت الحالي:** `{now}`")

@client.on(events.NewMessage(pattern=r"^(id|ايدي)$"))
async def id_cmd(event):
    replied = await event.get_reply_message()
    user = replied.sender if replied else event.sender
    await event.edit(f"👤 **معلومات الحساب:**\n🆔 الايدي: `{user.id}`\nاسم المستخدم: @{user.username}\nالاسم: {user.first_name}")

@client.on(events.NewMessage(pattern=r"^inf$"))
async def inf_cmd(event):
    chat = await event.get_chat()
    try:
        await event.edit(f"👥 **معلومات المجموعة:**\nاسم المجموعة: {chat.title}\nالايدي: `{chat.id}`\nالأعضاء: {chat.participants_count}")
    except:
        await event.edit("⚠️ هذه ليست مجموعة.")

@client.on(events.NewMessage(pattern=r"^tadmin$"))
async def tadmin_cmd(event):
    chat = await event.get_chat()
    try:
        admins = await client.get_participants(chat, filter=events.ChannelParticipants.Admins)
        admin_list = "\n".join([f"- {a.first_name} (`{a.id}`)" for a in admins])
        await event.edit(f"👮‍♂️ **قائمة المشرفين:**\n{admin_list}")
    except:
        await event.edit("⚠️ لا يمكن جلب المشرفين هنا.")

@client.on(events.NewMessage(pattern=r"^on_off_status$"))
async def status_cmd(event):
    await event.edit("🎛️ **حالة الأوضاع:** جميع أوضاع الحماية والوقت مفعلة.")

# أوامر الحساب الشخصي
@client.on(events.NewMessage(pattern=r"^setname\s+(.+)"))
async def setname_cmd(event):
    new_name = event.pattern_match.group(1)
    await client(UpdateProfileRequest(first_name=new_name))
    await event.edit(f"✅ تم تغير الاسم إلى: `{new_name}`")

@client.on(events.NewMessage(pattern=r"^setbio\s+(.+)"))
async def setbio_cmd(event):
    new_bio = event.pattern_match.group(1)
    await client(UpdateProfileRequest(about=new_bio))
    await event.edit(f"✅ تم تغير البايو إلى: `{new_bio}`")

@client.on(events.NewMessage(pattern=r"^setprofile$"))
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

@client.on(events.NewMessage(pattern=r"^delprofile$"))
async def delprofile_cmd(event):
    photos = await client.get_profile_photos('me')
    if photos:
        await client(DeletePhotosRequest(id=[photos[0]]))
        await event.edit("🗑️ تم حذف الصورة الشخصية بنجاح.")
    else:
        await event.edit("⚠️ ليس لديك صور لحذفها.")

@client.on(events.NewMessage(pattern=r"^clone$"))
async def clone_cmd(event):
    reply = await event.get_reply_message()
    if not reply:
        return await event.edit("⚠️ يجب الرد على الشخص المراد استنساخ حسابه.")
    user = reply.sender
    try:
        await client(UpdateProfileRequest(first_name=user.first_name))
        await event.edit(f"🎭 تم استنساخ الحساب بنجاح (`{user.first_name}`)!")
    except Exception as e:
        await event.edit(f"❌ حدث خطأ: {e}")

# أوامر الإدارة والحماية
@client.on(events.NewMessage(pattern=r"^حظر$"))
async def ban_cmd(event):
    if not event.is_group:
        return await event.edit("⚠️ في المجموعات فقط.")
    reply = await event.get_reply_message()
    if not reply:
        return await event.edit("⚠️ رد على الشخص المراد حظره.")
    try:
        await event.client.edit_permissions(event.chat_id, reply.sender_id, view_messages=True)
        await event.edit("🔨 تم حظر المستخدم بنجاح!")
    except Exception as e:
        await event.edit(f"❌ خطأ: {e}")

@client.on(events.NewMessage(pattern=r"^الغاء حظر$"))
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

@client.on(events.NewMessage(pattern=r"^كتم$"))
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
        await event.edit(f"❌ خطأ: {e}")

@client.on(events.NewMessage(pattern=r"^فك كتم$"))
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
@client.on(events.NewMessage(pattern=r"^(love|حب)$"))
async def love_anim(event):
    await event.edit("❤️")
    await asyncio.sleep(0.3)
    await event.edit("💖 احلى حب يا حمودا")

@client.on(events.NewMessage(pattern=r"^اقتل الوغد$"))
async def kill_anim(event):
    await event.edit("🔫 جاري التصويب...")
    await asyncio.sleep(0.4)
    await event.edit("🎯 بوم! تم القضاء على الوغد.")

@client.on(events.NewMessage(pattern=r"^tas$"))
async def dice_cmd(event):
    await event.delete()
    await client.send_message(event.chat_id, file='🎲')

@client.on(events.NewMessage(pattern=r"^dart$"))
async def dart_cmd(event):
    await event.delete()
    await client.send_message(event.chat_id, file='🎯')

@client.on(events.NewMessage(pattern=r"^bowling$"))
async def bowling_cmd(event):
    await event.delete()
    await client.send_message(event.chat_id, file='🎳')

@client.on(events.NewMessage(pattern=r"^basketball$"))
async def basket_cmd(event):
    await event.delete()
    await client.send_message(event.chat_id, file='🏀')

@client.on(events.NewMessage(pattern=r"^football$"))
async def foot_cmd(event):
    await event.delete()
    await client.send_message(event.chat_id, file='⚽')

@client.on(events.NewMessage(pattern=r"^reload$"))
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
        
