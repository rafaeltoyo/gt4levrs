using UnityEngine;

namespace HandTracking
{

    public class HandTrackingClient : MonoBehaviour
    {
        private HandTrackingRequester _handTrackingRequester;

        [SerializeField]
        private HandController hand;

        /// <summary>
        ///     Method to check if the hand tracking requester is waiting data or already received data
        /// </summary>
        /// <returns>True if waiting data</returns>
        private bool IsWaitingJoints()
        {
            return !_handTrackingRequester.DataReceived;
        }

        /// <summary>
        ///     Method to check if list of joints received is empty.
        /// </summary>
        /// <returns>True if list is empty</returns>
        private bool IsEmptyJoints()
        {
            return _handTrackingRequester.Joints.Count <= 0;
        }

        /// <summary>
        ///     Set the values from joints received to hand model joints
        /// </summary>
        private void ProcessJoints()
        {
            int i = 0;

            foreach (HandController.Joint j in hand.Joints)
            {
                Debug.Log(j.Name);

                if (j.Position != null)
                    j.Position.position = _handTrackingRequester.Joints[i];
                i++;
            }

            _handTrackingRequester.Joints.Clear();
        }

        /// <summary>
        ///     Restart the requester thread to receive new data
        /// </summary>
        private void RestartRequester()
        {
            if (_handTrackingRequester != null)
            {
                _handTrackingRequester.Stop();
            }

            _handTrackingRequester = new HandTrackingRequester();
            _handTrackingRequester.Start();
        }

        /** Unity behaviour methods */

        private void Start()
        {
            RestartRequester();
        }

        private void Update()
        {
            if (IsWaitingJoints())
            {
                //Debug.Log("Wating data!");
            }
            else
            {
                //Debug.Log("Running!");

                if (!IsEmptyJoints())
                {
                    ProcessJoints();
                }

                //RestartRequester();
            }
        }

        private void OnDestroy()
        {
            _handTrackingRequester.Stop();
        }
    }
}