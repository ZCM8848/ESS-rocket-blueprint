def recognize(model, picture):
    name = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '.', 11: '.'}
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

