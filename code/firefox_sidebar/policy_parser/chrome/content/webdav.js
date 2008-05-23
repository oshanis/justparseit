var store_location = "http://dig.csail.mit.edu/2008/webdav/policy.n3"; //the default value

function store()
{
	store_location = document.getElementById("store_location").value;
	webdav.manager.register(store_location, success);
	webdav.manager.save_file(store_location, request1.responseText, fetch);
	alert("The generated policy was successfully saved at "+store_location);
}

function fetch()
{
	content.window.location.replace(store_location,true);

}

function view()
{
//	store();
	alert("The generated policy was successfully saved at "+store_location);
}

function success()
{
        //TODO: Do something on the callback?
}
