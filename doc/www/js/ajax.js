function createRequest() {
	try {
	netscape.security.PrivilegeManager.enablePrivilege("UniversalBrowserRead");
  var request = null;
  try {
    request = new XMLHttpRequest();
  } catch (trymicrosoft) {
    try {
      request = new ActiveXObject("Msxml2.XMLHTTP");
    } catch (othermicrosoft) {
      try {
        request = new ActiveXObject("Microsoft.XMLHTTP");
      } catch (failed) {
        request = null;
      }
    }
  }
 } 
   catch (e) {
    alert("Permission UniversalBrowserRead denied.");
   }  
   
  
  if (request == null) {
    alert("Error creating request object!");
  } else {
    return request;
  }
}

var request1 = createRequest();
var request2 = createRequest();
