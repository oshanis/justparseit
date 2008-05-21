//////////////////////////////
// UI Specific Functions

function predefined()
{
	if (document.getElementById("sentence_pref").value == "0")
	{
		document.getElementById("sentence_text").disabled = true;
		document.getElementById("sentence_menu").disabled = false;
		new_sentence_flag = false;
	}
	if (document.getElementById("sentence_pref").value == "1")
	{
		document.getElementById("sentence_text").disabled = false;
		document.getElementById("sentence_menu").disabled = true;
		new_sentence_flag = true;
	}
}

/////////////////////////////


/////////////////////////////
// Request stuff

var request1= Util.XMLHTTPFactory();


function sendRequest(request, url) 
{
	try 
	{
		request.open("GET", url, true);
		request.onreadystatechange = update;
		request.send(null);
	} 
	catch(e) 
	{
		alert(e)
	}
}

function run() 
{
	var name = document.getElementById("name").value;
	var sentence = null
	
	if (document.getElementById("sentence_pref").value == "0"
		|| document.getElementById("sentence_pref").value == ""
		|| document.getElementById("sentence_pref").value == null)
	{
		sentence =document.getElementById("sentence_menu").value; 
	}
	else
	{
		sentence =document.getElementById("sentence_text").value; 
	}
	
	var domain = document.getElementById("domain").value;
  
	if (name != "")
	{
		var url = "http://scripts.mit.edu/~oshani/justparseit/code/server/run.py?name=" + escape(name) +"&sentence=" + escape(sentence) +"&domain=" + escape(domain);
		sendRequest(request1, url);
		content.window.location.replace(url,true);
	}
	else
	{
		alert("Please give a name for the policy!");
	}

}

function update() 
{
  if (request1.readyState == 4) {
    if (request1.status == 200) {
		var response = request1.responseText;
    } 
	else 
      alert("Error! Something is wrong.");
  } 
}
