#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
import easydownload
import numpy as np
import platform
import datetime
import shutil
import cv2
import os
if platform.system() == 'Windows':
    path_separator = '\\'
else:
    path_separator = '/'


def show(
        name
):
    cv2.imshow('Show', name)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def proc_background(
        image_dir: str,
        out_path: str = None,
        white_value: int = 200
):
    """
    处理背景图片，将暗色区域处理为黑色
    0是黑色，255是白色，可以理解为亮度
    将灰度超过一定值的像素保留，其他像素全部转换为黑色，方便识别
    灰度的shape:(height,weight)
    :param image_dir: 图片路径
    :param out_path: 输出路径
    :param white_value: 判定为白色的分界线值，达到这个值判定为白色，默认为200
    :return: 处理完成的图片路径
    """
    image_file_name = image_dir.split(path_separator)[-1:][0]  # 获取图片文件名
    image_proc_file_name = '.'.join([image_file_name.split('.')[0] + '_proc', image_file_name.split('.')[1]])  # 生成新文件名
    if out_path is None:
        out_path = image_dir.replace(image_file_name, '')
        if out_path[-1] == path_separator:
            out_path = out_path[:-1]
        else:
            pass
    else:
        pass
    proc_file_dir = "%s%s%s" % (out_path, path_separator, image_proc_file_name)

    image = cv2.imread(image_dir)  # 默认是按照BGR读取的
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 转换为灰度
    height = image_gray.shape[0]  # 高
    weight = image_gray.shape[1]  # 宽

    black_points = list()  # 判定为黑色的像素点
    for each_weight in range(weight):
        for each_height in range(height):
            if image_gray[each_height, each_weight] >= white_value:
                # 像素是白色，跳过
                continue
            else:
                black_points.append([
                    [each_height, each_weight],  # 左上角
                ])
    # 执行填充，将被判定为黑色的值填充为纯黑色
    for each_black_point in black_points:
        for each_point in each_black_point:
            image_gray[each_point[0], each_point[1]] = 0
    # 将处理后的图片存储为新的图片
    cv2.imwrite(proc_file_dir, image_gray)
    return proc_file_dir


def proc_slider(
        image_dir: str,
        out_path: str = None,
        white_value_max: int = 255,  # 灰度判断为白色的最大值
        alpha_white_max: int = None  # 透明度通道为白色的最大值
):
    """
    处理滑块图片
    0是黑色，255是白色，可以理解为亮度
    将灰度超过一定值的像素保留，其他像素全部转换为黑色，方便识别
    :param image_dir:
    :param out_path:
    :param white_value_max: 灰度判断为白色的最大值，例如：255
    :param alpha_white_max: 透明度通道为白色的最大值，例如：15
    :return:
    """
    image_file_name = image_dir.split(path_separator)[-1:][0]  # 获取图片文件名
    image_proc_file_name = '.'.join([image_file_name.split('.')[0] + '_proc', image_file_name.split('.')[1]])

    if out_path is None:
        out_path = image_dir.replace(image_file_name, '')
        if out_path[-1] == path_separator:
            out_path = out_path[:-1]
        else:
            pass
    else:
        pass
    proc_file_dir = "%s%s%s" % (out_path, path_separator, image_proc_file_name)

    image_unchanged = cv2.imread(image_dir, cv2.IMREAD_UNCHANGED)  # 4个通道
    image_gray = cv2.cvtColor(image_unchanged, cv2.COLOR_BGR2GRAY)  # 转换为灰度图，只有1个通道

    height = image_gray.shape[0]  # 高
    weight = image_gray.shape[1]  # 宽

    for each_height in range(height):
        for each_weight in range(weight):
            # 遍历图像的每个像素
            if alpha_white_max is not None:
                if image_unchanged[each_height, each_weight][3] <= alpha_white_max:
                    image_unchanged[each_height, each_weight] = [0, 0, 0, 0]  # 判定为透明区域的，直接改为纯透明
                else:
                    image_unchanged[each_height, each_weight] = [0, 0, 0, 255]  # 判定为不透明区域的，直接改为黑色不透明
            else:
                if image_gray[each_height, each_weight] >= white_value_max:
                    image_gray[each_height, each_weight] = 255  # 判定为最白区域的，直接改为白色
                else:
                    image_gray[each_height, each_weight] = 0  # 其他区域直接改为黑色
    if alpha_white_max is None:
        cv2.imwrite(proc_file_dir, image_gray)  # 存储灰度图
    else:
        cv2.imwrite(proc_file_dir, image_unchanged)
    return proc_file_dir


def identify_gap_locations(
        background_img_url: str = None,  # 背景图地址
        background_img_dir: str = None,
        slider_img_url: str = None,  # 滑块图地址
        slider_img_dir: str = None,
        save_path: str = None,  # 保存文件夹
        retain: bool = False,  # 保留文件，True：保留文件，False：不保留文件
        proc_slider_alpha_white_max: int = None
):
    """
    识别缺口位置
    """
    # 确定文件保存路径
    if save_path is None:
        current_path = os.path.dirname(os.path.abspath(__file__))
        time_str = datetime.datetime.now().strftime('%Y-%m-%d+%H-%M-%S')
        save_path = path_separator.join([current_path, 'temp_images', time_str])
    else:
        pass

    if background_img_dir is not None:
        background_dir = background_img_dir
    else:
        background_dir = easydownload.download(
            url=background_img_url,
            filename='background',
            suffix_name='png',
            path=save_path
        )['file_dir']  # 下载背景图

    if slider_img_dir is not None:
        slider_dir = slider_img_dir
    else:
        slider_dir = easydownload.download(
            url=slider_img_url,
            filename='slider',
            suffix_name='png',
            path=save_path
        )['file_dir']  # 下载滑块图

    background_proc_dir = proc_background(
        image_dir=background_dir
    )  # 处理背景图片
    slider_proc_dir = proc_slider(
        image_dir=slider_dir,
        alpha_white_max=proc_slider_alpha_white_max
    )  # 处理滑块图片

    # 获取尺寸
    background_w, background_h = cv2.imread(
        filename=background_proc_dir,
        flags=0
    ).shape[::-1]  # 背景图尺寸
    # print(background_w, background_h)
    slider_w, slider_h = cv2.imread(
        filename=slider_proc_dir,
        flags=0
    ).shape[::-1]  # 滑块尺寸
    # print(slider_w, slider_h)

    background_proc = cv2.imread(
        filename=background_proc_dir
    )
    slider_proc = cv2.imread(
        filename=slider_proc_dir
    )

    result = cv2.matchTemplate(
        slider_proc,
        background_proc,
        cv2.TM_CCOEFF_NORMED
    )
    identify_h, identify_w = np.unravel_index(
        result.argmax(),
        result.shape
    )

    cv2.rectangle(
        background_proc,
        (identify_w, identify_h),
        (identify_w + slider_w, identify_h + slider_h),
        (7, 249, 151),
        2
    )  # 展示圈出来的区域

    recognition = save_path + path_separator + 'recognition.jpg'
    cv2.imwrite(
        recognition,
        background_proc
    )
    # show(template)
    if retain is True:
        pass
    else:
        shutil.rmtree(path=save_path)  # 删除文件夹
    # print(identify_h, identify_w)
    res = {
        'background_w': background_w,  # 背景图 距离左上角的宽度
        'background_h': background_h,  # 背景图 距离左上角的高度
        'slider_w': slider_w,  # 滑块图 距离左上角的宽度
        'slider_h': slider_h,  # 滑块图 距离左上角的高度
        'identify_w': identify_w,  # 识别图 距离左上角的宽度，主要使用此字段的值
        'identify_h': identify_h,  # 识别图 距离左上角的高度
    }
    return res


def get_track(
        distance: int,
        current: int = 0,
        t: float = 0.5,
        v: float = 0,
        mid_percent: float = 0.8,
        a_ac: float = 2,
        a_de: float = -3
):
    """
    根据偏移量获取移动轨迹
    :param distance: 偏移量
    :param current: 当前位移
    :param t: 计算间隔，数值越小，越精细
    :param v: 初速度
    :param mid_percent: 减速阈值比例
    :param a_ac: 前期加速的加速度
    :param a_de: 后期减速的加速度
    :return: 移动轨迹
    """
    track = []  # 移动轨迹
    mid = distance * mid_percent  # 减速阈值

    while current < distance:
        if current < mid:
            a = a_ac  # 加速度，加速
        else:
            a = a_de  # 加速度，减速
        v0 = v  # 初速度v0
        v = v0 + a * t  # 当前速度v = v0 + at
        move = v0 * t + 1 / 2 * a * t * t  # 移动距离x = v0t + 1/2 * a * t^2

        cal_gap = int(move)  # 单次位移
        current += int(move)  # 累计位移
        if current > distance:
            cal_gap = cal_gap + distance - current
        track.append(cal_gap)
    return track
