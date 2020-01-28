using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.Text;
using System.Security.Cryptography;

public class Authorization : MonoBehaviour {
	private string path = Application.persistentDataPath;

	private void FileWrite(string name, string data)
	{
		// Create File Stream to path
		FileStream fs = new FileStream(path + "/" + name, FileMode.Create);
		// Write in binary
		byte[] bytes = new UTF8Encoding().GetBytes(data);
		fs.Write(bytes, 0, bytes.Length);
		// Close File
		fs.Close();
	}

	private string FileLoad(string name)
	{
		// Create File Stream to path
		FileStream fs = new FileStream(path + "/" + name, FileMode.Open);
		// 1588: 2048bit BASE64 RSA private key's length.
		byte[] bytes = new byte[1588];
		fs.Read(bytes, 0, bytes.Length);
		string result = new UTF8Encoding().GetString(bytes);
		fs.Close();

		return result;
	}

	private bool CheckNew()
	{
		return !(File.Exists(path + "/private.pem")
		 & File.Exists(path + "/public.pem"));
	}

	public string[] Load()
	{
		if (CheckNew() == true)
		{
			// Generate Keypair
			RSACryptoServiceProvider rsa = new RSACryptoServiceProvider();
			string publickey = rsa.ToXmlString(false);
			string privatekey = rsa.ToXmlString(true);

			FileWrite("private.pem", privatekey);
			FileWrite("public.pem", publickey);

			string[] kp = { publickey, privatekey };

			return kp;
		}
		else if (CheckNew() == false)
		{
			string publickey = FileLoad("public.pem");
			string privatekey = FileLoad("private.pem");
			string[] kp = { publickey, privatekey };

			return kp;
		}

		return new string[2];
	}
}
