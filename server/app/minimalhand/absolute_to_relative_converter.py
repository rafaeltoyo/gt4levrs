class CoordenateConverter:
    bones = [(0, 4, 3, 2, 1),

             (0, 8, 7, 6, 5),

             (0, 12, 11, 10, 9),

             (0, 16, 15, 14, 13),

             (0, 20, 19, 18, 17)]

    def convert_to_relative(self, absolute_coordenates):
        relative_coordenates = [0] * 21

        relative_coordenates[0] = absolute_coordenates[0]

        for finger_connections in self.bones:
            for connection in finger_connections[1:]:
                coord = absolute_coordenates[connection]

                if connection % 4 == 0:
                    last_finger_coordenates = relative_coordenates[0]
                else:
                    last_finger_coordenates = absolute_coordenates[connection + 1]

                coord_x = coord[0] - last_finger_coordenates[0]
                coord_y = coord[1] - last_finger_coordenates[1]
                coord_z = coord[2] - last_finger_coordenates[2]

                point = (coord_x, coord_y, coord_z)

                if connection != 0:
                    relative_coordenates[connection] = [point[0], point[1], point[2]]

        return relative_coordenates

    def convert_to_absolute(self, relative_coordenates):
        absolute_coordenates = [0] * 21

        absolute_coordenates[0] = relative_coordenates[0]

        for finger_connections in self.bones:
            last_finger_coordenates = (0, 0, 0)

            for connection in finger_connections:
                coord = relative_coordenates[connection]

                coord_x = round(coord[0] + last_finger_coordenates[0], 9)
                coord_y = round(coord[1] + last_finger_coordenates[1], 9)
                coord_z = round(coord[2] + last_finger_coordenates[2], 9)
                point = (coord_x, coord_y, coord_z)

                last_finger_coordenates = point

                if connection != 0:
                    absolute_coordenates[connection] = [point[0], point[1], point[2]]

        return absolute_coordenates
