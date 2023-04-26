import math


def degreeToRadian(degree):
    return degree * math.pi / 180


def radianToDegree(radian):
    return radian * 180 / math.pi


name_to_pos_limit = {
    "LHipYaw": (degreeToRadian(-30), degreeToRadian(30)),
    "LHipPitch": (degreeToRadian(-45), degreeToRadian(45)),
    "LHipRoll": (degreeToRadian(-30), degreeToRadian(30)),
    "LKnee": (degreeToRadian(-90), degreeToRadian(90)),
    "LAnklePitch": (degreeToRadian(-45), degreeToRadian(45)),
    "LAnkleRoll": (degreeToRadian(-30), degreeToRadian(30)),
    "RHipYaw": (degreeToRadian(-30), degreeToRadian(30)),
    "RHipPitch": (degreeToRadian(-45), degreeToRadian(45)),
    "RHipRoll": (degreeToRadian(-30), degreeToRadian(30)),
    "RKnee": (degreeToRadian(-90), degreeToRadian(90)),
    "RAnklePitch": (degreeToRadian(-45), degreeToRadian(45)),
    "RAnkleRoll": (degreeToRadian(-30), degreeToRadian(30)),
}

name_to_force_limit = {
    "LHipYaw": 2.5,
    "LHipPitch": 3,
    "LHipRoll": 14,
    "LKnee": 10,
    "LAnklePitch": 2.5,
    "LAnkleRoll": 2.5,
    # 'RHipYaw': 14,
    # 'RHipPitch': 14,
    # 'RHipRoll': 14,
    # 'RKnee': 14,
    # 'RAnklePitch': 14,
    # 'RAnkleRoll': 14,
}
