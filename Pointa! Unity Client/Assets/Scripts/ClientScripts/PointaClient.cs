using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class PointaClient : MonoBehaviour {
	public string targetURI;
	public GameObject ViewController;

	[SerializeField]
	private int[] localVar = new int[2];
	private string syncUrlTemp = "/inGame/{0}/?finalTimeStamp={1}&round={2}&phase={3}";

	private string[] keyPair;
	private Authorization auth;

	private IEnumerator SendRequest(string uri, string method, string data=null)
	{
		UnityWebRequest www;
		if (method == "GET")
		{
			www = UnityWebRequest.Get(uri);
		} else if (method == "POST")
		{
			www = UnityWebRequest.Post(uri, data);
		}
		www.SetRequestHeader("Content-Type", "application/json");
		yield return www.SendWebRequest();

	}

	// Use this for initialization
	void Start () {
		keyPair = auth.Load();
		
	}
	
	// Update is called once per frame
	void Update () {
		
	}
}
