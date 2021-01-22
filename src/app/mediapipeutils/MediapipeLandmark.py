
class MediapipeLandmark:

    def __init__(self, name, landmark):
        self.name = name
        self.x = landmark.x
        self.y = landmark.y
        self.z = landmark.z

    def __str__(self):
        return "{name};{x};{y};{z}".format(name=self.name, x=self.x, y=self.y, z=self.z)
