from socket_qqbot import socket_qqbot
from pycqBot.cqCode import strToCqCode,set_cq_code,strToCqCodeToDict

# message = "[CQ:at,qq=114514]早上好啊"
# CQCodemsg = strToCqCodeToDict(message)
# print(CQCodemsg[0])
#
# CQcodes = {'type': 'at', 'data': {'qq': '114514'}}
# newCQ = set_cq_code(CQcodes)
# print(newCQ)
# print(type(newCQ))

# HOST = "127.0.0.1"
# PORT = 9999
# BUFFER_SIZE = 1024
# MAX_LISTEN = 5
#
# bot = socket_qqbot(HOST=HOST, PORT=PORT, BUFFER_SIZE=BUFFER_SIZE, MAX_LISTEN=MAX_LISTEN)
# bot.send_message_to_cs("message")