import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# 读取CSV文件
df = pd.read_csv('thrust_data.csv', header=None)  # 替换'your_data.csv'为你的文件路径，若有表头，请指定header=0

# 获取数据
time = df[0].values
thrust = df[1].values

# 设置动画参数
fps = 30  # 帧率
max_time = np.max(time)

# 创建动画函数
def animate(i):
    plt.cla()
    plt.grid()
    plt.plot(time[:i], thrust[:i], 'b-')
    plt.xlabel('Time (s)')
    plt.ylabel('Thrust(kgf)')
    plt.title('MRLM-S-T5 Thrust vs. Time')
    plt.xlim(0, max_time)
    plt.ylim(np.min(thrust), np.max(thrust) + 1)

# 创建动画对象
fig = plt.figure()
anim = FuncAnimation(fig, animate, frames=len(time), interval=len(time) / max(time))
plt.show()

# 保存为MP4
#anim.save('thrust_animation.mov', fps=fps)