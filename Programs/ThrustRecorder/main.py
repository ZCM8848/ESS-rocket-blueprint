from Scripts import *
from ultralytics import YOLO

# define consts
video_to_process = ".\\src\\main.mp4"
curve = {}
model1 = YOLO(".\\Models\\model_123.pt")
model2 = YOLO(".\\Models\\model_180.pt")
name = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '.', 11: '.'}

# preprocess
print("preprocessing:")
for i in range(get_total_frames(video_to_process)):
    frame_image, timestamp = extract_frame(video_to_process, i)
    binary_image = image_thresholding(frame_image, timestamp=timestamp, save_path=".\\output")

# predict
print("Predicting:")
pictires = find_png_images(".\\output")
for pic in pictires:
    path = pic
    pic = pic.split("\\")[-1]
    pic = pic.split(".png")[0]
    pic = float(pic)

    result1 = recognize(model1, path)
    result2 = recognize(model2, path)
    if result1 is not None or result2 is not None:
        if result1 != result2:
            curve[pic] = result1 if result1 else result2
        else:
            curve[pic] = result1
        print(f"    {path} has reading: {curve[pic]}")

# postprocess
print("Postprocessing:")
sorted_curve = sort_dict_by_keys(curve)
time = list(sorted_curve.keys())
thrust = list(sorted_curve.values())
for i in range(len(time)):
    if i > 0 and i < len(time):
        delta = abs(thrust[i] - thrust[i - 1])
        if delta >= 1:
            print(f"    Abnormal value {thrust[i-1]} detected, removed.")
            del time[i-1]
            del thrust[i-1]
print()
sorted_curve = dict(zip(time, thrust))
to_csv(sorted_curve,".\\thrust_curve.csv")
print("saved")
plot_dict(sorted_curve, "The thrust curve of Mark's hand", xlabel="time", ylabel="thrust(kgf)")