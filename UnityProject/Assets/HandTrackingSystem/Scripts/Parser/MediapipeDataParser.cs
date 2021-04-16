using UnityEngine;

using System;
using System.Globalization;
using System.Collections.Generic;

using HandTracking.Models;

namespace HandTracking.Parser
{
    public class MediapipeDataParser : IHandTrackingDataParser
    {
        private const string ERROR_EMPTY_DATA = "Empty data!";
        private const string ERROR_INVALID_JSON = "Problem while parsing json from raw data!";
        private const string ERROR_EMPTY_HAND_DATA = "Empty hands data!";

        private Vector3 reference;

        /// <summary>
        ///     This method convert the received string into json and parse to Hands object
        /// </summary>
        /// <param name="rawData">Received string</param>
        /// <returns>Hands</returns>
        public HandTrackingData Parse(string rawData)
        {
            if (String.IsNullOrWhiteSpace(rawData))
                throw new Exception(ERROR_EMPTY_DATA);

            rawData = rawData.Trim();

            if (rawData.StartsWith("error"))
                throw new Exception(rawData);

            MediapipeJson json = JsonUtility.FromJson<MediapipeJson>(rawData);

            if (json == null)
                throw new Exception(ERROR_INVALID_JSON);

            if (json.hand_results == null || (json.hand_results.lhand == null && json.hand_results.rhand == null))
                throw new Exception(ERROR_EMPTY_HAND_DATA);

            ParsePose(json.body_results);

            return ParseTwoHands(json.hand_results);
        }

        /// <summary>
        ///     Parse the position of user from json data
        /// </summary>
        /// <param name="mpPose"></param>
        private void ParsePose(MediapipePoseJson mpPose)
        {
            if (mpPose == null ||
                mpPose.joints == null ||
                mpPose.joints.Count <= 0)
            {
                if (this.reference == null)
                    throw new Exception("Handtracking system needs a initial reference.");
                return;
            }

            MediapipeJointJson leftShoulder = mpPose.joints[(ushort)MediapipePose.LEFT_SHOULDER];
            MediapipeJointJson rightShoulder = mpPose.joints[(ushort)MediapipePose.RIGHT_SHOULDER];

            this.reference = new Vector3(
                (float) Math.Abs(leftShoulder.x - rightShoulder.x),
                (float) Math.Abs(leftShoulder.y - rightShoulder.y),
                (float) Math.Abs(leftShoulder.z - rightShoulder.z));
        }

        /// <summary>
        ///     Parse the hands from json data
        /// </summary>
        /// <param name="mpHands"></param>
        /// <returns></returns>
        private HandTrackingData ParseTwoHands(MediapipeTwoHandsJson mpHands)
        {
            return new HandTrackingData(ParseHand(mpHands.lhand), ParseHand(mpHands.rhand), this.reference);
        }

        /// <summary>
        ///     Parse a hand from data string
        /// </summary>
        /// <param name="mpHands">Parsed json</param>
        /// <returns>Parsed Hand</returns>
        private Hand ParseHand(MediapipeHandJson mpHands)
        {
            if (mpHands == null || !(mpHands.joints is object))
                throw new Exception(ERROR_EMPTY_HAND_DATA);

            List<HandJoint> joints = new List<HandJoint>();

            foreach (MediapipeJointJson mpJoint in mpHands.joints)
            {
                HandJoint joint = ParseJoint(mpJoint);
                if (joint != null)
                    joints.Add(joint);
            }
            if (joints.Count > 0)
            {
                return new Hand(
                    joints[(ushort)MediapipeJoints.WRIST],
                    ParseFinger(MediapipeFingers.THUMB, joints),
                    ParseFinger(MediapipeFingers.INDEX, joints),
                    ParseFinger(MediapipeFingers.MIDDLE, joints),
                    ParseFinger(MediapipeFingers.RING, joints),
                    ParseFinger(MediapipeFingers.PINKY, joints)
                );
            }
            else
            {
                return null;
            }
        }

        /// <summary>
        ///     Parse a joint from data string
        /// </summary>
        /// <param name="mpJoint">Parsed json with name, x, y and z</param>
        /// <returns>Parsed joint</returns>
        private HandJoint ParseJoint(MediapipeJointJson mpJoint)
        {
            if (mpJoint.name.Length > 0)
            {
                return new HandJoint(mpJoint.name)
                    .Update(
                        (float) (mpJoint.x * 10),
                        (float) (mpJoint.y * 10 * -1),
                        (float) (mpJoint.z * 10)
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
                joints[(ushort)MediapipeJoints.WRIST],
                joints[(ushort)finger],
                joints[(ushort)finger + 1],
                joints[(ushort)finger + 2],
                joints[(ushort)finger + 3]
            );
        }

        /// <summary>
        ///     Convert a string into float value if its possible
        /// </summary>
        /// <param name="value">String of number</param>
        /// <returns>Number</returns>
        private double ParseFloat(string value)
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
            public double x;
            public double y;
            public double z;
        }

        enum MediapipePose : ushort
        {
            LEFT_SHOULDER = 11,
            RIGHT_SHOULDER = 12
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
