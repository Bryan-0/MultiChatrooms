class Room:

    def __init__(self):
        self.roomList = []
    
    def readRooms(self):
        """
        Reads rooms saved in the .txt file.
        """
        with open('app/rooms.txt', 'r') as f:
            for line in f.readlines():
                self.roomList.append(line.strip())
    
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
    