using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace HandTracking.Models
{
    public class HandTrackingData
    {
        private Hand leftHand;
        private Hand rightHand;

        public HandTrackingData(Hand leftHand, Hand rightHand)
        {
            this.leftHand = leftHand;
            this.rightHand = rightHand;
        }

        public Hand LeftHand { get { return leftHand; } }

        public Hand RightHand { get { return rightHand; } }
    }
}