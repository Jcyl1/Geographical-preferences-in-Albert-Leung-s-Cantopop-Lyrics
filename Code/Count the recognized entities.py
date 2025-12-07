from collections import Counter
import csv

def extract_entities(lines):
    ns, nr = [], []
    entity, etype = [], None

    for line in lines + ['']:
        line = line.strip()
        if not line:
            if entity and etype:
                (ns if etype == 'ns' else nr).append(''.join(entity))
            entity, etype = [], None
            continue

        if '\t' not in line:
            continue
        token, tag = line.split('\t')

        if '-' in tag:
            prefix, t = tag.split('-')
        else:
            prefix, t = 'O', None

        if prefix == 'B':
            if entity and etype:
                (ns if etype == 'ns' else nr).append(''.join(entity))
            entity, etype = [token], t
        elif prefix == 'I' and t == etype:
            entity.append(token)
        elif prefix == 'E' and t == etype:
            entity.append(token)
            (ns if etype == 'ns' else nr).append(''.join(entity))
            entity, etype = [], None
        elif prefix == 'S':
            (ns if t == 'ns' else nr).append(token)
            entity, etype = [], None
        else:
            if entity and etype:
                (ns if etype == 'ns' else nr).append(''.join(entity))
            entity, etype = [], None

    return ns, nr

def show_top10(ns, nr):
    print("Top 10 ns (Japan):")
    for w, c in Counter(ns).most_common(10):
        print(f"{w}: {c}")
    print("\nTop 10 nr (Hong Kong):")
    for w, c in Counter(nr).most_common(10):
        print(f"{w}: {c}")

def show_all_counts(ns, nr):
    """
    统计并显示所有 ns (地名) 和 nr (地名) 的出现频次。
    """
    print("\n--- 所有 ns (地名) 出现频次统计 ---")
    ns_counts = Counter(ns)
    if not ns_counts:
        print("未提取到任何 ns (地名)。")
    else:
        for w, c in ns_counts.most_common():
            print(f"{w}: {c}")

    print("\n--- 所有 nr (地名) 出现频次统计 ---")
    nr_counts = Counter(nr)
    if not nr_counts:
        print("未提取到任何 nr (地名)。")
    else:
        for w, c in nr_counts.most_common():
            print(f"{w}: {c}")

def write_counts_to_csv(ns_words, nr_words):
    """
    将 ns 和 nr (地名) 的频次统计输出为 CSV 文件。
    """
    print("\n--- 正在将所有地名频次写入 'location_frequencies.csv' ---")
    ns_counts = Counter(ns_words)
    nr_counts = Counter(nr_words)

    with open("location_frequencies.csv", "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)

        # 写入表头
        writer.writerow(["type", "location", "frequency"])

        # 写入 ns (地名) 数据
        for w, c in ns_counts.most_common():
            writer.writerow(["ns", w, c])

        # 写入 nr (地名) 数据
        for w, c in nr_counts.most_common():
            writer.writerow(["nr", w, c])

    print("文件 'location_frequencies.csv' 写入成功。")


if __name__ == "__main__":
    with open("result.txt", encoding="utf-8") as f:
        lines = f.readlines()
    ns_words, nr_words = extract_entities(lines)

    # 1. 调用 Top 10 函数
    show_top10(ns_words, nr_words)

    # 2. 调用显示所有频次的函数
    show_all_counts(ns_words, nr_words)

    # 3. 调用新增的函数来输出 CSV 文件
    write_counts_to_csv(ns_words, nr_words)
