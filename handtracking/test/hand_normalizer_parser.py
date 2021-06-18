import numpy as np

from unittest import TestCase

from app.handler.hand_position_parser import HandPositionParser, HandResultWrapper


class HandNormalizerParserTest(TestCase):

    def test_parse(self):

        mock = HandResultWrapper(
            1,
            1,
            "Mock",
            size=5
        )

        # Mock data (min=0 max=2)
        mock.data[0] = np.asarray([0, 1, 1])
        mock.data[1] = np.asarray([1, 1, 1])    # ref 1 (pivot)
        mock.data[2] = np.asarray([2, 1, 1])    # ref 2
        mock.data[3] = np.asarray([1, 2, 1])
        mock.data[4] = np.asarray([1, 0, 1])

        # distance expected = 1
        # desired = 0.5
        # resize (x,y,z) = (x0,y0,z0) / 2

        HandPositionParser(
            desired_scale_factor=0.5,
            joint_ref1_id=1,
            joint_ref2_id=2,
            min_xyz_value=0,
            max_xyz_value=2
        ).parse(mock)

        print(mock.data)
