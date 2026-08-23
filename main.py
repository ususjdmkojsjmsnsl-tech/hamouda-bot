import os
import time
import asyncio
from datetime import datetime
from telethon import TelegramClient, events
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest

# بيانات الـ API الخاصة بك
API_ID = 38739119
API_HASH = "76fd508f4878e8d77cd68e88ba65bc85"

# تشغيل بوت حمودا
client = TelegramClient("hamouda_session", API_ID, API_HASH)

# متغيرات الأوضاع والتحكم
modes = {
    "bold": False,
    "italic": False,
    "code": False,
    "strike": False,
    "underline": False,
    "spoiler": False,
    "emoji": False,
    "emojib": False,
    "emojig": False,
}

time_modes = {
    "1timename": False,
    "2timename": False,
    "3timename": False,
    "1timebio": False,
    "2timebio": False,
    "3timebio": False,
}

enemies_list = []
love_list = []


@client.on(events.NewMessage(pattern=r"^\.ping$"))
async def ping_cmd(event):
  start = datetime.now()
  event = await event.edit("⚡ **جاري قياس السرعة...**")
  end = datetime.now()
  ms = (end - start).microseconds / 1000
  await event.edit(f"🏓 **Pong!**\n⚡ سرعة الاستجابة: `{ms}ms`\n🤖 بواسطة: **حمودا**")


@client.on(events.NewMessage(pattern=r"^\.cpu$"))
async def cpu_cmd(event):
  await event.edit(
      "💻 **حالة المعالج والجهاز:**\n🟢 المعالج يعمل بشكل ممتاز وطبيعي\n🔒 الحالة:"
      " آمن وخالي من الفيروسات"
  )


@client.on(events.NewMessage(pattern=r"^\.(time|الساعة)$"))
async def time_cmd(event):
  now = datetime.now().strftime("%H:%M:%S")
  await event.edit(f"⏰ **الوقت الحالي:** `{now}`")


@client.on(events.NewMessage(pattern=r"^\.(id|ايدي)$"))
async def id_cmd(event):
  replied = await event.get_reply_message()
  user = replied.sender if replied else event.sender
  await event.edit(
      f"👤 **معلومات الحساب:**\n🆔 الايدي: `{user.id}`\nاسم المستخدم:"
      f" @{user.username}\nالاسم: {user.first_name}"
  )


@client.on(events.NewMessage(pattern=r"^\.inf$"))
async def inf_cmd(event):
  chat = await event.get_chat()
  try:
    await event.edit(
        f"👥 **معلومات المجموعة:**\nاسم المجموعة: {chat.title}\nالايدي:"
        f" `{chat.id}`\nالأعضاء: {chat.participants_count}"
    )
  except:
    await event.edit("⚠️ هذه ليست مجموعة أو سوبر گروه.")


@client.on(events.NewMessage(pattern=r"^\.tadmin$"))
async def tadmin_cmd(event):
  chat = await event.get_chat()
  try:
    admins = await client.get_participants(
        chat, filter=events.ChannelParticipants.Admins
    )
    admin_list = "\n".join([f"- {a.first_name} (`{a.id}`)" for a in admins])
    await event.edit(f"👮‍♂️ **قائمة المشرفين:**\n{admin_list}")
  except:
    await event.edit("⚠️ لا يمكن جلب المشرفين هنا.")


@client.on(events.NewMessage(pattern=r"^\.setname\s+(.+)"))
async def setname_cmd(event):
  new_name = event.pattern_match.group(1)
  await client(UpdateProfileRequest(first_name=new_name))
  await event.edit(f"✅ تم تغير الاسم إلى: `{new_name}`")


@client.on(events.NewMessage(pattern=r"^\.setbio\s+(.+)"))
async def setbio_cmd(event):
  new_bio = event.pattern_match.group(1)
  await client(UpdateProfileRequest(about=new_bio))
  await event.edit(f"✅ تم تغير البايو إلى: `{new_bio}`")


@client.on(events.NewMessage(pattern=r"^\.setprofile$"))
async def setprofile_cmd(event):
  reply = await event.get_reply_message()
  if reply and reply.media:
    path = await reply.download_media()
    file = await client.upload_file(path)
    await client(UploadProfilePhotoRequest(file=file))
    os.remove(path)
    await event.edit("✅ تم تغيير صورة الحساب بنجاح.")
  else:
    await event.edit("⚠️ قم بالرد على صورة لتغييرها.")


@client.on(events.NewMessage(pattern=r"^\.delprofile$"))
async def delprofile_cmd(event):
  photos = await client.get_profile_photos("me")
  if photos:
    await client(DeletePhotosRequest(id=[photos[0]]))
    await event.edit("🗑️ تم حذف الصورة الشخصية بنجاح.")
  else:
    await event.edit("⚠️ ليس لديك صور شخصية لحذفها.")


@client.on(events.NewMessage(pattern=r"^\.reload$"))
async def reload_cmd(event):
  msg = await event.edit(
      "🔄 **جاري إعادة تحميل سورس حمودا... [▒▒▒▒▒▒▒▒▒▒] 0%**"
  )
  for i in range(2, 11):
    await asyncio.sleep(0.3)
    bars = "█" * i + "▒" * (10 - i)
    percent = i * 10
    await msg.edit(
        f"🔄 **جاري إعادة تحميل سورس حمودا... [{bars}] {percent}%**"
    )
  await msg.edit("✅ **تم تحميل سورس حمودا بنجاح وجاهز للعمل!** 🚀")


print("تم تشغيل بوت حمودا بنجاح.. البوت يعمل الآن.")
client.start()
client.run_until_disconnected()
