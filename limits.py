import math

def degreeToRadian(degree):
    return degree * math.pi / 180

name_to_pos_limit = {
    'LHipYaw': (degreeToRadian(-30)/1.2, degreeToRadian(30)/1.2),
    'LHipPitch': (degreeToRadian(-45)/1.2, degreeToRadian(45)/1.2),
    'LHipRoll': (degreeToRadian(-30)/1.2, degreeToRadian(30)/1.2),
    'LKnee': (degreeToRadian(-90)/1.2, degreeToRadian(90)/1.2),
    'LAnklePitch': (degreeToRadian(-45)/1.2, degreeToRadian(45)/1.2),
    'LAnkleRoll': (degreeToRadian(-30)/1.2, degreeToRadian(30)/1.2),
    'RHipYaw': (degreeToRadian(-30)/1.2, degreeToRadian(30)/1.2),
    'RHipPitch': (degreeToRadian(-45)/1.2, degreeToRadian(45)/1.2),
    'RHipRoll': (degreeToRadian(-30)/1.2, degreeToRadian(30)/1.2),
    'RKnee': (degreeToRadian(-90)/1.2, degreeToRadian(90)/1.2),
    'RAnklePitch': (degreeToRadian(-45)/1.2, degreeToRadian(45)/1.2),
    'RAnkleRoll': (degreeToRadian(-30)/1.2, degreeToRadian(30)/1.2),
}

name_to_force_limit = {
    'LHipYaw': 30,
    'LHipPitch': 30,
    'LHipRoll': 30,
    'LKnee': 30,
    'LAnklePitch': 30,
    'LAnkleRoll': 30,
    'RHipYaw': 30,
    'RHipPitch': 30,
    'RHipRoll': 30,
    'RKnee': 30,
    'RAnklePitch': 30,
    'RAnkleRoll': 30,
}
