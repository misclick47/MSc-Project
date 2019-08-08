'''
This file contains all the functions which return 4D feature and 3D feature
it has 3 types: 1x1x1, 3x3x3, 5x5x5

Author: Yan Gao
email: gaoy4477@gmail.com
'''

import cv2
import os
import numpy as np

import module.content as content

def get_masked_features(mask, img, size):
	# we can change the size of kernel here
	# like 1x1, 3x3, 5x5
	features = []
	coordinate = mask.nonzero()
	for i, j in zip(coordinate[0], coordinate[1]):
		if size == 3:
			features.append(img[i-1:i+2, j-1:j+2].ravel())
		elif size == 1:
			features.append(img[i, j])
		elif size == 5:
			features.append(img[i-2:i+3, j-2:j+3].ravel())
		else:
			raise ValueError('Have not assigned such size! Please choose 1, 3 or 5!')
	return features


def get_all_features_3(path, mask_centre, radius):
	# To obtain all features, we need to set a circle mask for our data
	# This is the difference to the previous function
	# it will return 3x3x3(x3) data
	print('Current slice:', path)

	time_slice = os.path.basename(os.path.dirname(path))
	# get the time stamp for this slice -> to licate its time stamp
	root_path = os.path.dirname(os.path.dirname(path))
	# get the root path
	all_timestamp = content.get_folder(root_path)

	time_slice_index = all_timestamp.index(time_slice)
	if time_slice_index == 0:
		target_t_list = [time_slice_index + 1, time_slice_index + 2]
	elif time_slice_index == (len(all_timestamp) - 1):
		target_t_list = [time_slice_index - 1, time_slice_index - 2]
	else:
		target_t_list = [time_slice_index -1, time_slice_index + 1]
	# this 'if' argument find the previous time stamp and next time stamp for current t

	current_path = os.path.dirname(path)
	previous_path = os.path.join(root_path, all_timestamp[target_t_list[0]])
	future_path = os.path.join(root_path, all_timestamp[target_t_list[1]])

	current_all_tif = content.get_allslice(current_path)
	previous_all_tif = content.get_allslice(previous_path)
	future_all_tif = content.get_allslice(future_path)
	# get all the tif content

	# this part of code for x3 space
	location_slice_index = current_all_tif.index(path)
	if location_slice_index == 0:
		target_space_list = [location_slice_index, location_slice_index+1, location_slice_index+2]
	elif location_slice_index == 1247:
		# totally there are 1248 slices, this is a magic number
		target_space_list = [location_slice_index, location_slice_index-2, location_slice_index-1]
	else:
		target_space_list = [location_slice_index, location_slice_index-1, location_slice_index+1]
	# this 'if' argument find the 3D space for given slice

	print('Loading 9 images...')
	img_1 = cv2.imread(current_all_tif[target_space_list[0]], -1)
	img_2 = cv2.imread(current_all_tif[target_space_list[1]], -1)
	img_3 = cv2.imread(current_all_tif[target_space_list[2]], -1)
	# three images for space
	img_4 = cv2.imread(previous_all_tif[target_space_list[0]], -1)
	img_5 = cv2.imread(previous_all_tif[target_space_list[1]], -1)
	img_6 = cv2.imread(previous_all_tif[target_space_list[2]], -1)
	img_7 = cv2.imread(future_all_tif[target_space_list[0]], -1)
	img_8 = cv2.imread(future_all_tif[target_space_list[1]], -1)
	img_9 = cv2.imread(future_all_tif[target_space_list[2]], -1)
	print('Finished!')
	# nine images for space + time

	# Here, I create the mask for the data
	# It needs us to assign centre and radius
	height, width = img_1.shape
	mask = np.zeros((height, width), np.uint8)
	cv2.circle(mask, mask_centre, radius, 1, thickness=-1)

	print('Getting features...')
	feature_img_1 = np.array(get_masked_features(mask, img_1, 3))
	feature_img_2 = np.array(get_masked_features(mask, img_2, 3))
	feature_img_3 = np.array(get_masked_features(mask, img_3, 3))
	feature_img_4 = np.array(get_masked_features(mask, img_4, 3))
	feature_img_5 = np.array(get_masked_features(mask, img_5, 3))
	feature_img_6 = np.array(get_masked_features(mask, img_6, 3))
	feature_img_7 = np.array(get_masked_features(mask, img_7, 3))
	feature_img_8 = np.array(get_masked_features(mask, img_8, 3))
	feature_img_9 = np.array(get_masked_features(mask, img_9, 3))
	# get all features
	print('Finished!')
	print('Concatenating...')
	feature_4D = np.concatenate((feature_img_1, feature_img_2, feature_img_3,
                                 feature_img_4, feature_img_5, feature_img_6,
                                 feature_img_7, feature_img_8, feature_img_9), axis=1)
	feature_3D = np.concatenate((feature_img_1, feature_img_2, feature_img_3), axis=1)
	print('Finished!')
    
	return feature_4D, feature_3D

def get_assign_features_3(path, x_coordinate, y_coordinate):
	print('Get 3x3 features')
	# name_slice = os.path.basename(path)
	# # get the name for this slice -> to locate its location
	time_slice = os.path.basename(os.path.dirname(path))
	# get the time stamp for this slice -> to licate its time stamp
	root_path = os.path.dirname(os.path.dirname(path))
	# get the root path
	all_timestamp = content.get_folder(root_path)

	time_slice_index = all_timestamp.index(time_slice)
	if time_slice_index == 0:
		target_t_list = [time_slice_index + 1, time_slice_index + 2]
	elif time_slice_index == (len(all_timestamp) - 1):
		target_t_list = [time_slice_index - 1, time_slice_index - 2]
	else:
		target_t_list = [time_slice_index -1, time_slice_index + 1]
	# this 'if' argument find the previous time stamp and next time stamp for current t

	current_path = os.path.dirname(path)
	previous_path = os.path.join(root_path, all_timestamp[target_t_list[0]])
	future_path = os.path.join(root_path, all_timestamp[target_t_list[1]])

	current_all_tif = content.get_allslice(current_path)
	previous_all_tif = content.get_allslice(previous_path)
	future_all_tif = content.get_allslice(future_path)
	# get all the tif content

	location_slice_index = current_all_tif.index(path)
	if location_slice_index == 0:
		target_space_list = [location_slice_index, location_slice_index+1, location_slice_index+2]
	elif location_slice_index == 1247:
		# totally there are 1248 slices, this is a magic number
		target_space_list = [location_slice_index, location_slice_index-2, location_slice_index-1]
	else:
		target_space_list = [location_slice_index, location_slice_index-1, location_slice_index+1]
	# this 'if' argument find the 3D space for given slice

	img_1 = cv2.imread(current_all_tif[target_space_list[0]], -1)
	img_2 = cv2.imread(current_all_tif[target_space_list[1]], -1)
	img_3 = cv2.imread(current_all_tif[target_space_list[2]], -1)
	# three images for space
	img_4 = cv2.imread(previous_all_tif[target_space_list[0]], -1)
	img_5 = cv2.imread(previous_all_tif[target_space_list[1]], -1)
	img_6 = cv2.imread(previous_all_tif[target_space_list[2]], -1)
	img_7 = cv2.imread(future_all_tif[target_space_list[0]], -1)
	img_8 = cv2.imread(future_all_tif[target_space_list[1]], -1)
	img_9 = cv2.imread(future_all_tif[target_space_list[2]], -1)
	# nine images for space + time

	feature_img_1 = img_1[x_coordinate-1:x_coordinate+2, y_coordinate-1:y_coordinate+2].ravel()
	feature_img_2 = img_2[x_coordinate-1:x_coordinate+2, y_coordinate-1:y_coordinate+2].ravel()
	feature_img_3 = img_3[x_coordinate-1:x_coordinate+2, y_coordinate-1:y_coordinate+2].ravel()
	feature_img_4 = img_4[x_coordinate-1:x_coordinate+2, y_coordinate-1:y_coordinate+2].ravel()
	feature_img_5 = img_5[x_coordinate-1:x_coordinate+2, y_coordinate-1:y_coordinate+2].ravel()
	feature_img_6 = img_6[x_coordinate-1:x_coordinate+2, y_coordinate-1:y_coordinate+2].ravel()
	feature_img_7 = img_7[x_coordinate-1:x_coordinate+2, y_coordinate-1:y_coordinate+2].ravel()
	feature_img_8 = img_8[x_coordinate-1:x_coordinate+2, y_coordinate-1:y_coordinate+2].ravel()
	feature_img_9 = img_9[x_coordinate-1:x_coordinate+2, y_coordinate-1:y_coordinate+2].ravel()
	# get all features

	feature_3D = np.concatenate((feature_img_1, feature_img_2, feature_img_3))
	feature_4D = np.concatenate((feature_img_1, feature_img_2, feature_img_3,
								 feature_img_4, feature_img_5, feature_img_6,
								 feature_img_7, feature_img_8, feature_img_9))

	return feature_4D, feature_3D




def get_all_features_1(path, mask_centre, radius):
	# it will return 1x1x1(x3) data
	print('Current slice:', path)

	time_slice = os.path.basename(os.path.dirname(path))
	# get the time stamp for this slice -> to licate its time stamp
	root_path = os.path.dirname(os.path.dirname(path))
	# get the root path
	all_timestamp = content.get_folder(root_path)

	time_slice_index = all_timestamp.index(time_slice)
	if time_slice_index == 0:
		target_t_list = [time_slice_index + 1, time_slice_index + 2]
	elif time_slice_index == (len(all_timestamp) - 1):
		target_t_list = [time_slice_index - 1, time_slice_index - 2]
	else:
		target_t_list = [time_slice_index -1, time_slice_index + 1]
	# this 'if' argument find the previous time stamp and next time stamp for current t

	current_path = os.path.dirname(path)
	previous_path = os.path.join(root_path, all_timestamp[target_t_list[0]])
	future_path = os.path.join(root_path, all_timestamp[target_t_list[1]])

	current_all_tif = content.get_allslice(current_path)
	previous_all_tif = content.get_allslice(previous_path)
	future_all_tif = content.get_allslice(future_path)
	# get all the tif content

	# this part of code for x1 space
	location_slice_index = current_all_tif.index(path)
	target_space_list = [location_slice_index]
	# this 'if' argument find the 3D space for given slice

	print('Loading 3 images...')
	img_1 = cv2.imread(current_all_tif[target_space_list[0]], -1)
	# one images for space
	img_2 = cv2.imread(previous_all_tif[target_space_list[0]], -1)
	# past image
	img_3 = cv2.imread(future_all_tif[target_space_list[0]], -1)
	print('Finished!')
	# future image
	# three images for space + time

	# Here, I create the mask for the data
	# It needs us to assign centre and radius
	height, width = img_1.shape
	mask = np.zeros((height, width), np.uint8)
	cv2.circle(mask, mask_centre, radius, 1, thickness=-1)

	print('Getting features...')
	feature_img_1 = get_masked_features(mask, img_1, 1)
	feature_img_2 = get_masked_features(mask, img_2, 1)
	feature_img_3 = get_masked_features(mask, img_3, 1)
	# get all features
	print('Finished!')
	print('Concatenating...')
	feature_4D = np.concatenate((feature_img_1, feature_img_2, feature_img_3), axis=1)
	feature_3D = np.array(feature_img_1)
	print('Finished!')

	return feature_4D, feature_3D

def get_assign_features_1(path, x_coordinate, y_coordinate):
	print('Get 1x1 features')
	# name_slice = os.path.basename(path)
	# # get the name for this slice -> to locate its location
	time_slice = os.path.basename(os.path.dirname(path))
	# get the time stamp for this slice -> to licate its time stamp
	root_path = os.path.dirname(os.path.dirname(path))
	# get the root path
	all_timestamp = content.get_folder(root_path)

	time_slice_index = all_timestamp.index(time_slice)
	if time_slice_index == 0:
		target_t_list = [time_slice_index + 1, time_slice_index + 2]
	elif time_slice_index == (len(all_timestamp) - 1):
		target_t_list = [time_slice_index - 1, time_slice_index - 2]
	else:
		target_t_list = [time_slice_index -1, time_slice_index + 1]
	# this 'if' argument find the previous time stamp and next time stamp for current t

	current_path = os.path.dirname(path)
	previous_path = os.path.join(root_path, all_timestamp[target_t_list[0]])
	future_path = os.path.join(root_path, all_timestamp[target_t_list[1]])

	current_all_tif = content.get_allslice(current_path)
	previous_all_tif = content.get_allslice(previous_path)
	future_all_tif = content.get_allslice(future_path)
	# get all the tif content

	# this part of code for x1 space
	location_slice_index = current_all_tif.index(path)
	target_space_list = [location_slice_index]
	# this 'if' argument find the 3D space for given slice


	img_1 = cv2.imread(current_all_tif[target_space_list[0]], -1)
	# one images for space
	img_2 = cv2.imread(previous_all_tif[target_space_list[0]], -1)
	# past image
	img_3 = cv2.imread(future_all_tif[target_space_list[0]], -1)
	# future image
	# three images for space + time

	feature_img_1 = img_1[x_coordinate, y_coordinate]
	feature_img_2 = img_2[x_coordinate, y_coordinate]
	feature_img_3 = img_3[x_coordinate, y_coordinate]
	# get all features

	feature_3D = np.array([feature_img_1], np.uint16)
	feature_4D = np.array([feature_img_1, feature_img_2, feature_img_3], np.uint16)

	return feature_4D, feature_3D


def get_all_features_5(path, mask_centre, radius):
	# it will return 5x5x5(x3) data
	print('Current slice:', path)

	time_slice = os.path.basename(os.path.dirname(path))
	# get the time stamp for this slice -> to licate its time stamp
	root_path = os.path.dirname(os.path.dirname(path))
	# get the root path
	all_timestamp = content.get_folder(root_path)

	time_slice_index = all_timestamp.index(time_slice)
	if time_slice_index == 0:
		target_t_list = [time_slice_index + 1, time_slice_index + 2]
	elif time_slice_index == (len(all_timestamp) - 1):
		target_t_list = [time_slice_index - 1, time_slice_index - 2]
	else:
		target_t_list = [time_slice_index -1, time_slice_index + 1]
	# this 'if' argument find the previous time stamp and next time stamp for current t

	current_path = os.path.dirname(path)
	previous_path = os.path.join(root_path, all_timestamp[target_t_list[0]])
	future_path = os.path.join(root_path, all_timestamp[target_t_list[1]])

	current_all_tif = content.get_allslice(current_path)
	previous_all_tif = content.get_allslice(previous_path)
	future_all_tif = content.get_allslice(future_path)
	# get all the tif content

	# this part of code for x5 space
	location_slice_index = current_all_tif.index(path)
	if location_slice_index == 0:
		target_space_list = [location_slice_index, location_slice_index+1, location_slice_index+2, location_slice_index+3, location_slice_index+4]
	elif location_slice_index == 1:
		target_space_list = [location_slice_index, location_slice_index-1, location_slice_index+1, location_slice_index+2, location_slice_index+3]
	elif location_slice_index == 1246:
		target_space_list = [location_slice_index, location_slice_index-3, location_slice_index-2, location_slice_index-1, location_slice_index+1]
	elif location_slice_index == 1247:
		# totally there are 1248 slices, this is a magic number
		target_space_list = [location_slice_index, location_slice_index-4, location_slice_index-3, location_slice_index-2, location_slice_index-1]
	else:
		target_space_list = [location_slice_index, location_slice_index-2, location_slice_index-1, location_slice_index+1, location_slice_index+2]
	# this 'if' argument find the 3D space for given slice

	print('Loading 15 images...')
	img_1 = cv2.imread(current_all_tif[target_space_list[0]], -1)
	img_2 = cv2.imread(current_all_tif[target_space_list[1]], -1)
	img_3 = cv2.imread(current_all_tif[target_space_list[2]], -1)
	img_4 = cv2.imread(current_all_tif[target_space_list[3]], -1)
	img_5 = cv2.imread(current_all_tif[target_space_list[4]], -1)
	# three images for space
	img_6 = cv2.imread(previous_all_tif[target_space_list[0]], -1)
	img_7 = cv2.imread(previous_all_tif[target_space_list[1]], -1)
	img_8 = cv2.imread(previous_all_tif[target_space_list[2]], -1)
	img_9 = cv2.imread(previous_all_tif[target_space_list[3]], -1)
	img_10 = cv2.imread(previous_all_tif[target_space_list[4]], -1)
	# previous timestamp
	img_11 = cv2.imread(future_all_tif[target_space_list[0]], -1)
	img_12 = cv2.imread(future_all_tif[target_space_list[1]], -1)
	img_13 = cv2.imread(future_all_tif[target_space_list[2]], -1)
	img_14 = cv2.imread(future_all_tif[target_space_list[3]], -1)
	img_15 = cv2.imread(future_all_tif[target_space_list[4]], -1)
	print('Finished!')
	# future tumestamp
	# nine images for space + time

	# Here, I create the mask for the data
	# It needs us to assign centre and radius
	height, width = img_1.shape
	mask = np.zeros((height, width), np.uint8)
	cv2.circle(mask, mask_centre, radius, 1, thickness=-1)

	print('Getting features...')
	feature_img_1 = get_masked_features(mask, img_1, 5)
	feature_img_2 = get_masked_features(mask, img_2, 5)
	feature_img_3 = get_masked_features(mask, img_3, 5)
	feature_img_4 = get_masked_features(mask, img_4, 5)
	feature_img_5 = get_masked_features(mask, img_5, 5)
	feature_img_6 = get_masked_features(mask, img_6, 5)
	feature_img_7 = get_masked_features(mask, img_7, 5)
	feature_img_8 = get_masked_features(mask, img_8, 5)
	feature_img_9 = get_masked_features(mask, img_9, 5)
	feature_img_10 = get_masked_features(mask, img_10, 5)
	feature_img_11 = get_masked_features(mask, img_11, 5)
	feature_img_12 = get_masked_features(mask, img_12, 5)
	feature_img_13 = get_masked_features(mask, img_13, 5)
	feature_img_14 = get_masked_features(mask, img_14, 5)
	feature_img_15 = get_masked_features(mask, img_15, 5)
	# get all features
	print('Finished!')
	print('Concatenating...')

	feature_4D = np.concatenate((feature_img_1,  feature_img_2,  feature_img_3,  feature_img_4,  feature_img_5,
								 feature_img_6,  feature_img_7,  feature_img_8,  feature_img_9,  feature_img_10,
								 feature_img_11, feature_img_12, feature_img_13, feature_img_14, feature_img_15), axis=1)
	feature_3D = np.concatenate((feature_img_1,  feature_img_2,  feature_img_3,  feature_img_4,  feature_img_5), axis=1)
	print('Finished!')

	return feature_4D, feature_3D



def get_assign_features_5(path, x_coordinate, y_coordinate):
	# name_slice = os.path.basename(path)
	# # get the name for this slice -> to locate its location
	print('Get 5x5 features')
	time_slice = os.path.basename(os.path.dirname(path))
	# get the time stamp for this slice -> to licate its time stamp
	root_path = os.path.dirname(os.path.dirname(path))
	# get the root path
	all_timestamp = content.get_folder(root_path)

	time_slice_index = all_timestamp.index(time_slice)
	if time_slice_index == 0:
		target_t_list = [time_slice_index + 1, time_slice_index + 2]
	elif time_slice_index == (len(all_timestamp) - 1):
		target_t_list = [time_slice_index - 1, time_slice_index - 2]
	else:
		target_t_list = [time_slice_index -1, time_slice_index + 1]
	# this 'if' argument find the previous time stamp and next time stamp for current t

	current_path = os.path.dirname(path)
	previous_path = os.path.join(root_path, all_timestamp[target_t_list[0]])
	future_path = os.path.join(root_path, all_timestamp[target_t_list[1]])

	current_all_tif = content.get_allslice(current_path)
	previous_all_tif = content.get_allslice(previous_path)
	future_all_tif = content.get_allslice(future_path)
	# get all the tif content

	# this part of code for x5 space
	location_slice_index = current_all_tif.index(path)
	if location_slice_index == 0:
		target_space_list = [location_slice_index, location_slice_index+1, location_slice_index+2, location_slice_index+3, location_slice_index+4]
	elif location_slice_index == 1:
		target_space_list = [location_slice_index, location_slice_index-1, location_slice_index+1, location_slice_index+2, location_slice_index+3]
	elif location_slice_index == 1246:
		target_space_list = [location_slice_index, location_slice_index-3, location_slice_index-2, location_slice_index-1, location_slice_index+1]
	elif location_slice_index == 1247:
		# totally there are 1248 slices, this is a magic number
		target_space_list = [location_slice_index, location_slice_index-4, location_slice_index-3, location_slice_index-2, location_slice_index-1]
	else:
		target_space_list = [location_slice_index, location_slice_index-2, location_slice_index-1, location_slice_index+1, location_slice_index+2]
	# this 'if' argument find the 3D space for given slice

	img_1 = cv2.imread(current_all_tif[target_space_list[0]], -1)
	img_2 = cv2.imread(current_all_tif[target_space_list[1]], -1)
	img_3 = cv2.imread(current_all_tif[target_space_list[2]], -1)
	img_4 = cv2.imread(current_all_tif[target_space_list[3]], -1)
	img_5 = cv2.imread(current_all_tif[target_space_list[4]], -1)
	# three images for space
	img_6 = cv2.imread(previous_all_tif[target_space_list[0]], -1)
	img_7 = cv2.imread(previous_all_tif[target_space_list[1]], -1)
	img_8 = cv2.imread(previous_all_tif[target_space_list[2]], -1)
	img_9 = cv2.imread(previous_all_tif[target_space_list[3]], -1)
	img_10 = cv2.imread(previous_all_tif[target_space_list[4]], -1)
	# previous timestamp
	img_11 = cv2.imread(future_all_tif[target_space_list[0]], -1)
	img_12 = cv2.imread(future_all_tif[target_space_list[1]], -1)
	img_13 = cv2.imread(future_all_tif[target_space_list[2]], -1)
	img_14 = cv2.imread(future_all_tif[target_space_list[3]], -1)
	img_15 = cv2.imread(future_all_tif[target_space_list[4]], -1)
	# future tumestamp
	# nine images for space + time

	feature_img_1 = img_1[x_coordinate-2:x_coordinate+3, y_coordinate-2:y_coordinate+3].ravel()
	feature_img_2 = img_2[x_coordinate-2:x_coordinate+3, y_coordinate-2:y_coordinate+3].ravel()
	feature_img_3 = img_3[x_coordinate-2:x_coordinate+3, y_coordinate-2:y_coordinate+3].ravel()
	feature_img_4 = img_4[x_coordinate-2:x_coordinate+3, y_coordinate-2:y_coordinate+3].ravel()
	feature_img_5 = img_5[x_coordinate-2:x_coordinate+3, y_coordinate-2:y_coordinate+3].ravel()
	feature_img_6 = img_6[x_coordinate-2:x_coordinate+3, y_coordinate-2:y_coordinate+3].ravel()
	feature_img_7 = img_7[x_coordinate-2:x_coordinate+3, y_coordinate-2:y_coordinate+3].ravel()
	feature_img_8 = img_8[x_coordinate-2:x_coordinate+3, y_coordinate-2:y_coordinate+3].ravel()
	feature_img_9 = img_9[x_coordinate-2:x_coordinate+3, y_coordinate-2:y_coordinate+3].ravel()
	feature_img_10 = img_10[x_coordinate-2:x_coordinate+3, y_coordinate-2:y_coordinate+3].ravel()
	feature_img_11 = img_11[x_coordinate-2:x_coordinate+3, y_coordinate-2:y_coordinate+3].ravel()
	feature_img_12 = img_12[x_coordinate-2:x_coordinate+3, y_coordinate-2:y_coordinate+3].ravel()
	feature_img_13 = img_13[x_coordinate-2:x_coordinate+3, y_coordinate-2:y_coordinate+3].ravel()
	feature_img_14 = img_14[x_coordinate-2:x_coordinate+3, y_coordinate-2:y_coordinate+3].ravel()
	feature_img_15 = img_15[x_coordinate-2:x_coordinate+3, y_coordinate-2:y_coordinate+3].ravel()
	# get all features

	feature_3D = np.concatenate((feature_img_1, feature_img_2, feature_img_3, feature_img_4, feature_img_5))
	feature_4D = np.concatenate((feature_img_1, feature_img_2, feature_img_3, feature_img_4, feature_img_5,
								 feature_img_6, feature_img_7, feature_img_8, feature_img_9, feature_img_10,
								 feature_img_11, feature_img_12, feature_img_13, feature_img_14, feature_img_15))

	return feature_4D, feature_3D





