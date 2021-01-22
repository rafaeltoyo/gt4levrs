using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace HandTracking.Models
{
    public class Hand
    {
        private Joint _wrist;
        private Finger _thumb;
        private Finger _index;
        private Finger _middle;
        private Finger _ring;
        private Finger _pinky;

        public Hand(Joint wrist, Finger thumb, Finger index, Finger middle, Finger ring, Finger pinky)
        {
            _wrist = wrist;
            _thumb = thumb;
            _index = index;
            _middle = middle;
            _ring = ring;
            _pinky = pinky;
        }

        public Joint Wrist => _wrist;
        public Finger Trumb => _thumb;
        public Finger Index => _index;
        public Finger Middle => _middle;
        public Finger Ring => _ring;
        public Finger Pinky => _pinky;
    }
}
