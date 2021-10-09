
import logging
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
@bot.on_message(pyrogram.filters.command(["search"]))
async def ytsearch(_, message: Message):
    try:
        if len(message.command) < 2:
            await message.reply_text("/поиску нужен аргумент!")
            return
        query = message.text.split(None, 1)[1]
        m = await message.reply_text("Ищем ....")
        results = YoutubeSearch(query, max_results=4).to_dict()
        i = 0
        text = ""
        while i < 4:
            text += f"Title - {results[i]['title']}\n"
            text += f"Duration - {results[i]['duration']}\n"
            text += f"Views - {results[i]['views']}\n"
            text += f"Channel - {results[i]['channel']}\n"
            text += f"https://youtube.com{results[i]['url_suffix']}\n\n"
            i += 1
        await m.edit(text, disable_web_page_preview=True)
    except Exception as e:
        await message.reply_text(str(e))    

def downloada(url, quality):
    
    if quality == "1":
        ydl_opts_start = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', #This Method Need ffmpeg
            'outtmpl': f'localhoct/%(id)s.%(ext)s',
            'no_warnings': True,
            'ignoreerrors': True,
            'noplaylist': True,
            'http_chunk_size': 20097152,
            'writethumbnail': True

        }
        with youtube_dl.YoutubeDL(ydl_opts_start) as ydl:
            result = ydl.extract_info("{}".format(url))
            title = ydl.prepare_filename(result)
            ydl.download([url])
        return title
    
    if quality == "2":
        ydl_opts_start = {
            'format': 'best', #This Method Don't Need ffmpeg , if you don't have ffmpeg use This 
            'outtmpl': f'localhoct/%(id)s.%(ext)s',
            'no_warnings': False,
            'logtostderr': False,
            'ignoreerrors': False,
            'noplaylist': True,
            'http_chunk_size': 2097152,
            'writethumbnail': True
        }
        with youtube_dl.YoutubeDL(ydl_opts_start) as ydl:
            result = ydl.extract_info("{}".format(url))
            title = ydl.prepare_filename(result)
            ydl.download([url])
        return f'{title}'
    
    if quality == "3":
        ydl_opts_start = {
            'format': 'best[height=480]',
            'outtmpl': f'localhoct/%(id)s.%(ext)s',
            'no_warnings': False,
            'logtostderr': False,
            'ignoreerrors': False,
            'noplaylist': True,
            'http_chunk_size': 2097152,
            'writethumbnail': True
        }
        with youtube_dl.YoutubeDL(ydl_opts_start) as ydl:
            result = ydl.extract_info("{}".format(url))
            title = ydl.prepare_filename(result)
            ydl.download([url])
        return f'{title}'

# here you can Edit Start message
# @app.on_message(filters.command('start', '/'))
# def start(c, m): # c Mean Client | m Mean Message
#     m.reply_text('Hi Welcome To @iLoaderBot \n Just Send Video Url To me and i\'ll try to upload the video and send it to you') #Edit it and add your Bot ID :)

             

bot.run()
