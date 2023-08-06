import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numba
from numba import njit
import random as rd
import time
import copy
from collections import defaultdict
import plotly.graph_objects as go
import pandas as pd
from numba.typed import List

class Bin:
    def __init__(self, bin_info):
        self.bin_info = bin_info
        self.wasted_space_list = []
        self.usable_space_list = [bin_info]
        self.prepack_item_space_list = []

    @property
    def get_cbm(self):
        return self.bin_info[0] * self.bin_info[1] * self.bin_info[2]

    @property
    def get_leftover_cbm(self):
        item_cbm = 0
        for bunch in self.prepack_item_space_list:
            bin, item, num_item, number_of_best_fit = bunch

            item_cbm += item[0] * item[1] * item[2] * num_item

        return self.get_cbm - item_cbm

    def decompress(self):
        pre_pack_item_space_list = self.prepack_item_space_list
        mylist = List()
        mylist.append(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0], np.int_))
        mylist.pop(0)
        for bunch in pre_pack_item_space_list:
            bin, item, num_item, number_of_best_fit = bunch
            mylist = insert___(bin, item, mylist, num_item, number_of_best_fit)

        mylist_final = [[item[0], item[1], item[2], item[5], item[6], item[7]] for item in mylist]
        self.mylist = mylist_final
        return mylist_final

    def draw_packed_bin(self):
        def get_random_color():
            return "#%06x" % rd.randint(0, 0xFFFFFF)

        color_list = []
        for i in range(1000):
            color_list.append(get_random_color())

        item_list = self.mylist

        data = []

        data.append(
            go.Mesh3d(
                x=[0, 0, int(self.bin_info[0]), int(self.bin_info[0]), 0, 0, int(self.bin_info[0]),
                   int(self.bin_info[0])],
                y=[0, int(self.bin_info[1]), int(self.bin_info[1]), 0, 0, int(self.bin_info[1]), int(self.bin_info[1]),
                   0],
                z=[0, 0, 0, 0, int(self.bin_info[2]), int(self.bin_info[2]), int(self.bin_info[2]),
                   int(self.bin_info[2])],
                # Intensity of each vertex, which will be interpolated and color-coded
                # i, j and k give the vertices of triangles

                # i  =  [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
                # j  =  [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
                # k  =  [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
                name='y',
                showscale=True,
                color="#555",
                opacity=0.1
            )
        )

        for index in range(len((item_list))):
            item = item_list[index]
            ox_item = int(item[3])
            oy_item = int(item[4])
            oz_item = int(item[5])

            extreme_x = int(item[0]) + ox_item
            extreme_y = int(item[1]) + oy_item
            extreme_z = int(item[2]) + oz_item

            data.append(
                go.Mesh3d(
                    x=[ox_item, ox_item, extreme_x, extreme_x, ox_item, ox_item, extreme_x, extreme_x],
                    y=[oy_item, extreme_y, extreme_y, oy_item, oy_item, extreme_y, extreme_y, oy_item],
                    z=[oz_item, oz_item, oz_item, oz_item, extreme_z, extreme_z, extreme_z, extreme_z],
                    # Intensity of each vertex, which will be interpolated and color-coded
                    # i, j and k give the vertices of triangles
                    i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
                    j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
                    k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
                    showscale=True,
                    color=get_random_color(),
                    opacity=1, flatshading=True
                )
            )
            data.append(go.Scatter3d(x=[0], y=[0], z=[0], mode='markers'))

        fig = go.Figure(data)
        fig.update_layout(
            autosize=False,
            width=1300,
            height=900,
            scene_aspectmode='data',
            scene_camera=dict(eye=dict(x=-2, y=-2, z=-1))
        )

        fig.show()


class Item:
    def __init__(self, item_info):
        self.item_info = item_info

    @property
    def get_cbm(self):
        return self.item_info[0] * self.item_info[1] * self.item_info[2] * self.item_info[3]


@njit(cache=True)
def compute_number_of_fit_with_rotation(bin_info, item_size):  # M_lwh, M_l, M_W, M_h, best_rotate
    best_num_item = -3
    best_rotation = -1

    result = np.empty((5), np.int_)
    OZ_rotation_lock = item_size[9]
    number_of_posible_rotation = 6
    if OZ_rotation_lock != 0:
        number_of_posible_rotation = 2

    for rotation in range(number_of_posible_rotation):
        infor_of_fit = compute_number_of_fit(bin_info,
                                             compute_rotate_item_size(item_size[0:3], rotation, OZ_rotation_lock))
        num_item = infor_of_fit[0]
        if num_item > best_num_item:
            best_num_item = num_item
            best_rotation = rotation
            result[0] = num_item

            result[1] = infor_of_fit[1]
            result[2] = infor_of_fit[2]
            result[3] = infor_of_fit[3]
            result[4] = best_rotation

    return result


@njit(cache=True)
def compute_box(bin_info, item_size, best_fit, item_size_rotate):  # decompose box, input: [size,position]

    box = np.empty((6, len(bin_info)), np.int_)
    for i in range(6):
        box[i] = np.copy(bin_info)

    M_lwh, M_l, M_w, M_h, best_rotate = best_fit[0], best_fit[1], best_fit[2], best_fit[3], best_fit[4]

    item_l = item_size_rotate[0]
    item_w = item_size_rotate[1]
    item_h = item_size_rotate[2]
    item_num = item_size_rotate[3]

    if M_lwh == 0:
        return box
    bin_l = bin_info[0]
    bin_w = bin_info[1]
    bin_h = bin_info[2]
    bin_pos_l = bin_info[3]
    bin_pos_w = bin_info[4]
    bin_pos_h = bin_info[5]

    temp_num = item_num
    if temp_num > M_lwh:
        temp_num = M_lwh
    OQ = bin_l
    N_l = math.ceil(temp_num / (M_w * M_h))  # 8
    num_item_front = temp_num - (N_l - 1) * M_w * M_h  # 20-2*4*2
    OF = N_l * item_l

    HI = M_w * item_w
    IJ = bin_w - HI
    JP = math.floor(temp_num / (M_w * M_h)) * item_l
    num_colum_face = math.ceil(num_item_front / M_h)
    FA = num_colum_face * item_w
    AB = (M_h - (num_colum_face * M_h - num_item_front)) * item_h
    num_box_AB = num_item_front % (M_h)
    FC = math.floor(num_item_front / M_h) * item_w
    CA = FA - FC

    FD = M_h * item_h
    box[0][0:7] = [bin_l - OF, bin_w, bin_h, bin_pos_l + OF, bin_pos_w, bin_pos_h, 0]
    box[1][0:7] = [item_l, bin_w - FA, bin_h, bin_pos_l + OF - item_l, bin_pos_w + FA, bin_pos_h, 1]
    box[2][0:7] = [item_l, FA - FC, bin_h - AB, bin_pos_l + OF - item_l, bin_pos_w + FC, AB + bin_pos_h, 2]

    box[3][0:7] = [item_l, FC, bin_h - FD, bin_pos_l + OF - item_l, bin_pos_w, FD + bin_pos_h, 3]

    box[4][0:7] = [OF - item_l, bin_w - HI, bin_h, bin_pos_l + 0, bin_pos_w + HI, bin_pos_h, 4]
    box[5][0:7] = [OF - item_l, HI, bin_h - FD, bin_pos_l + 0, bin_pos_w, FD + bin_pos_h, 5]

    return box


def move_item_to_prepack(bin_info, item_size, number_of_best_fit, pre_pack_item_space_list):
    item_size_pack = np.copy(item_size)
    item_size_pack[3] = min(item_size[3], number_of_best_fit[0])
    item_size[3] = item_size[3] - item_size_pack[3]
    pre_pack_item_space_list.append([bin_info, item_size_pack, item_size_pack[3], number_of_best_fit])


class Helper:
    def __init__(self):
        pass

    @staticmethod
    @njit(cache=True)
    # Cần viết lại hàm này.,
    def decompose_bin(bin_info, item_size):
        best_fit = compute_number_of_fit_with_rotation(bin_info, item_size)

        OZ_rotation_lock = item_size[9]

        new_rotate_size = compute_rotate_item_size(item_size, best_fit[4], OZ_rotation_lock)
        M_lwh = new_rotate_size[0]
        M_l = new_rotate_size[1]
        M_w = new_rotate_size[2]
        M_h = new_rotate_size[3]
        best_rotate = new_rotate_size[4]

        boxes = compute_box(bin_info, item_size, best_fit, new_rotate_size)
        if item_size[3] == 0:
            boxes = np.empty((6, len(bin_info)), np.int_)
            for i in range(6):

                for j in range(len(bin_info)):
                    if i == 0:
                        boxes[0][j] = bin_info[j]
                    else:
                        boxes[i][j] = 0
            boxes[0] = bin_info

        return boxes


helper = Helper()

@njit (cache= True)
def compute_rotate_item_size(size, rotate, OZ_rotation_lock): # return newsize after rotate. =0 1
    ROTATE_FIX =  np.array([  [0,1,2],  [1,0,2], [0,2,1], [1,2,0], [2,1,0],[2,0,1]], np.int_)
    ROTATE_FIX_WITH_OZ_LOCK =  np.array([  [0,1,2],  [1,0,2]], np.int_)

    if OZ_rotation_lock ==0:
        new  =   ROTATE_FIX[rotate]
    else:
        new  =   ROTATE_FIX_WITH_OZ_LOCK[rotate]

    new_size  =   np.concatenate((np.array([size[new[0]], size[new[1]], size[new[2]]], np.int_) , size[3:]   ))
    return new_size
@njit (cache= True)
def compute_number_of_fit(bin_info,item_size): #find number of fit of an item without rotate.
    M_l = math.floor(bin_info[0]/item_size[0])
    M_w = math.floor(bin_info[1]/item_size[1])
    M_h = math.floor(bin_info[2]/item_size[2])
    result  =  np.empty((4), np.int_)
    result[0] =  M_h*M_l*M_w
    result[1] =  M_l
    result[2] =  M_w
    result[3] =  M_h
    return result

@njit (cache= True)
def insert___(bin_info, item_size, mylist, number_item, number_of_best_fit):
    ITEM_L_ID  =  0
    ITEM_W_ID  =  1
    ITEM_H_ID  =  2

    ITEM_NUM  =  3
    ITEM_ROTATE =  4

    ITEM_POS_L_ID  = 5
    ITEM_POS_W_ID  =  6
    ITEM_POS_H_ID  = 7

    BIN_L_ID  =  0
    BIN_W_ID  =  1
    BIN_H_ID  =  2
    BIN_POS_L_ID  = 3
    BIN_POS_W_ID  =  4
    BIN_POS_H_ID  =  5
    BIN_ID  =  6
    M_lwh= number_of_best_fit[0]
    M_l= number_of_best_fit[1]
    M_w= number_of_best_fit[2]
    M_h= number_of_best_fit [3]
    best_rotate = number_of_best_fit[4]
    OZ_rotation_lock= item_size[9]
    rotate_size = compute_rotate_item_size(item_size, best_rotate, OZ_rotation_lock)
    # number_item  =  item_size[ITEM_NUM]
    if  number_item> M_lwh:
        number_item = M_lwh

    num_of_face= math.floor(number_item/(M_w*M_h))
    # số lát bánh mỳ
    for i in range(num_of_face):
        for j in range(M_w):
            a= rotate_size[ITEM_L_ID]
            b= rotate_size[ITEM_W_ID]
            c= rotate_size[ITEM_H_ID]*M_h

            d= M_h
            e= best_rotate #item_size[ITEM_ROTATE]

            f= bin_info[BIN_POS_L_ID]+ i*rotate_size[ITEM_L_ID]
            g= bin_info[BIN_POS_W_ID]+ j*rotate_size[ITEM_W_ID]
            h= bin_info[BIN_POS_H_ID]

            s= rotate_size[4]
            mylist.append( np.array([a, b, c, d, e, f, g, h, s], np.int_))

    left_over_of_face= number_item%(M_w*M_h)
    num_of_column = math.floor(left_over_of_face/M_h)
    for j in range(num_of_column):

        a= rotate_size[ITEM_L_ID]
        b= rotate_size[ITEM_W_ID]
        c= rotate_size[ITEM_H_ID] *M_h

        d= M_h
        e= best_rotate #item_size[ITEM_ROTATE]

        f= bin_info[BIN_POS_L_ID]+ num_of_face*rotate_size[ITEM_L_ID]
        g= bin_info[BIN_POS_W_ID]+ j*rotate_size[ITEM_W_ID]
        h= bin_info[BIN_POS_H_ID]

        s= rotate_size[4]
        mylist.append( np.array([a, b, c, d, e, f, g, h, s], np.int_))

    left_over_of_column = number_item % M_h
    if left_over_of_column>0:
        a= rotate_size[ITEM_L_ID]
        b= rotate_size[ITEM_W_ID]
        c= rotate_size[ITEM_H_ID]*left_over_of_column

        d= left_over_of_column
        e= best_rotate #item_size[ITEM_ROTATE]

        f= bin_info[BIN_POS_L_ID]+ num_of_face*rotate_size[ITEM_L_ID]
        g= bin_info[BIN_POS_W_ID]+ num_of_column*rotate_size[ITEM_W_ID]
        h= bin_info[BIN_POS_H_ID]

        s= rotate_size[4]
        mylist.append( np.array([a, b, c, d, e, f, g, h, s], np.int_))

    return mylist


class PackingABin:
    # C : pack
    # R : decompress to mylist/ mylist_final
    # U : repack
    # D : remove all and undo pack
    def __init__(self, bin, item_list=[]):
        self.bin = bin
        self.usable_space = bin.usable_space_list
        self.item_list = item_list
        self.original_item_list = copy.deepcopy(item_list)
        # self.pre_pack_item_space_list = bin.prepack_item_space_list
        self.original_bin_list = copy.deepcopy(bin.usable_space_list)
        self.last_state = copy.deepcopy(bin)
        self.recycle_item_list = []
        self.new_prepack_item_list = None
        self.helper = Helper()

    # vấn đề cần xử lý tương tự remove
    def undo_pack(self):
        self.recycle_item_list = self.convert_prepack_to_recycle_list()
        for attr, value in self.last_state.__dict__.items():
            setattr(self.bin, attr, getattr(self.last_state, attr))

    # remove xong cần lấy toàn bộ item trong recycle trả vào list of batch items
    def remove_all_item(self):
        self.recycle_item_list = self.convert_prepack_to_recycle_list(False)
        self.bin = Bin((np.array(self.bin.bin_info), np.int_))

    def pack(self):
        usable_space_list = copy.deepcopy(self.bin.usable_space_list)
        item_list = self.item_list
        min_item_dim = min([min(item.item_info[0], item.item_info[1], item.item_info[2]) for item in item_list])
        wasted_space_list = copy.deepcopy(self.bin.wasted_space_list)
        pre_pack_item_space_list_BACKUP = copy.deepcopy(self.bin.prepack_item_space_list)
        move_bin_to_next_item = []
        pre_pack_item_space_list = []
        self.last_state = copy.deepcopy(self.bin)
        self.bin.prepack_item_space_list = []

        for i in range(len(item_list)):
            item = item_list[i]

            count = 0
            if len(usable_space_list) == 0:
                break
            b = len(usable_space_list) - 1
            move_bin_to_next_item = []
            while True:

                b = len(usable_space_list) - 1

                if len(usable_space_list) == 0:
                    break
                if b == len(usable_space_list) or b < 0:
                    break

                temp_usable_space_list = []

                count = count + 1

                usable_space_list.sort(key=lambda x: -(x[0] ** 2 - x[2]))

                bin = usable_space_list[b]

                # wasted_space_list
                if min(bin[0], bin[1], bin[2]) < min_item_dim:
                    wasted_space_list.append(bin)
                    usable_space_list.pop(b)

                    continue
                # move_bin_to_next_item
                if item.item_info[3] == 0:
                    move_bin_to_next_item.append(bin)

                    usable_space_list.pop(b)
                    break

                # move_bin_to_next_item

                if min(bin[0], bin[1], bin[2]) < min([item.item_info[0], item.item_info[1], item.item_info[2]]):
                    move_bin_to_next_item.append(bin)
                    # cai nay, can cho vao next round
                    usable_space_list.pop(b)

                    continue

                number_of_best_fit = compute_number_of_fit_with_rotation(bin, item.item_info)
                number_of_fit = number_of_best_fit[0]
                # move_bin_to_next_item
                if number_of_fit == 0:
                    move_bin_to_next_item.append(bin)

                    usable_space_list.pop(b)

                    continue
                else:
                    box = self.helper.decompose_bin(bin, item.item_info)

                    for k in range(len(box)):
                        # wasted_space_list
                        if min(box[k][0], box[k][1], box[k][2]) < 1:
                            continue
                        # wasted_space_list
                        if min(box[k][0], box[k][1], box[k][2]) < min_item_dim:
                            wasted_space_list.append(box[k])
                            continue

                        temp_usable_space_list.append(box[k])
                    move_item_to_prepack(bin, item.item_info, number_of_best_fit, pre_pack_item_space_list)
                    usable_space_list.pop(b)

                    usable_space_list = usable_space_list + temp_usable_space_list

                    continue

            usable_space_list = usable_space_list + move_bin_to_next_item

        self.bin.wasted_space_list = wasted_space_list
        self.bin.usable_space_list = usable_space_list
        self.new_prepack_item_list = pre_pack_item_space_list
        self.bin.prepack_item_space_list = pre_pack_item_space_list_BACKUP + pre_pack_item_space_list

    def decompress(self):
        pre_pack_item_space_list = self.bin.prepack_item_space_list
        mylist = List()
        mylist.append(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0], np.int_))
        mylist.pop(0)
        for bunch in pre_pack_item_space_list:
            bin, item, num_item, number_of_best_fit = bunch
            mylist = insert___(bin, item, mylist, num_item, number_of_best_fit)

        mylist_final = [[item[0], item[1], item[2], item[5], item[6], item[7]] for item in mylist]
        self.mylist = mylist_final
        return mylist_final

    def convert_prepack_to_recycle_list(self, only_last_state=True):
        if only_last_state and self.new_prepack_item_list is not None:
            pre_pack_item_space_list = self.new_prepack_item_list
        else:
            pre_pack_item_space_list = self.bin.prepack_item_space_list
        final_dict = defaultdict(dict)

        recycle_item_list = []

        for bunch in pre_pack_item_space_list:
            bin, item, num_item, number_of_best_fit = bunch
            recycle_item_list.append([item, num_item])

        temp_dict = defaultdict(dict)

        for item_and_num in recycle_item_list:
            temp_dict[item_and_num[0][8], item_and_num[0][10]] = []
            final_dict[item_and_num[0][10]] = []

        for item_and_num in recycle_item_list:
            temp_dict[item_and_num[0][8], item_and_num[0][10]].append(item_and_num)

        for id_item_id_batch, item_and_num in temp_dict.items():
            root_item = item_and_num[0][0]

            total_num = sum([number_of_this_kind_item[1] for number_of_this_kind_item in item_and_num])
            root_item[3] = total_num
            final_dict[id_item_id_batch[1]].append(root_item)

        mylist_final = []
        for key, val in final_dict.items():
            mylist_final.append(val)

        return mylist_final

    def draw_packed_bin(self, bin, item_list):
        def get_random_color():
            return "#%06x" % rd.randint(0, 0xFFFFFF)

        color_list = []
        for i in range(1000):
            color_list.append(get_random_color())

        data = []

        data.append(
            go.Mesh3d(
                x=[0, 0, int(bin[0]), int(bin[0]), 0, 0, int(bin[0]), int(bin[0])],
                y=[0, int(bin[1]), int(bin[1]), 0, 0, int(bin[1]), int(bin[1]), 0],
                z=[0, 0, 0, 0, int(bin[2]), int(bin[2]), int(bin[2]), int(bin[2])],
                # Intensity of each vertex, which will be interpolated and color-coded
                # i, j and k give the vertices of triangles

                # i  =  [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
                # j  =  [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
                # k  =  [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
                name='y',
                showscale=True,
                color="#555",
                opacity=0.1
            )
        )

        for index in range(len((item_list))):
            item = item_list[index]
            ox_item = int(item[3])
            oy_item = int(item[4])
            oz_item = int(item[5])

            # true_size  =  item.get_dimension()

            extreme_x = int(item[0]) + ox_item
            extreme_y = int(item[1]) + oy_item
            extreme_z = int(item[2]) + oz_item
            # print(oz_item,extreme_x)

            data.append(
                go.Mesh3d(
                    x=[ox_item, ox_item, extreme_x, extreme_x, ox_item, ox_item, extreme_x, extreme_x],
                    y=[oy_item, extreme_y, extreme_y, oy_item, oy_item, extreme_y, extreme_y, oy_item],
                    z=[oz_item, oz_item, oz_item, oz_item, extreme_z, extreme_z, extreme_z, extreme_z],
                    # Intensity of each vertex, which will be interpolated and color-coded
                    # i, j and k give the vertices of triangles
                    i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
                    j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
                    k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
                    # name   =    " %s " %(item.name) ,
                    showscale=True,
                    # color  = 'red',
                    color=get_random_color(),
                    # hovertext  =  "box "+str(index),
                    opacity=1, flatshading=True
                )
            )
            data.append(go.Scatter3d(x=[0], y=[0], z=[0], mode='markers'))

        fig = go.Figure(data)
        # fig   =   go.Figure(data = [go.Mesh3d(x = [0], y = [0], z = [0], color = 'lightpink', opacity = 0.50)])
        fig.update_layout(
            autosize=False,
            width=1300,
            height=900,
            scene_aspectmode='data',
            scene_camera=dict(eye=dict(x=-2, y=-2, z=-1))
        )

        fig.show()

    def visualize_item(self):
        self.draw_packed_bin(self.original_bin_list[0], self.mylist)

    @staticmethod
    @njit(cache=True)
    def compute_number_of_fit(bin_info, item_size):  # find number of fit of an item without rotate.
        M_l = math.floor(bin_info[0] / item_size[0])
        M_w = math.floor(bin_info[1] / item_size[1])
        M_h = math.floor(bin_info[2] / item_size[2])
        result = np.empty((4), np.int_)
        result[0] = M_h * M_l * M_w
        result[1] = M_l
        result[2] = M_w
        result[3] = M_h
        return result


class Packer:
    def __init__(self, list_of_bin, list_of_item):
        self.list_of_bin = list_of_bin
        self.list_of_item = list_of_item

    def check_fit_batch_into_bin(self, bin, batch, keep_pack_result=False, keep_pack_if_fit_all=False):
        packing_problem = PackingABin(bin, batch)
        packing_problem.pack()

        left_over_itemCbm = sum([it.get_cbm for it in batch])

        fit = True

        if left_over_itemCbm > 0:
            fit = False

        if not keep_pack_result or not (fit and keep_pack_if_fit_all):
            packing_problem.undo_pack()
            thrown_items = packing_problem.recycle_item_list[0]
            for item in batch:
                for it in thrown_items:
                    if item.item_info[8] == it[8]:
                        item.item_info[3] += it[3]

            left_over_itemCbm = sum([it.get_cbm for it in batch])

        bin = copy.deepcopy(packing_problem.bin)

        return fit

    def restore_all_item_in_bin(self):

        batch_dict = defaultdict(dict)

        for id in self.batch_id_list:
            batch_dict[id] = []

        for bin in self.list_of_bin:
            packing_problem = PackingABin(bin)
            packing_problem.remove_all_item()

            thrown_items = packing_problem.recycle_item_list
            thrown_items = [x for batchz in thrown_items for x in batchz]

            for it in thrown_items:
                for batch in self.list_of_item:
                    for item in batch:
                        if (item.item_info[8] == it[8]).all() and (item.item_info[10] == it[10]).all():
                            item.item_info[3] += it[3]

    def check_fit_how_many_integer_bins(self, is_splittable_batch=False):
        bin_id = 0
        temp_batch_list = []

        batch_list = copy.deepcopy(self.list_of_item)

        batch_list_with_index = [[idx, b] for idx, b in enumerate(batch_list)]

        packed_batch = {}

        root_batch_index = 0

        while True:
            if len(batch_list_with_index) == 0:
                if len(temp_batch_list) > 0:
                    batch_list_with_index.extend(temp_batch_list)
                    temp_batch_list = []
                    bin_id += 1
                else:
                    break

            if bin_id >= len(self.list_of_bin):
                break

            current_batch_with_index = batch_list_with_index.pop(0)

            current_index, current_batch = current_batch_with_index

            total_cbm_temp_batch = sum([it.get_cbm for it in current_batch])

            if total_cbm_temp_batch > self.list_of_bin[bin_id].get_leftover_cbm:

                if is_splittable_batch:
                    packing_problem = PackingABin(self.list_of_bin[bin_id], current_batch)
                    packing_problem.pack()
                    packed_batch[current_index] = current_batch

                temp_batch_list.append([current_index, current_batch])
            else:

                packing_problem = PackingABin(self.list_of_bin[bin_id], current_batch)
                packing_problem.pack()

                left_over_batch_cbm = sum([it.get_cbm for it in current_batch])

                if left_over_batch_cbm > 0:

                    if not is_splittable_batch:
                        packing_problem.undo_pack()
                        # must restore item for current pack
                        thrown_items = packing_problem.recycle_item_list

                        thrown_items = [x for batchz in thrown_items for x in batchz]

                        for item in current_batch:
                            for it in thrown_items:
                                if item.item_info[8] == it[8]:
                                    item.item_info[3] += it[3]
                    else:
                        packed_batch[current_index] = current_batch

                    temp_batch_list.append([current_index, current_batch])
                else:
                    packed_batch[current_index] = current_batch

        nb_bin = sum([1 for bin in self.list_of_bin if bin.get_leftover_cbm - bin.get_cbm])

        final_batch_list = []

        for k, v in packed_batch.items():
            final_batch_list.insert(k, v)

        if final_batch_list:
            self.list_of_item = copy.deepcopy(final_batch_list)

        return nb_bin


