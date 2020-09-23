using UnityEngine;

namespace HandTracking
{

    public class HandTrackingClient : MonoBehaviour
    {
        private HandTrackingRequester _helloRequester;

        [SerializeField]
        private HandController hand;

        private void Start()
        {
            _helloRequester = new HandTrackingRequester();
            _helloRequester.Start();
        }

        private void Update()
        {
            if (!_helloRequester.DataReceived) return;

            Debug.Log("Running!");

            if (_helloRequester.Joints.Count <= 0) return;

            int i = 0;

            foreach(HandController.Joint j in hand.Joints)
            {
                Debug.Log(j.Name);

                if (j.Position != null)
                    j.Position.position = _helloRequester.Joints[i];
                i++;
            }

            _helloRequester.Joints.Clear();
        }

        private void OnDestroy()
        {
            _helloRequester.Stop();
        }
    }
}