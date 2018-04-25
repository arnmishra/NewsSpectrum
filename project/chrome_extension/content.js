function decideToSend() {
	validHostNames = ['www.nytimes.com', 'www.cnn.com']
	var hostname = document.location.hostname;
	var pathname = document.location.pathname;
	// check if on valid website
	// determine if it's an html file or if the pathname has more than 5 slashes which means most likely
	// an article
	if(validHostNames.includes(hostname) && (pathname.substr(pathname.length - 4) === 'html' || pathname.split('/').length >= 5)) { 
		console.log('send to server');
		return true;
	}
}

function showPrompt() {
    var txt;
    var person = prompt("Please enter your name:", "Harry Potter");
    if (person == null || person == "") {
        txt = "User cancelled the prompt.";
    } else {
        txt = "Hello " + person + "! How are you today?";
    }
    document.getElementById("demo").innerHTML = txt;
}

shouldSend = decideToSend();

if (shouldSend) {
	chrome.extension.sendRequest({message: "username_request"});
	chrome.runtime.onMessage.addListener(
	 	function(request, sender) {
	 		
	 		/*
	 		need to add the like or dislike button here
	 		and detect the click and send it in the ajax
	 		request
	 		*/
	 		var div=document.createElement("div"); 
			document.body.Child(div); 
			div.innerText="test123";

	  		username = request.message;
	  		console.log('Sending url with username: ' + username);
	  		var xhr =   $.ajax({
			        url: 'http://localhost:5000/chrome_extension',
			        type: "POST",
			        contentType: "application/json",
			        processData: false,
			        data: JSON.stringify({
			        	"username": username,
			        	"url": document.location.href
			        }),
			        success: function (response) {
			            console.log(response);
			        },
			        error: function (response) {
			            console.log(response);
			        }
	    		});
	  		console.log(xhr);
	});
}