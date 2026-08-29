import matplotlib.pyplot as plt
import numpy as np

# Streamlit云端渲染必须配置
plt.switch_backend("Agg")
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def draw_wave(t, signal, title="波形图", xlabel="时间 (s)", ylabel="幅值"):
    fig, ax = plt.subplots(figsize=(10,4), dpi=150)
    ax.plot(t, signal, color="#1f77b4", linewidth=1.4, antialiased=True)
    ax.grid(True, alpha=0.2)
    ax.axhline(y=0, color="#666666", lw=0.8)
    ax.set_title(title, fontsize=11)
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_ylabel(ylabel, fontsize=8)
    plt.tight_layout()
    return fig

def draw_spectrum(freq, amp, title="频谱图"):
    fig, ax = plt.subplots(figsize=(10,4), dpi=150)
    markerline, stemlines, baseline = ax.stem(freq, amp, basefmt=" ", linefmt="#ff6666", markerfmt="o")
    plt.setp(markerline, markersize=4)
    ax.grid(True, alpha=0.2)
    ax.axhline(y=0, color="#666666", lw=0.8)
    ax.set_title(title, fontsize=11)
    ax.set_xlabel("频率 (Hz)", fontsize=8)
    ax.set_ylabel("幅度", fontsize=8)
    ax.set_xlim(0, 50)
    plt.tight_layout()
    return fig

def draw_signal(text: str):
    """解析绘图指令，同时生成时域波形+频谱"""
    fs = 1000
    t_total = 1
    t = np.linspace(0, t_total, int(fs * t_total), endpoint=False)
    # 默认10Hz正弦信号
    f0 = 10
    signal = np.sin(2 * np.pi * f0 * t)

    # 关键词匹配不同信号
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

    # 计算FFT频谱
    N = len(signal)
    fft_vals = np.fft.fft(signal)
    fft_freq = np.fft.fftfreq(N, 1/fs)
    mask = fft_freq >= 0
    freq = fft_freq[mask]
    amp = np.abs(fft_vals[mask]) / N

    # 合并时域+频谱一张图
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10,6), dpi=150)
    # 时域子图
    ax1.plot(t, signal, color="#1f77b4", linewidth=1.4, antialiased=True)
    ax1.grid(True, alpha=0.2)
    ax1.axhline(y=0, color="#666666", lw=0.8)
    ax1.set_title("时域波形", fontsize=11)
    ax1.set_xlabel("时间 (s)", fontsize=8)
    ax1.set_ylabel("幅值", fontsize=8)
    # 频谱子图（已经修复老matplotlib兼容问题）
    markerline, stemlines, baseline = ax2.stem(freq, amp, basefmt=" ", linefmt="#ff6666", markerfmt="o")
    plt.setp(markerline, markersize=4)
    ax2.grid(True, alpha=0.2)
    ax2.axhline(y=0, color="#666666", lw=0.8)
    ax2.set_title("频谱图", fontsize=11)
    ax2.set_xlabel("频率 (Hz)", fontsize=8)
    ax2.set_ylabel("幅度", fontsize=8)
    ax2.set_xlim(0, 50)
    plt.tight_layout()
    return fig
