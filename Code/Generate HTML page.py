import folium


final_locations = [
    # --- 日本组 ---
    {'name': '东京 (Tokyo)', 'lat': 35.6804, 'lng': 139.7690, 'type': 'ns', 'freq': 8, 'lyric': '东京之旅一早比一世遥远'},
    {'name': '札幌 (Sapporo)', 'lat': 43.0618, 'lng': 141.3545, 'type': 'ns', 'freq': 3, 'lyric': '去札幌 看教堂'},
    {'name': '京都 (Kyoto)', 'lat': 35.0116, 'lng': 135.7681, 'type': 'ns', 'freq': 2, 'lyric': '任蜗居改变伴侣 逛京都却为谁'},
    {'name': '表参道 (Omotesando)', 'lat': 35.6653, 'lng': 139.7121, 'type': 'ns', 'freq': 2, 'lyric': '找不到归途 来到表参道'},
    {'name': '西武百货 (Seibu Hyakkaten)', 'lat': 35.6602, 'lng': 139.7003, 'type': 'ns', 'freq': 2, 'lyric': '商店 都关得太早 找挂念的西武'},
    {'name': '富士山 (Mt Fuji)', 'lat': 35.3606, 'lng': 138.7274, 'type': 'ns', 'freq': 1, 'lyric': '谁能凭爱意要富士山私有'},
    {'name': '小樽 (Otaru)', 'lat': 43.1902, 'lng': 140.9942, 'type': 'ns', 'freq': 1, 'lyric': '在小樽的臂弯抱紧'},
    {'name': '北海道 (Hokkaido)', 'lat': 43.4390591, 'lng': 142.5758521, 'type': 'ns', 'freq': 1, 'lyric': '你每次 面对北海道夜栏 可否错返我们时间'},
    {'name': '后乐园 (Korakuen)', 'lat': 34.6673, 'lng': 133.9362, 'type': 'ns', 'freq': 1, 'lyric': '大慨你都想 去后乐园'},
    {'name': '伊豆 (Izu)', 'lat': 34.9213362, 'lng': 138.9099469, 'type': 'ns', 'freq': 1, 'lyric': '别了伊豆后患无穷 没有胆一个到东京这么冻'},

    # --- 香港组 ---
    {'name': '湾仔 (Wan Chai)', 'lat': 22.2760, 'lng': 114.1751, 'type': 'nr', 'freq': 4, 'lyric': '回到现今 湾仔竟无法俯瞰'},
    {'name': '太平山 (Victoria Peak)', 'lat': 22.2759, 'lng': 114.1455, 'type': 'nr', 'freq': 3, 'lyric': '上太平山 不见不散'},
    {'name': '万年大厦 (Manning House)', 'lat': 22.2820206, 'lng': 114.1561509, 'type': 'nr', 'freq': 2, 'lyric': '以后在万年大厦门外 如果真可再碰到'},
    {'name': '狮子山 (Lion Rock)', 'lat': 22.3521000, 'lng': 114.1864444, 'type': 'nr', 'freq': 2, 'lyric': '想高攀狮子山 活路又路漫漫'},
    {'name': '糖街 (Sugar Street)', 'lat': 22.2798374, 'lng': 114.1865425, 'type': 'nr', 'freq': 1, 'lyric': '我的他 黄昏跟我闯荡糖街'},
    {'name': '钻石山 (Diamond Hill)', 'lat': 22.3499996, 'lng': 114.20, 'type': 'nr', 'freq': 1, 'lyric': '冲出胜利关革命湾钻石山'},
    {'name': '乐活道 (Broadwood Road)', 'lat': 22.2716259, 'lng': 114.1863429, 'type': 'nr', 'freq': 1, 'lyric': '在乐活道上那一对伴侣'},
    {'name': '兰桂坊 (Lan Kwai Fong)', 'lat': 22.2809846, 'lng': 114.1556541, 'type': 'nr', 'freq': 1, 'lyric': '没法推 痊愈了的美穗 跟她死党逼到兰桂坊一醉'},
    {'name': '白加道 (Barker Road)', 'lat': 22.2706545, 'lng': 114.1581584, 'type': 'nr', 'freq': 1, 'lyric': '横行直闯 车闪过白加道旁'},
    {'name': '星街 (Star Street)', 'lat': 22.2761315, 'lng': 114.1683060, 'type': 'nr', 'freq': 1, 'lyric': '人总要长大 消失的便当 难道会回到星街'}
]

def generate_color_coded_map():
    m = folium.Map(location=[28, 128], zoom_start=4, tiles='CartoDB positron')

    for loc in final_locations:
       
        if loc['type'] == 'ns': # 日本/远方
            icon_color = 'red'
            icon_name = 'plane' # 飞机图标
        else:                   # 香港/家
            icon_color = 'orange'
            icon_name = 'home'    # 房子图标

        popup_html = f"""
        <div style="font-family: Microsoft YaHei; width: 200px;">
            <h4 style="margin-bottom:5px; color: #333;">{loc['name']}</h4>

            <div style="background-color: #f0f0f0; padding: 5px; border-radius: 4px; margin-bottom: 8px;">
                <b>📍 出现频次:</b> <span style="color: red; font-weight: bold;">{loc['freq']} 次</span>
            </div>

            <i style="color: #555; border-left: 3px solid {icon_color}; padding-left: 8px; display: block;">
                "{loc['lyric']}"
            </i>
        </div>
        """

        # 添加标记
        folium.Marker(
            location=[loc['lat'], loc['lng']],
            # 使用 FontAwesome (fa) 图标库
            icon=folium.Icon(color=icon_color, icon=icon_name, prefix='fa'),
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"{loc['name']} ({loc['freq']}次)" # 鼠标悬停时也显示频次
        ).add_to(m)

    output_file = 'linxi_final_color_map.html'
    m.save(output_file)
    print(f"✅ 彩色分类地图已生成：{output_file}")

# 运行
generate_color_coded_map()
