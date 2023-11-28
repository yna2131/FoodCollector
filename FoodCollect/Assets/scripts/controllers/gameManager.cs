using UnityEngine; //Para la clase JsonUtility
using System.Net;
using System.IO;
using System;



public class gameManager : MonoBehaviour
{
    WebClient wc;

    public GameObject storagePrefab;

    public GameObject foodPrefab;

    public GameObject collectorAgentPrefab;

    public GameObject explorerAgentPrefab;

    public static Action OnMinuteChanged;

    private float minuteToRealTime = 0.5f;
    private float timer;

    public float interval = 0.5f;

    //public ModelResponse res { get; set; } // Public property to store the response


    // Start is called before the first frame update
    void Start()
    {
        timer = minuteToRealTime;

        wc = gameObject.AddComponent<WebClient>();
        //Debug.Log("Wc:" + wc);
        
        StartCoroutine(wc.GetData());
    }

    // void Update()
    // {
    //     for (int i = 0; i < res.Floor.Count; i++)
    //     {
    //         for (int j = 0; j < res.Floor[i].Count; j++)
    //         {
    //             if (res.Floor[i][j] == 10)
    //             {
    //                 Instantiate(storagePrefab, new Vector3(i, 0, j), Quaternion.identity);
    //             }
                    
    //             else if (res.Floor[i][j] > 0 && res.Floor[i][j] < 10)
    //             {
    //                 Instantiate(foodPrefab, new Vector3(i, 0, j), Quaternion.identity);
    //             }
                    
    //         }}
    // }
    
    

    

}
