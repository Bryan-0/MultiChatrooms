import random

class Room:

    def __init__(self):
        self.roomList = []
        self.roomInformation = {}
        self.colorList = ["red", "green", "blue", "purple", "maroon"]
    
    def setRandomColor(self):
        return random.choice(self.colorList)
    
    def readRooms(self):
        """
        Reads rooms saved in the .txt file and set roomInformation dict ready for each room.
        """
        with open('app/rooms.txt', 'r') as f:
            for line in f.readlines():
                self.roomList.append(line.strip())
        
        for room in self.roomList:
            self.roomInformation[room] = {'usersConnected': []}
    
    def getRoomList(self):
        """
        Returns current roomlist
        """
        return self.roomList
    
    def reloadRooms(self):
        """
        Resets rooms list and scan new rooms added.
        """
        self.roomList = []
        with open('app/rooms.txt', 'r') as f:
            for line in f.readlines():
                self.roomList.append(line.strip())
    
    def createRoom(self, roomName):
        """
        Creates a new chatroom.
        """
        with open('app/rooms.txt', 'a') as f:
            f.write("\n" + roomName)
        self.roomList.append(roomName)
        self.roomInformation[roomName] = {'usersConnected': []}
    
    def deleteRoom(self, roomName):
        """
        Deletes an existing chatroom.
        """
        currentRooms = []
        with open('app/rooms.txt', 'r') as f:
            for line in f.readlines():
                if line.strip() == roomName:
                    continue
                currentRooms.append(line.strip())

        with open('app/rooms.txt', 'w') as f:
            for room in currentRooms:
                f.write(f"{room}\n")
    
    def readRoomInformation(self, roomToRead):
        return self.roomInformation[roomToRead]
    
    def addUserToRoom(self, roomName, userName, userColor):
        self.roomInformation[roomName]['usersConnected'].append({'userName': userName, 'userColor': userColor})
    
    def removeUserFromRoom(self, roomName, userName, userColor):
        self.roomInformation[roomName]['usersConnected'].remove({'userName': userName, 'userColor': userColor})
    