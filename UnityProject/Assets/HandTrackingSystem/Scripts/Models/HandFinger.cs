using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace HandTracking.Models
{
    public class HandFinger
    {
        public HandFinger(HandJoint wrist, HandJoint joint0, HandJoint joint1, HandJoint joint2, HandJoint joint3)
        {
            Wrist = wrist;
            Joint0 = joint0;
            Joint1 = joint1;
            Joint2 = joint2;
            Joint3 = joint3;
        }

        public HandJoint Wrist { get; }
        public HandJoint Joint0 { get; }
        public HandJoint Joint1 { get; }
        public HandJoint Joint2 { get; }
        public HandJoint Joint3 { get; }

        public override string ToString()
        {
            return string.Format("[{0}; {1}; {2}; {3}; {4}]",
                 Wrist.ToString(),
                 Joint0.ToString(),
                 Joint1.ToString(),
                 Joint2.ToString(),
                 Joint3.ToString());
        }
    }
}
