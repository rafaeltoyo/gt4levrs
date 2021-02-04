using UnityEngine;
using System;

using HandTracking.Models;

namespace HandTracking
{
    public abstract class HandTrackingConsumer: MonoBehaviour
    {
        public abstract void consume(Hand hand);
    }
}