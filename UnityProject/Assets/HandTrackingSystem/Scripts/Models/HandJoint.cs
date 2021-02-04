using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace HandTracking.Models
{
    public class HandJoint
    {
        private Vector3 _coordenates;

        public HandJoint(string name)
        {
            Name = name;
        }

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
            return string.Format("{4}{0}; {1}; {2}; {3}{5}",
                 Name.ToString(),
                 X.ToString(),
                 Y.ToString(),
                 Z.ToString(),
                 '{',
                 '}');
        }
    }
}

