using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace HandTracking.Models
{
    /// <summary>
    ///     Hand representation
    /// </summary>
    public class Hand
    {
        /// <summary>
        ///     Default constructor
        /// </summary>
        /// <param name="wrist">Wrist joint</param>
        /// <param name="thumb">Thumb finger</param>
        /// <param name="index">Index finger</param>
        /// <param name="middle">Middle finger</param>
        /// <param name="ring">Ring finger</param>
        /// <param name="pinky">Pinky finger</param>
        public Hand(HandJoint wrist, HandFinger thumb, HandFinger index, HandFinger middle, HandFinger ring, HandFinger pinky)
        {
            Wrist = wrist;
            Trumb = thumb;
            Index = index;
            Middle = middle;
            Ring = ring;
            Pinky = pinky;
        }

        /// <summary>
        ///     Get a sequence of joints <br/>
        /// <list type="number">
        ///     <item>wrist</item>
        ///     <item>thumb joint0</item><item>thumb joint1</item><item>thumb joint2</item><item>thumb joint3</item>
        ///     <item>index joint0</item><item>index joint1</item><item>index joint2</item><item>index joint3</item>
        ///     <item>middle joint0</item><item>middle joint1</item><item>middle joint2</item><item>middle joint3</item>
        ///     <item>ring joint0</item><item>ring joint1</item><item>ring joint2</item><item>ring joint3</item>
        ///     <item>pinky joint0</item><item>pinky joint1</item><item>pinky joint2</item><item>pinky joint3</item>
        /// </list>
        /// </summary>
        /// <returns></returns>
        public Vector3[] ToVector3Array()
        {
            Vector3[] joints = new Vector3[21];

            joints[0] = Wrist.Coordenates;

            joints[1] = Trumb.Joint0.Coordenates;
            joints[2] = Trumb.Joint1.Coordenates;
            joints[3] = Trumb.Joint2.Coordenates;
            joints[4] = Trumb.Tip.Coordenates;

            joints[5] = Index.Joint0.Coordenates;
            joints[6] = Index.Joint1.Coordenates;
            joints[7] = Index.Joint2.Coordenates;
            joints[8] = Index.Tip.Coordenates;

            joints[9] = Middle.Joint0.Coordenates;
            joints[10] = Middle.Joint1.Coordenates;
            joints[11] = Middle.Joint2.Coordenates;
            joints[12] = Middle.Tip.Coordenates;

            joints[13] = Ring.Joint0.Coordenates;
            joints[14] = Ring.Joint1.Coordenates;
            joints[15] = Ring.Joint2.Coordenates;
            joints[16] = Ring.Tip.Coordenates;

            joints[17] = Pinky.Joint0.Coordenates;
            joints[18] = Pinky.Joint1.Coordenates;
            joints[19] = Pinky.Joint2.Coordenates;
            joints[20] = Pinky.Tip.Coordenates;

            return joints;
        }

        public void ToBones()
        {
            Vector3[] bones = new Vector3[21];

            // ???
            bones[0] = (Trumb.Joint0.Coordenates - Wrist.Coordenates).normalized;
            // Thumb Metacarpal
            bones[1] = (Trumb.Joint1.Coordenates - Trumb.Joint0.Coordenates).normalized;
            // Thumb Proximal Phalanx
            bones[2] = (Trumb.Joint2.Coordenates - Trumb.Joint1.Coordenates).normalized;
            // Thumb Distal Phalanx
            bones[3] = (Trumb.Tip.Coordenates - Trumb.Joint2.Coordenates).normalized;

            // Index Metacarpal
            bones[0] = (Index.Joint0.Coordenates - Wrist.Coordenates).normalized;
            // Index Proximal Phalanx
            bones[1] = (Index.Joint1.Coordenates - Index.Joint0.Coordenates).normalized;
            // Index Middle Phalanx
            bones[2] = (Index.Joint2.Coordenates - Index.Joint1.Coordenates).normalized;
            // Index Distal Phalanx
            bones[3] = (Index.Tip.Coordenates - Index.Joint2.Coordenates).normalized;

        }

        public HandJoint Wrist { get; }

        public HandFinger Trumb { get; }

        public HandFinger Index { get; }

        public HandFinger Middle { get; }

        public HandFinger Ring { get; }

        public HandFinger Pinky { get; }

        public override string ToString()
        {
            return string.Format("[ {0}, {1}, {2}, {3}, {4} ]",
                 Trumb.ToString(),
                 Index.ToString(),
                 Middle.ToString(),
                 Ring.ToString(),
                 Pinky.ToString());
        }
    }
}
