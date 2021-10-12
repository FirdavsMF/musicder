
import logging
import time
from pyrogram import Client as app
from pyrogram.types import Message
# from youtube_search import YoutubeSearch

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
import pyrogram

logging.getLogger("pyrogram").setLevel(logging.WARNING)
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
import youtube_dl
from youtube_search import YoutubeSearch
import requests, validators

import os
from config import Config

bot = Client(
    'SongPlayRoBot',
    bot_token = Config.BOT_TOKEN,
    api_id = Config.API_ID,
    api_hash = Config.API_HASH
)

## Extra Fns -------------------------------

# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


## Commands --------------------------------
@bot.on_message(filters.command(['start']))
def start(client, message):
    TamilBots = f'👋 Привет @{message.from_user.username}\n\nЯ бот 🎸для воспроизведения песен [🎶](https://telegra.ph/file/6cb884fe1cb943ec12df1.mp4)\n\nОтправьте название песни, которую вы хотите... 😍🥰🤗\n\nПример поиск музыка: " Название песни" \n\nСсылка из видео: ` https://youtube.com`'
    message.reply_text(
        text=TamilBots, 
         quote=False,
        # reply_markup=InlineKeyboardMarkup(
        #     [
        #         [
        #             InlineKeyboardButton('служба поддержки 👬', url='https://t.me/FirdavsMF'),
        #             InlineKeyboardButton('Добавь меня 🤗', url='https://t.me/SongPlayRoBot?startgroup=true')
        #         ]
        #     ]
        )

@bot.on_message()
def a(client, message):
    query = message.text
    # for i in message[1:]:
    #     query += ' ' + str(i)
    print(query)
    m = message.reply('🔎 ищу песню...')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            views = results[0]["views"]
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('ничего не нашел. попробуйте немного изменить написание😕')
            return
    except Exception as e:
        m.edit(
            "✖️ Ничего не найти. Извините.\n\n Попробуем другое ключевое слово или, возможно, правильно произнесем его по буквам\n\nEg.`/s Faded`"
        )
        print(str(e))
        return
    m.edit("🔎 Найти песню 🎶 Пожалуйста, ждите ⏳️ На несколько секунд [🚀](https://telegra.ph/file/67f41ae52a85dfc0551ae.mp4)")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'🎧 Заголовок : [{title[:35]}]({link})\n⏳ Продолжительность : `{duration}`\n🎬 Источник : [Youtube](https://youtu.be/3pN0W4KzzNY)\n👁‍🗨 просмотров : `{views}`\n\n💌 По : @....'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=False, title=title, duration=dur, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit('❌ Ошибка\n\n Сообщите об этой ошибке, которую нужно исправить @FirdavsMF ❤️')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
bot.run()
