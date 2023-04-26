import sys
import time
from limits import *
from zmqRemoteApi import RemoteAPIClient
import os
import random
import math
import os
from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
file_name = f'datasets/data_gen_{today}.txt'


def generateRandomBetween(min, max):
    return random.uniform(min, max)


client = RemoteAPIClient()
sim = client.getObject('sim')
client.setStepping(True)

sim.startSimulation()


LHipYaw = sim.getObject("/LHipYaw")
LHipPitch = sim.getObject("/LHipPitch")
LHipRoll = sim.getObject("/LHipRoll")
LKnee = sim.getObject("/LKnee")
LAnklePitch = sim.getObject("/LAnklePitch")
LAnkleRoll = sim.getObject("/LAnkleRoll")
RHipYaw = sim.getObject("/RHipYaw")
RHipPitch = sim.getObject("/RHipPitch")
RHipRoll = sim.getObject("/RHipRoll")
RKnee = sim.getObject("/RKnee")
RAnklePitch = sim.getObject("/RAnklePitch")
RAnkleRoll = sim.getObject("/LAnkleRoll")

name_to_joint = {
    # 'LHipYaw': LHipYaw,
    'LHipPitch': LHipPitch,
    'LHipRoll': LHipRoll,
    'LKnee': LKnee,
    'LAnklePitch': LAnklePitch,
    'LAnkleRoll': LAnkleRoll,
    # 'RHipYaw': RHipYaw,
    'RHipPitch': RHipPitch,
    'RHipRoll': RHipRoll,
    'RKnee': RKnee,
    'RAnklePitch': RAnklePitch,
    'RAnkleRoll': RAnkleRoll,
}

name_to_last_force = {
    'LHipYaw': 0,
    'LHipPitch': 0,
    'LHipRoll': 0,
    'LKnee': 0,
    'LAnklePitch': 0,
    'LAnkleRoll': 0,
    'RHipYaw': 0,
    'RHipPitch': 0,
    'RHipRoll': 0,
    'RKnee': 0,
    'RAnklePitch': 0,
    'RAnkleRoll': 0,
}

set_zero_force = False


def main():
    count = 0

    with open(file_name, 'a') as f:
        f.write('time PosLHipYaw VelLHipYaw ForLHipYaw PosLHipPitch VelLHipPitch ForLHipPitch PosLHipRoll VelLHipRoll ForLHipRoll PosLKnee VelLKnee ForLKnee PosLAnklePitch VelLAnklePitch ForLAnklePitch PosLAnkleRoll VelLAnkleRoll ForLAnkleRoll PosRHipYaw VelRHipYaw ForRHipYaw PosRHipPitch VelRHipPitch ForRHipPitch PosRHipRoll VelRHipRoll ForRHipRoll PosRKnee VelRKnee ForRKnee PosRAnklePitch VelRAnklePitch ForRAnklePitch PosRAnkleRoll VelRAnkleRoll ForRAnkleRoll')
        f.write('\n')

    client.step()
    set_random_forces()
    while True:
        client.step()
        if (count // 300 % 2 != 0):
            print('set zero forces')
            set_null_forces()
        else:
            print('set random forces')
            ensure_force_direction()

        if (count != 0):
            write_positions()
        print(
            f'count: {count}')
        count += 1


def set_random_forces():
    for name, joint in name_to_joint.items():
        force = gen_force()
        name_to_last_force[name] = force
        sim.setJointTargetForce(joint, force)


def gen_force():
    force = 1
    return generateRandomBetween(-force, force)


def ensure_force_direction():
    for name, joint in name_to_joint.items():
        limits = name_to_pos_limit[name]
        pos = sim.getJointPosition(joint)
        target_force = name_to_last_force[name]
        if not is_between(pos, limits) and is_in_same_direction(pos, target_force):
            force = abs(gen_force())
            if (pos >= limits[1]):
                force = -force
            sim.setJointTargetForce(joint, force)
            name_to_last_force[name] = force


def set_null_forces():
    for name, joint in name_to_joint.items():
        sim.setJointTargetForce(joint, 0)


def is_in_same_direction(first, second):
    if (first >= 0 and second >= 0):
        return True
    if (first < 0 and second < 0):
        return True
    return False


def is_between(value, limits):
    return value > limits[0] and value < limits[1]


def write_positions():
    PosLHipYaw = sim.getJointPosition(LHipYaw)
    VelLHipYaw = sim.getJointVelocity(LHipYaw)
    ForLHipYaw = sim.getJointForce(LHipYaw)

    PosLHipPitch = sim.getJointPosition(LHipPitch)
    VelLHipPitch = sim.getJointVelocity(LHipPitch)
    ForLHipPitch = sim.getJointForce(LHipPitch)

    PosLHipRoll = sim.getJointPosition(LHipRoll)
    VelLHipRoll = sim.getJointVelocity(LHipRoll)
    ForLHipRoll = sim.getJointForce(LHipRoll)

    PosLKnee = sim.getJointPosition(LKnee)
    VelLKnee = sim.getJointVelocity(LKnee)
    ForLKnee = sim.getJointForce(LKnee)

    PosLAnklePitch = sim.getJointPosition(LAnklePitch)
    VelLAnklePitch = sim.getJointVelocity(LAnklePitch)
    ForLAnklePitch = sim.getJointForce(LAnklePitch)

    PosLAnkleRoll = sim.getJointPosition(LAnkleRoll)
    VelLAnkleRoll = sim.getJointVelocity(LAnkleRoll)
    ForLAnkleRoll = sim.getJointForce(LAnkleRoll)

    # Right leg
    PosRHipYaw = sim.getJointPosition(RHipYaw)
    VelRHipYaw = sim.getJointVelocity(RHipYaw)
    ForRHipYaw = sim.getJointForce(RHipYaw)

    PosRHipPitch = sim.getJointPosition(RHipPitch)
    VelRHipPitch = sim.getJointVelocity(RHipPitch)
    ForRHipPitch = sim.getJointForce(RHipPitch)

    PosRHipRoll = sim.getJointPosition(RHipRoll)
    VelRHipRoll = sim.getJointVelocity(RHipRoll)
    ForRHipRoll = sim.getJointForce(RHipRoll)

    PosRKnee = sim.getJointPosition(RKnee)
    VelRKnee = sim.getJointVelocity(RKnee)
    ForRKnee = sim.getJointForce(RKnee)

    PosRAnklePitch = sim.getJointPosition(RAnklePitch)
    VelRAnklePitch = sim.getJointVelocity(RAnklePitch)
    ForRAnklePitch = sim.getJointForce(RAnklePitch)

    PosRAnkleRoll = sim.getJointPosition(RAnkleRoll)
    VelRAnkleRoll = sim.getJointVelocity(RAnkleRoll)
    ForRAnkleRoll = sim.getJointForce(RAnkleRoll)

    list = [
        sim.getSimulationTime(),

        PosLHipYaw,
        VelLHipYaw,
        ForLHipYaw,

        PosLHipPitch,
        VelLHipPitch,
        ForLHipPitch,

        PosLHipRoll,
        VelLHipRoll,
        ForLHipRoll,

        PosLKnee,
        VelLKnee,
        ForLKnee,

        PosLAnklePitch,
        VelLAnklePitch,
        ForLAnklePitch,

        PosLAnkleRoll,
        VelLAnkleRoll,
        ForLAnkleRoll,

        PosRHipYaw,
        VelRHipYaw,
        ForRHipYaw,

        PosRHipPitch,
        VelRHipPitch,
        ForRHipPitch,

        PosRHipRoll,
        VelRHipRoll,
        ForRHipRoll,

        PosRKnee,
        VelRKnee,
        ForRKnee,

        PosRAnklePitch,
        VelRAnklePitch,
        ForRAnklePitch,

        PosRAnkleRoll,
        VelRAnkleRoll,
        ForRAnkleRoll,
    ]

    with open(file_name, 'a') as f:
        line = ' '.join(str(e) for e in list)
        f.write(line)
        f.write('\n')


main()
