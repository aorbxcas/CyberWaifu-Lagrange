using System.Text.Json.Serialization;

namespace Lagrange.OneBot.Core.Entity.Action;

[Serializable]
public class OneBotGetMessage
{
    [JsonPropertyName("message_id")] public int MessageId { get; set; }
}