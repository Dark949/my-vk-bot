from vkbottle.bot import Bot, Message
import random

# Вставьте ваш токен
bot = Bot(token="vk1.a.43T-dxRm5u85Q3f34ab99otdlJAy32Xv8su7iEjnQsmKpL4KoosjtkVWn9VrjFZx-KDSEuUPtjL4vas8dju_CsUjNDOUyC_0uCeQkstYLhXoVTpJn_WH-U-CfoxW__T3gkpZWHiYttziHYj3kd-07gG9oLv51fvnuyXFe1eMFVuuTh6WsICp_m3ilekLMRhi-6mbaU0P1zp9nMTkB9IQ-w")

@bot.on.message(text="!кубик")
async def dice_handler(message: Message):
    # Генерируем случайное число для кубика
    number = random.randint(1, 6)
    
    # Создаем абсолютно случайный ID для ВК, чтобы обойти защиту от спама
    vk_spam_protection_id = random.randint(1, 100000000)
    
    # Отправляем сообщение со специальным параметром random_id
    await message.answer(
        f"🎲 Вам выпало число: {number}", 
        random_id=vk_spam_protection_id
    )

bot.run_forever()
