from ultralytics import YOLO
import os
import glob
import csv
import matplotlib.pyplot as plt

def find_png_images(directory):
    png_files = glob.glob(os.path.join(directory, '**', '*.png'), recursive=True)
    return png_files

def recognize(picture):
    global model
    value = ""
    results = model.predict(picture, verbose=False)
    boundaries = results[0].boxes.xyxy.tolist()
    classes = results[0].boxes.cls.tolist()
    
    boundaries_upperleft = [i[0] for i in boundaries]
    boundaries_upperleft_sorted = boundaries_upperleft.copy()
    boundaries_upperleft_sorted.sort()

    for i in boundaries_upperleft_sorted:
        value += name[classes[boundaries_upperleft.index(i)]]
    try:
        return float(value)
    except:
        return None

def to_csv(dictionary, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(['time', 'thrust'])

        for key, value in dictionary.items():
            writer.writerow([key, value])
    
    return None

def sort_dict_by_keys(input_dict):
    sorted_keys = sorted(input_dict.keys())
    
    sorted_dict = {key: input_dict[key] for key in sorted_keys}
    
    return sorted_dict

def plot_dict(data_dict, title, xlabel='Keys', ylabel='Values'):
    keys = list(data_dict.keys())
    values = list(data_dict.values())
    
    plt.figure()
    
    plt.plot(keys, values, marker='o')
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    plt.grid(True)
    
    plt.show()

curve = {}
model = YOLO(".\\model_123.pt")
name = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '.', 11: '.'}
pictires = find_png_images(".\\output")
for pic in pictires:
    path = pic
    pic = pic.split("\\")[-1]
    pic = pic.split(".png")[0]
    pic = float(pic)
    if recognize(path) is not None:
        curve[pic] = recognize(path)
        print(f"timestamp {pic} has reading: {curve[pic]}")

sorted_curve = sort_dict_by_keys(curve)
to_csv(sorted_curve,".\\thrust_curve.csv")
print("saved")
plot_dict(sorted_curve, "The thrust curve of Mark's hand", xlabel="time", ylabel="thrust(kgf)")