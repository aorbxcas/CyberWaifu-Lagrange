![cover](CyberWaifu-main/assets/cover.jpg)

<p align="center">
  <a href="https://github.com/Syan-Lin/CyberWaifu/stargazers"><img src="https://img.shields.io/github/stars/Syan-Lin/CyberWaifu?color=cd7373&amp;logo=github&amp;style=for-the-badge" alt="Github stars"></a>
  <img src="https://img.shields.io/badge/Python-3.10.10-blue?style=for-the-badge&logo=Python&logoColor=white&color=cd7373" alt="Python">
  <a href="./LICENSE"><img src="https://img.shields.io/github/license/Syan-Lin/CyberWaifu?&amp;color=cd7373&amp;style=for-the-badge" alt="License"></a>
</p>


---

### 介绍🔎
原CyberWaifu项目地址：<a href = https://github.com/Syan-Lin/CyberWaifu>https://github.com/Syan-Lin/CyberWaifu

原Lagrange项目地址：<a href = https://github.com/LagrangeDev/Lagrange.Core>https://github.com/LagrangeDev/Lagrange.Core</a>

github项目：<a href ="https://gitee.com/aorb233/cyber-waifu">点我跳转</a>

CyberWaifu 是一个使用 LLM 和 TTS 实现的聊天机器人，探索真实的聊天体验。

CyberWaifu-Lagrange 在原CyberWaifu的基础上，弃用了已弃用的 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) ，转而使用无头NTQQ项目[Lagrange](https://github.com/LagrangeDev/Lagrange.Core)进行QQ机器人的部署。

此外，该项目为原LLM内置了Agent助理用于调用工具，构建了Tools类用于存放工具，并且添加了自动图片搜索功能（待优化），并简化了表情包的使用。
请注意，此版本暂不支持Claude与TTS。



### 功能

✅ 预定义的思考链：使 AI 可以进行一定的逻辑思考，进行决策。例如在文本中添加 Emoji、发送表情包等等。

✅ 记忆数据库：自动总结对话内容并导入记忆数据库，根据用户的提问引入上下文，从而实现长时记忆。同时支持批量导入记忆，使人设更丰富、真实和可控。

✅ 现实感知：AI 可以感知现实的时间并模拟自己的状态和行为，例如晚上会在睡觉、用户隔很久回复会有相应反馈（这部分表现暂时不稳定）。

✅ 联网搜索：根据用户的信息，自主构造搜索决策，并引入上下文。

✅ QQ 机器人部署

✅ QQ 表情支持

✅ 人设模板、自定义人设

✅ 网络图片爬虫

⬜ edge-tts, azure 语音服务支持

⬜ vits, emotion-vits 支持

⬜ bark 支持

⬜ AI 绘图支持，将绘图引入思考链，使 AI 可以生成图片，例如 AI 自拍

### 安装💻

Python 版本：3.10.10

使用 conda:
```powershell
git clone https://github.com/Syan-Lin/CyberWaifu
cd CyberWaifu
conda create --name CyberWaifu python=3.10.10
conda activate CyberWaifu
pip install -r requirements.txt
```

#### QQ 机器人部署
运行Lagrange.Core.Test中的‘Program.cs’，第一次使用时注意先进行WTLogin生成登录凭证，再进行NTLogin。

详情参照Lagrange.Core原项目地址与文档：

Lagrange项目地址：<a href = “https://github.com/LagrangeDev/Lagrange.Core”>https://github.com/LagrangeDev/Lagrange.Core

Lagrange项目文档：<a href = "https://github.com/LagrangeDev/Lagrange.Core/blob/master/README_zh.md">https://github.com/LagrangeDev/Lagrange.Core/blob/master/README_zh.md



### 配置✏️

按照 `template.ini` 进行配置，配置完成后改名为 `config.ini`

#### 大语言模型配置

- OpenAI：需要配置 `openai_key`与代理服务器地址`base_url`，这部分网上有很多教程，就不赘述了



```json5
// 本项目针对私聊场景设计，目前不支持群组
{
    // 需要处理的 QQ 私聊信息，为空处理所有
    "user_id_list": [
        1234567,
        7654321
    ]
}
```

#### 人设 Prompt 配置
根据 `presets/charactor/模板.txt` 进行编写，将编写好的人设 Prompt 丢到 `presets/charactor` 目录下即可，随后在 `config.ini` 配置文件中的 `charactor` 字段填写文件名（不包含后缀名）

记忆设定同样是丢到 `presets/charactor` 目录下，多段记忆用空行分开，并在配置文件中填写 `memory` 字段

#### 联网搜索配置
在 [Google Serper](https://serper.dev/) 中注册并创建一个 API key，在 `config.ini` 中配置并开启即可。Google Serper 可以免费使用 1000 次调用，实测可以使用很久。

由于上下文长度的限制，目前搜索引入的内容并不多，只能获取简单的事实信息。

### 使用🎉
首先运行main.py，显示等待Socket连接成功后，再运行Lagarange

```powershell
conda activate CyberWaifu
python main.py
```
