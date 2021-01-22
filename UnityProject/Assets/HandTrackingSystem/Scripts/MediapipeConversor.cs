using System.Collections.Generic;
using System.Text.RegularExpressions;
using UnityEngine;

namespace HandTracking
{
    public class MediapipeConversor
    {
        private readonly Regex JOINT_MASK = new Regex(@"^[a-zA-Z_]+(;[0-9,.\-+e]+){3}");

        private List<Joint> _joints = new List<Joint>();

        public void Parse(string coordenates)
        {
            string[] joints = coordenates.Split('|');

            for (int i = 0; i < joints.Length; i++)
            {
                //_joints.Add(joints[i]);
            }
        }

        private void ParseJoint(string jointString)
        {
            if (JOINT_MASK.IsMatch(jointString))
            {
                string[] values = jointString.Split(';');
            }
            KeyValuePair<string, Vector3> joint =  new KeyValuePair<string, Vector3>();
        }
    }
}
