using HandTracking.Models;

namespace HandTracking.Parser
{
    public interface IHandTrackingDataParser
    {
        Hand Parse(string coordenates);
    }
}