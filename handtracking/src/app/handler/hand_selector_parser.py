from typing import List, Optional

from handtracking.src.app.handler.wrapper import HandResultWrapper, BodyResultWrapper


class HandSelectorParser:

    def parse(self,
              hands: List[HandResultWrapper],
              body: Optional[BodyResultWrapper] = None):
        """
        Select the most accurate hands.

        Parameters
        ----------
        hands
        body

        Returns
        -------
        The best left and right hand
        """
        left_hand: HandResultWrapper = None
        right_hand: HandResultWrapper = None

        for hand in hands:
            if hand.is_left():
                if left_hand is None or hand.greater_then(left_hand):
                    left_hand = hand
            elif hand.is_right():
                if right_hand is None or hand.greater_then(right_hand):
                    right_hand = hand

        if body:
            body.set_left_hand(left_hand)
            body.set_right_hand(right_hand)
        return left_hand, right_hand
