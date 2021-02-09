﻿using UnityEngine;

using HandTracking.Communication;
using HandTracking.Parser;
using HandTracking.Models;

namespace HandTracking
{

    public class HandTrackingController : MonoBehaviour
    {
        private CommunicationAdapter adapter;

        private IHandTrackingDataParser parser = new MediapipeDataParser();

        [SerializeField]
        private HandTrackingConsumer consumer;

        /// <summary>
        ///     Method to check if the hand tracking requester is waiting data or already received data
        /// </summary>
        /// <returns>True if waiting data</returns>
        private bool IsWaitingJoints()
        {
            return !adapter.DataReceived;
        }

        /// <summary>
        ///     Set the values from joints received to hand model joints
        /// </summary>
        private void ProcessJoints()
        {
            Hand hand = parser.Parse(adapter.Data);
            if (hand != null)
                consumer.consume(hand);
            adapter.CleanData();
        }

        /// <summary>
        ///     Restart the requester thread to receive new data
        /// </summary>
        private void RestartRequester()
        {
            if (adapter != null)
            {
                adapter.Stop();
            }

            adapter = new CommunicationAdapter();
            adapter.Start();
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

                ProcessJoints();

                RestartRequester();
            }
        }

        private void OnDestroy()
        {
            adapter.Stop();
        }
    }
}