using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace HandTracking.Models
{
    public class Finger
    {
        private Joint _wrist;
        private Joint _joint0;
        private Joint _joint1;
        private Joint _joint2;
        private Joint _joint3;

        public Finger(Joint wrist, Joint joint0, Joint joint1, Joint joint2, Joint joint3)
        {
            _wrist = wrist;
            _joint0 = joint0;
            _joint1 = joint1;
            _joint2 = joint2;
            _joint3 = joint3;
        }

        public Joint Wrist => _wrist;
        public Joint Joint0 => _joint0;
        public Joint Joint1 => _joint1;
        public Joint Joint2 => _joint2;
        public Joint Joint3 => _joint3;
    }
}
