# Geographical Preferences in Cantopo Lyricsof Albert Leung(林夕)

![Project Banner](https://img.shields.io/badge/Status-Completed-success) ![Python](https://img.shields.io/badge/Python-3.x-blue) ![License](https://img.shields.io/badge/License-MIT-green)

## 📖 Overview

**Albert Leung (林夕)** is arguably the most influential lyricist in the Chinese pop music, whose contemporary urban lyrics have shaped timeless classics for renowned artists. His unique talent for linking abstract emotions to tangible physical spaces led to our research. In past, some scholars have previously analysed the nature of words, emotional words, and time words in Albert Leung's lyrics, but there has been no analysis of the specific locations.

Thus this project applies Named Entity Recognition (NER) to analyse geographical imagination in over 1000 of Albert Leung’s Cantopop lyrics, investigating how he constructs distinct emotional spaces through geography—specifically the dichotomy between **Japan (The Distant/Travel)** and **Hong Kong (The Domestic/Home)**.

## ✨ Key Features

* **Robust Web Scraping**: A scraper designed to fetch lyrics from *Feitsui Lyrics*, featuring automatic retry logic and content cleaning (removing Pinyin/English).
* **Named Entity Recognition (NER)**: Utilization of BERT-based models to extract location entities from unstructured text.
* **Data Visualization**: 
    * **Statistical Analysis**: Bar charts illustrating the frequency of top locations.
    * **Word Clouds**: Visualizing the "geographic atmosphere" of the lyrics.
* **Interactive GIS Mapping**: 
    * Integration with **Google Earth (KML)** for precise manual geocoding.
    * Generation of an **Interactive Web Map** using `Folium`.
    * **Color-coded Clustering**: Red markers for Japan (Travel) vs. Orange markers for Hong Kong (Home), complete with lyric snippets in pop-ups.

## 🛠️ Tech Stack

* **Language**: Python 3.10+
* **Data Acquisition**: `requests`, `BeautifulSoup4`
* **Data Processing**: `pandas`, `re`, `xml`
* **NLP**: `transformers` (Hugging Face), `jieba` (optional)
* **Visualization**: `matplotlib`, `seaborn`, `wordcloud`, `folium`
