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

        public void Update(float x, float y, float z)
        {
            _coordenates.Set(x, y, z);
        }

        public string Name { get; }
        public float X => _coordenates.x;
        public float Y => _coordenates.y;
        public float Z => _coordenates.z;
    }
}

