// TC2008B Modelación de Sistemas Multiagentes con gráficas computacionales
// C# client to interact with Python server via POST
// Sergio Ruiz-Loza, Ph.D. March 2021

using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

public class WebClient : MonoBehaviour
{
    [System.Serializable]
    public class Datum
    {
        public List<List<double>> Floor { get; set; }
        public List<List<double>> AgentPositions { get; set; }
    }
    public class ModelResponse
    {
        // Define the structure of response data
        public int steps { get; set; }
        public List<Datum> data { get; set; } 

    }

    string url = "http://localhost:8585";
    public IEnumerator GetData()
    {
        using (UnityWebRequest www = UnityWebRequest.Get(url))
        {
             // Set up a DownloadHandlerBuffer to store the response data
            www.downloadHandler = new DownloadHandlerBuffer();

           // Set the request header to indicate that the expected response is in JSON format 
            www.SetRequestHeader("Content-Type", "application/json");

            // Send the GET request and wait for the response
            yield return www.SendWebRequest();          // Talk to Python

            // Check if there was a connection error or protocol error
            if (www.result == UnityWebRequest.Result.ConnectionError || www.result == UnityWebRequest.Result.ProtocolError)
            {
                // Log the error and return
                Debug.Log(www.error);
                yield break;
            }
            else
            {
            // Log the response data from the server
                Debug.Log(www.downloadHandler.text);    // Answer from Python
            
            // Deserialize the JSON response into a ModelResponse object
                ModelResponse res = JsonUtility.FromJson<ModelResponse>(www.downloadHandler.text);
            
            // Log the deserialized response object
                // Debug.Log(res.steps);
                // yield return res;
            }
        }
    }
}


