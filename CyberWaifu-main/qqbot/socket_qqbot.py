import calendar
import os
import socket
import string
import time

from pycqBot import cqLog
from pycqBot.cqCode import image,set_cq_code
from pycqBot.data import Message
# from Python310.Lib import logging
import logging
from waifu.Tools import divede_sentences
from waifu.Waifu import Waifu


class socket_qqbot:
    cqLog(level=logging.INFO, logPath='./qqbot/cqLogs')

    def __init__(self, waifu: Waifu, host="127.0.0.1", port=9999, send_text=True):
        self.socketBot = socket.socket()
        self.socketBot.bind((host, port))
        self.socketBot.listen()
        self.waifu = waifu
        self.send_text = send_text

    def def_socket_thread(self):
        c, addr = self.socketBot.accept()
        print("Socket已连接，等待Socket消息中...")
        try:
            while True:
                content = read_from_client(c)
                time.sleep(1)
                if len(content) > 0:
                    print('收到来自Socket消息')
                    print('消息内容：' + content)
                    self.create_reply(content, c)
                else:
                    continue
        except IOError as e:
            print(e.strerror)
        print('start socket thread!!!')

    def create_reply(self, message: str, c):
        if 'CQ' in message:
            return
        try:
            # reply = self.waifu.ask(message.message)
            reply = self.waifu.ask(message)

            sentences = divede_sentences(reply)
            for st in sentences:
                time.sleep(0.5)
                if st == '' or st == ' ':
                    continue
                if self.send_text:
                    part = self.waifu.add_emoji(st)
                    print(f'发送信息: {part}')
                    # logging.info(f'发送信息: {part}')
                    part = part.encode('utf-8')
                    c.send(part)
            file_name = self.waifu.finish_ask(reply)
            if not file_name == '':
                file_path = file_name
                abs_path = os.path.abspath(file_path)
                cq_reply = "%s" % image(file=abs_path)
                c.send(cq_reply.encode('utf-8'))

        except Exception as e:
            logging.error(e)


def read_from_client(c):
    """
    从客户端接收数据。

    参数:
    c -- 客户端连接对象。

    返回:
    客户端发送的字符串数据，如果无法接收，则返回空。
    """
    try:
        # 尝试接收客户端发送的数据，最多1024字节。
        return c.recv(1024).decode('utf-8')
    except IOError as e:
        # 打印IOError错误信息。
        print(e.strerror)

