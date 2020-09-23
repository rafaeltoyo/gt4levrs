using UnityEngine;
using System;
using System.Collections.Generic;

public class HandController : MonoBehaviour
{
    [Serializable]
    public class Joint
    {
        [SerializeField]
        private string name;
        [SerializeField]
        private Transform position;

        public string Name { get => name; set => name = value; }

        public Transform Position { get => position; set => position = value; }
    }

    [SerializeField]
    private List<Joint> joints;

    public List<Joint> Joints { get => joints; }

    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
