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
    'LHipYaw': sim.getObject("/LHipYaw"),
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

vel_limit = 0.5
pos_limit = 0.5

t = 0
count = 0
movement_i = 0
entries = 0

def main():

    for name in name_to_joint.keys():
        set_random_force(name)

    while True:
        global t, count, entries
        t = sim.getSimulationTime()

        config_joints()

        if are_force_mode(name_to_joint.values()):
            print(f'entries: {entries}')
            print(f'movement_i: {movement_i}')
            write_positions()
            entries += 1

        count += 1
        client.step()


def config_joints():
    if are_pos_mode(name_to_joint.values()) and are_stopped(name_to_joint.values()):
        global movement_i
        movement_i += 1
        set_random_force_for_all()
        return
    for name, joint in name_to_joint.items():
        pos = sim.getJointPosition(joint)
        # hit limit
        if not (is_between(pos, name_to_pos_limit[name])):
            go_to_zero_with_pos_for_all()
            global entries
            return
        # very low force
        elif is_force_mode(joint) and very_long_time_no_force_change(name):
            set_random_force(name)

def very_long_time_no_force_change(name):
    return t - name_to_last_target_force_change[name] > max_force_not_changing_time

def is_pos_mode(joint):
    return sim.getObjectInt32Param(
            joint, sim.jointintparam_dynctrlmode) == sim.jointdynctrl_position

def go_to_zero_with_pos_for_all():
    for name, joint in name_to_joint.items():
        go_to_zero_with_pos(name)

def are_pos_mode(joints):
    for joint in joints:
        if not is_pos_mode(joint):
            return False
    return True

def are_force_mode(joints):
    return not are_pos_mode(joints)

def are_stopped(joints):
    for joint in joints:
        if not has_stopped(joint):
            return False
    return True

def is_force_mode(joint):
    return not is_pos_mode(joint)

def has_stopped(joint):
    return sim.getJointVelocity(joint) < vel_limit and sim.getJointPosition(joint) < pos_limit

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
    force = gen_force(name)
    name_to_target_force[name] = force
    sim.setJointTargetForce(joint, force)
    name_to_last_target_force_change[name] = t

def go_to_zero_with_pos(name):
    joint = name_to_joint[name]
    set_pos_mode(joint)
    sim.setJointTargetPosition(joint, 0)

def is_between(value, limits):
    return value > limits[0] and value < limits[1]

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
