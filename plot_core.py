import matplotlib.pyplot as plt
import numpy as np

plt.switch_backend("Agg")
# 优先云端文泉驿字体，Windows本地自动回退黑体，两边都可用
plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei','SimHei']
plt.rcParams['axes.unicode_minus'] = False

def draw_signal(text: str):
    # 增加空值防护，text为None/空字符串直接返回默认波形
    if text is None:
        text = ""
    text = text.lower()
    
    fs = 1000
    t_total = 1
    t = np.linspace(0, t_total, int(fs * t_total), endpoint=False)
    f0 = 10
    signal = np.sin(2 * np.pi * f0 * t)
    # 下面原来的if判断就不要再写 .lower() 了！上面已经统一转小写
    if "20hz" in text:
        f0 = 20
        signal = np.sin(2 * np.pi * f0 * t)
    elif "方波" in text:
        f0 = 20
        signal = np.sign(np.sin(2 * np.pi * f0 * t))
    elif "脉冲" in text:
        signal = np.zeros_like(t)
        signal[:50] = 1
    elif "叠加" in text:
        signal = np.sin(2 * np.pi * 10 * t) + np.sin(2 * np.pi * 30 * t)
        
    # 剩下FFT、绘图、return fig全部保留不变
    N = len(signal)
    fft_vals = np.fft.fft(signal)
    fft_freq = np.fft.fftfreq(N, 1/fs)
    mask = fft_freq >= 0
    freq = fft_freq[mask]
    amp = np.abs(fft_vals[mask]) / N
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10,6), dpi=150)
    ax1.plot(t, signal, color="#1f77b4", linewidth=1.4)
    ax1.grid(True, alpha=0.2)
    ax1.set_title("Time‑domain Waveform")
    ax1.set_xlabel("t (s)")
    ax1.set_ylabel("Amplitude")
    markerline, stemlines, baseline = ax2.stem(freq, amp, basefmt=" ", linefmt="#ff6666", markerfmt="o")
    plt.setp(markerline, markersize=4)
    ax2.grid(True, alpha=0.2)
    ax2.set_title("Frequency Spectrum")
    ax2.set_xlabel("f (Hz)")
    ax2.set_ylabel("Magnitude")
    ax2.set_xlim(0, 50)
    fig.canvas.draw()
    plt.tight_layout()
    return fig
