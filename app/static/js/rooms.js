var userName = "";
var currentRoom = "";

function setUserData(name) {
    userName = name;
}

function joinRoom(roomName) {
    document.getElementById('chatTitle').innerHTML = `Chatroom: ${roomName}`;
    console.log(roomName)
}

function LeaveChatRoom() {
    if (currentRoom === "") return;

    //////
}