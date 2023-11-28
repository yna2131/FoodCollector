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
    string url = "http://localhost:8585";
    private ModelResponse res;

    public IEnumerator GetData()
    {
        using (UnityWebRequest www = UnityWebRequest.Get(url))
        {
            www.downloadHandler = new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type", "application/json");

            yield return www.SendWebRequest();

            if (www.result == UnityWebRequest.Result.ConnectionError || www.result == UnityWebRequest.Result.ProtocolError)
            {
                Debug.Log(www.error);
                yield break;
            }
            else
            {
                res = JsonUtility.FromJson<ModelResponse>(www.downloadHandler.text);
            }
        }
    }

    public ModelResponse GetResponse()
    {
        return res;
    }

    public override string ToString()
    {
        return "WebClient object data: " + (res != null ? res.ToString() : "null");
    }
}


