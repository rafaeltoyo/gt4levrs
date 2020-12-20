from copy import deepcopy

class CoordenateConverter:
    bones = [(0, 1, 2, 3, 4),

             (0, 5, 6, 7, 8),

             (0, 9, 10, 11, 12),

             (0, 13, 14, 15, 16),

             (0, 17, 18, 19, 20)]

    def convert_to_relative(self, absolute_coordenates):
        relative_coordenates = deepcopy(absolute_coordenates)

        for hand_index in range(len(relative_coordenates)):
            for finger_connections in self.bones:
                for connection in finger_connections[1:]:
                    coord = absolute_coordenates[hand_index].landmark[connection]

                    if connection % 4 == 0:
                        last_finger_coordenates = absolute_coordenates[hand_index].landmark[0]
                    else:
                        last_finger_coordenates = absolute_coordenates[hand_index].landmark[connection - 1]

                    coord_x = coord.x - last_finger_coordenates.x
                    coord_y = coord.y - last_finger_coordenates.y
                    coord_z = coord.z - last_finger_coordenates.z

                    if connection != 0:
                        relative_coordenates[hand_index].landmark[connection].x = coord_x
                        relative_coordenates[hand_index].landmark[connection].y = coord_y
                        relative_coordenates[hand_index].landmark[connection].z = coord_z

        return relative_coordenates

    def convert_to_absolute(self, relative_coordenates):
        absolute_coordenates = deepcopy(relative_coordenates)

        for hand_index in range(len(relative_coordenates)):
            for finger_connections in self.bones:
                last_finger_coordenates = deepcopy(relative_coordenates[hand_index].landmark[0])
                last_finger_coordenates.x = 0
                last_finger_coordenates.y = 0
                last_finger_coordenates.z = 0

                for connection in finger_connections:
                    coord = relative_coordenates[hand_index].landmark[connection]

                    print(connection)
                    coord_x = round(coord.x + last_finger_coordenates.x, 9)
                    coord_y = round(coord.y + last_finger_coordenates.y, 9)
                    coord_z = round(coord.z + last_finger_coordenates.z, 9)

                    if connection != 0:
                        absolute_coordenates[hand_index].landmark[connection].x = coord_x
                        absolute_coordenates[hand_index].landmark[connection].y = coord_y
                        absolute_coordenates[hand_index].landmark[connection].z = coord_z

                    last_finger_coordenates.x = coord_x
                    last_finger_coordenates.y = coord_y
                    last_finger_coordenates.z = coord_z

        return absolute_coordenates
