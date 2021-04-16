using HandTracking.Models;

namespace HandTracking.Parser
{
    public interface IHandTrackingDataParser
    {
        HandTrackingData Parse(string coordenates);
    }
}