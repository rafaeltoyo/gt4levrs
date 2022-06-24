using System.Collections;
using System.Collections.Generic;
using HandTracking.Models;
using UnityEngine;

public class SkeletonHand : HandTracking.HandTrackingConsumer
{
    [SerializeField] private GameObject hand;
    [SerializeField] private GameObject wrist;

    [SerializeField] private GameObject thumbJoint0;
    [SerializeField] private GameObject thumbJoint1;
    [SerializeField] private GameObject thumbJoint2;
    [SerializeField] private GameObject thumbJoint3;

    [SerializeField] private GameObject indexJoint0;
    [SerializeField] private GameObject indexJoint1;
    [SerializeField] private GameObject indexJoint2;
    [SerializeField] private GameObject indexJoint3;

    [SerializeField] private GameObject middleJoint0;
    [SerializeField] private GameObject middleJoint1;
    [SerializeField] private GameObject middleJoint2;
    [SerializeField] private GameObject middleJoint3;

    [SerializeField] private GameObject ringJoint0;
    [SerializeField] private GameObject ringJoint1;
    [SerializeField] private GameObject ringJoint2;
    [SerializeField] private GameObject ringJoint3;

    [SerializeField] private GameObject pinkyJoint0;
    [SerializeField] private GameObject pinkyJoint1;
    [SerializeField] private GameObject pinkyJoint2;
    [SerializeField] private GameObject pinkyJoint3;

    private Dictionary<GameObject, Quaternion> initialRotation = new Dictionary<GameObject, Quaternion>();

    private bool started = false;

    public override void consume(Hand hand)
    {
        if (!started)
            return;

        this.hand.transform.localPosition = new Vector3(
            -hand.Wrist.Coordenates.x,
            hand.Wrist.Coordenates.y,
            -hand.Wrist.Coordenates.z
        );

        this.hand.transform.localRotation = hand.GetRotation();
        this.hand.transform.RotateAround(this.hand.transform.position, Vector3.up, 180);

        Vector3 normal = hand.GetUpwardDirection();
        this.UpdateFinger(
            hand.Thumb,
            normal,
            this.thumbJoint0,
            this.thumbJoint1,
            this.thumbJoint2
        );
        this.UpdateFinger(
            hand.Index,
            normal,
            this.indexJoint0,
            this.indexJoint1,
            this.indexJoint2
        );
        this.UpdateFinger(
            hand.Middle,
            normal,
            this.middleJoint0,
            this.middleJoint1,
            this.middleJoint2
        );
        this.UpdateFinger(
            hand.Ring,
            normal,
            this.ringJoint0,
            this.ringJoint1,
            this.ringJoint2
        );
        this.UpdateFinger(
            hand.Pinky,
            normal,
            this.pinkyJoint0,
            this.pinkyJoint1,
            this.pinkyJoint2
        );
    }

    // Start is called before the first frame update
    void Start()
    {
        SaveInitialRotation(thumbJoint0);
        SaveInitialRotation(thumbJoint1);
        SaveInitialRotation(thumbJoint2);
        SaveInitialRotation(thumbJoint3);

        SaveInitialRotation(indexJoint0);
        SaveInitialRotation(indexJoint1);
        SaveInitialRotation(indexJoint2);
        SaveInitialRotation(indexJoint3);
        
        SaveInitialRotation(middleJoint0);
        SaveInitialRotation(middleJoint1);
        SaveInitialRotation(middleJoint2);
        SaveInitialRotation(middleJoint3);
        
        SaveInitialRotation(ringJoint0);
        SaveInitialRotation(ringJoint1);
        SaveInitialRotation(ringJoint2);
        SaveInitialRotation(ringJoint3);

        SaveInitialRotation(pinkyJoint0);
        SaveInitialRotation(pinkyJoint1);
        SaveInitialRotation(pinkyJoint2);
        SaveInitialRotation(pinkyJoint3);

        started = true;
    }

    // Update is called once per frame
    void FixedUpdate()
    {

    }

    private void SaveInitialRotation(GameObject joint)
    {
        initialRotation[joint] = joint.transform.localRotation;
    }

    private void UpdateThumb(HandFinger finger)
    {
        Vector3 bone1 = finger.Joint0.Coordenates - finger.Wrist.Coordenates;
        Vector3 bone2 = finger.Joint1.Coordenates - finger.Joint0.Coordenates;
        Vector3 bone3 = finger.Joint2.Coordenates - finger.Joint1.Coordenates;
        Vector3 bone4 = finger.Tip.Coordenates - finger.Joint2.Coordenates;

        this.SetAngle(thumbJoint0, -Vector3.Angle(bone2, bone1));
        this.SetAngle(thumbJoint1, -Vector3.Angle(bone3, bone2));
        this.SetAngle(thumbJoint2, -Vector3.Angle(bone4, bone3));
    }

    private void UpdateFinger(HandFinger finger,
                                Vector3 normal,
                                GameObject joint0,
                                GameObject joint1,
                                GameObject joint2)
    {
        Vector3 bone1 = finger.Joint1.Coordenates - finger.Joint0.Coordenates;
        Vector3 bone2 = finger.Joint2.Coordenates - finger.Joint1.Coordenates;
        Vector3 bone3 = finger.Tip.Coordenates - finger.Joint2.Coordenates;

        this.SetAngle(joint0, initialRotation[joint0].eulerAngles.z + 90 - (Vector3.Angle(bone1, normal)));
        this.SetAngle(joint1, -Vector3.Angle(bone2, bone1));
        this.SetAngle(joint2, -Vector3.Angle(bone3, bone2));
    }

    private void SetAngle(GameObject joint, float angle)
    {
        joint.transform.localRotation = Quaternion.Euler(
            initialRotation[joint].eulerAngles.x,
            initialRotation[joint].eulerAngles.y,
            angle
        );
    }
}
