using System;
using System.Collections.Generic;
using System.Text;
using System.Net.Sockets;
using System.Net;
using System.Threading;

using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Lagrange.Core.Internal.Packets.Message;

namespace Client
{
    public class SocketBot
    {
        Socket tcpClient;
        public static ManualResetEvent allDone = new ManualResetEvent(false);
        private static ManualResetEvent receiveDone = new ManualResetEvent(false);
        private static ManualResetEvent connectDone = new ManualResetEvent(false);
        private static ManualResetEvent sendDone = new ManualResetEvent(false);
        private static String response = String.Empty;

        public string resp;
        public delegate void MessageReceivedHandler(string message,uint targetUid,bool isGroupMsg);
        public event MessageReceivedHandler MessageReceived;

        private uint currentTargetUin;
        private bool isCurrentGroup;

        
        public SocketBot(string url,int port)
        {
            tcpClient = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            tcpClient.BeginConnect(IPAddress.Parse(url), port, new AsyncCallback(ConnectCallback), tcpClient);
            connectDone.WaitOne();
        }
        public SocketBot()
        {
            tcpClient = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            tcpClient.BeginConnect(IPAddress.Parse("127.0.0.1"), 9999, new AsyncCallback(ConnectCallback), tcpClient);
            connectDone.WaitOne();
        }
        //建立tcp连接
        public void ConnectCallback(IAsyncResult asyncConnect)
        {
            try
            {
                Socket client = (Socket)asyncConnect.AsyncState;
                client.EndConnect(asyncConnect);
                Console.WriteLine("Socket 已连接至 {0}", client.RemoteEndPoint.ToString());
                connectDone.Set();

            }
            catch (Exception e)
            {
                Console.WriteLine(e.ToString());
            }
        }
        //发送信息
        public void SendMsgToPy(string msg)
        {
            byte[] byteData = Encoding.UTF8.GetBytes(msg);
            tcpClient.BeginSend(byteData,0,byteData.Length,0,new AsyncCallback(SendCallback), tcpClient);
        }
        private static void SendCallback(IAsyncResult ar) {
            try
            {
                Socket handler = (Socket)ar.AsyncState;
                int bytesSent = handler.EndSend(ar);
                //Console.WriteLine("已向服务端发送{0}个字节...", bytesSent);
                sendDone.Set();
            }
            catch (Exception e) { 
                Console.WriteLine(e.ToString()); 
            }
        }
        //接收信息
        public void ReceiveMsgFromPy(uint targetUin,bool isGroupMsg)
        {
            try
            {
                currentTargetUin = targetUin;
                isCurrentGroup = isGroupMsg;
                StateObject state = new StateObject();
                state.workSocket = tcpClient;
                Console.WriteLine("收到来自py的消息...消息内容为：");
                IAsyncResult result = tcpClient.BeginReceive(state.buffer, 0, StateObject.BufferSize, 0, new AsyncCallback(ReceiveCallback), state);
            }
            catch (Exception e) { 
                Console.WriteLine(e.ToString());    
            }
        }
        
        private void ReceiveCallback(IAsyncResult ar)
        {
            try
            {

                StateObject state = (StateObject)ar.AsyncState;
                Socket client = state.workSocket;
                int bytesRead = client.EndReceive(ar);
                if (bytesRead > 0)
                {
                    state.sb.Append(Encoding.UTF8.GetString(state.buffer, 0, bytesRead));
                    client.BeginReceive(state.buffer, 0, StateObject.BufferSize, 0, new AsyncCallback(ReceiveCallback), state);
                }
                if (state.sb.Length > 0)
                {
                    response = state.sb.ToString();
                    state.sb = new StringBuilder();
                    MessageReceived?.Invoke(response,currentTargetUin,isCurrentGroup);
                }
                receiveDone.Set();


            }
            catch (Exception e) {
                Console.WriteLine(e.ToString()); 
            }
        }
        //关闭连接
        public void SocketClose()
        {
            tcpClient.Shutdown(SocketShutdown.Both);
            tcpClient.Close();
        }


        //private void OnReceiveCompleted(object sender, SocketAsyncEventArgs e)
        //{

        //    if (e.SocketError == SocketError.Success)
        //    {
        //        Console.WriteLine("接收到数据，内容为:");
        //        Console.WriteLine(e.ToString());
        //        // 处理接收到的数据...
        //        // 可以继续调用ReceiveAsync进行下一次异步接收
        //    }
        //    else
        //    {
        //        Console.WriteLine("接收数据失败，请检查控制台...");
        //        // 处理错误情况...
        //    }
        //}
        //void SendMessageTopy(string message)
        //{

        //    byte[] data = Encoding.UTF8.GetBytes(message);
        //    while (true)
        //        udpClient.SendTo(data, serverPoint);
        //    Console.ReadKey();
        //}
    }

}