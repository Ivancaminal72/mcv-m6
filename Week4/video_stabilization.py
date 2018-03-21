import cv2
import numpy as np

from block_matching import get_block_matching


# def get_stabilization(prev_img, motion):
#
#     stabilized_prev_img = np.zeros(prev_img.shape)
#
#     for idx in range(prev_img.shape[0]):
#         for idy in range(prev_img.shape[1]):
#
#             #if motion[idx, idy, 2] is not 0:
#             stabilized_prev_img[idx, idy] = prev_img[idx + int(motion[idx, idy, 0]), idy + int(motion[idx, idy, 1])]
#
#     return stabilized_prev_img



# Backward prediction
def video_stabilization(sequence, block_size_x, block_size_y, search_area_x, search_area_y, compensation = 'backward'):


    N = len(sequence)+1

    prev_img = sequence[0]

    sequence_stabilized = np.copy(sequence)
    sequence_stabilized = np.zeros(sequence.shape)

    for idx in range(1, N):
        print(idx, N)
        curr_img = sequence[idx]

        optical_flow = get_block_matching(curr_img, prev_img, block_size_x, block_size_y, search_area_x, search_area_y, compensation = 'backward')

        u = np.median(optical_flow[:,:,0])
        v = np.median(optical_flow[:,:,1])

        # translation matrix
        affine_H = np.float32([[1, 0, -u],
                               [0, 1, -v]])

        stabilized_frame = cv2.warpAffine(curr_img, affine_H, (curr_img.shape[1], curr_img.shape[0]))

        # update the previous image to the estabilized current image
        prev_img = stabilized_frame

        sequence_stabilized [idx-1, :, :] = stabilized_frame


    return  sequence_stabilized


# =================================
import os
from utils import *
import matplotlib.pyplot as plt

data_path = '../../databases'
PlotsDirectory = '../plots/Week4/task21/'

if not os.path.exists(PlotsDirectory):
    os.makedirs(PlotsDirectory)

name = 'traffic'
seq_range = np.array([950, 1050])


[seq, y] = load_data(data_path, name, seq_range, grayscale=True)


block_size_x, block_size_y, search_area_x, search_area_y = 5, 5, 10, 10
est_seq = video_stabilization(seq, block_size_x, block_size_y, search_area_x, search_area_y, compensation = 'backward')

np.save(PlotsDirectory + 'traffic_stabilized_bloque5_area10.npy', est_seq)
write_images2(est_seq, PlotsDirectory, 'traffic_stabilized_bloque5_area10_')

# sequence = seq
# N = 3  # len(sequence)+1
#
# prev_img = sequence[0]
#
# sequence_stabilized = np.copy(sequence)
#
# for idx in range(1, N):
#     print(idx, N)
#     curr_img = sequence[idx]
#
#     optical_flow = get_block_matching(curr_img, prev_img, block_size_x, block_size_y, search_area_x, search_area_y,
#                                       compensation='backward')
#
#     mean_x = np.mean(optical_flow[:, :, 0])
#     mean_y = np.mean(optical_flow[:, :, 1])
#     #print(mean_x)
#     #print(mean_y)
#
#     # optical_flow[:, :, 0] = np.around(optical_flow[:, :, 0], decimals=2)
#     # optical_flow[:, :, 1] = np.around(optical_flow[:, :, 1], decimals=2)
#     # unique_x, counts_x = np.unique(optical_flow[:, :, 0], return_counts=True)
#     # unique_y, counts_y = np.unique(optical_flow[:, :, 1], return_counts=True)
#
#     optical_flow[:, :, 0] = np.ones(optical_flow.shape[:2]) * mean_x
#     optical_flow[:, :, 1] = np.ones(optical_flow.shape[:2]) * mean_y
#
#     # optical_flow[:,:,0][abs(optical_flow[:,:,0])<(mean_x)] = 0
#     # optical_flow[:, :, 1][abs(optical_flow[:, :, 1])<(mean_y)] = 0
#
#     stabilized_frame = get_stabilization(prev_img, optical_flow)
#     prev_img = curr_img
#
#     sequence_stabilized[idx - 1, :, :] = stabilized_frame
#
#
# for i in range(N):
#     cv2.imshow('original', seq[i])
#     cv2.imshow('image', sequence_stabilized[i])
#     cv2.waitKey(delay=0)


#write_video(est_seq, "traffic_stabilized.avi")