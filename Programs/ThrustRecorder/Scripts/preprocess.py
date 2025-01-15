import cv2
import os

total_frames = 0
def get_total_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return total_frames

def extract_frame(video_path, frame_number):
    """
    从视频文件中提取指定编号的帧图像，并返回灰度图像和时间戳。

    参数：
    - video_path: 视频文件路径。
    - frame_number: 要提取的帧号（0表示第一帧）。

    返回：
    - 提取的特定帧的灰度图像和时间戳。
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("无法打开视频文件。")

    # 将视频流移动到指定帧
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    ret, img = cap.read()
    if not ret:
        raise ValueError(f"无法读取第 {frame_number} 帧。")
    
    # 获取当前帧的时间戳（以秒为单位）
    timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
    
    # 将图像转换为灰度模式
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    cap.release()  # 关闭视频文件

    return gray_img, timestamp

def image_thresholding(image_path_or_frame, threshold_value=127, save_path="output", timestamp=None):
    """
    使用全局阈值进行图像二值化，并保存结果。

    参数：
    - image_path_or_frame: 图像文件的路径或从 video 中提取的帧。
    - threshold_value: 阈值，通常介于 0 和 255 之间，默认为127。
    - save_path: 保存图像的目录。
    - timestamp: 当前帧的时间戳，用于命名保存的文件。

    返回：
    - 二值化的图像（灰度级图像）。
    """
    
    # 根据输入类型判断是文件路径还是视频帧
    if isinstance(image_path_or_frame, str):
        img = cv2.imread(image_path_or_frame, cv2.IMREAD_GRAYSCALE)
    else:
        img = image_path_or_frame

    if img is None:
        raise ValueError("无法加载指定的图像。")

    # 应用全局阈值进行二值化
    _, binary_img = cv2.threshold(img, threshold_value, 255, cv2.THRESH_BINARY)

    # 如果提供了时间戳，则保存图像
    if timestamp is not None:
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        file_name = f"{save_path}/{timestamp:.3f}.png"
        cv2.imwrite(file_name, binary_img)
        print(f"    Saved: {file_name}")

    return binary_img