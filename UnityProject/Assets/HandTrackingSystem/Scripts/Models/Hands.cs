using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace HandTracking.Models
{
    public class Hands
    {
        public Hands(Hand leftHand, Hand rightHand) {
            LeftHand = leftHand;
            RightHand = rightHand;
        }

        public Hand LeftHand { get; }

        public Hand RightHand { get; }
    }
}