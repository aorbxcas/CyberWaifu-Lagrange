using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Text.RegularExpressions;

namespace Lagrange.Core.Test.CqCode;

public static class CQCode
{
    //提取str中的CQCode
    public static List<Dictionary<string, string>> StrToCqCode(string message)
    {
        if (message.Contains("[CQ") == false)
        {
            return null;
        }
        List<Dictionary<string, string>> cqCodeList = new List<Dictionary<string, string>>();
        while (message.Contains("[CQ") != false)
        {
            string currentMessage = message;
            int cqLength = currentMessage.IndexOf(']') - currentMessage.IndexOf('[');
            currentMessage = currentMessage.Substring(currentMessage.IndexOf('[') + 1, cqLength - 1);
            //message = message.Replace("[", "");
            //message = message.Replace("]", "");
            string[] messagesList;
            Dictionary<string, string> messagesDict = new Dictionary<string, string>();
            messagesList = currentMessage.Split(',');
            //循环使string数组转换为dictionary
            if (messagesList == null) continue;
            for (int i = 0; i < messagesList.Length; i++)
            {
                string[] ddata;
                if (messagesList[i].Contains("CQ"))
                {
                    ddata = messagesList[i].Split(':');
                    messagesDict.Add(ddata[0], ddata[1]);
                    continue;
                }
                ddata = messagesList[i].Split('=');
                messagesDict.Add(ddata[0], ddata[1]);
            }
            message = message.Remove(message.IndexOf('[') , cqLength + 1);
            Console.WriteLine("删除后的字符串："+message);
            cqCodeList.Add(messagesDict);
        }
        return cqCodeList;
        //if (message.Contains("[CQ") == false)
        //{
        //    return null;
        //}
        //int cqLength = message.IndexOf(']') - message.IndexOf('[');
        //message = message.Substring(message.IndexOf('[') + 1, cqLength - 1);
        ////message = message.Replace("[", "");
        ////message = message.Replace("]", "");
        //string[] messagesList;
        //Dictionary<string, string> messagesDict = new Dictionary<string, string>();
        //messagesList = message.Split(',');
        ////循环使string数组转换为dictionary
        //if (messagesList == null) return null;
        //for (int i = 0; i < messagesList.Length; i++)
        //{
        //    string[] ddata;
        //    if (messagesList[i].Contains("CQ")){
        //        ddata = messagesList[i].Split(':');
        //        messagesDict.Add(ddata[0], ddata[1]);
        //        continue;
        //    }
        //    ddata = messagesList[i].Split('=');
        //    messagesDict.Add(ddata[0], ddata[1]);
        //}
        //return messagesDict;
    }

    public static string DeleteCQCode(string message)
    {
        string pattern = @"\[[^()]*\]";
        string result = Regex.Replace(message, pattern, "");
        return result;

    }

}



//enum CQType
//{
//Text,
//At,
//Image,
//Face,
//Reply,
//Record,
//Xml,
//Json,
//App,
//Plain,
//Mention,
//MentionAll,
//MentionHere,
//Share,
//Forward,
//Poke,
//Dice,
//Shake,
//Rss,
//Music,
//Video,
//Location
//}