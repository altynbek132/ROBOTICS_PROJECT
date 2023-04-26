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

client = RemoteAPIClient()
sim = client.getObject('sim')
client.setStepping(True)
sim.startSimulation()

name_to_joint = {
    # 'LHipYaw': sim.getObject("/LHipYaw"),
    'LHipPitch': sim.getObject("/LHipPitch"),
    'LHipRoll': sim.getObject("/LHipRoll"),
    'LKnee': sim.getObject("/LKnee"),
    'LAnklePitch': sim.getObject("/LAnklePitch"),
    'LAnkleRoll': sim.getObject("/LAnkleRoll"),
    # 'RHipYaw': sim.getObject("/RHipYaw"),
    # 'RHipPitch': sim.getObject("/RHipPitch"),
    # 'RHipRoll': sim.getObject("/RHipRoll"),
    # 'RKnee': sim.getObject("/RKnee"),
    # 'RAnklePitch': sim.getObject("/RAnklePitch"),
    # 'RAnkleRoll': sim.getObject("/LAnkleRoll"),
}

name_to_target_force = dict.fromkeys(name_to_joint.keys(), 0)

name_to_last_target_force_change = dict.fromkeys(name_to_joint.keys(), 0)

max_force_not_changing_time = 1

last_time_joints_reset = 0

vel_limit = degreeToRadian((45*4)/5)

t = 0
count = 0
movement_i = 0
entries = 0


def main():

    for name in name_to_joint.keys():
        set_random_force(name)
        client.step()

    while True:
        global t, count, entries
        t = sim.getSimulationTime()

        # print count
        # print(f'count: {count}')
        config_joints()

        if are_force_mode(name_to_joint.values()):
            print(f'entries: {entries}')
            # print(f'movement_i: {movement_i}')
            write_positions()
            entries += 1

        count += 1
        client.step()


def config_joints():
    global last_time_joints_reset

    if are_pos_mode(name_to_joint.values()):
        if (t - last_time_joints_reset) > 1:
            set_random_force_for_all()
        if slowed_down(name_to_joint.values()) and are_all_joints_in_limits():
            global movement_i
            movement_i += 1
            print('* new movement *')
            set_random_force_for_all()
        return
    for name, joint in name_to_joint.items():
        pos = sim.getJointPosition(joint)
        # hit limit
        if not (is_between(pos, name_to_pos_limit[name], reserve_fraction=0.1)):
            print(f'* {name} exceeded limit pos:{radianToDegree(pos)} *')
            reset_all_joints()
            last_time_joints_reset = t
            return
        # very low force
        elif is_force_mode(joint) and very_long_time_no_force_change(name):
            set_random_force(name)

def are_all_joints_in_limits():
    for name, joint in name_to_joint.items():
        pos = sim.getJointPosition(joint)
        if not (is_between(pos, name_to_pos_limit[name], reserve_fraction=0.2)):
            return False
    return True

def very_long_time_no_force_change(name):
    return t - name_to_last_target_force_change[name] > max_force_not_changing_time


def is_pos_mode(joint):
    return sim.getObjectInt32Param(
        joint, sim.jointintparam_dynctrlmode) == sim.jointdynctrl_position


def reset_all_joints():
    for name, joint in name_to_joint.items():
        reset_joint(name)


def are_pos_mode(joints):
    for joint in joints:
        if not is_pos_mode(joint):
            return False
    return True


def are_force_mode(joints):
    return not are_pos_mode(joints)


def slowed_down(joints):
    for joint in joints:
        if not has_stopped(joint):
            return False
    return True


def is_force_mode(joint):
    return not is_pos_mode(joint)


def has_stopped(joint):
    return abs(sim.getJointVelocity(joint)) < vel_limit


def set_pos_mode(joint):
    sim.setObjectInt32Param(
        joint, sim.jointintparam_dynctrlmode, sim.jointdynctrl_position)


def set_force_mode(joint):
    sim.setObjectInt32Param(
        joint, sim.jointintparam_dynctrlmode, sim.jointdynctrl_force)


def set_random_force_for_all():
    for name in name_to_joint.keys():
        set_random_force(name)


def set_random_force(name):
    joint = name_to_joint[name]
    set_force_mode(joint)
    pos = sim.getJointPosition(joint)
    force = gen_force(name)
    if (pos < 0 and force < 0) or (pos > 0 and force > 0):
        force = -force
    name_to_target_force[name] = force
    sim.setJointTargetForce(joint, force)
    name_to_last_target_force_change[name] = t



def reset_joint(name):
    joint = name_to_joint[name]
    set_pos_mode(joint)
    pos = sim.getJointPosition(joint)
    # sim.setJointTargetVelocity(joint, vel_limit/2)
    sim.setJointTargetPosition(joint, min_pos(pos, name_to_pos_limit[name], reserve_fraction=0.3))

def min_pos(pos, limits, reserve_fraction=0):
    limits = [limits[0]*(1-reserve_fraction), limits[1]*(1-reserve_fraction)]
    if pos < 0:
        if abs(pos) > abs(limits[0]):
            return limits[0]
        return pos
    if pos > limits[1]:
        return limits[1]
    return pos

def is_between(value, limits, reserve_fraction=0):
    return value > limits[0]*(1-reserve_fraction) and value < limits[1]*(1-reserve_fraction)


def gen_force(joint_name):
    force = name_to_force_limit[joint_name]
    return generateRandomBetween(-force, force)


def write_positions():
    def write_header():
        with open(file_name, 'a') as f:
            names = name_to_joint.keys()
            l = ['time']
            for name in names:
                l.append(f'Pos{name}')
                l.append(f'Vel{name}')
                l.append(f'For{name}')
            f.write(' '.join(l))
            f.write('\n')

    if not os.path.exists('datasets'):
        os.makedirs('datasets')

    file_name = f'datasets/data_gen_{today}-{movement_i}.txt'

    l = [t]
    for joint in name_to_joint.values():
        l.append(sim.getJointPosition(joint))
        l.append(sim.getJointVelocity(joint))
        l.append(sim.getJointForce(joint))

    with open(file_name, 'a') as f:
        if os.stat(file_name).st_size == 0:
            write_header()
        line = ' '.join(str(e) for e in l)
        f.write(line)
        f.write('\n')


def generateRandomBetween(min, max):
    return random.uniform(min, max)


if __name__ == '__main__':
    main()
