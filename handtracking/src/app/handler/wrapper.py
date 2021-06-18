import numpy as np


########################################################################################################################

class IndexMapper:
    """
    This class maps the pose detection framework indices.
    """

    def __init__(self):
        """
        Basic index mapper
        """
        pass

    def map(self, index: int):
        """
        This method converts framework index to application index.
        The basic implementation just returns the original index.
        If a custom behaviour is needed then implements a child and set into result wrapper.

        Parameters
        ----------
        index Framework index

        Returns
        -------
        Application index
        """
        return index


########################################################################################################################

class ResultWrapper:
    """
    This class wraps joints.
    """

    def __init__(self,
                 size: int = 21,
                 index_mapper: IndexMapper = IndexMapper()):
        """

        Parameters
        ----------
        size
        index_mapper
        """
        self._size = size

        self.data = np.zeros((size, 3)).astype("float32")
        self.names = [""] * size
        self.index_mapper = index_mapper

    def add(self, name: str, idx: int, x, y, z):
        idx = self.index_mapper.map(idx)

        if not (0 <= idx < self._size):
            raise RuntimeError("Invalid index {}!".format(idx))

        self.names[idx] = name
        self.data[idx][0] = x
        self.data[idx][1] = y
        self.data[idx][2] = z

    def json(self):
        return [self._joint_json(idx) for idx in range(len(self.names))]

    def _joint_json(self, idx: int):
        idx = self.index_mapper.map(idx)

        if not (0 <= idx < self._size):
            raise RuntimeError("Invalid index {}!".format(idx))

        return {
            "name": self.names[idx],
            "x": float(self.data[idx][0]),
            "y": float(self.data[idx][1]),
            "z": float(self.data[idx][2])
        }


########################################################################################################################

class HandResultWrapper(ResultWrapper):
    """
    Wrapper for Hand information.
    """

    def __init__(self,
                 index: int,
                 score: float,
                 label: str,
                 size: int = 21,
                 index_mapper: IndexMapper = IndexMapper()):
        """

        Parameters
        ----------
        index
        score
        label
        size
        index_mapper
        """
        super().__init__(size, index_mapper)
        self._index = index
        self._score = score
        self._label = label

    def is_left(self):
        return self._label.startswith("Left")

    def is_right(self):
        return self._label.startswith("Right")

    def greater_then(self, target):
        return isinstance(target, HandResultWrapper) and self._score > target._score

    def json(self):
        return {
            "index": self._index,
            "score": self._score,
            "label": self._label,
            "joints": super().json()
        }


class BodyResultWrapper(ResultWrapper):
    """
    Wrapper for Body information.
    """

    _left_hand: HandResultWrapper
    _right_hand: HandResultWrapper

    def __init__(self,
                 size: int = 21,
                 index_mapper: IndexMapper = IndexMapper()):
        """

        Parameters
        ----------
        index
        score
        label
        size
        index_mapper
        """
        super().__init__(size, index_mapper)
        self._left_hand = None
        self._right_hand = None

    def set_left_hand(self, left_hand: HandResultWrapper):
        self._left_hand = left_hand

    def set_right_hand(self, right_hand: HandResultWrapper):
        self._right_hand = right_hand

    def json(self):
        json = {}
        if self._left_hand or self._right_hand:
            json['hand_results'] = self._hands_json()
        json['body_results'] = super().json()
        return json

    def _hands_json(self):
        return {
            'lhand': self._left_hand.json() if self._left_hand else None,
            'rhand': self._right_hand.json() if self._right_hand else None
        }


########################################################################################################################
