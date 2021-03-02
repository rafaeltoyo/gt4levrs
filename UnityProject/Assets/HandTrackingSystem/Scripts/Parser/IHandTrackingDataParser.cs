using HandTracking.Models;

namespace HandTracking.Parser
{
    public interface IHandTrackingDataParser
    {
        Hands Parse(string coordenates);
    }
}