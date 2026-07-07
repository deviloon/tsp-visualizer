import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import matplotlib.animation as animation

st.set_page_config(page_title="TSP Visualizer", layout="centered")

st.title("Визуализация задачи коммивояжера")
st.subheader("Ссылка на репозиторий: https://sourcecraft.dev/derklugekopf/tsp")

col1, col2 = st.columns(2)

with col1:
    default_coords = """999 218
-849 233
-857 748
-97 624
324 -592
231 -11
-107 664
-750 -254
-650 -155
-923 -287
-320 410
-251 22
-330 -145
-135 -700
507 -839
-760 691
-726 -657
498 -626
-942 -177
-862 760
87 -581
-95 -483
131 -201
-719 971
-930 927
-274 -715
649 343
-693 767
436 -404
287 191
560 -839
317 131
-694 -601
-128 637
778 -410
538 58
-807 -408
-889 505
455 -863
-49 -955
-4 319
-265 640
296 717
300 608
-80 -726
-71 -818
-551 137
198 45
197 -203
830 -638
-409 -515
-327 -552
818 83
-88 966
-93 -932
564 663
251 -266
-493 -626
640 -780
-689 497"""
    coords_input = st.text_area("Координаты городов (X Y):", value=default_coords, height=250)

with col2:
    default_solution = "25 24 54 7 4 34 42 11 41 44 43 56 27 1 53 36 32 30 48 6 23 49 57 29 18 35 50 59 31 15 39 5 21 22 14 45 46 40 55 26 52 51 58 17 33 37 10 19 8 9 13 12 47 2 38 60 16 28 3 20"
    solution_input = st.text_area("Последовательность пути:", value=default_solution, height=250)

interval = st.slider("Интервал обновления (мс):", min_value=50, max_value=1000, value=150, step=50)

@st.cache_resource
def build_animation(coords_text, solution_text, frame_interval):
    
    coordinates = []
    for line in coords_text.strip().split('\n'):
        if line:
            x, y = map(int, line.split())
            coordinates.append((x, y))

    
    path_indices = [int(node) - 1 for node in solution_text.split()]

    
    path_coords = [coordinates[idx] for idx in path_indices]
    path_coords.append(path_coords[0])

    route_x, route_y = zip(*path_coords)
    cities_x, cities_y = zip(*coordinates)

    # Построение графика
    fig, ax = plt.subplots(figsize=(8, 6.5))
    ax.set_xlim(min(cities_x) - 100, max(cities_x) + 100)
    ax.set_ylim(min(cities_y) - 100, max(cities_y) + 100)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_title("Обход городов коммивояжером", fontsize=12)

    
    ax.scatter(cities_x, cities_y, color='red', s=45, edgecolors='black', zorder=2)

    # Номера городов
    for i, (x, y) in enumerate(coordinates):
        ax.annotate(f"{i + 1}", (x, y), textcoords="offset points", xytext=(0, 6), ha='center', fontsize=8, color='darkslategray')

    line, = ax.plot([], [], color='royalblue', linestyle='-', linewidth=2, zorder=1)
    traveler, = ax.plot([], [], color='lime', marker='o', markersize=10, markeredgecolor='black', zorder=3)
    step_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=10, bbox=dict(facecolor='white', alpha=0.7))

    def init():
        line.set_data([], [])
        traveler.set_data([], [])
        step_text.set_text('')
        return line, traveler, step_text

    def update(frame):
        line.set_data(route_x[:frame + 1], route_y[:frame + 1])
        traveler.set_data([route_x[frame]], [route_y[frame]])
        if frame < len(path_indices):
            step_text.set_text(f"Шаг: {frame + 1}/{len(path_indices)}\nГород: {path_indices[frame] + 1}")
        else:
            step_text.set_text("Маршрут завершен")
        return line, traveler, step_text

    ani = animation.FuncAnimation(
        fig, 
        update, 
        frames=len(path_coords), 
        init_func=init, 
        blit=True, 
        interval=frame_interval, 
        repeat=True
    )
    
    
    html_data = ani.to_jshtml()
    plt.close(fig)
    return html_data

if st.button("Сгенерировать анимацию"):
    with st.spinner("Пожалуйста, подождите."):
        try:
            
            animation_html = build_animation(coords_input, solution_input, interval)
            
            components.html(animation_html, height=750)
        except Exception as e:
            st.error(f"Произошла ошибка при обработке данных: {e}")