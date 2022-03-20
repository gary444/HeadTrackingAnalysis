import csv
import cv2 as cv
import numpy as np
import math 
from enum import Enum
from pyquaternion import Quaternion
import unittest


def angle_between_quaternions(q1,q2):

    q1 = q1.normalised
    q2 = q2.normalised
    qd = q1.conjugate * q2

    return qd.angle


class TestSum(unittest.TestCase):

    def test_angle(self):

        q1 = Quaternion(axis=[1, 0, 0], degrees=30)
        q2 = Quaternion(axis=[1, 0, 0], degrees=60)
        self.assertAlmostEqual(math.degrees(angle_between_quaternions(q1,q2)), 30)

        q1 = Quaternion(axis=[0.9,0.4,0.1], degrees=10.5)
        q2 = Quaternion(axis=[0.9,0.4,0.1], degrees=32.5)
        self.assertAlmostEqual(math.degrees(angle_between_quaternions(q1,q2)), 22)


if __name__ == '__main__':
    unittest.main()