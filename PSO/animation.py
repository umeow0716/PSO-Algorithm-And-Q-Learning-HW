import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

history = []

def show_animation(recorded, epoch=0):
    data = []
    
    if 't_0' not in recorded:
        return
    
    fig, ax = plt.subplots()
    ax.set_xlim(-150, 150)
    ax.set_ylim(-150, 150)

    particle_len = len([0 for p in recorded['t_0'].values() if 'pos' in p])
    
    colors = np.random.rand(particle_len, 3)
    scat = ax.scatter([0]*particle_len, [0]*particle_len, c=colors, s=10)
    
    red_dot = ax.scatter([1000], [1000], 
        s=20, c="red", marker="o", edgecolors="black")

    red_text = ax.text(1000, 1000, 
        "global best", color="red", fontsize=8, weight="bold")
    
    def init():
        scat.set_offsets([[0,0],[0,0]])
        return scat,
    
    def update(frame: int):
        global history
        points = frames[frame]

        # 把新點加入歷史
        history.extend(points)

        # # 只保留最近 N 個點避免太長
        N = 500
        if len(history) > N:
            history = history[-N:]
        
        all_colors = []
        for j, h in enumerate(history):
            alpha = (j+1) / len(history)  # 從淡到深
            all_colors.append((*(colors[j % 10]), alpha))  # 藍色 (R,G,B,alpha)

        scat.set_offsets(history)
        scat.set_facecolor(all_colors)
        
        red_dot.set_offsets(data[frame])
        red_text.set_position((data[frame][0] + 2, data[frame][1] + 2))

        return scat, red_dot, red_text
        
    frames = []
    for t_key in sorted(recorded.keys(), key=lambda k: int(k.split("_")[1])):  # 按 t_順序排序
        particles = recorded[t_key]
        points = [p["pos"] for p in particles.values() if 'pos' in p]
        data.append(particles['global_best'])
        frames.append(points)
        
    ani = animation.FuncAnimation(
        fig, update, frames=len(frames),
        init_func=init, blit=False, interval=1, repeat=False
    )

    plt.show()
