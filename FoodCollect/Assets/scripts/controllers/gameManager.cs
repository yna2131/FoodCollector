using UnityEngine; //Para la clase JsonUtility
using System.Net;
using System.IO;
using System.Collections;



public class gameManager : MonoBehaviour
{
    WebClient wc;
    ModelResponse res;

    public GameObject storagePrefab;

    public GameObject foodPrefab;

    //public GameObject collectorAgentPrefab;

    public GameObject explorerAgentPrefab;

    // public static Action OnMinuteChanged;

    private float minuteToRealTime = 0.5f;
    private float timer;

    public float interval = 0.5f;
    
    //WebClient.ModelResponse res;

    // Start is called before the first frame update
    void Start()
    {
        timer = minuteToRealTime;

        wc = gameObject.AddComponent<WebClient>();
        StartCoroutine(GetDataAndAssignResponse());
    }

    private IEnumerator GetDataAndAssignResponse()
    {
        yield return wc.GetData();

        res = wc.GetResponse();

        if (res != null && res.data != null && res.data.Count > 0)
        {
            // Your logic for instantiating objects based on response data
            for (int i = 0; i < 20; i++)
            {
                for (int j = 0; j < 20; j++)
                {
                    int a = i * 20 + j;
                    if (res.data[0].Floor != null && a < res.data[0].Floor.Count)
                    {
                        if (res.data[0].Floor[a] == 10)
                        {
                            Instantiate(storagePrefab, new Vector3(i, 0, j), Quaternion.identity);
                        }

                        float floorValue = res.data[0].Floor[a];
                        // Debug.Log("Floor[" + a + "] = " + floorValue);

                        if (Mathf.Approximately(floorValue, 1.0f))
                        {
                            // Debug.Log("Instantiate food 123");
                            Instantiate(foodPrefab, new Vector3(i, 2, j), Quaternion.identity);
                        }
                    }
                    foreach (var agent in res.data[0].AgentPositions)
                    {
                        Debug.Log("Agent: " + agent);
                        Instantiate(explorerAgentPrefab, new Vector3(i, 2, j), Quaternion.identity);
                    }
                }
            }

            
        }
        else
        {
            Debug.LogError("Response or its properties are null or empty.");
        }
    }

    void Update()
    {}
        
    
    

    

}
