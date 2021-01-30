using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace HandTracking.Models
{
    public class Hand
    {
        public Hand(HandJoint wrist, HandFinger thumb, HandFinger index, HandFinger middle, HandFinger ring, HandFinger pinky)
        {
            Wrist = wrist;
            Trumb = thumb;
            Index = index;
            Middle = middle;
            Ring = ring;
            Pinky = pinky;
        }

        public HandJoint Wrist { get; }
        public HandFinger Trumb { get; }
        public HandFinger Index { get; }
        public HandFinger Middle { get; }
        public HandFinger Ring { get; }
        public HandFinger Pinky { get; }
    }
}
