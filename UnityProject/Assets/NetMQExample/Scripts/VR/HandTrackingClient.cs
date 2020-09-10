using UnityEngine;

namespace VR
{

    public class HandTrackingClient : MonoBehaviour
    {
        private HandTrackingRequester _helloRequester;

        private void Start()
        {
            _helloRequester = new HandTrackingRequester();
            _helloRequester.Start();
        }

        private void OnDestroy()
        {
            _helloRequester.Stop();
        }
    }
}