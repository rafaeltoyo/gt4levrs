using UnityEngine;

using HandTracking.Models;

namespace HandTracking.Utils
{
    public class HandUtils
    {

        public static Vector3 ToBone(HandJoint jointA, HandJoint jointB)
        {
            return (jointB.Coordenates - jointA.Coordenates);
        }
    }
}