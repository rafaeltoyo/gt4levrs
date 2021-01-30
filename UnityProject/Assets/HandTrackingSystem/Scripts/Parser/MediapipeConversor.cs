using System.Collections.Generic;
using System.Text.RegularExpressions;
using UnityEngine;

using HandTracking.Models;

namespace HandTracking.Parser
{
    public class MediapipeConversor : IHandTrackingDataParser
    {
        private readonly Regex JOINT_MASK = new Regex(@"^[a-zA-Z_]+(;[0-9,.\-+e]+){3}");

        private List<HandJoint> _joints = new List<HandJoint>();

        /// <summary>
        ///     Método responsável por converter a String de dados, recebida do serviço de handtracking, para objeto Hand.
        /// </summary>
        /// <param name="coordenates">String recebida com os dados</param>
        /// <returns>Objeto Hand</returns>
        public Hand Parse(string coordenates)
        {
            string[] joints = coordenates.Split('|');

            for (int i = 0; i < joints.Length; i++)
            {
                //_joints.Add(joints[i]);
            }

            return null;
        }

        private
        void ParseJoint(string jointString)
        {
            if (JOINT_MASK.IsMatch(jointString))
            {
                string[] values = jointString.Split(';');
            }
            KeyValuePair<string, Vector3> joint = new KeyValuePair<string, Vector3>();
        }
    }
}
