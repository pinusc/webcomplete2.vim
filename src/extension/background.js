/*
 On startup, connect to the "ping_pong" app.
 */
var port = browser.runtime.connectNative("webcomplete");

/*
 Listen for messages from the app.
 */
port.onMessage.addListener((response) => {
    console.log("BA Received: " + response);
    // var sending = browser.tabs.sendMessage(1, "Received: " + response);
});

port.onDisconnect.addListener((response) => {
    // var sending = browser.tabs.sendMessage(1, "Disconnect. ");
    console.log("BA Disconnect");
});


/*
 On a click on the browser action, send the app a message.
 */
browser.browserAction.onClicked.addListener(() => {
    var sending = browser.tabs.sendMessage(1, "req");
});

browser.runtime.onMessage.addListener(function(msg) {
    if (Array.isArray(msg)) {
        port.postMessage(msg);
    } else if (typeof msg === "object") {
        console.log(msg);
    } else {
        console.log("BF received: " + msg);
    }
});

browser.tabs.onUpdated.addListener((tabId, changeInfo, tabInfo) => {
    var sending = browser.tabs.sendMessage(tabId, "req");
});
