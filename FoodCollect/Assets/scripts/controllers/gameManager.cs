using UnityEngine; //Para la clase JsonUtility
using System.Net;
using System.IO;
using System.Collections;
using System.Collections.Generic;



public class gameManager : MonoBehaviour
{
    WebClient wc;
    ModelResponse res;

    public GameObject storagePrefab;

    public GameObject foodPrefab;

    public GameObject collectorAgentPrefab;

    public GameObject explorerAgentPrefab;

    // public static Action OnMinuteChanged;

    private float minuteToRealTime = 0.01f;
    private float timer;

    public float interval = 1f;
    
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
        List <GameObject> toDelete = new List<GameObject>();

        if (res != null && res.data != null && res.data.Count > 0)
        {
            // Your logic for instantiating objects based on response data
            for (int i = 0; i < res.data.Count; i++)
            {
                Step(i, toDelete);
            

            yield return new WaitForSeconds(interval);

            foreach (GameObject go in toDelete)
            {
                Destroy(go);
                toDelete = new List<GameObject>();
            }
            }
            
        }
        else
        {
            Debug.LogError("Response or its properties are null or empty.");
        }
    }


    void Step(int step, List<GameObject> toDelete)
    {
            for (int i = 0; i < 20; i++)
            {
                for (int j = 0; j < 20; j++)
                {
                    int a = i * 20 + j;
                    if (res.data[step].Floor != null && a < res.data[step].Floor.Count)
                    {
                        if (res.data[step].Floor[a] == 10)
                        {
                            GameObject storage = Instantiate(storagePrefab, new Vector3(i, 0, j), Quaternion.Euler(0,90,0));
                            toDelete.Add(storage);
                        }

                        float floorValue = res.data[step].Floor[a];
                        // Debug.Log("Floor[" + a + "] = " + floorValue);

                        if (Mathf.Approximately(floorValue, 1.0f))
                        {
                            // Debug.Log("Instantiate food 123");
                            GameObject food = Instantiate(foodPrefab, new Vector3(i, 1, j), Quaternion.Euler(90, 0, 0));
                            toDelete.Add(food);

                        }
                    }
                    
                    

                    if (res.data[step].AgentPositions != null && a < res.data[step].AgentPositions.Count)

                    {
                        if (res.data[step].AgentPositions[a] == 1)
                        {
                            GameObject collector = Instantiate(collectorAgentPrefab, new Vector3(i, 0.5f, j), Quaternion.identity);
                            toDelete.Add(collector);

                        }
                        else if (res.data[step].AgentPositions[a] == 2)
                        {
                            GameObject explorer = Instantiate(explorerAgentPrefab, new Vector3(i, 0.5f, j), Quaternion.identity);
                            toDelete.Add(explorer);
                        }
                    }
                }
            }

    }
    void Update()
    {}
        
    
    

    

}
