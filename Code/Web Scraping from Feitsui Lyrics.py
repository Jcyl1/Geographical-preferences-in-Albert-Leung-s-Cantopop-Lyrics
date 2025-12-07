!pip install requests bs4

import requests
from bs4 import BeautifulSoup
import time
import re
import os

class LyricScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        })
        self.base_url = 'https://www.feitsui.com'

    def get_lyric_links(self, url):
        
        try:
            print(f"正在请求搜索结果页: {url}")
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'

            if response.status_code != 200:
                print(f"请求失败，状态码: {response.status_code}")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')

            # 查找所有包含歌词链接的元素
            lyric_links = []

            # 查找所有链接
            all_links = soup.find_all('a', href=True)
            for link in all_links:
                href = link.get('href', '')
                if '/zh-hans/lyrics/' in href:
                    full_url = self.base_url + href if href.startswith('/') else href
                    if full_url not in lyric_links:
                        lyric_links.append(full_url)

            print(f"共找到 {len(lyric_links)} 个歌词页面链接")
            return lyric_links

        except Exception as e:
            print(f"获取歌词链接时出错: {e}")
            return []

    def extract_lyrics_text(self, lyric_url):
        
        try:
            print(f"正在访问歌词页面: {lyric_url}")
            response = self.session.get(lyric_url, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')

            # 精确提取歌词 - 直接分析HTML结构
            return self.extract_lyrics_direct(soup)

        except Exception as e:
            print(f"提取歌词时出错 ({lyric_url}): {e}")
            return None

    def extract_lyrics_direct(self, soup):
        
        try:
            # 找到歌词区域
            article = soup.find('article', class_='romanization')
            if not article:
                print("未找到歌词区域")
                return None

            # 获取所有段落
            paragraphs = article.find_all('p')
            all_lyric_lines = []

            for p in paragraphs:
                # 获取段落中的所有文本节点
                text_nodes = p.find_all(text=True, recursive=True)

                for text_node in text_nodes:
                    text = text_node.strip()
                    if not text:
                        continue

                    # 跳过明显的非歌词内容
                    if any(keyword in text for keyword in
                          ['翡翠粤语歌词', 'https://www.feitsui.com', '微信搜索', '二维码', '关注公众号']):
                        continue

                    # 检查是否是拼音行
                    if self.is_pinyin_line(text):
                        continue

                    # 提取纯中文歌词
                    chinese_text = self.extract_chinese_only(text)
                    if chinese_text and len(chinese_text) >= 2:
                        all_lyric_lines.append(chinese_text)

            # 如果上面的方法没找到足够歌词，尝试备用方法
            if len(all_lyric_lines) < 10:
                all_lyric_lines = self.extract_lyrics_alternative(article)

            # 清理和组织歌词
            if all_lyric_lines:
                # 移除重复但保留顺序
                unique_lyrics = []
                for line in all_lyric_lines:
                    if line not in unique_lyrics:
                        unique_lyrics.append(line)

                # 格式化为易读的歌词
                formatted_lyrics = self.format_lyrics_readable(unique_lyrics)
                print(f"成功提取 {len(formatted_lyrics.splitlines())} 行歌词")
                return formatted_lyrics

            return None

        except Exception as e:
            print(f"直接提取歌词时出错: {e}")
            return None

    def extract_lyrics_alternative(self, article):
        """备用方法：逐行分析提取歌词"""
        try:
            # 获取article的完整文本
            full_text = article.get_text()
            lines = full_text.split('\n')

            lyric_lines = []
            in_lyrics = False

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # 检测歌词开始
                if not in_lyrics and any(marker in line for marker in ['粤拼 Lyrics', '微信搜索']):
                    in_lyrics = True
                    continue

                # 检测歌词结束
                if in_lyrics and any(marker in line for marker in ['标签 Tags', '您可能也喜欢']):
                    break

                # 如果在歌词区域
                if in_lyrics:
                    # 跳过明显的非歌词行
                    if any(keyword in line for keyword in
                          ['翡翠粤语歌词', 'https://www.feitsui.com', '微信搜索', '二维码', '关注公众号']):
                        continue

                    # 跳过拼音行
                    if self.is_pinyin_line(line):
                        continue

                    # 提取中文歌词
                    chinese_line = self.extract_chinese_only(line)
                    if chinese_line and len(chinese_line) >= 2:
                        lyric_lines.append(chinese_line)

            return lyric_lines

        except Exception as e:
            print(f"备用方法提取歌词时出错: {e}")
            return []

    def is_pinyin_line(self, text):
        
        # 拼音行通常包含大量小写字母和数字
        pinyin_pattern = r'[a-z]+\d+'
        matches = re.findall(pinyin_pattern, text)

        # 如果拼音部分超过行长度的一半，认为是拼音行
        pinyin_length = sum(len(match) for match in matches)
        return pinyin_length > len(text) * 0.3

    def extract_chinese_only(self, text):
        """只提取中文字符和中文标点"""
        # 移除所有非中文字符和非中文标点
        chinese_only = re.sub(r'[^\u4e00-\u9fff，。！？、\s]', '', text)
        # 合并多余空格
        chinese_only = re.sub(r'\s+', ' ', chinese_only).strip()
        return chinese_only

    def format_lyrics_readable(self, lyric_lines):
       
        if not lyric_lines:
            return ""

        # 组织歌词结构
        formatted = []

        # 按行长度分组处理
        for line in lyric_lines:
            # 如果行很短，可能是标题或重复的副歌
            if len(line) <= 8:
                formatted.append(line)
            else:
                # 对于长行，保持原样
                formatted.append(line)

        return '\n'.join(formatted)

    def extract_song_info(self, url):
        
        try:
            response = self.session.get(url, timeout=5)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')

            # 从页面标题提取信息
            title = soup.title.text if soup.title else ""

            # 尝试从标题中提取歌手和歌名
            if ' - ' in title:
                parts = title.split(' - ')
                if len(parts) >= 2:
                    return parts[0].strip()

            return title.split(' - ')[0] if ' - ' in title else title

        except:
            return "未知歌曲"

    def scrape_all_lyrics(self, start_url, output_file='linxi_lyrics_complete.txt', max_pages=10):
        
        print("开始获取歌词页面链接...")
        lyric_links = self.get_lyric_links(start_url)

        if not lyric_links:
            print("未找到歌词页面链接，尝试直接生成链接...")
            lyric_links = [f"{self.base_url}/zh-hans/lyrics/{i}" for i in range(1, max_pages+1)]
            print(f"生成了 {len(lyric_links)} 个歌词页面链接")

        all_lyrics = []
        successful_count = 0

        print(f"\n开始提取 {len(lyric_links)} 个页面的歌词...")
        for i, lyric_url in enumerate(lyric_links, 1):
            print(f"\n[{i}/{len(lyric_links)}] 处理: {lyric_url}")

            lyrics = self.extract_lyrics_text(lyric_url)
            if lyrics:
                song_info = self.extract_song_info(lyric_url)

                all_lyrics.append({
                    'url': lyric_url,
                    'info': song_info,
                    'text': lyrics
                })
                successful_count += 1
                print(f"✓ 成功提取第 {successful_count} 首歌词: {song_info}")

                # 实时保存进度
                self.save_progress(all_lyrics, f"progress_{output_file}")
            else:
                print(f"✗ 无法提取歌词")

            time.sleep(1)

        # 最终保存
        if all_lyrics:
            self.save_final_result(all_lyrics, output_file)
            print(f"\n完成！成功提取 {successful_count} 首歌词")
            print(f"歌词已保存到: {output_file}")
        else:
            print("未能提取到任何歌词")

    def save_progress(self, lyrics_data, filename):
        """保存进度"""
        with open(filename, 'w', encoding='utf-8') as f:
            for i, item in enumerate(lyrics_data, 1):
                f.write(f"=== 歌词 {i} ===\n")
                f.write(f"来源: {item['url']}\n")
                f.write(f"歌曲: {item['info']}\n")
                f.write(item['text'] + '\n')
                f.write('\n' + '='*50 + '\n\n')

    def save_final_result(self, lyrics_data, filename):
        """保存最终结果"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"=== 林夕歌词合集 (共{len(lyrics_data)}首) ===\n\n")
            for i, item in enumerate(lyrics_data, 1):
                f.write(f"【歌词 {i}】{item['info']}\n")
                f.write(f"来源: {item['url']}\n")
                f.write(item['text'] + '\n')
                f.write('\n' + '-'*50 + '\n\n')

# 精确测试函数 - 直接分析HTML结构
def precise_test():
    """精确测试 - 直接分析HTML结构提取完整歌词"""
    scraper = LyricScraper()
    test_url = "https://www.feitsui.com/zh-hans/lyrics/63"

    print(f"精确测试页面: {test_url}")
    response = scraper.session.get(test_url, timeout=10)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到歌词区域
    article = soup.find('article', class_='romanization')
    if not article:
        print("未找到歌词区域")
        return False

    print("找到歌词article区域")

    # 方法1: 精确分析每个段落
    paragraphs = article.find_all('p')
    print(f"找到 {len(paragraphs)} 个段落")

    all_lyrics = []

    for i, p in enumerate(paragraphs):
        print(f"\n分析段落 {i+1}:")

        # 获取段落中的所有直接文本子节点
        text_nodes = p.find_all(text=True, recursive=False)
        for text_node in text_nodes:
            text = text_node.strip()
            if text and not any(keyword in text for keyword in ['翡翠粤语歌词', 'https://']):
                chinese_text = scraper.extract_chinese_only(text)
                if chinese_text and len(chinese_text) >= 2:
                    print(f"  找到歌词: {chinese_text}")
                    all_lyrics.append(chinese_text)

    # 方法2: 如果方法1没找到足够歌词，尝试其他方法
    if len(all_lyrics) < 10:
        print("\n方法1提取不完整，尝试方法2...")
        # 获取article的完整文本并手动分离
        full_text = article.get_text()
        lines = full_text.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 跳过明显的非歌词行
            if any(keyword in line for keyword in
                  ['翡翠粤语歌词', 'https://www.feitsui.com', '微信搜索', '二维码', '关注公众号']):
                continue

            # 跳过拼音行
            if scraper.is_pinyin_line(line):
                continue

            # 提取中文歌词
            chinese_line = scraper.extract_chinese_only(line)
            if chinese_line and len(chinese_line) >= 2 and chinese_line not in all_lyrics:
                print(f"  方法2找到歌词: {chinese_line}")
                all_lyrics.append(chinese_line)

    # 整理最终歌词
    if all_lyrics:
        final_lyrics = '\n'.join(all_lyrics)
        print(f"\n完整提取的歌词 ({len(all_lyrics)} 行):")
        print("="*80)
        print(final_lyrics)
        print("="*80)

        # 保存结果
        with open('test_result_precise.txt', 'w', encoding='utf-8') as f:
            f.write(f"测试页面: {test_url}\n")
            f.write("完整提取的歌词:\n")
            f.write("="*80 + "\n")
            f.write(final_lyrics + "\n")
            f.write("="*80 + "\n")

        print("精确测试结果已保存到 test_result_precise.txt")
        return True
    else:
        print("未能提取完整歌词")
        return False

def main():
    # 先运行精确测试
    if precise_test():
        # 如果测试成功，询问是否继续爬取所有歌词
        if input("\n精确测试成功！是否继续爬取所有歌词? (y/n): ").lower() == 'y':
            # 初始化爬虫
            scraper = LyricScraper()

            # 林夕歌词搜索结果页
            start_url = 'https://www.feitsui.com/tag_s/1.html'

            # 输出文件名
            output_file = '林夕歌词合集_精确版.txt'

            # 开始爬取
            scraper.scrape_all_lyrics(start_url, output_file, max_pages=50)
    else:
        print("精确测试失败")

if __name__ == '__main__':
    main()
