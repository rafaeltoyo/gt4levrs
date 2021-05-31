from google.protobuf.json_format import MessageToDict
import mediapipe.python.solutions.hands as mp_hands
from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmarkList

from src.app.mediapipeutils.mediapipe_result_normalizer import MediapipeResultNormalizer


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
        self.normalizer = MediapipeResultNormalizer()

    def reset_hands(self):
        self.left_hand = {
            "score": 0.0,
            "joints": []
        }
        self.right_hand = {
            "score": 0.0,
            "joints": []
        }

    def parse_and_normalize(self, result):
        parsed_result = self.parse(result)
        normalized_z_hand_result = self.normalizer.scale_z_coordenate(parsed_result)
        normalized_xyz_hand_result = self.normalizer.scale_xy_coordinate(normalized_z_hand_result)
        return normalized_xyz_hand_result

    def parse(self, result):
        self.reset_hands()

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
