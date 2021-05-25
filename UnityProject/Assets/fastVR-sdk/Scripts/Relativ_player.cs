// Copyright 2017 Relativty. All rights reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

public class Relativ_player : MonoBehaviour {

	wrmhl Relativ_headset = new wrmhl(); // wrmhl is the bridge beetwen your computer and hardware.

	Relativ_setup Relativ_setup = new Relativ_setup(); // This class allow auto config

	public string portName;

	public int baudRate;

	public int ReadTimeout;

	string[] sep = new string[] {","};

	string data;

	void Start () {
		portName = Relativ_setup.getPort();

		baudRate = Relativ_setup.getBaudRate();

		ReadTimeout = Relativ_setup.getTimeout();

		Relativ_headset.set (portName, baudRate, ReadTimeout, 1); // This method set the communication with the following vars;
		//                              Serial Port, Baud Rates and Read Timeout.
		try {
			Relativ_headset.connect (); // This method open the Serial communication with the vars previously given.
		} catch (IOException ex) {
			Debug.LogError("Headset not found!");
			Relativ_headset = null;
			throw ex;
		}
	}

	// Update is called once per frame
	void Update () {
		if (Relativ_headset == null)
			return;

		data = Relativ_headset.readQueue (); // myDevice.read() return the data coming from the device using thread.

		if (data == null)
			return;

		string[] values = data.Split (sep, System.StringSplitOptions.RemoveEmptyEntries);

		float w = float.Parse (values[3]);
		float x = float.Parse (values[0]);
		float y = float.Parse (values[1]);
		float z = float.Parse (values[2]);
		float[] EulerAngles = Relativ_math_transform.getEuler(w, x, y, z);

		transform.localEulerAngles = new Vector3 (EulerAngles[0],EulerAngles[1],EulerAngles[2]);

	}

	void OnApplicationQuit() { // close the Thread and Serial Port
		if (Relativ_headset != null)
			Relativ_headset.close();
	}
}
