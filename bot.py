import os
import json
import logging
import asyncio
import random
from datetime import datetime
from telethon import TelegramClient
from telethon.errors import ChatWriteForbiddenError
import requests

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

api_id = '28623401'
api_hash = 'cc0da46d8b083ae05289ade6315df9f4'

target_groups = set()
target_private_chats = set()
processed_groups = {}
processed_private_chats = {} 

script_directory = os.path.dirname(os.path.realpath(__file__))
images_folder = "images"
images_directory = os.path.join(script_directory, images_folder)
status_file = "status.json"

def create_images_directory():
    try:
        if not os.path.exists(images_directory):
            os.makedirs(images_directory)
            logger.info("Direktori 'images' berhasil dibuat.")
    except OSError as e:
        logger.error(f"Error: {e}")

messages = [
    """🎯 Promosikan bisnis Anda dengan layanan iklan yang tepat! 

💼✨ Kami menyediakan layanan iklan Google ADS dan Facebook ADS yang efektif untuk meningkatkan visibilitas dan penjualan website serta toko online Anda. 

Layanan kami mencakup: 

-✨ Pembuatan dan pengelolaan kampanye iklan Google ADS dan Facebook ADS 
-✨ pembuatan website bisnis atau toko online  
-✨ Khursus pembelajaran Ads all kampanye 
-✨ pembuatan B0T promosi agar akun telegram post promosi otomatis di semua grup publik 

Dapatkan hasil terbaik dan jaminan kinerja terbaik untuk promosi bisnis Anda. 

Hubungi: 

[whatsapp official kami +6285213000029](https://wa.me/+6285213000029) 
[facebook official kami zenius tobuhu](https://www.facebook.com/jasaiklanpromosiads) 
[website official kami](https://www.jasa-iklan-google-ads-black.rf.gd/) 
telegram official kami @adsblack15

untuk konsultasi gratis! 

NOTE: 
HUBUNGI AKUN DI ATAS .AKUN INI ADALAH B0T
HATI HATI PENIPUAN KAMI TIDAK MELAYANI JASA SELAIN KONTAK YANG TERTERA DI POST INI ATAU DI WEBSITE OFFICIAL KAMI 

#jasapromosi #jasagoogleads #jasafbads""",

    """🚀 Ingin memperluas jangkauan bisnis Anda? 

Gunakan layanan jasa iklan kami! 

💼💥 Dapatkan promosi yang tepat sasaran dengan layanan Google ADS dan Facebook ADS. 

Layanan kami mencakup:  

-✨ Jasa Google ads & Meta ads / facebook ads 
-✨ Pembuatan B0T untuk akun telegram agar post promosi di semua grup publik otomatis 
-✨ Pembuatan Website bisnis atau Toko online yang menarik  
-✨ kelas khursus belajar iklan Ads   

Manfaatkan strategi iklan yang terukur untuk meningkatkan lalu lintas dan konversi di website dan toko online Anda. 

Hubungi: 

[whatsapp official kami +6285213000029](https://wa.me/+6285213000029) 
[facebook official kami zenius tobuhu](https://www.facebook.com/jasaiklanpromosiads) 
[website official kami](https://www.jasa-iklan-google-ads-black.rf.gd/) 
telegram official kami @adsblack15

untuk konsultasi gratis! 

NOTE: 
HUBUNGI AKUN DI ATAS .AKUN INI ADALAH B0T
HATI HATI PENIPUAN KAMI TIDAK MELAYANI JASA SELAIN KONTAK YANG TERTERA DI POST INI ATAU DI WEBSITE OFFICIAL KAMI 

#jasapromosi #jasagoogleads #jasafbads""",

    """💼 Jadikan bisnis Anda lebih dikenal dengan layanan iklan yang tepat! 

🌟🎯 Kami menyediakan layanan iklan Google ADS dan Facebook ADS yang efektif untuk meningkatkan kesadaran merek dan menjangkau audiens target secara lebih efisien. 

Layanan kami meliputi: 

-✨ Pengelola iklan ADS Google dan lainnya 
-✨ Pembuatan Website bisnis atau toko online Desain Menarik 
-✨ Buat B0T promosi telegram agar akun telegram post promosi di semua grup publik telegram secara otomatis  
-✨ Khursus pembelajaaran ADS  

Dapatkan hasil terbaik dan optimalisasi iklan yang tepat. 

Hubungi: 

[whatsapp official kami +6285213000029](https://wa.me/+6285213000029) 
[facebook official kami zenius tobuhu](https://www.facebook.com/jasaiklanpromosiads) 
[website official kami](https://www.jasa-iklan-google-ads-black.rf.gd/) 
telegram official kami @adsblack15 

untuk konsultasi gratis! 

NOTE: 
HUBUNGI AKUN DI ATAS .AKUN INI ADALAH B0T
HATI HATI PENIPUAN KAMI TIDAK MELAYANI JASA SELAIN KONTAK YANG TERTERA DI POST INI ATAU DI WEBSITE OFFICIAL KAMI 

#jasapromosi #jasagoogleads #jasafbads"""
]

async def send_random_message(client):
    global target_groups, target_private_chats  
    try:
        await client.start()
        logger.info("Client berhasil dijalankan.")

        while True:
            await update_target_groups(client)
            await update_target_private_chats(client)

            if not target_groups and not target_private_chats:
                logger.info("Tidak ada grup atau pesan pribadi yang ditemukan.")
                await asyncio.sleep(30)
                continue

            for group_id, group_title in target_groups:
                if group_title in ["GADS ROYALHOKI77", "ADS ROYAL"]:
                    logger.info(f"Melewati pengiriman pesan ke grup '{group_title}'.")
                    continue
                await send_message_to_group(client, group_id, group_title)
                await asyncio.sleep(120)
            for chat_id, username in target_private_chats:
                await send_message_to_private_chat(client, chat_id, username)
                await asyncio.sleep(120)
            await asyncio.sleep(120)
    except Exception as e:
        logger.error(f"Ada kesalahan dalam mengirim pesan acak: {e}")

async def load_status():
    global processed_groups, processed_private_chats
    if os.path.exists(status_file):
        with open(status_file, 'r') as f:
            data = json.load(f)
            processed_groups = data.get('processed_groups', {})
            processed_private_chats = data.get('processed_private_chats', {})

async def save_status():
    data = {
        'processed_groups': processed_groups,
        'processed_private_chats': processed_private_chats
    }
    with open(status_file, 'w') as f:
        json.dump(data, f)

async def update_target_groups(client):
    global target_groups
    target_groups.clear()
    async for dialog in client.iter_dialogs():
        if dialog.is_group:
            target_groups.add((dialog.id, dialog.title))
    logger.info("Target grup diperbarui.")

async def update_target_private_chats(client):
    global target_private_chats
    target_private_chats.clear()
    async for dialog in client.iter_dialogs():
        if dialog.is_user:
            target_private_chats.add((dialog.id, dialog.entity.username))
    logger.info("Target pesan pribadi diperbarui.")

async def send_message_to_group(client, group_id, group_title):
    global messages  
    try:
        available_images = [image for image in os.listdir(images_directory)]
        sent_images = processed_groups.get(group_id, [])
        available_images = list(set(available_images) - set(sent_images))

        if not available_images:
            logger.info(f"Semua gambar sudah dikirim ke grup {group_title}.")
            return

        image_name = random.choice(available_images)
        image_path = os.path.join(images_directory, image_name)

        message = random.choice(messages)  

        await client.send_file(group_id, image_path, caption=message)
        logger.info(f"Pesan dan gambar terkirim ke grup {group_title}. Gambar: {image_name}")

        if group_id in processed_groups:
            processed_groups[group_id].append(image_name)
        else:
            processed_groups[group_id] = [image_name]

        await save_status()

    except ChatWriteForbiddenError:
        logger.error(f"Anda tidak dapat menulis di grup {group_title}.")
    except Exception as e:
        logger.error(f"Ada kesalahan dalam mengirim pesan ke grup {group_title}: {e}")

async def send_message_to_private_chat(client, chat_id, username):
    global processed_private_chats  
    try:
        available_images = [image for image in os.listdir(images_directory)]
        sent_images = processed_private_chats.get(chat_id, [])
        available_images = list(set(available_images) - set(sent_images))

        if not available_images:
            logger.info(f"Semua gambar sudah dikirim ke {username}.")
            return

        image_name = random.choice(available_images)
        image_path = os.path.join(images_directory, image_name)

        message = random.choice(messages)

        await client.send_file(chat_id, image_path, caption=message)
        logger.info(f"Pesan dan gambar terkirim ke {username}. Gambar: {image_name}")

        if chat_id in processed_private_chats:
            processed_private_chats[chat_id].append(image_name)
        else:
            processed_private_chats[chat_id] = [image_name]

        await save_status()

    except ChatWriteForbiddenError:
        logger.error(f"Anda tidak dapat menulis ke {username}.")
    except Exception as e:
        logger.error(f"Ada kesalahan dalam mengirim pesan ke {username}: {e}")

async def send_log_to_telegram(client, message):
    try:
        await client.send_message('me', message)
        logger.info("Log dikirim ke Telegram.")
    except Exception as e:
        logger.error(f"Gagal mengirim log ke Telegram: {e}")

async def get_geoip_info(ip_address):
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Gagal mendapatkan informasi GeoIP untuk {ip_address}.")
            return None
    except Exception as e:
        logger.error(f"Error: {e}")
        return None

async def log_incoming_messages(client):
    try:
        await client.start()
        me = await client.get_me()

        async for event in client.iter_messages('me'):
            if event.from_id != me.id:
                sender_id = event.sender_id
                sender_username = event.sender.username or "Not Available"
                sender_name = event.sender.first_name or "Not Available"
                message_text = event.message

                ip_address = requests.get('https://api.ipify.org').text
                geoip_info = await get_geoip_info(ip_address)

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if geoip_info:
                    country = geoip_info.get('country', 'Not Available')
                    region = geoip_info.get('region', 'Not Available')
                    city = geoip_info.get('city', 'Not Available')
                    await client.send_message('your_telegram_id', f"Incoming Message Details:\nTimestamp: {timestamp}\nSender ID: {sender_id}\nUsername: {sender_username}\nName: {sender_name}\nCountry: {country}\nRegion: {region}\nCity: {city}\nMessage: {message_text}")
                else:
                    await client.send_message('your_telegram_id', f"Incoming Message Details:\nTimestamp: {timestamp}\nSender ID: {sender_id}\nUsername: {sender_username}\nName: {sender_name}\nIP Address: {ip_address}\nMessage: {message_text}")
    except Exception as e:
        logger.error(f"Gagal menangani pesan masuk: {e}")

async def main():
    client = TelegramClient('user', api_id, api_hash)
    create_images_directory()
    await asyncio.gather(
        send_log_to_telegram(client, "Program dimulai."),
        send_random_message(client),
        log_incoming_messages(client)
    )
    await send_log_to_telegram(client, "Program selesai.")

if __name__ == "__main__":
    asyncio.run(main())
