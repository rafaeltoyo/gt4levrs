using System.Collections;
using System.Collections.Generic;
using HandTracking.Models;
using UnityEngine;

public class MyDummyHand : HandTracking.HandTrackingConsumer
{
    private GameObject[] joints;

    public override void consume(Hand hand)
    {
        Vector3[] coords = hand.ToVector3Array();

        Debug.Log(hand.ToString());
        
        for (int i = 0; i < coords.Length; i++)
        {
            joints[i].transform.position = coords[i];
        }
    }

    // Start is called before the first frame update
    void Start()
    {
        joints = new GameObject[21];

        for (int i = 0; i < joints.Length; i++)
        {
            joints[i] = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            joints[i].transform.localScale = new Vector3(0.1f, 0.1f, 0.1f);
        }
    }

    // Update is called once per frame
    void FixedUpdate()
    {

    }
}
