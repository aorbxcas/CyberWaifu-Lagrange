using Lagrange.Core.Common;
using Lagrange.Core.Common.Interface;
using Lagrange.Core.Common.Interface.Api;
using Lagrange.Core.Internal.Event.System;
using Lagrange.Core.Message;
using Lagrange.Core.Message.Entity;
using Lagrange.Core.Utility.Extension;
using Lagrange.Core.Test.qqBot;
using Lagrange.Core.Test.CqCode;
using Client;
using System.Configuration;

namespace Lagrange.Core.Test.Tests;

// ReSharper disable once InconsistentNaming
public class NTLoginTest
{

    public async Task LoginByPassword()
    {
        string host = ConfigurationManager.AppSettings["SocketHost"];
        int port = int.Parse(ConfigurationManager.AppSettings["SocketPort"]);
        uint QQUid = uint.Parse(ConfigurationManager.AppSettings["QQUid"]);
        string QQPassword = ConfigurationManager.AppSettings["QQPassword"];
        //Console.WriteLine("请输入您的QQ号码：");
        //string input = Console.ReadLine();
        //QQUid = uint.Parse(input);
        //Console.WriteLine("请输入您的QQ密码：");
        //input = Console.ReadLine();
        //QQPassword = input;
        var deviceInfo = WtLoginTest.GetDeviceInfo();
        var keyStore = WtLoginTest.LoadKeystore() ?? new BotKeystore(QQUid,QQPassword);
        SocketBot socketBot = new SocketBot(host,port);


        if (keyStore == null)
        {
            Console.WriteLine("Please login by QrCode first");
            return;
        }

        var bot = BotFactory.Create(new BotConfig() 
        {
            UseIPv6Network = false,
            GetOptimumServer = true,
            AutoReconnect = true,
            Protocol = Protocols.Linux
        }, deviceInfo, keyStore);

        socketBot.MessageReceived += OnMessageReceive;

        bot.Invoker.OnBotLogEvent += (_, @event) =>

        {
            Utility.Console.ChangeColorByTitle(@event.Level);
            Console.WriteLine(@event.ToString());
        };
        
        bot.Invoker.OnBotOnlineEvent += (_, @event) =>
        {
            Console.WriteLine(@event.ToString());
            WtLoginTest.SaveKeystore(bot.UpdateKeystore());
        };
        
        bot.Invoker.OnBotCaptchaEvent += (_, @event) =>
        {
            Console.WriteLine(@event.ToString());
            var captcha = Console.ReadLine();
            var randStr = Console.ReadLine();
            if (captcha != null && randStr != null) bot.SubmitCaptcha(captcha, randStr);
        };
        
        bot.Invoker.OnGroupInvitationReceived += (_, @event) =>
        {
            Console.WriteLine(@event.ToString());

        };
        bot.Invoker.OnGroupMessageReceived += (_, @event) =>
        {

            if (@event.Chain.GetEntity<MentionEntity>() == null) return;
            if (@event.Chain.GetEntity<MentionEntity>().Uin == bot.BotUin)
            {
                var messageText = @event.Chain.GetEntity<TextEntity>();
                uint targetUin = (uint)@event.Chain.GroupUin;
                Console.WriteLine("准备向py发送消息："+ messageText.Text);
                if (messageText.Text == " ") return;
                socketBot.SendMsgToPy(messageText.Text);
                socketBot.ReceiveMsgFromPy(targetUin, true);
            }

        };
        bot.Invoker.OnFriendMessageReceived += (_, @event) =>
        {
            var messageText = @event.Chain.GetEntity<TextEntity>();
            uint targetUin = @event.Chain.FriendInfo.Uin;

            if (messageText == null) return;
            socketBot.SendMsgToPy(messageText.Text);
            socketBot.ReceiveMsgFromPy(targetUin,false);
            //var myChain = MessageBuilder.Friend(515056601).Text(receiveMessage);
            //bot.SendMessage(myChain.Build());
        };
        void OnMessageReceive(string message,uint targetUin,bool isGroupMsg)
        {
            Console.WriteLine("targetUid值为："+targetUin);

            Console.WriteLine("接收到消息： " + message);

            string messageText = CQCode.DeleteCQCode(message);
            var messageChain = isGroupMsg ? MessageBuilder.Group(targetUin) : MessageBuilder.Friend(targetUin);

            if (message != "")
            {
                messageChain.Text(messageText);
            }

            List<Dictionary<string, string>> CqDicList = CQCode.StrToCqCode(message);
            if (CqDicList != null)
            {
                foreach (var cqDict in CqDicList)
                {
                    if (cqDict != null)
                    {
                        switch (cqDict["CQ"])
                        {
                            case "at":
                                Console.WriteLine("at");
                                break;
                            case "face":
                                Console.WriteLine("face");
                                messageChain.Face(ushort.Parse(cqDict["id"]));
                                break;
                            case "image":
                                Console.WriteLine("image");
                                messageChain.Image(cqDict["file"]);
                                break;
                            case "record":
                                Console.WriteLine("record");
                                break;
                            case "rps":
                                Console.WriteLine("rps");
                                break;
                            case "dice":
                                Console.WriteLine("dice");
                                break;
                        }
                    }
                }
            }
            bot.SendMessage(messageChain.Build());

        }

        await bot.LoginByPassword();

        var friendChain = MessageBuilder.Friend(515056601)
                .Text("This is the friend message sent by Lagrange.Core");
        // await bot.SendMessage(friendChain.Build());

        await Task.Delay(1000);
    }


}