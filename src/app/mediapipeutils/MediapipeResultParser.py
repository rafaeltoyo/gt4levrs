import json
from google.protobuf.json_format import MessageToDict

import mediapipe.python.solutions.hands as mp_hands


class MediapipeResultParser:

    def __init__(self):
        self.left_hand = {
            "score": 0.0,
            "joints": []
        }
        self.right_hand = {
            "score": 0.0,
            "joints": []
        }
        self._metadata = []
        self._values = []
        self._hand_index = 0
        self._joint_index = 0

    def parse(self, result):

        parsed = []

        # Expected same size
        self._metadata = result.multi_handedness
        self._values = result.multi_hand_landmarks

        for hand_handedness in result.multi_handedness:
            handedness = MessageToDict(hand_handedness)
            parsed.append({
                "index": handedness["classification"][0]["index"],
                "score": handedness["classification"][0]["score"],
                "label": handedness["classification"][0]["label"]
            })

        count = 0
        for hand_landmarks in result.multi_hand_landmarks:
            parsed[count]["joints"] = self.parse_hand(hand_landmarks)
            count += 1

        for item in parsed:
            if item["label"] == "Left":
                if item["score"] > self.left_hand["score"]:
                    self.left_hand = item
            elif item["label"] == "Right":
                if item["score"] > self.right_hand["score"]:
                    self.right_hand = item

        return json.dumps({"lhand": self.left_hand, "rhand": self.right_hand})

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
