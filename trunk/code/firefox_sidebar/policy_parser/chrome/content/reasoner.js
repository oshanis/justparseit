var request2= Util.XMLHTTPFactory(); //for the reasoner
var request3= Util.XMLHTTPFactory(); //for the log
var logData = null;

function fetchLog()
{
	var log = document.getElementById("log").value;
	try 
	{
		request3.open("GET", log, true);
		request3.onreadystatechange = getLogData;
		request3.send(null);
	}
	catch(e)
	{
		alert(e);
	}
}

function reasoner()
{
	var policyData = request1.responseText;

	if (logData != "" && policyData != "")
	{
		var url = "http://mr-burns.w3.org/cgi-bin/server_cgi.py";
		var params = "log=" + escape(logData) +"&policy=" + escape(policyData);
		sendReasonerRequest(url,params);
//		content.window.document.replace(url,true);
	}
	else
	{
		alert("Please give the log and the policy!");
	}

}

function sendReasonerRequest(url,params) 
{
	try 
	{
		request2.onreadystatechange = updateResult;
		request2.open("POST", url, true);
		request2.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
		request2.setRequestHeader("Content-length", params.length);
		request2.setRequestHeader("Connection", "close");
		request2.send(params);
	} 
	catch(e) 
	{
		alert(e)
	}
}

function updateResult() 
{
  if (request2.readyState == 4) {
    if (request2.status == 200) {
		var response = request2.responseText;
		content.document.write("<pre>"+response+"</pre>");
    } 
	else 
      alert(request2.status);
  } 
}

function getLogData()
{
  if (request3.readyState == 4) {
    if (request3.status == 200) {
		logData = request3.responseText;
		alert("Log file successfully fetched!");
    } 
	else 
      alert("Log file missing?");
  } 
}