using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace HandTracking.Models
{
    public class HandTrackingData
    {
        public HandTrackingData(Hand leftHand, Hand rightHand, Vector3 reference) {
            LeftHand = leftHand;
            RightHand = rightHand;
            Reference = reference;
        }

        public Vector3 Reference { get; }

        public Hand LeftHand { get; }

        public Hand RightHand { get; }
    }
}