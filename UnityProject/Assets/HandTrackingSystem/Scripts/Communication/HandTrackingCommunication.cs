using System;
using System.Collections.Generic;
using System.Globalization;
using System.Text.RegularExpressions;

using AsyncIO;
using NetMQ;
using NetMQ.Sockets;
using UnityEngine;

using HandTracking.Models;
using HandTracking.Parser;

namespace HandTracking
{
    /// <summary>
    ///     Classe de comunicação com o dispositivo de handtracking
    /// </summary>
    public class HandTrackingCommunication : RunAbleThread
    {
        private const string VR_DEVICE_ADDRESS = "tcp://localhost:5555";

        private const string MSG_HANDSHAKE = "handtracking";

        private const string MSG_ACK = "ack";

        private const string MSG_NEXT = "next";

        private Regex jointMask = new Regex(@"^[a-zA-Z_]+(;[0-9,.\-+e]+){3}");

        private bool _dataReceived;

        private IHandTrackingDataParser _parser;

        private Hand _leftHand;

        private Hand _rightHand;

        public HandTrackingCommunication(IHandTrackingDataParser parser): base()
        {
            _parser = parser;
            CleanData();
        }

        public bool DataReceived {
            get
            {
                if (_dataReceived)
                {
                    _dataReceived = false;
                    return true;
                }
                return false;
            }
        }

        private void CleanData()
        {
            _dataReceived = false;
            _leftHand = null;
            _rightHand = null;
        }

        private string TryRead(RequestSocket client)
        {
            string message = null;

            while (Running)
            {
                if (client.TryReceiveFrameString(out message))
                {
                    return message;
                }
            }
            return null;
        }

        private bool IsValidJoint(string joint)
        {
            return (joint != null) && jointMask.IsMatch(joint);
        }

        private float[] ParseJoint(string joint)
        {
            float[] points = new float[3];

            try
            {
                string[] pieces = joint.Split(';');

                points[0] = float.Parse(pieces[1], CultureInfo.InvariantCulture.NumberFormat);
                points[1] = float.Parse(pieces[2], CultureInfo.InvariantCulture.NumberFormat);
                points[2] = float.Parse(pieces[3], CultureInfo.InvariantCulture.NumberFormat);

            }
            catch (Exception)
            {
                points[0] = 0;
                points[1] = 0;
                points[2] = 0;
            }

            return points;
        }

        protected override void Run()
        {
            ForceDotNet.Force(); // this line is needed to prevent unity freeze after one use, not sure why yet

            if (_dataReceived) return;

            using (RequestSocket client = new RequestSocket())
            {
                client.Connect(VR_DEVICE_ADDRESS);

                // Request hand tracking function
                client.SendFrame(MSG_HANDSHAKE);

                // Waiting for ack from server
                string coordenates = TryRead(client);
                Debug.Log(coordenates);

                if (coordenates != null && coordenates.Length > 0)
                {
                    _leftHand = _parser.Parse(coordenates);
                }

            }

            NetMQConfig.Cleanup(); // this line is needed to prevent unity freeze after one use, not sure why yet

            _dataReceived = true;
        }
    }

}
