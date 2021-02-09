using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace HandTracking.Models
{
    /// <summary>
    ///     Finger representation with 5 joints (wrist and 4 joints).
    /// </summary>
    public class HandFinger
    {
        /// <summary>
        ///     Default constructor
        /// </summary>
        /// <param name="wrist">Wrist joints</param>
        /// <param name="joint0">First joints of finger</param>
        /// <param name="joint1">Second joints of finger</param>
        /// <param name="joint2">Third joints of finger</param>
        /// <param name="tip">Fingertip</param>
        public HandFinger(HandJoint wrist, HandJoint joint0, HandJoint joint1, HandJoint joint2, HandJoint tip)
        {
            Wrist = wrist;
            Joint0 = joint0;
            Joint1 = joint1;
            Joint2 = joint2;
            Tip = tip;
        }

        public HandJoint Wrist { get; }

        public HandJoint Joint0 { get; }

        public HandJoint Joint1 { get; }

        public HandJoint Joint2 { get; }
        
        public HandJoint Tip { get; }

        public override string ToString()
        {
            return string.Format("[{0}; {1}; {2}; {3}; {4}]",
                 Wrist.ToString(),
                 Joint0.ToString(),
                 Joint1.ToString(),
                 Joint2.ToString(),
                 Tip.ToString());
        }
    }
}
