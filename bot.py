import os
import json
import logging
import asyncio
import random
from datetime import datetime
from telethon import TelegramClient

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

api_id = '28623401'
api_hash = 'cc0da46d8b083ae05289ade6315df9f4'

script_directory = r"E:\iklan saya"
images_folder = "images"
status_file = "status.json"

client = TelegramClient('user', api_id, api_hash)

target_groups = set()
processed_groups = {}

target_private_chats = set()
processed_private_chats = {}

messages = [
    "[🎯 Promosikan bisnis Anda dengan layanan iklan yang tepat! \n  \n  💼✨ Kami menyediakan layanan iklan Google ADS dan Facebook ADS yang efektif untuk meningkatkan visibilitas dan penjualan website serta toko online Anda. \n  \n  Layanan kami mencakup: \n  \n - Pembuatan dan pengelolaan kampanye iklan Google ADS dan Facebook ADS \n \n  Penargetan yang tepat sasaran untuk audiens potensial Anda \n \n - Pengoptimalan iklan untuk meningkatkan ROI dan konversi \n  \n - Analisis kinerja kampanye untuk strategi yang lebih baik di masa depan \n  \n Dapatkan hasil terbaik dan jaminan kinerja terbaik untuk promosi bisnis Anda. \n  \n hubungi @adsblack12 untuk konsultasi gratis! \n  \n  #jasapromosi #jasagoogleads #jasafbads]",
    
    "[🚀 Ingin memperluas jangkauan bisnis Anda? \n  \n  Gunakan layanan jasa iklan kami! \n  \n  💼💥 Dapatkan promosi yang tepat sasaran dengan layanan Google ADS dan Facebook ADS. \n  \n  Layanan kami mencakup:  \n \n - Penyusunan strategi iklan yang dipersonalisasi sesuai dengan kebutuhan bisnis Anda \n  \n - Pengelolaan kampanye iklan yang terukur dan efektif \n  \n - Optimalisasi iklan berbasis data untuk hasil yang lebih baik \n  \n - Monitoring kinerja kampanye secara berkala untuk peningkatan yang berkelanjutan \n  \n Manfaatkan strategi iklan yang terukur untuk meningkatkan lalu lintas dan konversi di website dan toko online Anda. \n  \n  Hubungi @adsblack12 sekarang juga! \n  \n  #jasapromosi #jasagoogleads #jasafbads]",

    "[💼 Jadikan bisnis Anda lebih dikenal dengan layanan iklan yang tepat! \n  \n  🌟🎯 Kami menyediakan layanan iklan Google ADS dan Facebook ADS yang efektif untuk meningkatkan kesadaran merek dan menjangkau audiens target secara lebih efisien. \n  \n  Layanan kami meliputi: \n  \n - Identifikasi target pasar dan penargetan iklan yang spesifik \n  \n - Kreativitas dalam pembuatan materi iklan yang menarik perhatian \n  \n - Pemantauan kinerja kampanye secara berkala untuk peningkatan yang berkelanjutan \n  \n - Konsultasi dan strategi iklan yang disesuaikan dengan kebutuhan bisnis Anda \n  \n Dapatkan hasil terbaik dan optimalisasi iklan yang tepat. \n  \n  Hubungi @adsblack12 untuk konsultasi gratis! \n  \n  #jasapromosi #jasagoogleads #jasafbads]"
]

async def send_random_message():
    """Kirim pesan acak ke grup-grup target setiap 10 menit."""
    try:
        await load_status()

        while True:
            await update_target_groups()
            await update_target_private_chats()

            if not target_groups and not target_private_chats:
                logger.info("Tidak ada grup atau pesan pribadi yang ditemukan.")
                print("Tidak ada grup atau pesan pribadi yang ditemukan.")
                await asyncio.sleep(60)
                continue

            for group_id in target_groups:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Mengirim pesan ke grup {group_id}...")
                await send_message_to_group(group_id)
                await asyncio.sleep(300)  
            for chat_id in target_private_chats:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Mengirim pesan ke pesan pribadi {chat_id}...")
                await send_message_to_private_chat(chat_id)
                await asyncio.sleep(300)  
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Proses pengiriman pesan selesai. Menunggu 10 menit untuk mengirim pesan berikutnya...")
            await asyncio.sleep(600)  
    except Exception as e:
        logger.error(f"Ada kesalahan dalam mengirim pesan acak: {e}")
        print(f"Ada kesalahan dalam mengirim pesan acak: {e}")

async def load_status():
    """Memuat status pengiriman dari file status.json jika ada."""
    global processed_groups, processed_private_chats
    if os.path.exists(status_file):
        with open(status_file, 'r') as f:
            data = json.load(f)
            processed_groups = data.get('processed_groups', {})
            processed_private_chats = data.get('processed_private_chats', {})

async def save_status():
    """Menyimpan status pengiriman ke file status.json."""
    data = {
        'processed_groups': processed_groups,
        'processed_private_chats': processed_private_chats
    }
    with open(status_file, 'w') as f:
        json.dump(data, f)

async def update_target_groups():
    """Perbarui daftar grup target."""
    global target_groups
    target_groups.clear()
    async for dialog in client.iter_dialogs():
        if dialog.is_group:
            target_groups.add(dialog.id)

async def update_target_private_chats():
    """Perbarui daftar pesan pribadi target."""
    global target_private_chats
    target_private_chats.clear()
    async for dialog in client.iter_dialogs():
        if dialog.is_user:
            target_private_chats.add(dialog.id)

async def send_message_to_group(group_id):
    """Kirim pesan acak tertempel gambar ke grup."""
    try:
        available_images = [image for image in os.listdir(os.path.join(script_directory, images_folder))]
        sent_images = processed_groups.get(group_id, [])
        available_images = list(set(available_images) - set(sent_images))

        if not available_images:
            logger.info(f"Semua gambar sudah dikirim ke grup {group_id}.")
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Semua gambar sudah dikirim ke grup {group_id}.")
            return

        image_name = random.choice(available_images)
        image_path = os.path.join(script_directory, images_folder, image_name)

        message = random.choice(messages)

        try:
            print("[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Mengirim pesan dan gambar...")
            await client.send_file(group_id, image_path, caption=message)
            logger.info(f"Pesan dan gambar terkirim ke grup {group_id}.")
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Pesan dan gambar terkirim ke grup {group_id}.")

            if group_id in processed_groups:
                processed_groups[group_id].append(image_name)
            else:
                processed_groups[group_id] = [image_name]

            await save_status()
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Gambar terkirim ke grup {group_id}. Tunggu sebelum mengirim ke grup berikutnya...")

        except Exception as e:
            logger.error(f"Gagal mengirim pesan dan gambar ke grup {group_id}: {e}")
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Gagal mengirim pesan dan gambar ke grup {group_id}: {e}")

    except Exception as e:
        logger.error(f"Ada kesalahan dalam mengirim pesan ke grup {group_id}: {e}")
        print(f"Ada kesalahan dalam mengirim pesan ke grup {group_id}: {e}")

async def send_message_to_private_chat(chat_id):
    """Kirim pesan acak tertempel gambar ke pesan pribadi."""
    try:
        available_images = [image for image in os.listdir(os.path.join(script_directory, images_folder))]
        sent_images = processed_private_chats.get(chat_id, [])
        available_images = list(set(available_images) - set(sent_images))

        if not available_images:
            logger.info(f"Semua gambar sudah dikirim ke pesan pribadi {chat_id}.")
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Semua gambar sudah dikirim ke pesan pribadi {chat_id}.")
            return

        image_name = random.choice(available_images)
        image_path = os.path.join(script_directory, images_folder, image_name)

        message = random.choice(messages)

        try:
            print("[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Mengirim pesan dan gambar...")
            await client.send_file(chat_id, image_path, caption=message)
            logger.info(f"Pesan dan gambar terkirim ke pesan pribadi {chat_id}.")
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Pesan dan gambar terkirim ke pesan pribadi {chat_id}.")

            if chat_id in processed_private_chats:
                processed_private_chats[chat_id].append(image_name)
            else:
                processed_private_chats[chat_id] = [image_name]

            await save_status()
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Gambar terkirim ke pesan pribadi {chat_id}. Tunggu sebelum mengirim ke pesan pribadi berikutnya...")

        except Exception as e:
            logger.error(f"Gagal mengirim pesan dan gambar ke pesan pribadi {chat_id}: {e}")
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Gagal mengirim pesan dan gambar ke pesan pribadi {chat_id}: {e}")

    except Exception as e:
        logger.error(f"Ada kesalahan dalam mengirim pesan ke pesan pribadi {chat_id}: {e}")
        print(f"Ada kesalahan dalam mengirim pesan ke pesan pribadi {chat_id}: {e}")

async def main():
    """Fungsi utama untuk menjalankan aplikasi."""
    try:
        await client.start()
        await send_random_message()

    except Exception as e:
        logger.error(f"Terjadi kesalahan: {e}")
        print(f"Terjadi kesalahan: {e}")

asyncio.get_event_loop().run_until_complete(main())
