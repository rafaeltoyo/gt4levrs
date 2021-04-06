from google.protobuf.json_format import MessageToDict
import mediapipe.python.solutions.hands as mp_hands


class HandPoseResultParser:

    def __init__(self):
        self.left_hand = {
            "score": 0.0,
            "joints": []
        }
        self.right_hand = {
            "score": 0.0,
            "joints": []
        }

    def parse(self, result):
        hand_data = result.multi_hand_landmarks
        if not hand_data:
            return {}

        parsed = []

        for hand_handedness in result.multi_handedness:
            handedness = MessageToDict(hand_handedness)
            parsed.append({
                "index": handedness["classification"][0]["index"],
                "score": handedness["classification"][0]["score"],
                "label": handedness["classification"][0]["label"]
            })

        for index in range(len(hand_data)):
            parsed[index]["joints"] = self.parse_hand(hand_data[index])

        for item in parsed:
            if item["label"] == "Left":
                if item["score"] > self.left_hand["score"]:
                    self.left_hand = item
            elif item["label"] == "Right":
                if item["score"] > self.right_hand["score"]:
                    self.right_hand = item

        return {"lhand": self.left_hand, "rhand": self.right_hand}

    def parse_hand(self, hand_landmarks):
        values = []

        for landmark in hand_landmarks.landmark:
            item = {
                "name": mp_hands.HandLandmark(len(values)).name,
                "x": landmark.x,
                "y": landmark.y,
                "z": landmark.z
            }

            values.append(item)

        return values
