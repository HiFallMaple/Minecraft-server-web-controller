$(document).ready(function () {
    // Socket.IO Start connect
    var socket = io.connect();


    // Socket.IO send message
    $("#send").click(function (e) {
        // Send message
        socket.emit('send', $('#message').val())
        // Clear input field
        $('#message').val('')
    });

    // Socket.IO get message
    socket.on('get', function (data) {
        console.log(`get: ${data}`)
    });

    // Socket.IO get test
    socket.on("message", function (data) {
        console.log(`message: ${data}`)
    });

    // Socket.IO send test
    $("#test").click(function (e) {
        socket.emit('test')
    });
})