import logging
import re
import os
import json
import datetime
from typing import List

import requests
from dateutil.parser import parse
from langchain.schema import HumanMessage, BaseMessage
from lxml import etree
from termcolor import colored
import urllib.request
import re
import random


def get_first_sentence(text: str):
    sentences = re.findall(r'.*?[~。！？…]+', text)
    if len(sentences) == 0:
        return '', text
    first_sentence = sentences[0]
    after = text[len(first_sentence):]
    return first_sentence, after


def divede_sentences(text: str) -> List[str]:
    sentences = re.findall(r'.*?[~。！？…]+', text)
    if len(sentences) == 0:
        return [text]
    return sentences


def make_message(text: str):
    data = {
        "msg": text,
        "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return HumanMessage(content=json.dumps(data, ensure_ascii=False))


def message_period_to_now(message: BaseMessage):
    '''返回最后一条消息到现在的小时数'''
    print(message.content)
    last_time = json.loads(message.content)['time']
    last_time = parse(last_time)
    now_time = parse(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    duration = (now_time - last_time).total_seconds() / 3600
    return duration


def load_prompt(filename: str):
    file_path = f'./presets/charactor/{filename}.txt'
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            system_prompt = f.read()
        print(colored(f'人设文件加载成功！({file_path})', 'green'))
    except:
        print(colored(f'人设文件: {file_path} 不存在', 'red'))
    return system_prompt


# def load_emoticon(emoticons: list):
#     data = {'images': []}
#     files = []
#     for i in range(0, len(emoticons), 2):
#         data['images'].append({
#             'file_name': emoticons[i][1],
#             'description': emoticons[i+1][1]
#         })
#         files.append(f'./presets/emoticon/{emoticons[i][1]}')
#     try:
#         with open(f'./presets/emoticon/emoticon.json', 'w',encoding='utf-8') as f:
#             json.dump(data, f, ensure_ascii=False)
#         for file in files:
#             if not os.path.exists(file):
#                 raise FileNotFoundError(file)
#         print(colored(f'表情包加载成功！({len(files)} 个表情包文件)', 'green'))
#     except FileNotFoundError as e:
#         print(colored(f'表情包加载失败，图片文件 {e} 不存在！', 'red'))
#     except:
#         print(colored(f'表情包加载失败，请检查配置', 'red'))

def load_emoticon(emoticons: list):
    folder_path = "./presets/emoticon"
    if os.path.exists(folder_path + "/" + "emoticon.json"):
        os.remove(folder_path + "/" + "emoticon.json")
    data = {'images': []}
    files = []
    for folder_name in os.listdir(folder_path):
        for file_name in os.listdir(folder_path + "/" + folder_name):
            data['images'].append({
                'file_name': folder_name + "/" + file_name,
                'description': folder_name
            })
            files.append(folder_path + "/" + folder_name + "/" + file_name)

    try:
        with open(f'./presets/emoticon/emoticon.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
        for file in files:
            if not os.path.exists(file):
                raise FileNotFoundError(file)
        print(colored(f'表情包加载成功！({len(files)} 个表情包文件)', 'green'))
    except FileNotFoundError as e:
        print(colored(f'表情包加载失败，图片文件 {e} 不存在！', 'red'))
    except:
        print(colored(f'表情包加载失败，请检查配置', 'red'))

    # data = {'images': []}
    # files = []
    # for i in range(0, len(emoticons), 2):
    #     data['images'].append({
    #         'file_name': emoticons[i][1],
    #         'description': emoticons[i+1][1]
    #     })
    #     files.append(f'./presets/emoticon/{emoticons[i][1]}')
    # try:
    #     with open(f'./presets/emoticon/emoticon.json', 'w',encoding='utf-8') as f:
    #         json.dump(data, f, ensure_ascii=False)
    #     for file in files:
    #         if not os.path.exists(file):
    #             raise FileNotFoundError(file)
    #     print(colored(f'表情包加载成功！({len(files)} 个表情包文件)', 'green'))
    # except FileNotFoundError as e:
    #     print(colored(f'表情包加载失败，图片文件 {e} 不存在！', 'red'))
    # except:
    #     print(colored(f'表情包加载失败，请检查配置', 'red'))


def load_memory(filename: str, waifuname):
    file_path = f'./presets/charactor/{filename}.txt'
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            memory = f.read()
        if os.path.exists(f'./memory/{waifuname}.csv'):
            print(colored(f'记忆数据库存在，不导入记忆', 'yellow'))
            return ''
        else:
            chunks = memory.split('\n\n')
            print(colored(f'记忆导入成功！({len(chunks)} 条记忆)', 'green'))
    except:
        print(colored(f'记忆文件文件: {file_path} 不存在', 'red'))

    return memory


def str2bool(text: str):
    if text == 'True' or text == 'true':
        return True
    elif text == 'False' or text == 'false':
        return False
    else:
        print(colored(f'无法将 {text} 转换为布尔值，请检查配置文件！'))
        raise ValueError()


# 从贴吧获取并返回一张图片
def get_photo_from_tieba(url="https://tieba.baidu.com/f?kw=%E5%90%8A%E5%9B%BE&ie=utf-8&pn="):
    result_photo = None
    while result_photo is None:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Cookie": "XFI=5c33c270-29ff-11ef-9c79-d1fbac9db0f6; XFCS=D1EE01F296DEF60AB3B7CB48195A2FDA6FD2F5209154529C11CBA06990A3514B; XFT=+bBaUY4jbx1q+D/NcGebEyRzKmZUzu3E2qNx9DDGzUA=; BIDUPSID=93F9E30864D9D0D408B5089C43810AA6; PSTM=1704521005; BAIDUID=93F9E30864D9D0D41A2BBEC8874D2AB9:FG=1; H_WISE_SIDS_BFESS=60270_60282_60289_60297; newlogin=1; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1716127097,1716832498,1717123976,1717144063; BDUSS=N4fk9wcXRuTlJxRVBFZHROZkpQZkc3dXpQUS1OQkdvdXZLUFd-SFJYV0FINFJtRVFBQUFBJCQAAAAAAAAAAAEAAADJI1b~YW9yYjcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAICSXGaAklxmQl; BDUSS_BFESS=N4fk9wcXRuTlJxRVBFZHROZkpQZkc3dXpQUS1OQkdvdXZLUFd-SFJYV0FINFJtRVFBQUFBJCQAAAAAAAAAAAEAAADJI1b~YW9yYjcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAICSXGaAklxmQl; STOKEN=7d163f21302716c1aaa9253cb5282ada20c9d1bdf06d82be5228b93efe547a6a; Hm_lvt_049d6c0ca81a94ed2a9b8ae61b3553a5=1717343517; H_PS_PSSID=60297_60327_60336; H_WISE_SIDS=60297_60327_60336; BAIDUID_BFESS=93F9E30864D9D0D41A2BBEC8874D2AB9:FG=1; ZFY=znq9XtmuEs6jO50UXDmbbR8txTp6lNbIqAQxHN0PjzU:C; delPer=0; PSINO=1; BAIDU_WISE_UID=wapp_1718333177737_817; USER_JUMP=-1; Hm_lvt_292b2e1608b0823c1cb6beef7243ef34=1717342809,1717869915,1718168541,1718333177; st_key_id=17; arialoadData=false; BCLID=9695099365197374845; BCLID_BFESS=9695099365197374845; BDSFRCVID=v4KOJeC62Co7c63te1q1bVtoMGnv6RQTH6f3U1LMr9Q6XGTXBWeuEG0PzM8g0KAhQ_9vogKKymOTHuPF_2uxOjjg8UtVJeC6EG0Ptf8g0x5; BDSFRCVID_BFESS=v4KOJeC62Co7c63te1q1bVtoMGnv6RQTH6f3U1LMr9Q6XGTXBWeuEG0PzM8g0KAhQ_9vogKKymOTHuPF_2uxOjjg8UtVJeC6EG0Ptf8g0x5; H_BDCLCKID_SF=tbC8VCDKJDD3H48k-4QEbbQH-UnLqbTeHmOZ04n-ah05hRj9yROqjpLJ-RjJLt-eWR5-3tom3UTdsq76Wh35K5tTQP6rLqcTMHc4KKJxbPDVEpoL0-K-M6t8hUJiBbcLBan7LxJIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbC8lejuaj65LeU5eetjK2CntsJOOaCv6DpbOy4oWK441DN5KhUTJ5RvjLnoCbUQJhpIwbt5K3M04X-o9-hvT-54e2p3FBUQZV-cKQft20b0LqtbGXqOaJDLe0R7jWhvBDq72ybomQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8IjHCeJ6F8tRFqoCvt-5rDHJTg5DTjhPrMbU6tWMT-MTryKK8-K4nkfbK6XRJD3R0ZbNbAq4Qa-HnRhlRNB-3iV-OxDUvnyxAZWJ3ELfQxtNRJQ66n0fcmHCQFDPoobUPU2fc9LUvtLgcdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj2CKLtKDBbDDCj6L3-RJH-xQ0KnLXKKOLVM5MJp7ketn4hUt5D4_bylO-tho4KHcJ-J0bWCTqH4o2QhrdQf4WWb3ebTJr32Qr-fTxMfQpsIJM5bLVLUDl0MKqajJ-aKvia-TEBMb1ffJDBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTDMFhe6QBDHDeq6-JfK7y0nT855rEDJ7v-ITjhPrM5GOiWMT-0bFH5bA5KKL5fbKlKjQD3R0eXtJX-j5NLGn7_JLbQCjd8t_w0jjiQp0RLRJ--xQxtNRE2CnjtpvNjMj3eJjobUPU2fc9LUvtLgcdot5yBbc8eIna5hjkbfJBQttjQn3hfIkjXIKLK-oj-D-xD5D23e; H_BDCLCKID_SF_BFESS=tbC8VCDKJDD3H48k-4QEbbQH-UnLqbTeHmOZ04n-ah05hRj9yROqjpLJ-RjJLt-eWR5-3tom3UTdsq76Wh35K5tTQP6rLqcTMHc4KKJxbPDVEpoL0-K-M6t8hUJiBbcLBan7LxJIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbC8lejuaj65LeU5eetjK2CntsJOOaCv6DpbOy4oWK441DN5KhUTJ5RvjLnoCbUQJhpIwbt5K3M04X-o9-hvT-54e2p3FBUQZV-cKQft20b0LqtbGXqOaJDLe0R7jWhvBDq72ybomQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8IjHCeJ6F8tRFqoCvt-5rDHJTg5DTjhPrMbU6tWMT-MTryKK8-K4nkfbK6XRJD3R0ZbNbAq4Qa-HnRhlRNB-3iV-OxDUvnyxAZWJ3ELfQxtNRJQ66n0fcmHCQFDPoobUPU2fc9LUvtLgcdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj2CKLtKDBbDDCj6L3-RJH-xQ0KnLXKKOLVM5MJp7ketn4hUt5D4_bylO-tho4KHcJ-J0bWCTqH4o2QhrdQf4WWb3ebTJr32Qr-fTxMfQpsIJM5bLVLUDl0MKqajJ-aKvia-TEBMb1ffJDBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTDMFhe6QBDHDeq6-JfK7y0nT855rEDJ7v-ITjhPrM5GOiWMT-0bFH5bA5KKL5fbKlKjQD3R0eXtJX-j5NLGn7_JLbQCjd8t_w0jjiQp0RLRJ--xQxtNRE2CnjtpvNjMj3eJjobUPU2fc9LUvtLgcdot5yBbc8eIna5hjkbfJBQttjQn3hfIkjXIKLK-oj-D-xD5D23e; 4283835337_FRSVideoUploadTip=1; video_bubble4283835337=1; wise_device=0; XFI=a666cda0-29fb-11ef-ba11-7978ac10668a; XFCS=6925F709CB1B25A72C6A9274151AC65CA513CB7BD6ECDA819FAF4BB6522E1FED; XFT=XObKpO5PSZwzQncSBwAf49hUjuD/ZjZl7r8Tmg8Bxd4=; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; tb_as_data=2806b41bb3e8aa941f91c9bb3082c2b81ee028c6568a0f0b437c51d36edd22c058dc1d3643fef3bf6b26c84d1dd15d4161422f569caf387708c7987b4b8668c5483ed1572b882bf85282bfc2854d1f1cb7c2e2248360ebf0516e9b1ee88f848e786e6ea85da16b73a4856b274d1a96b9; Hm_lpvt_292b2e1608b0823c1cb6beef7243ef34=1718336221; BA_HECTOR=85210l81812k8hal2k0k002l1bo91p1j6nemt1v; ab_sr=1.0.1_N2JmYTBiODY4MzIwMWVmYWY4ZmU3OTQ0MzAyMDJkZWMxODdjOGU1NDFhMGFhZDRjOTRlYTdmMWNkNzFjMmVlOWY0YTNiMDlmNjJkODZhNThlZmY1MmUzZjE0NDBjNDFmOTY4ZjgwNzE4OTRiYzI2NDE2NWM0ODljNTY3NjM3ZDYxYTBkNjI0ODg0MjE4NDk2ZTNkY2IxZmEzZmYxYjRmNjczOWJjYzU5MzQ2M2VjNGY0OGVlOGJjOTk3ZGUyMmM5; st_data=202aab5628fc72e3a6fadaee7d287687f306d3ff4627340727ee4e6400c2197c905c98da2f042e098502e2db6c3818fcc3be6baba2a5a8c1c084bea5e3c47d22c65183e4c7654e11f983387822d1d53975d220edc9e13b34f9b887f4058f948dc4c9b3ec4695c0167646a410fd3980a3ca9c8edff5441094c69e3f372d0e1d99defad7542b902e316a6453f17b8eff46; st_sign=e489b10a; RT=\"z=1&dm=baidu.com&si=37b4de14-1dcc-48d8-9b69-5f8d28017843&ss=lxe37etl&sl=x&tt=ut4&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=1tdst&ul=1thp9\"",
        }
        outer_url = url + str(random.randint(0, 1000000))
        outer_html = requests.get(outer_url, headers=headers)
        outer_html = outer_html.text.replace('<!--','').replace('-->','')
        selector = etree.HTML(outer_html)

        url_list = selector.xpath('.//div[@class="threadlist_lz clearfix"]/div/a/@href')

        random_url_num = random.randint(0, len(url_list) - 1)
        next_url = 'http://tieba.baidu.com' + url_list[random_url_num]

        if not os.path.exists('photo'):
            os.mkdir('photo')
        # root_path = os.getcwd()
        # os.chdir('photo')
        # next_url="https://tieba.baidu.com/p/7718581561?red_tag=0715206355"
        rep = requests.get(next_url, headers=headers)
        rep.encoding = 'utf-8'
        html = etree.HTML(rep.text)
        # 通过xpath筛选出所需要的代码信息
        img_url_list = html.xpath('//*[@class="BDE_Image"]/@src')

        if len(img_url_list) <= 0:
            continue

        logging.info(f"已从{next_url}中获取图片，正在储存发送中...")
        random_img_num = random.randint(0, len(img_url_list) - 1)
        urllib.request.urlretrieve(img_url_list[random_img_num], 'waifu/photo/pic.jpg')
        result_photo = 'photo/pic.jpg'

        if os.path.exists("waifu/photo/pic.jpg"):
            return result_photo
        else:
            continue
        # img_selector = etree.HTML("https://tieba.baidu.com/p/7718581561?red_tag=0715206355")
        # img_url_list = img_selector.xpath('//*[@class="skipAutoFix"]')
        # random_img_num = random.randint(0, len(img_url_list) - 1)
        # print(urllib.request.urlretrieve(img_url_list[random_img_num], 'pic.jpg'))
