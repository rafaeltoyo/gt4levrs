using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace HandTracking.Models
{
    public class Joint
    {
        private string _name;
        private Vector3 _coordenates;

        public Joint(string name)
        {
            _name = name;
        }

        public void Update(float x, float y, float z)
        {
            _coordenates.Set(x, y, z);
        }

        public string Name => _name;
        public float X => _coordenates.x;
        public float Y => _coordenates.y;
        public float Z => _coordenates.z;
    }
}

