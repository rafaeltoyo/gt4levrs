using UnityEngine;

using System;
using System.Globalization;
using System.Collections.Generic;
using System.Text.RegularExpressions;

using HandTracking.Models;

namespace HandTracking.Parser
{
    public class MediapipeDataParser : IHandTrackingDataParser
    {

        private List<HandJoint> _joints = new List<HandJoint>();

        /// <summary>
        ///     This method convert the received string into json and parse to Hands object
        /// </summary>
        /// <param name="rawData">Received string</param>
        /// <returns>Hands</returns>
        public Hands Parse(string rawData)
        {
            if (rawData != null)
            {
                rawData = rawData.Trim();
            }

            if (rawData.Length <= 0 || rawData.StartsWith("error"))
            {
                Debug.Log("Error!");
                return null;
            }

            MediapipeJson json = JsonUtility.FromJson<MediapipeJson>(rawData);

            return ParseHands(json);
        }

        /// <summary>
        ///     Parse the hands from raw data string
        /// </summary>
        /// <param name="json"></param>
        /// <returns></returns>
        private Hands ParseHands(MediapipeJson json)
        {
            if (json == null || json.hand_results == null)
                return null;
            return new Hands(ParseHand(json.hand_results.lhand), ParseHand(json.hand_results.rhand));
        }

        /// <summary>
        ///     Parse a hand from data string
        /// </summary>
        /// <param name="coordenates">Parsed json</param>
        /// <returns>Parsed Hand</returns>
        private Hand ParseHand(MediapipeHandJson json)
        {
            if (json == null || ! (json.joints is object))
                return null;

            List<HandJoint> joints = new List<HandJoint>();
            
            foreach (MediapipeJointJson joint in json.joints)
            {
                HandJoint hj = ParseJoint(joint);
                if (hj != null)
                    joints.Add(hj);
            }
            if (joints.Count > 0) {
                return new Hand(
                    joints[(ushort) MediapipeJoints.WRIST],
                    ParseFinger(MediapipeFingers.THUMB, joints),
                    ParseFinger(MediapipeFingers.INDEX, joints),
                    ParseFinger(MediapipeFingers.MIDDLE, joints),
                    ParseFinger(MediapipeFingers.RING, joints),
                    ParseFinger(MediapipeFingers.PINKY, joints)
                );
            } else {
                return null;
            }
        }

        /// <summary>
        ///     Parse a joint from data string
        /// </summary>
        /// <param name="coordenates">Parsed json with name, x, y and z</param>
        /// <returns>Parsed joint</returns>
        private HandJoint ParseJoint(MediapipeJointJson json)
        {
            if (json.name.Length > 0)
            {
                return new HandJoint(json.name)
                    .Update(
                        json.x * 3,
                        json.y * 3 * -1,
                        json.z * 3
                    );
            }
            return null;
        }

        /// <summary>
        ///     Parse a finger from its name and hand's joints
        /// </summary>
        /// <param name="finger">Finger to parse</param>
        /// <param name="joints">All joints</param>
        /// <returns>Parsed finger</returns>
        private HandFinger ParseFinger(MediapipeFingers finger, List<HandJoint> joints)
        {
            return new HandFinger(
                joints[(ushort) MediapipeJoints.WRIST],
                joints[(ushort) finger],
                joints[(ushort) finger + 1],
                joints[(ushort) finger + 2],
                joints[(ushort) finger + 3]
            );
        }

        /// <summary>
        ///     Convert a string into float value if its possible
        /// </summary>
        /// <param name="v">String of number</param>
        /// <returns>Number</returns>
        private float ParseFloat(string v)
        {
            try
            {
                return float.Parse(v, CultureInfo.InvariantCulture.NumberFormat);
            }
            catch (Exception)
            {
                return 0;
            }
        }

        [Serializable]
        class MediapipeJson
        {
            public MediapipePoseJson body_results;
            public MediapipeTwoHandsJson hand_results;
        }

        [Serializable]
        class MediapipePoseJson
        {
            public List<MediapipeJointJson> joints;
        }

        [Serializable]
        class MediapipeTwoHandsJson
        {
            public MediapipeHandJson lhand;
            public MediapipeHandJson rhand;
        }

        [Serializable]
        class MediapipeHandJson
        {
            public string index;
            public double score;
            public string label;
            public List<MediapipeJointJson> joints;
        }

        [Serializable]
        class MediapipeJointJson
        {
            public string name;
            public float x;
            public float y;
            public float z;
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
}
