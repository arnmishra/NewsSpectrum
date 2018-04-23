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

shouldSend = decideToSend();

if (shouldSend) {
	chrome.extension.sendRequest({message: "username_request"});
	chrome.runtime.onMessage.addListener(
	 	function(request, sender) {
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