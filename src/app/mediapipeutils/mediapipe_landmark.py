import json

class MediapipeLandmark:

    def __init__(self, name, landmark):
        self.name = name
        self.x = landmark.x
        self.y = landmark.y
        self.z = landmark.z

    def __str__(self):
        return json.dumps(self.__dict__)
