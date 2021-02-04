using AsyncIO;
using NetMQ;
using NetMQ.Sockets;
using UnityEngine;

namespace HandTracking.Communication
{
    /// <summary>
    ///     Communication Adapter with VR Device.
    /// </summary>
    public class CommunicationAdapter : RunAbleThread
    {
        public string Data { get; private set; }

        public bool DataReceived { get; private set; }

        /// <summary>
        ///     Clean received data.
        /// </summary>
        public void CleanData()
        {
            if (DataReceived)
            {
                this.Data = null;
                this.DataReceived = false;
            }
        }

        /// <summary>
        ///     Try receive frame string from server.
        /// </summary>
        /// <param name="socket">Socket</param>
        /// <returns>Data read</returns>
        private string TryRead(RequestSocket socket)
        {
            string message = null;

            while (Running)
            {
                if (socket.TryReceiveFrameString(out message))
                {
                    return message;
                }
            }
            return null;
        }

        /// <summary>
        ///     Run the thread.
        ///     <br />
        ///     Create a socket and connect with VR device.
        ///     <br />
        ///     So try read something from socket and save.
        /// </summary>
        protected override void Run()
        {
            CleanData();

            ForceDotNet.Force(); // this line is needed to prevent unity freeze after one use, not sure why yet

            try
            {
                using (RequestSocket socket = new RequestSocket())
                {
                    // Connect with VR device
                    socket.Connect(CommunicationConstants.VR_DEVICE_ADDRESS);

                    // Request hand tracking function
                    socket.SendFrame(CommunicationConstants.MSG_HANDSHAKE);

                    // Waiting data from server
                    this.Data = TryRead(socket);
                    Debug.Log(this.Data);
                }
            }
            finally
            {
                NetMQConfig.Cleanup(); // this line is needed to prevent unity freeze after one use, not sure why yet

                this.DataReceived = (this.Data != null) && (this.Data.Trim().Length > 0);
            }
        }
    }
}