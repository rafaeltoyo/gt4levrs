using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using UnityEngine;

namespace HandTracking.Models
{
    /// <summary>
    ///     Hands joint representation
    /// </summary>
    public class HandJoint
    {
        private Vector3 _coordenates;

        /// <summary>
        ///     Default constructor
        /// </summary>
        /// <param name="name">Name of joint</param>
        public HandJoint(string name)
        {
            Name = name;
        }

        /// <summary>
        ///     Update x,y,z values.
        /// </summary>
        /// <param name="x">x value</param>
        /// <param name="y">y value</param>
        /// <param name="z">z value</param>
        /// <returns>Joint instance</returns>
        public HandJoint Update(float x, float y, float z)
        {
            _coordenates.Set(x, y, z);
            return this;
        }

        public string Name { get; }

        public float X => _coordenates.x;

        public float Y => _coordenates.y;

        public float Z => _coordenates.z;

        public Vector3 Coordenates => new Vector3(X, Y, Z);

        public override string ToString()
        {
            return string.Format("{{ \"name\": \"{0}\", \"x\": {1:0.###}, \"y\": {2:0.###}, \"z\"{3:0.###} }}",
                 Name.ToString(),
                 X.ToString(CultureInfo.InvariantCulture),
                 Y.ToString(CultureInfo.InvariantCulture),
                 Z.ToString(CultureInfo.InvariantCulture));
        }
    }
}

