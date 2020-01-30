using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using System.Threading;

[System.Serializable]
public class LoginRequest
{
	public string UUID;
}

[System.Serializable]
public class OutgamePayload
{
	public string Action;
	public string Target;
}

public class PointaClient : MonoBehaviour {
	public string targetURI;
	public GameObject ViewController;

	[SerializeField]
	private int[] localVar = new int[2];
	private string syncUrlTemp = "/inGame/{0}/?finalTimeStamp={1}&round={2}&phase={3}";

	private string key;

	private int responseCode;
	private string responseBody;

	private IEnumerator SendRequest(string uri, string method, string data=null)
	{
		UnityWebRequest www = new UnityWebRequest();
		if (method == "GET")
		{
			www = UnityWebRequest.Get(uri);
		} else if (method == "POST")
		{
			www = UnityWebRequest.Post(uri, data);
			www.SetRequestHeader("Content-Type", "application/json");
		}
		yield return www.SendWebRequest();

		responseCode = (int)www.responseCode;
		responseBody = www.downloadHandler.text;

	}

	// Use this for initialization
	void Start () {
		// Login Request
		OutgamePayload payload = new OutgamePayload();
		payload.Action = "Ready";
		payload.Target = "null";
		string payloadS = JsonUtility.ToJson(payload, false);
		StartCoroutine(SendRequest(targetURI+"/outGame/null", "POST", payloadS));
		if (responseCode == 200)
		{
			LoginRequest loadedData;
			loadedData = JsonUtility.FromJson<LoginRequest>(responseBody);
			key = loadedData.UUID;
			System.Console.WriteLine("Logged in! Your key is" + key);
		}

	}
	
	// Update is called once per frame
	void Update () {
		
	}
}
