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
file_name = f'datasets_no_t_gen/data_gen_{today}.txt'

def generateRandomAngleBetween(min, max):
    return random.uniform(min, max)


client = RemoteAPIClient()
sim = client.getObject('sim')
client.setStepping(True)

sim.stopSimulation()
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
    'LHipYaw': LHipYaw,
    'LHipPitch': LHipPitch,
    'LHipRoll': LHipRoll,
    'LKnee': LKnee,
    'LAnklePitch': LAnklePitch,
    'LAnkleRoll': LAnkleRoll,
    'RHipYaw': RHipYaw,
    'RHipPitch': RHipPitch,
    'RHipRoll': RHipRoll,
    'RKnee': RKnee,
    'RAnklePitch': RAnklePitch,
    'RAnkleRoll': RAnkleRoll,
}


def main():
    count = 0

    with open(file_name, 'a') as f:
        f.write('time PosLHipYaw VelLHipYaw ForLHipYaw PosLHipPitch VelLHipPitch ForLHipPitch PosLHipRoll VelLHipRoll ForLHipRoll PosLKnee VelLKnee ForLKnee PosLAnklePitch VelLAnklePitch ForLAnklePitch PosLAnkleRoll VelLAnkleRoll ForLAnkleRoll PosRHipYaw VelRHipYaw ForRHipYaw PosRHipPitch VelRHipPitch ForRHipPitch PosRHipRoll VelRHipRoll ForRHipRoll PosRKnee VelRKnee ForRKnee PosRAnklePitch VelRAnklePitch ForRAnklePitch PosRAnkleRoll VelRAnkleRoll ForRAnkleRoll')
        f.write('\n')

    while True:
        if (count != 0):
            for name, joint in name_to_joint.items():
                force = sim.getJointForce(joint);
                print(f'{name}: {force}')
        if (count%700 == 0):
            set_positions()
        if (count != 0):
            write_positions()
        print(
            f'sim time: {sim.getSimulationTime()}, lines: {count}')
        client.step()
        count += 1


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


LHipYawMax = degreeToRadian(30)
LHipPitchMax = degreeToRadian(45)
LHipRollMax = degreeToRadian(30)
LKneeMax = degreeToRadian(90)
LAnklePitchMax = degreeToRadian(45)
LAnkleRollMax = degreeToRadian(30)
RHipYawMax = degreeToRadian(30)
RHipPitchMax = degreeToRadian(45)
RHipRollMax = degreeToRadian(30)
RKneeMax = degreeToRadian(90)
RAnklePitchMax = degreeToRadian(45)
RAnkleRollMax = degreeToRadian(30)

# min
LHipYawMin = -LHipYawMax
LHipPitchMin = -LHipPitchMax
LHipRollMin = -LHipRollMax
LKneeMin = -LKneeMax
LAnklePitchMin = -LAnklePitchMax
LAnkleRollMin = -LAnkleRollMax
RHipYawMin = -RHipYawMax
RHipPitchMin = -RHipPitchMax
RHipRollMin = -RHipRollMax
RKneeMin = -RKneeMax
RAnklePitchMin = -RAnklePitchMax
RAnkleRollMin = -RAnkleRollMax

def set_positions():
    sim.setJointTargetPosition(
        LHipYaw, generateRandomAngleBetween(LHipYawMin, LHipYawMax))
    sim.setJointTargetPosition(
        LHipPitch, generateRandomAngleBetween(LHipPitchMin, LHipPitchMax))
    sim.setJointTargetPosition(
        LHipRoll, generateRandomAngleBetween(LHipRollMin, LHipRollMax))
    sim.setJointTargetPosition(
        LKnee, generateRandomAngleBetween(LKneeMin, LKneeMax))
    sim.setJointTargetPosition(
        LAnklePitch, generateRandomAngleBetween(LAnklePitchMin, LAnklePitchMax))
    sim.setJointTargetPosition(
        LAnkleRoll, generateRandomAngleBetween(LAnkleRollMin, LAnkleRollMax))
    sim.setJointTargetPosition(
        RHipYaw, generateRandomAngleBetween(RHipYawMin, RHipYawMax))
    sim.setJointTargetPosition(
        RHipPitch, generateRandomAngleBetween(RHipPitchMin, RHipPitchMax))
    sim.setJointTargetPosition(
        RHipRoll, generateRandomAngleBetween(RHipRollMin, RHipRollMax))
    sim.setJointTargetPosition(
        RKnee, generateRandomAngleBetween(RKneeMin, RKneeMax))
    sim.setJointTargetPosition(
        RAnklePitch, generateRandomAngleBetween(RAnklePitchMin, RAnklePitchMax))
    sim.setJointTargetPosition(
        RAnkleRoll, generateRandomAngleBetween(RAnkleRollMin, RAnkleRollMax))


try:
    main()
finally:
    print('shutdown...')
    sim.stopSimulation()
