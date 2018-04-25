function addButtonsToPage(bodyClassName) {
	var elems = document.getElementsByClassName(bodyClassName);

	var arr = Array.from(elems);
	console.log(arr);
	var articleBody = arr.pop();

	console.log('Got article body: ');
	console.log(articleBody);

	var likeBtn = document.createElement("BUTTON");
	var likeText = document.createTextNode("Like Article");
	likeBtn.appendChild(likeText);

	var dislikeBtn = document.createElement("BUTTON");
	var dislikeText = document.createTextNode("Dislike Article");
	dislikeBtn.appendChild(dislikeText);

	console.log('After creating like and dislike buttons');

	articleBody.appendChild(likeBtn);
	articleBody.appendChild(dislikeBtn);

	console.log('After appending buttons to article body');
}

function decideToSend() {
	validHostNames = ['www.nytimes.com', 'www.cnn.com']
	var hostname = document.location.hostname;
	var pathname = document.location.pathname;
	// check if on valid website
	// determine if it's an html file or if the pathname has more than 5 slashes which means most likely
	// an article
	if(validHostNames.includes(hostname) && (pathname.substr(pathname.length - 4) === 'html' || pathname.split('/').length >= 5)) {
		switch(hostname) {
			case validHostNames[0]:
				console.log('NYT');
				addButtonsToPage('story-body-supplemental');
				break;

			case validHostNames[1]:
				console.log('CNN!');
				addButtonsToPage('zn-body__read-all');
				break;

			default:
				console.log('Page other than NYT/CNN?');
		}

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