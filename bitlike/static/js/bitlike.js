// The websocket is global to ensure it doesn't get garbage-collected.
var ws;

function connectWebSocket()
{
    var origin = window.location.origin;
    var scheme = origin.substr(0, origin.indexOf("//") + 2);
    var netloc = origin.substr(scheme.length);
    netloc = netloc.substr(0, (netloc + "/").indexOf("/"));
    ws = new WebSocket(
        scheme === "file://" ?
        "ws://localhost:8888/websocket" :
        scheme === "http://" ?
        "ws://" + netloc + "/websocket" :
        "wss://" + netloc + "/websocket");
    var connected = false;
    ws.onopen = function() {
       console.log("WebSocket connected");
       connected = true;
    };
    ws.onmessage = function (evt) {
        var device = JSON.parse(evt.data);
        var pixels = device.display.pixels;
        var glows = ['00','1c','38','55','71','8d','aa','c6','e2','ff'];
        for (var y=0; y < 5; y++) {
            for (var x=0; x < 5; x++) {
                var val = pixels[y][x];
                val |= 0;  // Convert floating-point number to integer.
                if (val < 0) val = 0;
                if (val > 9) val = 9;
                var bg = '#' + glows[val] + '0000';
                document.getElementById('pixel'+y+x).style.background = bg;
            }
        }
    };
    ws.onclose = function() {
        // Avoid spamming the console logs when looping without connecting.
        if (connected) {
            console.log("WebSocket disconnected");
        }
        // Try again after 3 seconds.  (And again... and again...)
        setTimeout(connectWebSocket, 3000);
    };
}

connectWebSocket();
