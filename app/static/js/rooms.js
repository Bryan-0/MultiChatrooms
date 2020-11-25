var userName = "";
var currentRoom = "";

function setUserData(name) {
    userName = name;
}

function joinRoom(roomName) {
    document.getElementById('chatTitle').innerHTML = `Chatroom: ${roomName}`;
    currentRoom = roomName;

    document.getElementById('chatroomsContainer').style.display = 'none';
    document.getElementById('chatContainer').style.display = 'block';
    socket.emit('userJoinedChatroom', {'roomName': roomName, 'userName': userName});

    document.getElementById('usersConnected').innerHTML += `- ${userName} <br>` 
}

function getUsersConnected(data) {
    document.getElementById('usersConnected').innerHTML = "";
    for (let user of data['userName']) {
        document.getElementById('usersConnected').innerHTML += `- <span style="background-color: gray; color: ${user['userColor']}">${user['userName']}<span> <br>`
    }
}

function LeaveChatRoom() {
    if (currentRoom === "") return;

    document.getElementById('chatContainer').style.display = 'none';
    document.getElementById('innerMessages').innerHTML = "";
    document.getElementById('chatroomsContainer').style.display = 'block';
    socket.emit('userLeftChatroom', {'roomName': currentRoom, 'userName': userName});
}

function sendUserMessage(currentUser, userMessage, toRoom) {
    if (userMessage === "") return;
    if (userMessage[0] === "/") {
        socket.emit('command', {'userName': currentUser, 'userCommand': userMessage})
        return;
    }
    socket.emit('roomMessage', {'userName': currentUser, 'userMessage': escapeHTML(userMessage), 'roomName': toRoom})
}

function showMessage(data) {
    document.getElementById('innerMessages').innerHTML += `- <strong><span style="background-color: lightgray; color: ${data['userColor']}">${data['userName']}</span></strong>: ${data['userMessage']}<br>`
}

function commandResponse(data) {
    document.getElementById('innerMessages').innerHTML += `- <strong><span style="background-color: lightgray;">${escapeHTML(data['response'])}</span></strong><br>`
}

function escapeHTML(text) {
    return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

var inputMessage = document.getElementById("inputMessage");       
inputMessage.addEventListener("keyup", function(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        sendUserMessage(userName, inputMessage.value, currentRoom);
        document.getElementById('inputMessage').value = "";
    }
});