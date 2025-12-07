# Geographical Preferences in Cantopo Lyrics of Albert Leung(林夕)

![Project Banner](https://img.shields.io/badge/Status-Completed-success) ![Python](https://img.shields.io/badge/Python-3.x-blue) ![License](https://img.shields.io/badge/License-MIT-green)

## 📖 Overview

**Albert Leung (林夕)** is arguably the most influential lyricist in the Chinese pop music, whose contemporary urban lyrics have shaped timeless classics for renowned artists. His unique talent for linking abstract emotions to tangible physical spaces led to our research. In past, some scholars have previously analysed the nature of words, emotional words, and time words in Albert Leung's lyrics, but there has been no analysis of the specific locations.

Thus this project applies Named Entity Recognition (NER) to analyse geographical imagination in over 1000 Cantopop lyricsof Albert Leung, investigating how he constructs distinct emotional spaces through geography—specifically the dichotomy between **Japan (The Distant/Travel)** and **Hong Kong (The Domestic/Home)**.

## 🛠️ Methodlogy

* **Prepare training data**: Create a training data comprising 40 representative songs that feature locations by other Hong Kong lyricists. This dataset was split, tagged and converted to BERT’s input format, using a Bert-base-Chinese model for fine-tuning.
* **Prepare predicting data**: Collect a testing data of over 1,000 Cantopo Lyrics of Albert Leung(林夕) via Python-based web scraping on Feitsui Lyric [https://www.feitsui.com] and then clean the data to remove irrelevant content, aiming to retain only the actual lyrics.
* **Fine-tuned NER model with training data**: Segment the testing data uses line-by-line processing.
* **Visualization**: Count the recognized entities and do visualisations basde on preliminary analysis, including a bar chart, a word cloud and a map.

## ✨ Key Features

* **Robust Web Scraping**: A scraper designed to fetch lyrics from *Feitsui Lyrics*, featuring automatic retry logic and content cleaning (removing Pinyin/English).
* **Named Entity Recognition (NER)**: Utilization of BERT-based models to extract location entities from unstructured text.
* **Data Visualization**: 
    * **Statistical Analysis**: Bar charts illustrating the frequency of top locations.
    * **Word Clouds**: Visualizing the "geographic atmosphere" of the lyrics.
* **Interactive GIS Mapping**: 
    * Integration with **Google Earth** for precise manual geocoding.
    * Generation of an **Interactive Web Map** using `Folium`.
    * **Color-coded Clustering**: Red markers for Japan (Travel) vs. Orange markers for Hong Kong (Home), complete with lyric snippets in pop-ups.

## ⚙ Tech Stack

* **Language**: Python 3.10+
* **Data Acquisition**: `requests`, `BeautifulSoup4`
* **Data Processing**: `pandas`, `re`, `xml`
* **NLP**: `transformers` (Hugging Face), `jieba` (optional)
* **Visualization**: `matplotlib`, `seaborn`, `wordcloud`, `folium`
