console.log("Content script loaded");

browser.runtime.onMessage.addListener(function(msg) {
    if (msg === "req") {
        console.log("F We have a request to deliver all the words!");
        browser.runtime.sendMessage(get_words());
    } else if (msg === "req") {
        console.log("F Connected!");
    } else {
        console.log("F received: " + msg);
    }
});

function get_words() {
    var patt = /\w+/gu;
    var text = document.body.innerText;
    var res = text.match(patt);
    return res
}
