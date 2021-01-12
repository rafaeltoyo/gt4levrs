using System;
using System.Collections.Generic;
using System.Globalization;
using System.Text.RegularExpressions;

using AsyncIO;
using NetMQ;
using NetMQ.Sockets;
using UnityEngine;

namespace HandTracking
{

    public class HandTrackingRequester : RunAbleThread
    {
        private const string VR_DEVICE_ADDRESS = "tcp://localhost:5555";

        private const string MSG_HANDSHAKE = "handtracking";

        private const string MSG_ACK = "ack";

        private const string MSG_NEXT = "next";

        private Regex jointMask = new Regex(@"^joint(;[0-9,.\-+e]+){3}");

        private bool _dataReceived;

        private List<Vector3> _joints;

        public HandTrackingRequester(): base()
        {
            _dataReceived = false;
            _joints = new List<Vector3>();
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

        public List<Vector3> Joints { get => _joints; }

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

        private bool IsValidJoint(string message)
        {
            return (message != null) && jointMask.IsMatch(message);
        }

        private float[] ParseJoint(string message)
        {
            float[] points = new float[3];

            try
            {
                string[] pieces = message.Split(';');

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
                string handshake = TryRead(client);
                Debug.Log(handshake);

                if (handshake != null && handshake.StartsWith(MSG_ACK))
                {
                    // Request all joints until receive "end"
                    for (int i = 0; i < 30 && Running; i++)
                    {
                        // Request next information
                        client.SendFrame(MSG_NEXT);

                        // Wait server response
                        string message = TryRead(client);
                        Debug.Log(message);

                        // Handling the server response
                        if (IsValidJoint(message))
                        {
                            float[] points = ParseJoint(message);

                            Debug.Log(string.Format("{0}, {1}, {2}", points[0], points[1], points[2]));

                            _joints.Add(new Vector3(points[0], points[1], points[2]));
                        }
                        else
                        {
                            break;
                        }
                    }
                }

            }

            NetMQConfig.Cleanup(); // this line is needed to prevent unity freeze after one use, not sure why yet

            _dataReceived = true;
        }
    }

}
