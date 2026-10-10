from vkbottle.bot import Bot, Message
import random
import sqlite3
import asyncio

# ⚠️ ВПИШИТЕ ВАШ ТОКЕН МЕЖДУ КАВЫЧКАМИ:
bot = Bot(token="vk1.a.43T-dxRm5u85Q3f34ab99otdlJAy32Xv8su7iEjnQsmKpL4KoosjtkVWn9VrjFZx-KDSEuUPtjL4vas8dju_CsUjNDOUyC_0uCeQkstYLhXoVTpJn_WH-U-CfoxW__T3gkpZWHiYttziHYj3kd-07gG9oLv51fvnuyXFe1eMFVuuTh6WsICp_m3ilekLMRhi-6mbaU0P1zp9nMTkB9IQ-w")

# Настройка базы данных
conn = sqlite3.connect("bot_database.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        coins INTEGER DEFAULT 100
    )
""")
conn.commit()
conn.close()

@bot.on.message(text="!кубик")
async def dice_handler(message: Message):
    number = random.randint(1, 6)
    await message.answer(f"🎲 Вам выпало число: {number}", random_id=random.randint(1, 100000000))

@bot.on.message(text="!монеты")
async def coins_handler(message: Message):
    user_id = message.from_id
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT coins FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    
    if result is None:
        cursor.execute("INSERT INTO users (user_id, coins) VALUES (?, ?)", (user_id, 100))
        conn.commit()
        balance = 100
    else:
        balance = result[0] if isinstance(result, tuple) else result
        
    bonus = random.randint(1, 15)
    new_balance = balance + bonus
    cursor.execute("UPDATE users SET coins = ? WHERE user_id = ?", (new_balance, user_id))
    conn.commit()
    conn.close()
    
    await message.answer(
        f"💰 Ваш баланс: {new_balance} монет!\n(Бонус за активность: +{bonus})", 
        random_id=random.randint(1, 100000000)
    )

# Хитрый веб-сервер внутри кода, чтобы Render не ругался на порты
async def handle_ping(reader, writer):
    await reader.read(100)
    message = "HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK"
    writer.write(message.encode())
    await writer.drain()
    writer.close()

async def main():
    import os
    port = int(os.environ.get("PORT", 10000))
    # Запускаем веб-сервер на нужном порту параллельно с ботом
    await asyncio.start_server(handle_ping, '0.0.0.0', port)
    
    # Запускаем бота ВК
    await bot.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
