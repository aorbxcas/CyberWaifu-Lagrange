using ProtoBuf;

// ReSharper disable InconsistentNaming
#pragma warning disable CS8618

namespace Lagrange.Core.Internal.Packets.Action.HttpConn;

[ProtoContract]
internal class HttpConn0x6ff_501
{
    [ProtoMember(0x501)] public HttpConn HttpConn { get; set; }
}