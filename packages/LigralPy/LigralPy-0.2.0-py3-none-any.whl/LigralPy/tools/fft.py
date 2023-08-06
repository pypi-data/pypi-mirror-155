from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from scipy.signal import find_peaks

df = pd.read_csv("data.csv", sep="\t")
a = df["b"].to_numpy()
# print(a)
f_sample = 100  # 采样率
T_sample = 1 / f_sample  # 采样区间长度
n = len(a)  # 信号长度
real_time = n / f_sample  # 实际经过的时间

k = np.arange(n)  # 采样点数
x = k / real_time  # x轴
print(x, k, real_time)

window = np.hamming(n)
# window = np.ones(n) #矩形窗
a1 = window * a
YY = np.fft.fft(a1)  # 未归一化
Y = YY / n
x = x[: int(n / 2)]
f_max_ampl = x[np.argmax(Y[: int(n / 2)])]
print("峰值出现在：", x[find_peaks(abs(Y[: int(n / 2)]))[0]])

print("最大幅值的响应：", f_max_ampl, "Hz", f"ω={f_max_ampl*2*np.pi} ")
plt.subplot(311)
plt.plot(x, abs(Y[: int(n / 2)]))
plt.xlim((0, 3))
plt.subplot(312)
plt.plot(window)
plt.subplot(313)
plt.plot(a1)
plt.show()
