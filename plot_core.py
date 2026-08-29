import matplotlib.pyplot as plt
import numpy as np

plt.switch_backend("Agg")
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def draw_signal(text: str):
    fs = 1000
    t_total = 1
    t = np.linspace(0, t_total, int(fs * t_total), endpoint=False)
    f0 = 10
    signal = np.sin(2 * np.pi * f0 * t)

    if "20hz" in text.lower():
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

    N = len(signal)
    fft_vals = np.fft.fft(signal)
    fft_freq = np.fft.fftfreq(N, 1/fs)
    mask = fft_freq >= 0
    freq = fft_freq[mask]
    amp = np.abs(fft_vals[mask]) / N

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10,6), dpi=150)
    ax1.plot(t, signal, color="#1f77b4", linewidth=1.4)
    ax1.grid(True, alpha=0.2)
    ax1.set_title("时域波形")
    ax1.set_xlabel("时间 (s)")
    ax1.set_ylabel("幅值")

    markerline, stemlines, baseline = ax2.stem(freq, amp, basefmt=" ", linefmt="#ff6666", markerfmt="o")
    plt.setp(markerline, markersize=4)
    ax2.grid(True, alpha=0.2)
    ax2.set_title("频谱图")
    ax2.set_xlabel("频率 (Hz)")
    ax2.set_ylabel("幅度")
    ax2.set_xlim(0, 50)

    fig.canvas.draw()
    plt.tight_layout()
    return fig
