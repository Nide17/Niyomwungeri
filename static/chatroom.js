document.addEventListener('DOMContentLoaded', () => {

    // Connect websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // configure button
    socket.on('connect', () => {

        // Tell the server that the user has joined
        socket.emit('entered');

        // Forget user's last chatroom when you try to create new chatroom
        document.querySelector('#newChannel').addEventListener('click', () => {
            localStorage.removeItem('last_channel');
        });

        // When user leaves chatroom redirect to '/'
        document.querySelector('#leave').addEventListener('click', () => {

            // Notify the server user has left
            socket.emit('left');

            localStorage.removeItem('last_channel');
            window.location.replace('/');
        })

        // Forget user's last chatroom when logged out
        document.querySelector('#logout').addEventListener('click', () => {
            localStorage.removeItem('last_channel');
        });

        // use 'Enter' key to send a message
        document.querySelector('#comment').addEventListener("keydown", event => {
            if (event.key == "Enter") {
                document.getElementById("send-button").click();
            }
        });

        // use 'Enter' key to send a photo
        document.querySelector('#exampleFormControlFile1').addEventListener("keydown", event => {
            if (event.key == "Enter") {
                document.getElementById("send-button").click();
            }
        });
        
        // Send button emits a "message sent" event
        document.querySelector('#send-button').addEventListener("click", () => {
            
            // Save time in format HH:MM:SS
            let timestamp = new Date;
            timestamp = timestamp.toLocaleTimeString();

            // Save user input
            let msg = document.getElementById("comment", "exampleFormControlFile1").value;
            
            socket.emit('send message', msg, timestamp);
            
            
            // empty the input field
            document.getElementById("comment", "exampleFormControlFile1").value = '';
            
        });
    });
    
    // When user joins a chatroom, give message about him/her.
    socket.on('status', data => {

        // send message of joined user.
        let row =  `${data.msg}` + 'now'
        document.querySelector('#chat').value += row + '\n';

        // Save user's current chatroom on localStorage
        localStorage.setItem('last_channel', data.channel)
    })

    // When a message is announced, add it to the textarea.
    socket.on('announce message', data => {

        // Format the message
        let row = `${data.timestamp}` + '- ' + '' + `${data.user}` + ' said: ' + '\n' + `${data.msg}`
        document.querySelector('#chat').value += row + '\n'
    })

    
});