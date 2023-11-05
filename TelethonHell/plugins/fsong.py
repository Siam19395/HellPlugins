from telethon.errors.rpcerrorlist import YouBlockedUserError
from TelethonHell.plugins import *


@hell_cmd(pattern="fs(?:\s|$)([\s\S]*)")
async def find_audio_or_video(hellevent):
    if not hellevent.reply_to_msg_id:
        await eod(hellevent, "__Reply to any user's audio or video message.__")
        return

    reply_message = await hellevent.get_reply_message()
    if not reply_message.media and not reply_message.document:
        await eod(hellevent, "__Reply to an audio or video file.__")
        return

    # Check if the replied message is an audio or video file
    if reply_message.media and (reply_message.media.document.mime_type.startswith('audio') or reply_message.media.document.mime_type.startswith('video')):
        chat = "@Music_Source_Bot"
    else:
        await eod(hellevent, "__You can only reply to audio or video files.__")
        return

    if reply_message.sender.bot:
        await eod(hellevent, "__Reply to an actual user's message.__")
        return

    MSG = await eor(hellevent, "__Sending the file to the Database__")

    async with hellevent.client.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await asyncio.sleep(0.8)
            await conv.send_file(reply_message)
        except YouBlockedUserError:
            await eod(hellevent, "Unblock @Music_Source_Bot and try again.")
            return

        await asyncio.sleep(0.8)
        await MSG.edit("**Done**")
        await asyncio.sleep(0.8)
        await MSG.edit("__Searching the song in the server__")
        await asyncio.sleep(0.8)

        try:
            response = await conv.get_response(timeout=10)
        except asyncio.exceptions.TimeoutError:
            logging.error("1st Response timed out")
            DLT = await MSG.edit("1st Response timed out")
            await asyncio.sleep(15)
            await DLT.delete()
            return

        try:
            response2 = await conv.get_response(timeout=10)
        except asyncio.exceptions.TimeoutError:
            logging.error("2nd Response timed out")
            DLT = await MSG.edit("2nd Response timed out")
            await asyncio.sleep(15)
            await DLT.delete()
            return

        try:
            await MSG.edit("__Getting result.......__")
            await asyncio.sleep(4.5)
            response3 = await conv.get_response(timeout=30)
        except asyncio.exceptions.TimeoutError:
            logging.error("3rd Response timed out")
            DLT = await MSG.edit("3rd Response timed out")
            await asyncio.sleep(15)
            await DLT.delete()
            return

        response_text = response2.text.replace("[Find song](http://t.me/Music_Source_Bot)", "")
        dlt = await MSG.edit("__Parsing the result please wait....__")
        await dlt.delete()

        if "The song could not be found. Try again." in response2.text:
            msg_dlt = await hellevent.client.send_message(hellevent.chat_id, response2.text.strip(), reply_to=reply_message)
            await asyncio.sleep(12)
            await msg_dlt.delete()
        elif response3 and response3.media:
            await hellevent.client.send_file(hellevent.chat_id, response3.media, caption=response_text.strip(, reply_to=reply_message)
        else:
            await hellevent.client.send_message(hellevent.chat_id, response_text.strip(), reply_to=reply_message)



CmdHelp("fsong").add_command(
    "fs", "<reply to a audio or video>", "Fetches the name song of replied audio or video."
).add_info(
    "Song Finder"
).add_warning(
    "✅ Harmless Module."
).add()


  
