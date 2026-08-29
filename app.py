import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 云端matplotlib强制配置，必须放在最前面
plt.switch_backend("Agg")
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ============【你原来所有的代码、侧边栏、数据库、知识点页码逻辑全部保留在这里，不用删除】============

prompt = st.chat_input("输入你的问题，或展开左侧面板复制符号...")
if prompt:
    with st.chat_message("user"):
        st.write(prompt)
    
    # 临时强制绘图测试，直接在当前文件生成图，不调用外部plot_core
    try:
        st.write("✅ 代码成功进入绘图流程！") # 这个文字如果能出来，说明走到绘图代码了
        fs = 1000
        t_total = 1
        t = np.linspace(0, t_total, int(fs * t_total), endpoint=False)
        signal = np.zeros_like(t)
        signal[:50] = 1

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

        with st.chat_message("assistant"):
            st.write("📊 即将渲染图片")
            st.pyplot(fig)
    except Exception as e:
        with st.chat_message("assistant"):
            st.error(f"绘图出错：{str(e)}")
