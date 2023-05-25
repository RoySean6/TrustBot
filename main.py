import os
import telebot
import sqlite3
from dotenv import load_dotenv
import zipfile
import shutil

load_dotenv()

bot = telebot.TeleBot(os.getenv('TELEBOT_TOKEN'))
admin_id = int(os.getenv('ADMIN_ID'))  # 管理员用户 ID, 可在配置文件中指定
reply_message = os.getenv('REPLY_MESSAGE', 'Attention!!! A damn scammer has sent a message')

def create_table_if_not_exists():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE users (
            username TEXT
        )''')
    except sqlite3.OperationalError:
        pass  # Table already exists, do nothing
    finally:
        conn.close()

@bot.message_handler(commands=['add_user'])
def add_user(message):
    if message.from_user.id == admin_id:
        username = message.text.split(' ')[1]
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        result = c.fetchone()
        if not result:
            c.execute("INSERT INTO users VALUES (?)", (username,))
            conn.commit()
            conn.close()
            bot.reply_to(message, "骗子添加成功!")
        else:
            bot.reply_to(message, "已存在，勿重复添加")

@bot.message_handler(commands=['remove_user'])
def remove_user(message):
    if message.from_user.id == admin_id:
        username = message.text.split(' ')[1]
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        result = c.fetchone()

        if result:
            c.execute("DELETE FROM users WHERE username=?", (username,))
            conn.commit()
            bot.reply_to(message, "删除成功!")
        else:
            bot.reply_to(message, "用户不存在!")
        conn.close()

def save_message_to_log(message):
    log_filename = "group_messages.log"
    check_and_compress_log(log_filename)
    with open(log_filename, "a", encoding="utf-8") as log_file:
        log_file.write(f"{message}\n")

def check_and_compress_log(log_filename):
    if os.path.exists(log_filename) and os.path.getsize(log_filename) > 10 * 1024 * 1024:
        compressed_filename = f"{log_filename[:-4]}_archive.zip"
        with zipfile.ZipFile(compressed_filename, 'w', zipfile.ZIP_DEFLATED) as archive:
            archive.write(log_filename)
        os.remove(log_filename)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def send_message(message):
    #print(message)
    if message.chat.type == 'group':
        save_message_to_log(message)
        username = message.from_user.username
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        result = c.fetchone()
        conn.close()
        if result:
            bot.reply_to(message, f"@{result[0]} {reply_message}")
        else:
            # 用户不在数据库中, 不做任何操作
            pass

create_table_if_not_exists()
bot.polling()