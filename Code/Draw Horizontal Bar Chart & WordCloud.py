!apt-get update
!apt-get install -y fonts-wqy-zenhei
!fc-cache -fv


import matplotlib.font_manager as fm
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud


# Find the path of the newly installed font
font_path = None
for font in fm.findSystemFonts(fontpaths=None, fontext='ttf'):
    if 'wqy-zenhei' in font.lower():
        font_path = font
        break

if font_path:
    print(f"Found wqy-zenhei font at: {font_path}")

    # Add the font to Matplotlib's font manager
    fm.fontManager.addfont(font_path)

    # Get the actual font name that Matplotlib registers for it
    prop = fm.FontProperties(fname=font_path)
    font_name = prop.get_name()
    print(f"Matplotlib registered font name: {font_name}")

    # Set the font globally for Matplotlib
    plt.rcParams['font.sans-serif'] = [font_name, 'DejaVu Sans', 'Arial']
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['axes.unicode_minus'] = False

else:
    print("wqy-zenhei font not found, please check installation.")
    # Fallback or error handling if font not found

try:
    # Changed filename to match the output from the previous cell
    df = pd.read_csv('location_frequencies.csv', encoding='gbk')
except UnicodeDecodeError:
    df = pd.read_csv('location_frequencies.csv', encoding='utf-8-sig')

df = df.sort_values(by='frequency', ascending=False)

# Filter for the top 10 locations
df_top10 = df.head(10)

plt.figure(figsize=(12, 8))
sns.barplot(x='frequency', y='location', hue='type', data=df_top10,
            palette={'ns': '#FF6B6B', 'nr': '#FFE66D'}, dodge=False) # 'dodge=False' prevents bars from dodging when 'hue' is used
plt.title('林夕歌词中的地名频次Top10', fontsize=16)
plt.ylabel('(红色=日本, 黄色=香港)')
plt.xlabel(' ')
plt.tight_layout()
plt.savefig('location_bar_chart.png')


freq_dict = dict(zip(df['location'], df['frequency']))
wc = WordCloud(
    font_path=font_path,
    width=800, height=400,
    background_color='white',
    colormap='plasma'
)
wc.generate_from_frequencies(freq_dict)

plt.figure(figsize=(10, 5))
plt.imshow(wc)
plt.axis('off')
plt.savefig('location_wordcloud.png')
