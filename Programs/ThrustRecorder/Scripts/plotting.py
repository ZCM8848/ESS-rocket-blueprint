import matplotlib.pyplot as plt

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