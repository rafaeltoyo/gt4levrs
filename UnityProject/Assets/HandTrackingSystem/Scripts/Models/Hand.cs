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

        public Vector3[] ToVector3Array()
        {
            Vector3[] joints = new Vector3[21];

            joints[0] = Wrist.Coordenates;

            joints[1] = Trumb.Joint0.Coordenates;
            joints[2] = Trumb.Joint1.Coordenates;
            joints[3] = Trumb.Joint2.Coordenates;
            joints[4] = Trumb.Joint3.Coordenates;

            joints[5] = Index.Joint0.Coordenates;
            joints[6] = Index.Joint1.Coordenates;
            joints[7] = Index.Joint2.Coordenates;
            joints[8] = Index.Joint3.Coordenates;

            joints[9] = Middle.Joint0.Coordenates;
            joints[10] = Middle.Joint1.Coordenates;
            joints[11] = Middle.Joint2.Coordenates;
            joints[12] = Middle.Joint3.Coordenates;

            joints[13] = Ring.Joint0.Coordenates;
            joints[14] = Ring.Joint1.Coordenates;
            joints[15] = Ring.Joint2.Coordenates;
            joints[16] = Ring.Joint3.Coordenates;

            joints[17] = Pinky.Joint0.Coordenates;
            joints[18] = Pinky.Joint1.Coordenates;
            joints[19] = Pinky.Joint2.Coordenates;
            joints[20] = Pinky.Joint3.Coordenates;

            return joints;
        }

        public override string ToString()
        {
            return string.Format("[{0}; {1}; {2}; {3}; {4}]",
                 Trumb.ToString(),
                 Index.ToString(),
                 Middle.ToString(),
                 Ring.ToString(),
                 Pinky.ToString());
        }
    }
}
