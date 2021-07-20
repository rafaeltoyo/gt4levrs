using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;

namespace HandTracking.Models
{
    public class HandBone
    {
        public static readonly Dictionary<HandBoneIndex, HandBone> Bones = new Dictionary<HandBoneIndex, HandBone>()
        {
            { HandBoneIndex.THUMB_METACARPAL, new HandBone(HandJointIndex.WRIST, HandJointIndex.THUMB_CMC) },
            { HandBoneIndex.THUMB_PROXIMAL, new HandBone(HandJointIndex.THUMB_CMC, HandJointIndex.THUMB_MCP) },
            { HandBoneIndex.THUMB_MIDDLE, new HandBone(HandJointIndex.THUMB_MCP, HandJointIndex.THUMB_IP) },
            { HandBoneIndex.THUMB_DISTAL, new HandBone(HandJointIndex.THUMB_IP, HandJointIndex.THUMB_TIP) },

            //{ HandBoneIndex.INDEX_METACARPAL, new HandBone(HandJointIndex.WRIST, HandJointIndex.INDEX_FINGER_MCP) },
            { HandBoneIndex.INDEX_PROXIMAL, new HandBone(HandJointIndex.INDEX_FINGER_MCP, HandJointIndex.INDEX_FINGER_PIP) },
            { HandBoneIndex.INDEX_MIDDLE, new HandBone(HandJointIndex.INDEX_FINGER_PIP, HandJointIndex.INDEX_FINGER_DIP) },
            { HandBoneIndex.INDEX_DISTAL, new HandBone(HandJointIndex.INDEX_FINGER_DIP, HandJointIndex.INDEX_FINGER_TIP) },

            //{ HandBoneIndex.MIDDLE_METACARPAL, new HandBone(HandJointIndex.WRIST, HandJointIndex.MIDDLE_FINGER_MCP) },
            { HandBoneIndex.MIDDLE_PROXIMAL, new HandBone(HandJointIndex.MIDDLE_FINGER_MCP, HandJointIndex.MIDDLE_FINGER_PIP) },
            { HandBoneIndex.MIDDLE_MIDDLE, new HandBone(HandJointIndex.MIDDLE_FINGER_PIP, HandJointIndex.MIDDLE_FINGER_DIP) },
            { HandBoneIndex.MIDDLE_DISTAL, new HandBone(HandJointIndex.MIDDLE_FINGER_DIP, HandJointIndex.MIDDLE_FINGER_TIP) },

            //{ HandBoneIndex.RING_METACARPAL, new HandBone(HandJointIndex.WRIST, HandJointIndex.RING_FINGER_MCP) },
            { HandBoneIndex.RING_PROXIMAL, new HandBone(HandJointIndex.RING_FINGER_MCP, HandJointIndex.RING_FINGER_PIP) },
            { HandBoneIndex.RING_MIDDLE, new HandBone(HandJointIndex.RING_FINGER_PIP, HandJointIndex.RING_FINGER_DIP) },
            { HandBoneIndex.RING_DISTAL, new HandBone(HandJointIndex.RING_FINGER_DIP, HandJointIndex.RING_FINGER_TIP) },

            { HandBoneIndex.PINKY_METACARPAL, new HandBone(HandJointIndex.WRIST, HandJointIndex.PINKY_MCP) },
            { HandBoneIndex.PINKY_PROXIMAL, new HandBone(HandJointIndex.PINKY_MCP, HandJointIndex.PINKY_PIP) },
            { HandBoneIndex.PINKY_MIDDLE, new HandBone(HandJointIndex.PINKY_PIP, HandJointIndex.PINKY_DIP) },
            { HandBoneIndex.PINKY_DISTAL, new HandBone(HandJointIndex.PINKY_DIP, HandJointIndex.PINKY_TIP) },

            { HandBoneIndex.THUMB_TO_INDEX, new HandBone(HandJointIndex.THUMB_CMC, HandJointIndex.INDEX_FINGER_MCP) },
            { HandBoneIndex.INDEX_TO_MIDDLE, new HandBone(HandJointIndex.INDEX_FINGER_MCP, HandJointIndex.MIDDLE_FINGER_MCP) },
            { HandBoneIndex.MIDDLE_TO_RING, new HandBone(HandJointIndex.MIDDLE_FINGER_MCP, HandJointIndex.RING_FINGER_MCP) },
            { HandBoneIndex.RING_TO_PINKY, new HandBone(HandJointIndex.RING_FINGER_MCP, HandJointIndex.PINKY_MCP) },
        };
        private HandBone(HandJointIndex joint0, HandJointIndex joint1)
        {
            Joint0 = joint0;
            Joint1 = joint1;
        }

        public HandJointIndex Joint0 { get; }
        public HandJointIndex Joint1 { get; }
    }

    public enum HandBoneIndex : ushort
    {
        THUMB_METACARPAL, THUMB_PROXIMAL, THUMB_MIDDLE, THUMB_DISTAL,
        INDEX_METACARPAL, INDEX_PROXIMAL, INDEX_MIDDLE, INDEX_DISTAL,
        MIDDLE_METACARPAL, MIDDLE_PROXIMAL, MIDDLE_MIDDLE, MIDDLE_DISTAL,
        RING_METACARPAL, RING_PROXIMAL, RING_MIDDLE, RING_DISTAL,
        PINKY_METACARPAL, PINKY_PROXIMAL, PINKY_MIDDLE, PINKY_DISTAL,
        THUMB_TO_INDEX, INDEX_TO_MIDDLE, MIDDLE_TO_RING, RING_TO_PINKY
    }

    public enum HandJointIndex : ushort
    {
        WRIST,
        THUMB_CMC, THUMB_MCP, THUMB_IP, THUMB_TIP,
        INDEX_FINGER_MCP, INDEX_FINGER_PIP, INDEX_FINGER_DIP, INDEX_FINGER_TIP,
        MIDDLE_FINGER_MCP, MIDDLE_FINGER_PIP, MIDDLE_FINGER_DIP, MIDDLE_FINGER_TIP,
        RING_FINGER_MCP, RING_FINGER_PIP, RING_FINGER_DIP, RING_FINGER_TIP,
        PINKY_MCP, PINKY_PIP, PINKY_DIP, PINKY_TIP
    }
}