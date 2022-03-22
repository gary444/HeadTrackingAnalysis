
import csv
import cv2 as cv
import numpy as np
import math 
from enum import Enum
from pyquaternion import Quaternion


data_base_path="data/AUD_APMR202201_test/tracking/formatted/"
num_dyads=9
num_trials=3

output_path="data/head_movement_analysis.csv"

class Recording(object):
    def __init__(self):
        super(Recording, self).__init__()
        self.head_positions = []
        self.head_rotations = []
        self.time_stamps    = []
        self.head_movement_speeds = []
        self.head_rotation_speeds = []


def read_file(filename):
    recording = Recording()
    # read csv file(s)
    print("Loading data from file: " + filename)
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:

            # print(row)

            pos_x = float(row[0])
            pos_y = float(row[1])
            pos_z = float(row[2])
            recording.head_positions.append((pos_x, pos_y, pos_z))

            rot_x = float(row[3])
            rot_y = float(row[4])
            rot_z = float(row[5])
            rot_w = float(row[6])
            recording.head_rotations.append((rot_x, rot_y, rot_z, rot_w))

            time = float(row[18])
            recording.time_stamps.append(time)

    print("Found " + str(len(recording.head_positions)) + " entries") 

    return recording

# visualise positions on an image. render paths as lines
# convert positions to normalised 2D coordinates (effectively orthogonal projection matrix, looking along one of the axes)
def visualise_recording(rec):
    img_w=300.0
    img_h=300.0
    canvas   = np.zeros((int(img_w), int(img_h), 3), dtype="uint8")
    h_draw_col = (0, 0, 255)


    room_bbox_min = np.array((-2, 0, -2))
    room_bbox_max = np.array(( 2, 3,  2))
    room_bbox_size = room_bbox_max - room_bbox_min


    for p_idx in range(1,len(rec.head_positions)):

        p = rec.head_positions[p_idx]
        last_p = rec.head_positions[p_idx-1]

        line_start = (np.asarray(p) - room_bbox_min) / room_bbox_size
        line_end = (np.asarray(last_p) - room_bbox_min) / room_bbox_size

        cv.line(canvas, (int(line_start[0]*img_w), int(img_h) - int(line_start[1]*img_h)), (int(line_end[0]*img_w),  int(img_h) - int(line_end[1]*img_h)), h_draw_col)


    cv.imshow("Canvas", canvas)
    cv.waitKey(0)

def calculate_mean_head_speed(rec):

    last_time = rec.time_stamps[0];
    last_pos  = np.array(rec.head_positions[0]);

    accum_time = 0.0
    accum_dist = 0.0

    for frame in range(1,len(rec.head_positions)):


        time = rec.time_stamps[frame];
        pos  = np.array(rec.head_positions[frame]);


        time_diff    = time - last_time
        displacement = np.linalg.norm(pos - last_pos)

        speed=0.0
        if time_diff > 0.0:
            speed = displacement / time_diff
        rec.head_movement_speeds.append(speed)

        accum_time += time_diff
        accum_dist += displacement

        last_time = time
        last_pos  = pos

    if accum_time > 0.0:
        mean_speed = accum_dist / accum_time
        print("from " + str(len(rec.head_positions)) + ", mean head movement speed = " + str(mean_speed) + " m/s")
        return mean_speed
    else:
        return 0.0

# https://stackoverflow.com/questions/57063595/how-to-obtain-the-angle-between-two-quaternions
def angle_between_quaternions(q1,q2):

    q1 = q1.normalised
    q2 = q2.normalised
    qd = q1.conjugate * q2

    return qd.angle

def calculate_mean_head_rotation_speed(rec):

    last_time = rec.time_stamps[0];
    last_rot  = Quaternion(np.array(rec.head_rotations[0]));

    accum_time = 0.0
    accum_rot = 0.0

    for frame in range(1,len(rec.head_positions)):

        time = rec.time_stamps[frame];
        rot  = Quaternion(np.array(rec.head_rotations[frame]));

        time_diff = time - last_time
        angular_displacement = angle_between_quaternions(rot, last_rot)

        rot_speed=0.0
        if time_diff > 0.0:
            rot_speed = angular_displacement / time_diff
        rec.head_rotation_speeds.append(rot_speed)

        accum_time += time_diff
        accum_rot += angular_displacement

        last_time = time
        last_rot  = rot

    if accum_time > 0.0:
        mean_rot_speed = accum_rot / accum_time
        print("from " + str(len(rec.head_rotations)) + ", mean head rotation speed = " + str(mean_rot_speed) + " rad/s")
        return mean_rot_speed
    else:
        return 0.0




class Condition(Enum):
    FACE_TO_FACE=0
    SPATIAL=1
    NO_SPATIAL=2

conditionOrders = [
Condition.FACE_TO_FACE, Condition.SPATIAL, Condition.NO_SPATIAL,
Condition.NO_SPATIAL, Condition.FACE_TO_FACE, Condition.SPATIAL,
Condition.SPATIAL, Condition.NO_SPATIAL, Condition.FACE_TO_FACE,
Condition.FACE_TO_FACE, Condition.NO_SPATIAL, Condition.SPATIAL,
Condition.SPATIAL, Condition.FACE_TO_FACE, Condition.NO_SPATIAL,
Condition.NO_SPATIAL, Condition.SPATIAL, Condition.FACE_TO_FACE]

def get_condition(dyad,trial):
    dyad = dyad % 6
    trial = trial % 3
    return conditionOrders[dyad*3+trial]


spatial_speed = 0
spatial_rot_speed = 0
spatial_duration = 0

non_spatial_speed = 0
non_spatial_rot_speed = 0
non_spatial_duration = 0

all_mean_spatial_speed = []
all_mean_spatial_rot_speed = []
all_mean_non_spatial_speed = []
all_mean_non_spatial_rot_speed = []


all_spatial_speed = []
all_spatial_rot_speed = []
all_non_spatial_speed = []
all_non_spatial_rot_speed = []



with open(output_path, 'w', newline='') as f:

    writer = csv.writer(f)
    writer.writerow(['dyad', 'partner', 'trial', 'duration_s','speed_m_s', 'rot_speed_rad_s', 'condition'])

    # loop through all dyads, partners, and trials
    for dyad in range(0, num_dyads):
        for partner in range(0,2):
            for trial in range(0, num_trials):

                filename=data_base_path+"dyad_" + str(dyad) + "_partner" + str(partner) + "_trial" + str(trial) + "_" + "Head" + "_track.csv"
                recording = read_file(filename)


                duration =  recording.time_stamps[-1] - recording.time_stamps[0] 
                speed = calculate_mean_head_speed(recording)
                rot_speed = calculate_mean_head_rotation_speed(recording)
                condition = get_condition(dyad, trial)

                # print("found " + str(len(recording.head_positions)) + " head positions")
                # print("found " + str(len(recording.head_movement_speeds)) + " head movement speeds")
                
                # print("found " + str(len(recording.head_rotations)) + " head rotations")
                # print("found " + str(len(recording.head_rotation_speeds)) + " head rotation speeds")
                

                if condition == Condition.SPATIAL:
                    spatial_speed += (speed*duration)
                    spatial_rot_speed += (rot_speed*duration)
                    spatial_duration += duration

                    all_mean_spatial_speed.append(speed)
                    all_mean_spatial_rot_speed.append(rot_speed)

                    if speed > 0:
                        all_spatial_speed.extend(recording.head_movement_speeds)
                        all_spatial_rot_speed.extend(recording.head_rotation_speeds)

                elif condition == Condition.NO_SPATIAL:
                    non_spatial_speed += (speed*duration)
                    non_spatial_rot_speed += (rot_speed*duration)
                    non_spatial_duration += duration

                    all_mean_non_spatial_speed.append(speed)
                    all_mean_non_spatial_rot_speed.append(rot_speed)

                    if speed > 0:
                        all_non_spatial_speed.extend(recording.head_movement_speeds)
                        all_non_spatial_rot_speed.extend(recording.head_rotation_speeds)

                writer.writerow([dyad, partner, trial, duration, speed, rot_speed, condition])
                

spatial_speed /= spatial_duration
spatial_rot_speed /= spatial_duration

non_spatial_speed /= non_spatial_duration
non_spatial_rot_speed /= non_spatial_duration

print("SPATIAL:")
print("Head movement speed: " + str(spatial_speed) + " m/s")
print("Head rotation speed: " + str(spatial_rot_speed) + " rad/s") 

print("NON SPATIAL:")
print("Head movement speed: " + str(non_spatial_speed) + " m/s")
print("Head rotation speed: " + str(non_spatial_rot_speed) + " rad/s")


with open('data/head_movement_speed.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['SPATIAL', 'NO_SPATIAL'])

    for i in range(0, max(len(all_mean_spatial_speed), len(all_mean_non_spatial_speed))):
        
        sp_speed = 0
        nsp_speed = 0

        if (i < len(all_mean_spatial_speed)):
            sp_speed = all_mean_spatial_speed[i]
        if (i < len(all_mean_non_spatial_speed)):
                nsp_speed = all_mean_non_spatial_speed[i]
        
        writer.writerow([sp_speed, nsp_speed])

with open('data/head_rotation_speed.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['SPATIAL', 'NO_SPATIAL'])

    for i in range(0, max(len(all_mean_spatial_rot_speed), len(all_mean_non_spatial_rot_speed))):
        
        sp_rot_speed = 0
        nsp_rot_speed = 0

        if (i < len(all_mean_spatial_rot_speed)):
            sp_rot_speed = all_mean_spatial_rot_speed[i]
        if (i < len(all_mean_non_spatial_rot_speed)):
                nsp_rot_speed = all_mean_non_spatial_rot_speed[i]
        
        writer.writerow([sp_rot_speed, nsp_rot_speed])


with open('data/all_head_movement_speed_spatial.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for s in all_spatial_speed:
        writer.writerow([s])
        
with open('data/all_head_movement_speed_nonspatial.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for s in all_non_spatial_speed:
        writer.writerow([s])
        
with open('data/all_head_rotation_speed_spatial.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for s in all_spatial_rot_speed:
        writer.writerow([s])
        
with open('data/all_head_rotation_speed_nonspatial.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for s in all_non_spatial_rot_speed:
        writer.writerow([s])
        

