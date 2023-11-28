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
    
    //WebClient.ModelResponse res;

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
    //     for (int i = 0; i < res.data[0].Floor.Count; i++)
    //     {
    //         for (int j = 0; j < res.data[0].Floor[i].Count; j++)
    //         {
    //             if (res.data[0].Floor[i][j] == 10)
    //             {
    //                 Instantiate(storagePrefab, new Vector3(i, 0, j), Quaternion.identity);
    //             }
                    
    //             else if (res.data[0].Floor[i][j] > 0 && res.data[0].Floor[i][j] < 10)
    //             {
    //                 Instantiate(foodPrefab, new Vector3(i, 0, j), Quaternion.identity);
    //             }
                    
    //         }}
    // }
    
    

    

}
