function getUserName(domain, name, callback) {
    chrome.cookies.get({"url": domain, "name": name}, function(cookie) {
        if (cookie != null && cookie.value != undefined) {
          callback(cookie.value);
        } else {
          callback(false);
        }
    });
}

function returnMessage(messageToReturn)
{
 chrome.tabs.getSelected(null, function(tab) {
  chrome.tabs.sendMessage(tab.id, {message: messageToReturn});
 });
}

chrome.extension.onRequest.addListener(function(request, sender)
{
 	getUserName("http://localhost", "username", function(username) {
 		if(username != false) {
 			returnMessage(username);
 		} else {
 			alert('Login to store this article to your News Spectrum account!')
 		}
 	})
});