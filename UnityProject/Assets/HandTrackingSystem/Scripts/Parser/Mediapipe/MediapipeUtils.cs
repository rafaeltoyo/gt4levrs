using System;
using System.Globalization;

namespace HandTracking.Parser.Mediapipe
{
    /// <summary>
    /// Utilities method
    /// </summary>
    class MediapipeUtils
    {
        /// <summary>
        /// Convert a string into double value if its possible
        /// </summary>
        /// <param name="value">Payload</param>
        /// <returns>Double value parsed</returns>
        public static double ParseDouble(string value)
        {
            try
            {
                return double.Parse(value, CultureInfo.InvariantCulture.NumberFormat);
            }
            catch (Exception)
            {
                return 0;
            }
        }

        /// <summary>
        /// Convert a string into float value if its possible
        /// </summary>
        /// <param name="value">Payload</param>
        /// <returns>Float value parsed</returns>
        public static float ParseFloat(string value)
        {
            try
            {
                return float.Parse(value, CultureInfo.InvariantCulture.NumberFormat);
            }
            catch (Exception)
            {
                return 0;
            }
        }
    }

    /// <summary>
    /// Errors messages
    /// </summary>
    class MediapipeErrors
    {
        public const string ERROR_EMPTY_DATA = "Empty data!";
        public const string ERROR_INVALID_JSON = "Problem while parsing json from raw data!";
        public const string ERROR_EMPTY_HAND_DATA = "Empty hands data!";
    }

    enum MediapipePose : ushort
    {
        LEFT_SHOULDER = 11,
        RIGHT_SHOULDER = 12,
        LEFT_WRIST = 15,
        RIGHT_WRIST = 16
    }

    enum MediapipeFingers : ushort
    {
        THUMB = MediapipeJoints.THUMB_CMC,
        INDEX = MediapipeJoints.INDEX_FINGER_MCP,
        MIDDLE = MediapipeJoints.MIDDLE_FINGER_MCP,
        RING = MediapipeJoints.RING_FINGER_MCP,
        PINKY = MediapipeJoints.PINKY_MCP
    }

    enum MediapipeJoints
    {
        WRIST,
        THUMB_CMC, THUMB_MCP, THUMB_IP, THUMB_TIP,
        INDEX_FINGER_MCP, INDEX_FINGER_PIP, INDEX_FINGER_DIP, INDEX_FINGER_TIP,
        MIDDLE_FINGER_MCP, MIDDLE_FINGER_PIP, MIDDLE_FINGER_DIP, MIDDLE_FINGER_TIP,
        RING_FINGER_MCP, RING_FINGER_PIP, RING_FINGER_DIP, RING_FINGER_TIP,
        PINKY_MCP, PINKY_PIP, PINKY_DIP, PINKY_TIP
    }
}