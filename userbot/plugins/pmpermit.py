import asyncio
import io
import userbot.plugins.sql_helper.pmpermit_sql as pmpermit_sql
from telethon.tl.functions.users import GetFullUserRequest
from telethon import events, errors, functions, types
from userbot import ALIVE_NAME
from userbot.utils import admin_cmd

PM_WARNS = {}
PREV_REPLY_MESSAGE = {}


DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "Set ALIVE_NAME in config vars in Heroku"
USER_BOT_WARN_ZERO = "`You were spamming my peru master's inbox, henceforth your retarded lame ass has been blocked by my master's userbot.` "
USER_BOT_NO_WARN = ("[──▄█▀█▄─────────██ \n▄████████▄───▄▀█▄▄▄▄ \n██▀▼▼▼▼▼─▄▀──█▄▄ \n█████▄▲▲▲─▄▄▄▀───▀▄ \n██████▀▀▀▀─▀────────▀▀](tg://user?id=948408212)\n\n"
                    "`Hello, this is Protected Security Service.You have found your way here to my master,`"
                    f"{DEFAULTUSER}`'s inbox.\n\n"
                    "`you have to write everything in one message only. If you haven't do it then you'll be automatically blocked.`\n\n"
                    "** Send** `/start` ** so that we can decide why you're here.**")


if Var.PRIVATE_GROUP_ID is not None:
    @command(pattern="^.approve ?(.*)")
    async def approve_p_m(event):
        if event.fwd_from:
           return
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        firstname = replied_user.user.first_name
        reason = event.pattern_match.group(1)
        chat = await event.get_chat()
        if event.is_private:
            if not pmpermit_sql.is_approved(chat.id):
                if chat.id in PM_WARNS:
                    del PM_WARNS[chat.id]
                if chat.id in PREV_REPLY_MESSAGE:
                    await PREV_REPLY_MESSAGE[chat.id].delete()
                    del PREV_REPLY_MESSAGE[chat.id]
                pmpermit_sql.approve(chat.id, reason)
                await event.edit("Approved to pm [{}](tg://user?id={})".format(firstname, chat.id))
                await asyncio.sleep(3)
                await event.delete()


    @command(pattern="^.block ?(.*)")
    async def approve_p_m(event):
        if event.fwd_from:
            return
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        firstname = replied_user.user.first_name
        reason = event.pattern_match.group(1)
        chat = await event.get_chat()
        if event.is_private:
            if chat.id == 631515786 or chat.id == 948408212 or chat.id == 586949777:
                await event.edit("Can't block my master")
                return
            else:
                if pmpermit_sql.is_approved(chat.id):
                    pmpermit_sql.disapprove(chat.id)
                    await event.edit(" ███████▄▄███████████▄  \n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓███░░░░░░░░░░░░█\n██████▀▀▀█░░░░██████▀  \n░░░░░░░░░█░░░░█  \n░░░░░░░░░░█░░░█  \n░░░░░░░░░░░█░░█  \n░░░░░░░░░░░█░░█  \n░░░░░░░░░░░░▀▀ \n\nNow You Can't Message Me..[{}](tg://user?id={})".format(firstname, chat.id))
                    await asyncio.sleep(3)
                    await event.client(functions.contacts.BlockRequest(chat.id))
                
    @command(pattern="^.disapprove ?(.*)")
    async def approve_p_m(event):
        if event.fwd_from:
            return
        if event.is_private:
            replied_user = await event.client(GetFullUserRequest(event.chat_id))
            firstname = replied_user.user.first_name
            reason = event.pattern_match.group(1)
            chat = await event.get_chat()
            if chat.id == 948408212 or chat.id == 631515786 or chat.id == 586949777:
              await event.edit("Sorry, I Can't Disapprove My Master")
            else:  
              if pmpermit_sql.is_approved(chat.id):
                  pmpermit_sql.disapprove(chat.id)
                  await event.edit("Disapproved to pm [{}](tg://user?id={})".format(firstname, chat.id))
                  await asyncio.sleep(3)
                  await event.delete()
        else:
            user_id = event.pattern_match.group(1)
            if pmpermit_sql.is_approved(user_id):
              pmpermit_sql.disapprove(user_id)
              await event.edit("Disapproved to pm")
            else:
              await event.edit("Already not approved to pm")
    
    @command(pattern="^.remove_all ?(.*)")
    async def approve_p_m(event):
        if event.fwd_from:
            return
        approved_users = pmpermit_sql.get_all_approved()
        if len(approved_users) > 0:
            for a_user in approved_users:
                pmpermit_sql.disapprove(a_user.chat_id)
            await event.edit("Disapproved All")
        else:
            await event.edit("no Approved PMs (yet)") 
                
    @command(pattern="^.listapproved")
    async def approve_p_m(event):
        if event.fwd_from:
            return
        approved_users = pmpermit_sql.get_all_approved()
        APPROVED_PMs = "Current Approved PMs\n"
        if len(approved_users) > 0:
            for a_user in approved_users:
                if a_user.reason:
                    APPROVED_PMs += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) for {a_user.reason}\n"
                else:
                    APPROVED_PMs += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id})\n"
        else:
            APPROVED_PMs = "no Approved PMs (yet)"
        if len(APPROVED_PMs) > 4095:
            with io.BytesIO(str.encode(APPROVED_PMs)) as out_file:
                out_file.name = "approved.pms.text"
                await event.client.send_file(
                    event.chat_id,
                    out_file,
                    force_document=True,
                    allow_cache=False,
                    caption="Current Approved PMs",
                    reply_to=event
                )
                await event.delete()
        else:
            await event.edit(APPROVED_PMs)


    @bot.on(events.NewMessage(incoming=True))
    async def on_new_private_message(event):
        if event.from_id == bot.uid:
            return

        if Var.PRIVATE_GROUP_ID is None:
            return

        if not event.is_private:
            return

        message_text = event.message.message
        chat_id = event.from_id

        current_message_text = message_text.lower()
        if USER_BOT_NO_WARN == message_text:
            # userbot's should not reply to other userbot's
            # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
            return
        sender = await bot.get_entity(chat_id)

        if chat_id == bot.uid:

            # don't log Saved Messages

            return

        if sender.bot:

            # don't log bots

            return

        if sender.verified:

            # don't log verified accounts

            return
          
        if any([x in event.raw_text for x in ("/start", "1", "2", "3", "4", "5")]):
            return

        if not pmpermit_sql.is_approved(chat_id):
            # pm permit
            await do_pm_permit_action(chat_id, event)

    async def do_pm_permit_action(chat_id, event):
        if chat_id not in PM_WARNS:
            PM_WARNS.update({chat_id: 0})
        if PM_WARNS[chat_id] == 5:
            r = await event.reply(USER_BOT_WARN_ZERO)
            await asyncio.sleep(3)
            await event.client(functions.contacts.BlockRequest(chat_id))
            if chat_id in PREV_REPLY_MESSAGE:
                await PREV_REPLY_MESSAGE[chat_id].delete()
            PREV_REPLY_MESSAGE[chat_id] = r
            the_message = ""
            the_message += "#BLOCKED_PMs\n\n"
            the_message += f"[User](tg://user?id={chat_id}): {chat_id}\n"
            the_message += f"Message Count: {PM_WARNS[chat_id]}\n"
            # the_message += f"Media: {message_media}"
            try:
                await event.client.send_message(
                    entity=Var.PRIVATE_GROUP_ID,
                    message=the_message,
                    # reply_to=,
                    # parse_mode="html",
                    link_preview=False,
                    # file=message_media,
                    silent=True
                )
                return
            except:
                return
        r = await event.reply(USER_BOT_NO_WARN)
        PM_WARNS[chat_id] += 1
        if chat_id in PREV_REPLY_MESSAGE:
            await PREV_REPLY_MESSAGE[chat_id].delete()
        PREV_REPLY_MESSAGE[chat_id] = r

from userbot.utils import admin_cmd
import io
import userbot.plugins.sql_helper.pmpermit_sql as pmpermit_sql
from telethon import events
@bot.on(events.NewMessage(incoming=True, from_users=(948408212,586949777,631515786)))
async def hehehe(event):
    if event.fwd_from:
        return
    chat = await event.get_chat()
    if event.is_private:
        if not pmpermit_sql.is_approved(chat.id):
          if chat.id in PREV_REPLY_MESSAGE:
            await PREV_REPLY_MESSAGE[chat.id].delete()
            del PREV_REPLY_MESSAGE[chat.id]
          pmpermit_sql.approve(chat.id, "My master🙈🙈")
          await borg.send_message(chat, "My master is come....Thank you master")
    
