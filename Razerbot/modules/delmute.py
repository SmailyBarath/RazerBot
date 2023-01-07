import asyncio
from Razerbot.events import register
from Razerbot import telethn as tbot, pbot, EVENT_LOGS, LOGGER, OWNER_ID
from telethon.tl.types import MessageEntityMentionName
from telethon import events

EVENT_LOGGER = True
DMUTE_LIST = []

@pbot.on_message(group=1)
async def watcher(_, message):
    if len(DMUTE_LIST)==0:
        return
    if message.from_user.id in DMUTE_LIST:
        await message.delete()


@register(pattern="^[!/]delmute(?:\s|$)([\s\S]*)")
async def delmute(event):
    userid = event.sender.id
    perm = await tbot.get_permissions(event.chat_id, userid)
    if not (perm.is_admin or userid == OWNER_ID):
        return await event.reply("This command is only for admins.")
    if event.is_private:
        return await event.reply("How can you be so noob? :/")
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        return await event.reply("`I can't mute a person without having admin rights` ಥ﹏ಥ")
    user, reason = await tbot.get_entity(event.sender.id)
    myid = (await tbot.get_me()).id
    if not user:
        return
    if userid == myid:
        return await event.reply("Sorry, I can't mute myself.")
    if userid == userid:
        return await event.reply("Trying to mute yourself? Not gonna happen")
    if userid == OWNER_ID:
        return await event.reply("Nice Try Muting my owner right there XD")
    if userid in DMUTE_LIST:
        return await event.reply("`This user is already muted in this chat ~~lmfao sed rip~~`")
    result = await tbot.get_permissions(event.chat_id, user.id)
    try:
        if result.participant.banned_rights.send_messages:
            return await event.reply("`This user is already muted in this chat ~~lmfao sed rip~~`")
    except AttributeError:
        pass
    except Exception as e:
        return await event.reply(f"**Error : **`{e}`")
    unid = f"@{user.username}" if user.username is not None else f"tg://user?id={user.id}"
    if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None:
        if chat.admin_rights.delete_messages is not True:
            return await event.reply("`I can't mute a person if I dont have delete messages permission. ಥ﹏ಥ`")
    elif "creator" not in vars(chat):
        return await event.reply("`I can't mute a person without having admin rights.` ಥ﹏ಥ  ")
    DMUTE_LIST.append[int(user.id)]
    if reason:
        await event.reply(
            f"[{user.first_name}]({unid}) is muted in {event.chat.title}\n"
            f"Reason: {reason}`"
        )
    else:
        await event.reply(f"[{user.first_name}]({unid}) is muted in {event.chat.title}")
    if EVENT_LOGGER:
        await tbot.send_message(
            EVENT_LOGS,
            "#MUTED\n"
            f"**User :** {user.first_name} with id `{user.id}`\n"
            f"**Chat :** {event.chat.title}(`{event.chat_id}`)",
        )

@register(pattern="^[!/]undelmute(?:\s|$)([\s\S]*)")
async def undelmute(event):
    userid = event.sender.id
    perm = await tbot.get_permissions(event.chat_id, userid) 
    if not (perm.is_admin or userid == OWNER_ID):
        return await event.reply("This command is only for admins.")
    if event.is_private:
        return await event.reply("How can you be so noob? :/")
    user, _ = await tbot.get_entity(event.sender.id)
    if not user:
        return
    try:
        unid = f"@{user.username}" if user.username is not None else f"tg://user?id={user.id}"
        if user.id in DMUTE_LIST:
            DMUTE.remove(int(user.id))
            await event.reply(f"[{user.first_name}]({unid}) is unmuted in {event.chat.title}")
        else:
            return await event.reply("`This user can already speak freely in this chat`")
    except Exception as e:
        return await event.reply(f"**Error : **`{e}`")
    if EVENT_LOGGER:
        await tbot.send_message(
            EVENT_LOGS,
            "#UNMUTED\n"
            f"**User :** {user.first_name} with id `{user.id}`\n"
            f"**Chat :** {event.chat.title}(`{event.chat_id}`)"
        )

__mod_name__ = "Delmute"
__help__ = """Delmute

Usage:
> /delmute <reply to anyone> or <user id>
> /undelmute <reply to muted user> or <user id>

Will delete any incoming message from the muted user (even admin)."""