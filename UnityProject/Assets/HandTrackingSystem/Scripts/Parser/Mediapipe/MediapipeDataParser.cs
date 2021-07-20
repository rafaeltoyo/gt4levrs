using UnityEngine;

using System;
using System.Collections.Generic;

using HandTracking.Models;

namespace HandTracking.Parser.Mediapipe
{
    public class MediapipeDataParser : IHandTrackingDataParser
    {

        private Vector3 reference = new Vector3(0, 0, 0);
        private Vector3 leftWrist = new Vector3(0, 0, 0);
        private Vector3 rightWrist = new Vector3(0, 0, 0);
        private const int SCALE = 5;

        /// <summary>
        ///     This method convert the received string into json and parse to Hands object
        /// </summary>
        /// <param name="rawData">Received string</param>
        /// <returns>Hands</returns>
        public HandTrackingData Parse(string rawData)
        {
            if (String.IsNullOrWhiteSpace(rawData))
                throw new Exception(MediapipeErrors.ERROR_EMPTY_DATA);

            rawData = rawData.Trim();

            if (rawData.StartsWith("error"))
                throw new Exception(rawData);

            MediapipeJson json = JsonUtility.FromJson<MediapipeJson>(rawData);

            if (json == null)
                throw new Exception(MediapipeErrors.ERROR_INVALID_JSON);

            if (json.hand_results == null || (json.hand_results.lhand == null && json.hand_results.rhand == null))
                throw new Exception(MediapipeErrors.ERROR_EMPTY_HAND_DATA);

            ParsePose(json.body_results);

            return ParseTwoHands(json.hand_results);
        }

        /// <summary>
        ///     Parse the position of user from json data
        /// </summary>
        /// <param name="mpPose"></param>
        private void ParsePose(List<MediapipeJointJson> mpPose)
        {
            if (mpPose == null ||
                mpPose.Count <= 0)
            {
                if (this.reference == null)
                    throw new Exception("Handtracking system needs a initial reference.");
                return;
            }

            MediapipeJointJson mpLeftWrist = mpPose[(ushort)MediapipePose.LEFT_WRIST];
            MediapipeJointJson mpRightWrist = mpPose[(ushort)MediapipePose.RIGHT_WRIST];

            this.leftWrist = this.MediapipeJointToVector3(mpLeftWrist);
            this.rightWrist = this.MediapipeJointToVector3(mpRightWrist);

            MediapipeJointJson mpLeftShoulder = mpPose[(ushort)MediapipePose.LEFT_SHOULDER];
            MediapipeJointJson mpRightShoulder = mpPose[(ushort)MediapipePose.RIGHT_SHOULDER];

            Vector3 leftShoulder = this.MediapipeJointToVector3(mpLeftShoulder);
            Vector3 rightShoulder = this.MediapipeJointToVector3(mpRightShoulder);

            if (leftShoulder.Equals(Vector3.zero))
                return;
            if (rightShoulder.Equals(Vector3.zero))
                return;

            this.reference = Vector3.Lerp(leftShoulder, rightShoulder, 0.5f);
            this.reference.z = 0f;
        }

        private Vector3 MediapipeJointToVector3(MediapipeJointJson json)
        {
            return new Vector3((float)json.x, (float)json.y, (float)json.z);
        }

        private Vector3 UnityCoordenateAdjustment(Vector3 pos)
        {
            pos *= SCALE;
            pos.x *= -1;
            pos.y *= -1;
            return pos;
        }

        /// <summary>
        ///     Parse the hands from json data
        /// </summary>
        /// <param name="mpHands"></param>
        /// <returns></returns>
        private HandTrackingData ParseTwoHands(MediapipeTwoHandsJson mpHands)
        {
            Hand leftHand = ParseHand(mpHands.lhand, true);
            Hand rightHand = ParseHand(mpHands.rhand, false);
            /*
            if (leftHand != null)
                leftHand.SetWristPosition(this.leftWrist);

            if (rightHand != null)
                rightHand.SetWristPosition(this.rightWrist);
            */
            return new HandTrackingData(leftHand, rightHand);
        }

        /// <summary>
        ///     Parse a hand from data string
        /// </summary>
        /// <param name="mpHands">Parsed json</param>
        /// <returns>Parsed Hand</returns>
        private Hand ParseHand(MediapipeHandJson mpHands, bool isLeft)
        {
            if (mpHands == null || !(mpHands.joints is object))
                throw new Exception(MediapipeErrors.ERROR_EMPTY_HAND_DATA);

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
                    ParseFinger(MediapipeFingers.PINKY, joints),
                    isLeft
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
                Vector3 joint = this.MediapipeJointToVector3(mpJoint);
                return new HandJoint(mpJoint.name)
                    .Update(this.UnityCoordenateAdjustment(joint - this.reference));
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

        [Serializable]
        class MediapipeJson
        {
            public List<MediapipeJointJson> body_results;
            public MediapipeTwoHandsJson hand_results;
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
    }
}
