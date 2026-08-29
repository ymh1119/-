import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 云端matplotlib必须配置
plt.switch_backend("Agg")
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

st.title("仿真绘图专家")
prompt = st.chat_input("输入绘图指令")

if prompt:
    with st.chat_message("user"):
        st.write(prompt)
    try:
        # 直接生成波形+频谱
        fs = 1000
        t_total = 1
        t = np.linspace(0, t_total, int(fs * t_total), endpoint=False)
        signal = np.zeros_like(t)
        signal[:50] = 1

        # FFT频谱
        fft_vals = np.fft.fft(signal)
        fft_freq = np.fft.fftfreq(len(signal), 1/fs)
        mask = fft_freq >= 0
        freq = fft_freq[mask]
        amp = np.abs(fft_vals[mask]) / len(signal)

        fig, (ax1, ax2) = plt.subplots(2,1,figsize=(10,6),dpi=150)
        ax1.plot(t, signal, color="#1f77b4", linewidth=1.4)
        ax1.set_title("时域波形")
        ax1.set_xlabel("时间(s)")
        ax1.set_ylabel("幅值")
        ax1.grid(alpha=0.2)

        # 【这里就是你要改的地方】
        markerline, stemlines, baseline = ax2.stem(freq, amp, basefmt=" ", linefmt="#ff6666", markerfmt="o")
        plt.setp(markerline, markersize=4)
        
        ax2.set_title("频谱图")
        ax2.set_xlabel("频率(Hz)")
        ax2.set_ylabel("幅度")
        ax2.set_xlim(0,50)
        ax2.grid(alpha=0.2)
        plt.tight_layout()

        with st.chat_message("assistant"):
            st.pyplot(fig)
    except Exception as e:
        with st.chat_message("assistant"):
            st.error(f"绘图出错：{str(e)}")
