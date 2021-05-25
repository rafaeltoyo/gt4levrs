using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace HandTracking.Models
{
    public class HandTrackingData
    {
        private Vector3 reference;
        private Hand leftHand;
        private Hand rightHand;

        public HandTrackingData(Hand leftHand, Hand rightHand, Vector3 reference)
        {
            this.leftHand = leftHand;
            this.rightHand = rightHand;
            this.reference = reference;
        }

        public Vector3 Reference { get { return reference; } }

        public Hand LeftHand { get { return leftHand; } }

        public Hand RightHand { get { return rightHand; } }
    }
}