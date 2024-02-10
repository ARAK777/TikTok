import re
import os
import json
import time
import random
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command, Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from download import download_video
from random_id import photo_id, sticker_id
from class_distribution import DistributionState

from database import (
    database_initialization,
    get_user_language,
    set_user_language,
    new_user,
    get_users_count,
    get_users,
    add_new_download,
    get_downloads,
)
from dotenv import load_dotenv
from os.path import join, dirname


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


bot_token = os.environ.get("bot_token")
admin_id = os.environ.get("admin_id")
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
loop = asyncio.get_event_loop()
database_initialization()


with open("language/lang.json", "r", encoding="utf-8") as lang_file:
    lang = json.load(lang_file)

with open("language/strings_ru.json", "r", encoding="utf-8") as ru_file:
    strings_ru = json.load(ru_file)

with open("language/strings_en.json", "r", encoding="utf-8") as en_file:
    strings_en = json.load(en_file)

with open("language/strings_uk.json", "r", encoding="utf-8") as uk_file:
    strings_uk = json.load(uk_file)

with open("language/strings_de.json", "r", encoding="utf-8") as de_file:
    strings_de = json.load(de_file)

with open("language/strings_fr.json", "r", encoding="utf-8") as fr_file:
    strings_fr = json.load(fr_file)

with open("language/strings_es.json", "r", encoding="utf-8") as es_file:
    strings_es = json.load(es_file)

with open("language/strings_jap.json", "r", encoding="utf-8") as jap_file:
    strings_jap = json.load(jap_file)

with open("language/strings_ko.json", "r", encoding="utf-8") as ko_file:
    strings_ko = json.load(ko_file)

with open("language/strings_zh_hans.json", "r", encoding="utf-8") as zh_hans_file:
    strings_zh_hans = json.load(zh_hans_file)

with open("language/strings_zh_hant.json", "r", encoding="utf-8") as zh_hant_file:
    strings_zh_hant = json.load(zh_hant_file)


@dp.message_handler(Command('start'))
async def start_command(message: types.Message):
    new_user(message.chat.id)
    user_id = message.from_user.id
    language = get_user_language(user_id)
    keyboard_language = types.InlineKeyboardMarkup(row_width=2)
    keyboard_language.add(types.InlineKeyboardButton(text="🇺🇦 Українська", callback_data="set_language_uk"),
                         types.InlineKeyboardButton(text="🇬🇧 English", callback_data="set_language_en"))
    keyboard_language.add(types.InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_language_ru"),
                         types.InlineKeyboardButton(text="🇩🇪 Deutsch", callback_data="set_language_de"))
    keyboard_language.add(types.InlineKeyboardButton(text="🇫🇷 Français", callback_data="set_language_fr"),
                         types.InlineKeyboardButton(text="🇪🇸 Español", callback_data="set_language_es"))
    keyboard_language.add(types.InlineKeyboardButton(text="🇯🇵 日本語", callback_data="set_language_jap"),
                         types.InlineKeyboardButton(text="🇰🇷 한국인", callback_data="set_language_ko"))
    keyboard_language.add(types.InlineKeyboardButton(text="🇨🇳 中国人", callback_data="set_language_zh_hans"),
                         types.InlineKeyboardButton(text="🇨🇳 中國人", callback_data="set_language_zh_hant"))
    if language is None:
        gif_url = "https://t.me/AEh4oo/99"
        await message.answer_animation(gif_url, caption=lang["lang"], reply_markup=keyboard_language, parse_mode='HTML')
    else:
        if language == "ru":
            random_photo = random.choice(photo_id)
            await message.answer_photo(random_photo, strings_ru["start"], parse_mode='HTML')
        elif language == "en":
            random_photo = random.choice(photo_id)
            await message.answer_photo(random_photo, strings_en["start"], parse_mode='HTML')
        elif language == "uk":
            random_photo = random.choice(photo_id)
            await message.answer_photo(random_photo, strings_uk["start"], parse_mode='HTML')
        elif language == "de":
            random_photo = random.choice(photo_id)
            await message.answer_photo(random_photo, strings_de["start"], parse_mode='HTML')
        elif language == "fr":
            random_photo = random.choice(photo_id)
            await message.answer_photo(random_photo, strings_fr["start"], parse_mode='HTML')
        elif language == "es":
            random_photo = random.choice(photo_id)
            await message.answer_photo(random_photo, strings_es["start"], parse_mode='HTML')
        elif language == "jap":
            random_photo = random.choice(photo_id)
            await message.answer_photo(random_photo, strings_jap["start"], parse_mode='HTML')
        elif language == "ko":
            random_photo = random.choice(photo_id)
            await message.answer_photo(random_photo, strings_ko["start"], parse_mode='HTML')
        elif language == "zh_hans":
            random_photo = random.choice(photo_id)
            await message.answer_photo(random_photo, strings_zh_hans["start"], parse_mode='HTML')
        elif language == "zh_hant":
            random_photo = random.choice(photo_id)
            await message.answer_photo(random_photo, strings_zh_hant["start"], parse_mode='HTML')


@dp.message_handler(Command('help'))
async def help_command(message: types.Message):
    user_id = message.from_user.id
    language = get_user_language(user_id)
    if language == "ru":
        await message.answer(strings_ru["help"], parse_mode='HTML', disable_web_page_preview=True)
    elif language == "en":
        await message.answer(strings_en["help"], parse_mode='HTML', disable_web_page_preview=True)
    elif language == "uk":
        await message.answer(strings_uk["help"], parse_mode='HTML', disable_web_page_preview=True)
    elif language == "de":
         await message.answer(strings_de["help"], parse_mode='HTML', disable_web_page_preview=True)
    elif language == "fr":
         await message.answer(strings_fr["help"], parse_mode='HTML', disable_web_page_preview=True)
    elif language == "es":
         await message.answer(strings_es["help"], parse_mode='HTML', disable_web_page_preview=True)
    elif language == "jap":
         await message.answer(strings_jap["help"], parse_mode='HTML', disable_web_page_preview=True)
    elif language == "ko":
         await message.answer(strings_ko["help"], parse_mode='HTML', disable_web_page_preview=True)
    elif language == "zh_hans":
         await message.answer(strings_zh_hans["help"], parse_mode='HTML', disable_web_page_preview=True)
    elif language == "zh_hant":
         await message.answer(strings_zh_hant["help"], parse_mode='HTML', disable_web_page_preview=True)


@dp.message_handler(Command('lang'))
async def lang_command(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text="🇺🇦 Українська", callback_data="set_language_uk"),
                 types.InlineKeyboardButton(text="🇬🇧 English", callback_data="set_language_en"))
    keyboard.add(types.InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_language_ru"),
                 types.InlineKeyboardButton(text="🇩🇪 Deutsch", callback_data="set_language_de"))
    keyboard.add(types.InlineKeyboardButton(text="🇫🇷 Français", callback_data="set_language_fr"),
                 types.InlineKeyboardButton(text="🇪🇸 Español", callback_data="set_language_es"))
    keyboard.add(types.InlineKeyboardButton(text="🇯🇵 日本語", callback_data="set_language_jap"),
                 types.InlineKeyboardButton(text="🇰🇷 한국인", callback_data="set_language_ko"))
    keyboard.add(types.InlineKeyboardButton(text="🇨🇳 中国人", callback_data="set_language_zh_hans"),
                 types.InlineKeyboardButton(text="🇨🇳 中國人", callback_data="set_language_zh_hant"))
    gif_url = "https://t.me/AEh4oo/99"
    await message.answer_animation(gif_url, caption=lang["lang"], reply_markup=keyboard, parse_mode='HTML')


@dp.message_handler(Command('donate'))
async def donate(message: types.Message):
    if os.getenv("PAYMENTS_TOKEN").split(':')[1] == 'TEST':
        await bot.send_invoice(message.chat.id,
                               title="Donation",
                               description="Thank you!!!",
                               provider_token=os.getenv("PAYMENTS_TOKEN"),
                               currency="USD",
                               is_flexible=False,
                               prices=[types.LabeledPrice(label="Support the bot", amount=5*100)],
                               start_parameter="donation",
                               payload="donation-invoice-payload")


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")
    await bot.send_message(message.chat.id, text=f"<b>Thank you!!!</b>\nThe payment of <b>{message.successful_payment.total_amount // 100} {message.successful_payment.currency}</b> was successful!!!", parse_mode='HTML')


@dp.message_handler(Command('stats'))
async def stats_command(message: types.Message):
    user_id = message.from_user.id
    language = get_user_language(user_id)
    if str(message.chat.id) in admin_id:
        downloads_count = get_downloads()
        if language == "ru":
            await message.answer(strings_ru["stats_admin"].format(users_count=len(get_users_count()), downloads_count=downloads_count), parse_mode='HTML')
        elif language == "uk":
            await message.answer(strings_uk["stats_admin"].format(users_count=len(get_users_count()), downloads_count=downloads_count), parse_mode='HTML')
        elif language == "en":
            await message.answer(strings_en["stats_admin"].format(users_count=len(get_users_count()), downloads_count=downloads_count), parse_mode='HTML')
        elif language == "de":
            await message.answer(strings_de["stats_admin"].format(users_count=len(get_users_count()), downloads_count=downloads_count), parse_mode='HTML')
        elif language == "fr":
            await message.answer(strings_fr["stats_admin"].format(users_count=len(get_users_count()), downloads_count=downloads_count), parse_mode='HTML')
        elif language == "es":
            await message.answer(strings_es["stats_admin"].format(users_count=len(get_users_count()), downloads_count=downloads_count), parse_mode='HTML')
        elif language == "jap":
            await message.answer(strings_jap["stats_admin"].format(users_count=len(get_users_count()), downloads_count=downloads_count), parse_mode='HTML')
        elif language == "ko":
            await message.answer(strings_ko["stats_admin"].format(users_count=len(get_users_count()), downloads_count=downloads_count), parse_mode='HTML')
        elif language == "zh_hans":
            await message.answer(strings_zh_hans["stats_admin"].format(users_count=len(get_users_count()), downloads_count=downloads_count), parse_mode='HTML')
        elif language == "zh_hant":
            await message.answer(strings_zh_hant["stats_admin"].format(users_count=len(get_users_count()), downloads_count=downloads_count), parse_mode='HTML')
    else:
        if language == "ru":
            await message.answer(strings_ru["stats_user"], parse_mode='HTML')
        elif language == "uk":
            await message.answer(strings_uk["stats_user"], parse_mode='HTML')
        elif language == "en":
            await message.answer(strings_en["stats_user"], parse_mode='HTML')
        elif language == "de":
            await message.answer(strings_de["stats_user"], parse_mode='HTML')
        elif language == "fr":
            await message.answer(strings_fr["stats_user"], parse_mode='HTML')
        elif language == "es":
            await message.answer(strings_es["stats_user"], parse_mode='HTML')
        elif language == "jap":
            await message.answer(strings_jap["stats_user"], parse_mode='HTML')
        elif language == "ko":
            await message.answer(strings_ko["stats_user"], parse_mode='HTML')
        elif language == "zh_hans":
            await message.answer(strings_zh_hans["stats_user"], parse_mode='HTML')
        elif language == "zh_hant":
            await message.answer(strings_zh_hant["stats_user"], parse_mode='HTML')


@dp.message_handler(Command('send'))
async def send_command(message: types.Message, state: FSMContext):
    if str(message.chat.id) in admin_id:
        async with state.proxy() as data:
            data['user_id'] = message.chat.id
        await DistributionState.WaitForMedia.set()
        user_id = message.from_user.id
        language = get_user_language(user_id)
        if language == "ru":
            await message.answer(strings_ru["send_admin"], parse_mode='HTML')
        elif language == "en":
            await message.answer(strings_en["send_admin"], parse_mode='HTML')
        elif language == "uk":
            await message.answer(strings_uk["send_admin"], parse_mode='HTML')
        elif language == "de":
            await message.answer(strings_de["send_admin"], parse_mode='HTML')
        elif language == "fr":
            await message.answer(strings_fr["send_admin"], parse_mode='HTML')
        elif language == "es":
            await message.answer(strings_es["send_admin"], parse_mode='HTML')
        elif language == "jap":
            await message.answer(strings_jap["send_admin"], parse_mode='HTML')
        elif language == "ko":
            await message.answer(strings_ko["send_admin"], parse_mode='HTML')
        elif language == "zh_hans":
            await message.answer(strings_zh_hans["send_admin"], parse_mode='HTML')
        elif language == "zh_hant":
            await message.answer(strings_zh_hant["send_admin"], parse_mode='HTML')
    else:
        user_id = message.from_user.id
        language = get_user_language(user_id)
        if language == "ru":
            await message.answer(strings_ru["send_user"], parse_mode='HTML')
        elif language == "en":
            await message.answer(strings_en["send_user"], parse_mode='HTML')
        elif language == "uk":
            await message.answer(strings_uk["send_user"], parse_mode='HTML')
        elif language == "de":
            await message.answer(strings_de["send_user"], parse_mode='HTML')
        elif language == "fr":
            await message.answer(strings_fr["send_user"], parse_mode='HTML')
        elif language == "es":
            await message.answer(strings_es["send_user"], parse_mode='HTML')
        elif language == "jap":
            await message.answer(strings_jap["send_user"], parse_mode='HTML')
        elif language == "ko":
            await message.answer(strings_ko["send_user"], parse_mode='HTML')
        elif language == "zh_hans":
            await message.answer(strings_zh_hans["send_user"], parse_mode='HTML')
        elif language == "zh_hant":
            await message.answer(strings_zh_hant["send_user"], parse_mode='HTML')


@dp.message_handler(content_types=['document', 'video', 'audio', 'voice', 'animation', 'photo', 'text'], state=DistributionState.WaitForMedia)
async def handle_media(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['media'] = message
        keyboard = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("✅", callback_data="confirm_media"),
            types.InlineKeyboardButton("❌", callback_data="cancel_media"))
        await DistributionState.ConfirmMedia.set()
        user_id = message.from_user.id
        language = get_user_language(user_id)
        if language == "ru":
            await message.reply(strings_ru["check_broadcast"], reply_markup=keyboard, parse_mode='HTML')
        elif language == "en":
            await message.reply(strings_en["check_broadcast"], reply_markup=keyboard, parse_mode='HTML')
        elif language == "uk":
            await message.reply(strings_uk["check_broadcast"], reply_markup=keyboard, parse_mode='HTML')
        elif language == "de":
            await message.reply(strings_de["check_broadcast"], reply_markup=keyboard, parse_mode='HTML')
        elif language == "fr":
            await message.reply(strings_fr["check_broadcast"], reply_markup=keyboard, parse_mode='HTML')
        elif language == "es":
            await message.reply(strings_es["check_broadcast"], reply_markup=keyboard, parse_mode='HTML')
        elif language == "jap":
            await message.reply(strings_jap["check_broadcast"], reply_markup=keyboard, parse_mode='HTML')
        elif language == "ko":
            await message.reply(strings_ko["check_broadcast"], reply_markup=keyboard, parse_mode='HTML')
        elif language == "zh_hans":
            await message.reply(strings_zh_hans["check_broadcast"], reply_markup=keyboard, parse_mode='HTML')
        elif language == "zh_hant":
            await message.reply(strings_zh_hant["check_broadcast"], reply_markup=keyboard, parse_mode='HTML')


@dp.callback_query_handler(Text(equals="confirm_media"), state=DistributionState.ConfirmMedia)
async def confirm_media(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        user_id = data['user_id']
        media = data['media']
        text_message = data.get('text_message')
        async def throttle_send(delay):
            nonlocal last_sent_time
            current_time = time.time()
            time_since_last_sent = current_time - last_sent_time
            if time_since_last_sent < delay:
                await asyncio.sleep(delay - time_since_last_sent)
            last_sent_time = time.time()
        user_id = data['user_id']
        language = get_user_language(user_id)
        if language == "ru":
            start_broadcast = strings_ru["start_broadcast"]
            media_too_large = strings_ru["media_too_large"]
            broadcast_completed = strings_ru["broadcast_completed"]
        elif language == "en":
            start_broadcast = strings_en["start_broadcast"]
            media_too_large = strings_en["media_too_large"]
            broadcast_completed = strings_en["broadcast_completed"]
        elif language == "uk":
            start_broadcast = strings_uk["start_broadcast"]
            media_too_large = strings_uk["media_too_large"]
            broadcast_completed = strings_uk["broadcast_completed"]
        elif language == "de":
            start_broadcast = strings_de["start_broadcast"]
            media_too_large = strings_de["media_too_large"]
            broadcast_completed = strings_de["broadcast_completed"]
        elif language == "fr":
            start_broadcast = strings_fr["start_broadcast"]
            media_too_large = strings_fr["media_too_large"]
            broadcast_completed = strings_fr["broadcast_completed"]
        elif language == "es":
            start_broadcast = strings_es["start_broadcast"]
            media_too_large = strings_es["media_too_large"]
            broadcast_completed = strings_es["broadcast_completed"]
        elif language == "jap":
            start_broadcast = strings_jap["start_broadcast"]
            media_too_large = strings_jap["media_too_large"]
            broadcast_completed = strings_jap["broadcast_completed"]
        elif language == "ko":
            start_broadcast = strings_ko["start_broadcast"]
            media_too_large = strings_ko["media_too_large"]
            broadcast_completed = strings_ko["broadcast_completed"]
        elif language == "zh_hans":
            start_broadcast = strings_zh_hans["start_broadcast"]
            media_too_large = strings_zh_hans["media_too_large"]
            broadcast_completed = strings_zh_hans["broadcast_completed"]
        elif language == "zh_hant":
            start_broadcast = strings_zh_hant["start_broadcast"]
            media_too_large = strings_zh_hant["media_too_large"]
            broadcast_completed = strings_zh_hant["broadcast_completed"]
        await callback_query.message.edit_reply_markup()
        await bot.send_message(user_id, start_broadcast, parse_mode='HTML')
        users_list = get_users()
        media_id = None
        media_type = None
        media_size = 0
        if media.document:
            media_id = media.document.file_id
            media_type = 'document'
            media_size = media.document.file_size
        elif media.video:
            media_id = media.video.file_id
            media_type = 'video'
            media_size = media.video.file_size
        elif media.audio:
            media_id = media.audio.file_id
            media_type = 'audio'
            media_size = media.audio.file_size
        elif media.voice:
            media_id = media.voice.file_id
            media_type = 'voice'
            media_size = media.voice.file_size
        elif media.animation:
            media_id = media.animation.file_id
            media_type = 'animation'
            media_size = media.animation.file_size
        elif media.photo:
            media_id = media.photo[-1].file_id
            media_type = 'photo'
            media_size = 0
        elif media.text:
            media_type = 'text'
            text_message = media.text
        if media_size <= 10 * 1024 * 1024:
            last_sent_time = 0
            media_sent = 0
            block_users = 0
            for user in users_list:
                await throttle_send(1)
                caption = media.caption
                if caption:
                    caption = re.sub(r'([\\_~`>#+\-|=|{}()\[\].!])', r'\\\1', caption)
                try:
                    if media_type == 'text':
                        await bot.send_message(user, text_message, parse_mode=types.ParseMode.MARKDOWN)
                    elif media_type == 'photo':
                        await bot.send_photo(user, photo=media_id, caption=caption, parse_mode=types.ParseMode.MARKDOWN_V2)
                    else:
                        await bot.send_document(user, document=media_id, caption=caption, parse_mode=types.ParseMode.MARKDOWN_V2)
                    media_sent += 1
                    last_sent_time = time.time()
                except:
                    block_users += 1
            completed_message = broadcast_completed.format(media_sent=media_sent, block_users=block_users)
            await bot.send_message(user_id, completed_message, parse_mode='HTML')
        else:
            await bot.send_message(user_id, media_too_large, parse_mode='HTML')
        await state.finish()


@dp.callback_query_handler(Text(equals="cancel_media"), state=DistributionState.ConfirmMedia)
async def cancel_media(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    language = get_user_language(user_id)
    await state.finish()
    await callback_query.message.edit_reply_markup()
    if language == "ru":
        await bot.answer_callback_query(callback_query.id, strings_ru["off_broadcast"], show_alert=True)
    elif language == "en":
        await bot.answer_callback_query(callback_query.id, strings_en["off_broadcast"], show_alert=True)
    elif language == "uk":
        await bot.answer_callback_query(callback_query.id, strings_uk["off_broadcast"], show_alert=True)
    elif language == "de":
        await bot.answer_callback_query(callback_query.id, strings_de["off_broadcast"], show_alert=True)
    elif language == "fr":
        await bot.answer_callback_query(callback_query.id, strings_fr["off_broadcast"], show_alert=True)
    elif language == "es":
        await bot.answer_callback_query(callback_query.id, strings_es["off_broadcast"], show_alert=True)
    elif language == "jap":
        await bot.answer_callback_query(callback_query.id, strings_jap["off_broadcast"], show_alert=True)
    elif language == "ko":
        await bot.answer_callback_query(callback_query.id, strings_ko["off_broadcast"], show_alert=True)
    elif language == "zh_hans":
        await bot.answer_callback_query(callback_query.id, strings_zh_hans["off_broadcast"], show_alert=True)
    elif language == "zh_hant":
        await bot.answer_callback_query(callback_query.id, strings_zh_hant["off_broadcast"], show_alert=True)


@dp.message_handler(content_types=['text'])
async def tiktok_download(message: types.Message):
    if re.compile('https://[a-zA-Z]+.tiktok.com/').match(message.text):
        channel_member = await bot.get_chat_member("@OFFpoliceBots", message.chat.id)
        if channel_member.status == "left":
            status_button = types.InlineKeyboardMarkup()
            user_id = message.from_user.id
            language = get_user_language(user_id)
            if language == "ru":
                status_button.add(types.InlineKeyboardButton(text=strings_ru["button_url"], url='https://t.me/OFFpoliceBots'))
                status_button.row(types.InlineKeyboardButton(text=strings_ru["button_check"], callback_data='check_subscription'))
                caption_check = strings_ru["text_check"]
            elif language == "en":
                status_button.add(types.InlineKeyboardButton(text=strings_en["button_url"], url='https://t.me/OFFpoliceBots'))
                status_button.row(types.InlineKeyboardButton(text=strings_en["button_check"], callback_data='check_subscription'))
                caption_check = strings_en["text_check"]
            elif language == "uk":
                status_button.add(types.InlineKeyboardButton(text=strings_uk["button_url"], url='https://t.me/OFFpoliceBots'))
                status_button.row(types.InlineKeyboardButton(text=strings_uk["button_check"], callback_data='check_subscription'))
                caption_check = strings_uk["text_check"]
            elif language == "de":
                status_button.add(types.InlineKeyboardButton(text=strings_de["button_url"], url='https://t.me/OFFpoliceBots'))
                status_button.row(types.InlineKeyboardButton(text=strings_de["button_check"], callback_data='check_subscription'))
                caption_check = strings_de["text_check"]
            elif language == "fr":
                status_button.add(types.InlineKeyboardButton(text=strings_fr["button_url"], url='https://t.me/OFFpoliceBots'))
                status_button.row(types.InlineKeyboardButton(text=strings_fr["button_check"], callback_data='check_subscription'))
                caption_check = strings_fr["text_check"]
            elif language == "es":
                status_button.add(types.InlineKeyboardButton(text=strings_es["button_url"], url='https://t.me/OFFpoliceBots'))
                status_button.row(types.InlineKeyboardButton(text=strings_es["button_check"], callback_data='check_subscription'))
                caption_check = strings_es["text_check"]
            elif language == "jap":
                status_button.add(types.InlineKeyboardButton(text=strings_jap["button_url"], url='https://t.me/OFFpoliceBots'))
                status_button.row(types.InlineKeyboardButton(text=strings_jap["button_check"], callback_data='check_subscription'))
                caption_check = strings_jap["text_check"]
            elif language == "ko":
                status_button.add(types.InlineKeyboardButton(text=strings_ko["button_url"], url='https://t.me/OFFpoliceBots'))
                status_button.row(types.InlineKeyboardButton(text=strings_ko["button_check"], callback_data='check_subscription'))
                caption_check = strings_ko["text_check"]
            elif language == "zh_hans":
                status_button.add(types.InlineKeyboardButton(text=strings_zh_hans["button_url"], url='https://t.me/OFFpoliceBots'))
                status_button.row(types.InlineKeyboardButton(text=strings_zh_hans["button_check"], callback_data='check_subscription'))
                caption_check = strings_zh_hans["text_check"]
            elif language == "zh_hant":
                status_button.add(types.InlineKeyboardButton(text=strings_zh_hant["button_url"], url='https://t.me/OFFpoliceBots'))
                status_button.row(types.InlineKeyboardButton(text=strings_zh_hant["button_check"], callback_data='check_subscription'))
                caption_check = strings_zh_hant["text_check"]
            photo_url = "https://t.me/AEh4oo/92"
            await bot.send_photo(chat_id=message.chat.id, photo=photo_url, caption=caption_check, reply_markup=status_button, parse_mode='HTML')
            await message.delete()
            return
        try:
            user_id = message.from_user.id
            language = get_user_language(user_id)
            if language == "ru":
            	processing = strings_ru["processing"]
            elif language == "en":
            	processing = strings_en["processing"]
            elif language == "uk":
            	processing = strings_uk["processing"]
            elif language == "de":
            	processing = strings_de["processing"]
            elif language == "fr":
            	processing = strings_fr["processing"]
            elif language == "es":
            	processing = strings_es["processing"]
            elif language == "jap":
            	processing = strings_jap["processing"]
            elif language == "ko":
            	processing = strings_ko["processing"]
            elif language == "zh_hans":
            	processing = strings_zh_hans["processing"]
            elif language == "zh_hant":
            	processing = strings_zh_hant["processing"]
            random_sticker = random.choice(sticker_id)
            sticker_message = await bot.send_sticker(chat_id=message.chat.id, sticker=random_sticker)
            processing_message = await bot.send_message(chat_id=message.chat.id, text=processing, parse_mode='HTML')
            video_url, likes, comments, repost, views, description, channel_url, channel_name = await download_video(message.text)
            url_button = types.InlineKeyboardMarkup()
            url_button.add(types.InlineKeyboardButton(text='🌀 Shazam Bot', url='https://t.me/OFFpoliceShazamBot'))
            await bot.send_chat_action(message.chat.id, "upload_video")
            user_id = message.from_user.id
            language = get_user_language(user_id)
            if language == "ru":
            	video_caption = strings_ru["video_caption"]
            elif language == "en":
            	video_caption = strings_en["video_caption"]
            elif language == "uk":
            	video_caption = strings_uk["video_caption"]
            elif language == "de":
            	video_caption = strings_de["video_caption"]
            elif language == "fr":
            	video_caption = strings_fr["video_caption"]
            elif language == "es":
            	video_caption = strings_es["video_caption"]
            elif language == "jap":
            	video_caption = strings_jap["video_caption"]
            elif language == "ko":
            	video_caption = strings_ko["video_caption"]
            elif language == "zh_hans":
            	video_caption = strings_zh_hans["video_caption"]
            elif language == "zh_hant":
            	video_caption = strings_zh_hant["video_caption"]
            video_caption = video_caption.format(description=description, channel_url=channel_url, channel_name=channel_name, views=views, likes=likes, comments=comments, repost=repost, message_text=message.text)
            await bot.send_video(chat_id=message.chat.id, video=video_url, caption=video_caption, parse_mode='HTML', reply_markup=url_button)
            add_new_download()
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await bot.delete_message(chat_id=message.chat.id, message_id=sticker_message.message_id)
            await bot.delete_message(chat_id=message.chat.id, message_id=processing_message.message_id)
        except Exception as e:
            user_id = message.from_user.id
            language = get_user_language(user_id)
            if language == "ru":
                error_message = strings_ru["error_message"]
            elif language == "en":
                error_message = strings_en["error_message"]
            elif language == "uk":
                error_message = strings_uk["error_message"]
            elif language == "de":
                error_message = strings_de["error_message"]
            elif language == "fr":
                error_message = strings_fr["error_message"]
            elif language == "es":
                error_message = strings_es["error_message"]
            elif language == "jap":
                error_message = strings_jap["error_message"]
            elif language == "ko":
                error_message = strings_ko["error_message"]
            elif language == "zh_hans":
                error_message = strings_zh_hans["error_message"]
            elif language == "zh_hant":
                error_message = strings_zh_hant["error_message"]
            await bot.send_message(chat_id=message.chat.id, text=error_message.format(e), parse_mode='HTML')
            print(e)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await bot.delete_message(chat_id=message.chat.id, message_id=sticker_message.message_id)
            await bot.delete_message(chat_id=message.chat.id, message_id=processing_message.message_id)  
    else:
        user_id = message.from_user.id
        language = get_user_language(user_id)
        if language == "ru":
            no_url = strings_ru["no_url"]
        elif language == "en":
            no_url = strings_en["no_url"]
        elif language == "uk":
            no_url = strings_uk["no_url"]
        elif language == "de":
            no_url = strings_de["no_url"]
        elif language == "fr":
            no_url = strings_fr["no_url"]
        elif language == "es":
            no_url = strings_es["no_url"]
        elif language == "jap":
            no_url = strings_jap["no_url"]
        elif language == "ko":
            no_url = strings_ko["no_url"]
        elif language == "zh_hans":
            no_url = strings_zh_hans["no_url"]
        elif language == "zh_hant":
            no_url = strings_zh_hant["no_url"]
        no_url_message = await bot.send_message(chat_id=message.chat.id, text=no_url, parse_mode='HTML')
        await message.delete()
        await asyncio.sleep(5)
        await bot.delete_message(chat_id=message.chat.id, message_id=no_url_message.message_id)


@dp.callback_query_handler(lambda query: query.data == 'check_subscription')
async def check_subscription(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    try:
        channel_member = await bot.get_chat_member("@OFFpoliceBots", user_id)
        language = get_user_language(user_id)
        if language == "ru":
            success_message = strings_ru["success_message"]
            failure_message = strings_ru["failure_message"]
        elif language == "en":
            success_message = strings_en["success_message"]
            failure_message = strings_en["failure_message"]
        elif language == "uk":
            success_message = strings_uk["success_message"]
            failure_message = strings_uk["failure_message"]
        elif language == "de":
            success_message = strings_de["success_message"]
            failure_message = strings_de["failure_message"]
        elif language == "fr":
            success_message = strings_fr["success_message"]
            failure_message = strings_fr["failure_message"]
        elif language == "es":
            success_message = strings_es["success_message"]
            failure_message = strings_es["failure_message"]
        elif language == "jap":
            success_message = strings_jap["success_message"]
            failure_message = strings_jap["failure_message"]
        elif language == "ko":
            success_message = strings_ko["success_message"]
            failure_message = strings_ko["failure_message"]
        elif language == "zh_hans":
            success_message = strings_zh_hans["success_message"]
            failure_message = strings_zh_hans["failure_message"]
        elif language == "zh_hant":
            success_message = strings_zh_hant["success_message"]
            failure_message = strings_zh_hant["failure_message"]
        if channel_member.status == "member":
            await bot.answer_callback_query(callback_query.id, text=success_message, show_alert=True)
            await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
        else:
            await bot.answer_callback_query(callback_query.id, text=failure_message, show_alert=True)
    except Exception as e:
        print(e)


@dp.callback_query_handler(lambda query: query.data in ["set_language_ru", "set_language_en", "set_language_uk", "set_language_de", "set_language_fr", "set_language_es", "set_language_jap", "set_language_ko", "set_language_zh_hans", "set_language_zh_hant"])
async def set_language(call: types.CallbackQuery):
    user_id = call.from_user.id
    if call.data == "set_language_ru":
        language = "ru"
    elif call.data == "set_language_en":
        language = "en"
    elif call.data == "set_language_uk":
        language = "uk"
    elif call.data == "set_language_de":
        language = "de"
    elif call.data == "set_language_fr":
        language = "fr"
    elif call.data == "set_language_es":
        language = "es"
    elif call.data == "set_language_jap":
        language = "jap"
    elif call.data == "set_language_ko":
        language = "ko"
    elif call.data == "set_language_zh_hans":
        language = "zh_hans"
    elif call.data == "set_language_zh_hant":
        language = "zh_hant"
    set_user_language(user_id, language)
    await call.message.delete()
    if language == "ru":
        random_photo = random.choice(photo_id)
        await call.message.answer_photo(random_photo, strings_ru["start"], parse_mode='HTML')
    elif language == "en":
        random_photo = random.choice(photo_id)
        await call.message.answer_photo(random_photo, strings_en["start"], parse_mode='HTML')
    elif language == "uk":
        random_photo = random.choice(photo_id)
        await call.message.answer_photo(random_photo, strings_uk["start"], parse_mode='HTML')
    elif language == "de":
         random_photo = random.choice(photo_id)
         await call.message.answer_photo(random_photo, strings_de["start"], parse_mode='HTML')
    elif language == "fr":
         random_photo = random.choice(photo_id)
         await call.message.answer_photo(random_photo, strings_fr["start"], parse_mode='HTML')
    elif language == "es":
         random_photo = random.choice(photo_id)
         await call.message.answer_photo(random_photo, strings_es["start"], parse_mode='HTML')
    elif language == "jap":
         random_photo = random.choice(photo_id)
         await call.message.answer_photo(random_photo, strings_jap["start"], parse_mode='HTML')
    elif language == "ko":
         random_photo = random.choice(photo_id)
         await call.message.answer_photo(random_photo, strings_ko["start"], parse_mode='HTML')
    elif language == "zh_hans":
         random_photo = random.choice(photo_id)
         await call.message.answer_photo(random_photo, strings_zh_hans["start"], parse_mode='HTML')
    elif language == "zh_hant":
         random_photo = random.choice(photo_id)
         await call.message.answer_photo(random_photo, strings_zh_hant["start"], parse_mode='HTML')


if __name__ == '__main__':
    loop.create_task(executor.start_polling(dp, skip_updates=True))
    loop.run_forever()
