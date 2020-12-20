from unittest import TestCase

from src.app.minimalhand.absolute_to_relative_converter import CoordenateConverter


class TestCoordenateConverter(TestCase):
    def test_convert_to_relative(self):
        coordenates = [[1.27597041e-02, 9.41501141e-01, 1.00139499e-01],
                       [-2.34609812e-01, 6.20229602e-01, 1.83042407e-01],
                       [-5.01167357e-01, 3.94060999e-01, 4.02991921e-02],
                       [-6.99572623e-01, 2.32226282e-01, -5.26629239e-02],
                       [-1.00056851e+00, -1.28933206e-01, -1.21166535e-01],
                       [-2.46091962e-01, 5.22544608e-02, -1.55043518e-02],
                       [-2.85253227e-01, -3.42651010e-01, -2.46661380e-01],
                       [-3.93070698e-01, -6.05078578e-01, -2.76089132e-01],
                       [-4.16778684e-01, -8.46302330e-01, -2.25474626e-01],
                       [-1.45308721e-09, 7.21926074e-09, -2.33334996e-09],
                       [-8.42270926e-02, -4.50516552e-01, -1.15868330e-01],
                       [-1.10038094e-01, -7.33366787e-01, -2.11645275e-01],
                       [-1.38610885e-01, -1.02814829e+00, -2.02106297e-01],
                       [1.68927386e-01, -9.39629972e-04, -1.34856263e-02],
                       [1.82951182e-01, -4.13838357e-01, -2.87785120e-02],
                       [1.11523606e-01, -7.52275407e-01, -3.10091302e-04],
                       [1.05317995e-01, -8.82876515e-01, -8.58452320e-02],
                       [3.66755933e-01, 1.09025486e-01, -1.77965045e-01],
                       [5.02578020e-01, -2.48430163e-01, -1.65026024e-01],
                       [4.91339743e-01, -2.75196433e-01, -9.33910683e-02],
                       [5.60323000e-01, -4.01352644e-01, -1.90445967e-02]]

        converter = CoordenateConverter()

        relative_coordenates = converter.convert_to_relative(absolute_coordenates=coordenates)

        absolute2_coordenates = converter.convert_to_absolute(relative_coordenates)

        print(coordenates)
        print(relative_coordenates)
        print(absolute2_coordenates)
