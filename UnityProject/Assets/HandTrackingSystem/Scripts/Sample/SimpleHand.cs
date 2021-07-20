using System;
using System.Collections.Generic;
using HandTracking.Models;
using UnityEngine;

public class SimpleHand : HandTracking.HandTrackingConsumer
{
    private Dictionary<HandJointIndex, GameObject> joints = new Dictionary<HandJointIndex, GameObject>();
    private Dictionary<HandBoneIndex, GameObject> bones = new Dictionary<HandBoneIndex, GameObject>();
    private bool once = false;
    
    public override void consume(Hand hand)
    {
        Vector3[] coordinates = hand.ToVector3Array();

        Debug.Log(hand.ToString());

        UpdateJoints(coordinates);
        UpdateBones(coordinates);
    }

    private void UpdateJoints(Vector3[] coordinates)
    {
        foreach (HandJointIndex jointId in Enum.GetValues(typeof(HandJointIndex))) {
            joints[jointId].transform.localPosition = coordinates[(ushort)jointId];
        }
    }

    private void UpdateBones(Vector3[] coordinates)
    {
        foreach (HandBoneIndex boneId in Enum.GetValues(typeof(HandBoneIndex))) {
            // Current bone
            HandBone boneData = HandBone.Bones[boneId];
            
            // Bone joints
            Vector3 joint0 = coordinates[(ushort)boneData.Joint0];
            Vector3 joint1 = coordinates[(ushort)boneData.Joint1];
            
            // Position between joints (center of bone)
            bones[boneId].transform.localPosition = Vector3.Lerp(joint0, joint1, 0.5f);

            // Direction of bone
            Vector3 dirV = (joint1 - joint0).normalized;

            Vector3 cylDefaultOrientation = Vector3.up;

            Vector3 rotAxisV = (dirV + cylDefaultOrientation).normalized;
            
            bones[boneId].transform.localRotation = new Quaternion(rotAxisV.x, rotAxisV.y, rotAxisV.z, 0);

            bones[boneId].transform.localScale = new Vector3(
                0.1f,
                Vector3.Distance(joint1, joint0) * 0.5f,
                0.1f
            );
        }
    }

    // Start is called before the first frame update
    void Start()
    {
        foreach (HandJointIndex jointId in Enum.GetValues(typeof(HandJointIndex))) {
            joints.Add(jointId, createJoint(this.gameObject, "joint " + Enum.GetName(typeof(HandJointIndex), jointId)));
        }
        foreach (HandBoneIndex boneId in Enum.GetValues(typeof(HandBoneIndex))) {
            bones.Add(boneId, createBone(this.gameObject, "bone " + Enum.GetName(typeof(HandBoneIndex), boneId)));
        }
    }

    // Update is called once per frame
    void FixedUpdate()
    {

    }

    private GameObject createJoint(GameObject parent, string name) {
        GameObject gameObject = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        gameObject.name = name;
        gameObject.transform.SetParent(parent.transform);
        gameObject.transform.localScale = new Vector3(0.1f, 0.1f, 0.1f);
        gameObject.GetComponent<Collider>().isTrigger = true;
        return gameObject;
    }

    private GameObject createBone(GameObject parent, string name) {
        GameObject gameObject = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
        gameObject.name = name;
        gameObject.transform.SetParent(parent.transform);
        gameObject.transform.localScale = new Vector3(0.1f, 0.1f, 0.1f);
        gameObject.GetComponent<Collider>().isTrigger = true;
        return gameObject;
    }
}
