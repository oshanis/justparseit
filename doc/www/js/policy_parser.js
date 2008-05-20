function createRequest() {
  var request = null;
  try 
  {
	netscape.security.PrivilegeManager.enablePrivilege('UniversalBrowserRead');
	request = new XMLHttpRequest();
  } 
  catch (trymicrosoft) 
  {
    try 
	{
      request = new ActiveXObject("Msxml2.XMLHTTP");
    } 
	catch (othermicrosoft) 
	{
      try 
	  {
        request = new ActiveXObject("Microsoft.XMLHTTP");
      } 
	  catch (failed) 
	  {
        request = null;
      }
    }
  }

  
  if (request == null) {
    alert("Error creating request object!");
  } 
  else {
    return request;
  }
}

function sendRequest(request, url) {
	try 
	{
		netscape.security.PrivilegeManager.enablePrivilege('UniversalBrowserRead');
		request.open("GET", url, true);
		request.onreadystatechange = update;
		request.send(null);
	} 
	catch(e) 
	{
		alert(e)
	}
}

function parse() {

  var name = document.getElementById("name").value;
  var sentence = document.getElementById("sentence").value;
  var domain = document.getElementById("domain").value;

  var status_div = 
   document.getElementById("status");
  /* var status = getText(status_div);
  if (status == "") {
  
    replaceText(status_div, "Running Policy Parser to generate ..." +
                name + " AIR policy");
  */
    var url = "http://scripts.mit.edu/~oshani/justparseit/code/server/run.py?name=" + escape(name) +"&sentence=" + escape(sentence) +"&domain=" + escape(domain);
	var request1 = createRequest();
	sendRequest(request1, url);
  /*}
  else {
      alert("Sorry! Wait till the sentence parses");
  }*/
}

function update() {
  if (request1.readyState == 4) {
    if (request1.status == 200) {
		var response = request1.responseText;
		var status_div = document.getElementById("status");
		replaceText(status_div, "");
		alert(name + " AIR Policy Parsed");
		request1 = createRequest();
    } 
	else 
      alert("Error! Request status is " + request1.status);
  } 
}

function replaceText(el, text) {
  if (el != null) {
    clearText(el);
    var newNode = document.createTextNode(text);
    el.appendChild(newNode);
  }
}

function clearText(el) {
  if (el != null) {
    if (el.childNodes) {
      for (var i = 0; i < el.childNodes.length; i++) {
        var childNode = el.childNodes[i];
        el.removeChild(childNode);
      }
    }
  }
}

function getText(el) {
  var text = "";
  if (el != null) {
    if (el.childNodes) {
      for (var i = 0; i < el.childNodes.length; i++) {
        var childNode = el.childNodes[i];
        if (childNode.nodeValue != null) {
          text = text + childNode.nodeValue;
        }
      }
    }
  }
  return text;
}