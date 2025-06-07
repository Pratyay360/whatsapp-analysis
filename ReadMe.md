<!-- filepath: /home/warlokk/Documents/machine-learning-project-whatsapp/ReadMe.md -->
# 💬 WhatsApp Chat Analyzer

[![Python Version](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-orange.svg)](https://streamlit.io)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](#contributing)

Dive deep into your WhatsApp conversations with this powerful and intuitive analyzer! Built with Streamlit, this application transforms your chat exports into insightful visualizations and comprehensive analytics, helping you understand communication patterns, user engagement, and much more.

## ✨ Key Features
- 📊 **Comprehensive Statistics**: Get a bird's-eye view with counts for messages, words, media shared, and links.
- 📈 **Dynamic Timeline Analysis**: Explore activity trends with monthly and daily message breakdowns.
- 🗓️ **Activity Heatmaps**: Visualize weekly and monthly engagement patterns at a glance.
- 👥 **In-depth User Analytics**: Identify the most active users and their contribution percentages.
- ☁️ **Interactive Word Clouds**: Discover the most frequently used words in your chats.
- 📝 **Advanced Text Analysis**: Uncover common words with intelligent stop-word filtering.
- 😊 **Emoji Insights**: See which emojis dominate your conversations.
- 💭 **Sentiment Analysis**: Gauge the emotional tone of messages using TextBlob & VADER.
- 📏 **Message Pattern Insights**: Analyze message length distributions and response times.
- 🚀 **Conversation Dynamics**: Find out who initiates conversations most often.
- 🔗 **URL Tracking**: Analyze shared domains and link statistics.
- 📄 **Exportable PDF Reports**: Download comprehensive analysis summaries as PDF files.
- 🗂️ **Multi-file ZIP Support**: If you upload a ZIP with multiple .txt files, you can select which chat to analyze.

## 📸 Screenshots
*(Placeholder: Add a few screenshots of the application in action here to showcase its features and UI.)*
*E.g., Dashboard overview, timeline analysis, word cloud, sentiment analysis chart.*

## 🚀 Getting Started

Follow these steps to get the WhatsApp Chat Analyzer up and running on your local machine.

### Prerequisites
- Python 3.8 or higher (Python 3.12+ recommended)
- `pip` (Python package installer)
- `git` (for cloning the repository)

### Installation
1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url> # Replace <your-repo-url> with the actual URL
    cd machine-learning-project-whatsapp
    ```

2.  **Create and activate a virtual environment** (recommended):
    ```bash
    # For Linux/macOS
    python3 -m venv env
    source env/bin/activate

    # For Windows
    python -m venv env
    .\env\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 🏃‍♀️ Running the Application

You can run the application locally using Docker (recommended for easiest setup), or directly with Python.

### 🚀 Run Locally with Docker

Run these commands to run the application locally:

```bash
docker pull ghcr.io/pratyay360/whatsapp-analysis:latest

docker run --rm -it -p 8501:8501 ghcr.io/pratyay360/whatsapp-analysis

```
or 
```bash
docker pull docker.io/pratyay360/whatsapp-analyzer:latest

docker run --rm -it -p 8501:8501 docker.io/pratyay360/whatsapp-analyzer:latest

```


Then open your browser and go to [http://localhost:8501](http://localhost:8501).

### 🐍 Run with Python (Alternative)

1.  **Launch the Streamlit app:**
    ```bash
    streamlit run app.py
    ```

2.  **Access in your browser:**
    - The application should automatically open in your default web browser.
    - If not, navigate to `http://localhost:8501`.

## 🔧 How to Use

### 1. Export Your WhatsApp Chat
- Open WhatsApp on your mobile device.
- Navigate to the specific chat (individual or group) you wish to analyze.
- Tap the three-dot menu (⋮) in the top-right corner.
- Select **More** → **Export chat**.
- Crucially, choose **"Without Media"**. This ensures faster processing and a smaller file size.
- Save or send the exported `.txt` file or `.zip` (if your device exports as ZIP) to your computer.

### 2. Analyze Your Chat
- Once the Streamlit application is running, use the sidebar to upload your exported `.txt` or `.zip` file.
- If you upload a ZIP with multiple .txt files, you will be prompted to select which chat to analyze.
- After a successful upload, you can select a specific user for focused analysis or choose "Overall" to analyze the entire group's activity.
- Click the "Show Detailed Analysis" button to generate and display the insights.
- Use the **Download PDF Report** button to save your analysis as a PDF file.

## 📊 In-Depth Analysis Capabilities

The analyzer provides a rich set of tools to dissect your chat data:

### 📈 Timeline & Activity
-   **Monthly & Daily Timelines**: Track message volume over different periods.
-   **Activity Heatmap**: Visualize hourly activity across the days of the week.

### 👥 User-Specific Insights
-   **Most Active Users**: Identify key contributors.
-   **Participation Percentages**: Understand each user's share of messages.
-   **Response Time Analysis**: (Overall view) Analyze how quickly messages are typically responded to.

### 📝 Textual & Content Analysis
-   **Word Clouds & Common Words**: Visualize and list frequently used vocabulary.
-   **Message Length Distribution**: See the typical length of messages.
-   **Emoji Usage**: Discover the most popular emojis and their frequencies.

### 💭 Advanced Analytics
-   **Sentiment Analysis**: Classify messages as positive, negative, or neutral.
-   **Conversation Starters**: Identify who typically initiates discussions.
-   **URL Analysis**: Track shared domains and website links.
-   **Media Sharing Statistics**: Count of images, videos, and documents shared.

## 🛠️ Technologies Used

This project leverages a suite of powerful Python libraries:

-   **Core Framework**: `streamlit` for the interactive web application.
-   **Data Handling**: `pandas` for efficient data manipulation and analysis.
-   **Visualizations**:
    -   `plotly` for interactive charts and graphs.
    -   `matplotlib` & `seaborn` for static plots.
    -   `wordcloud` for generating word cloud images.
-   **Text & Sentiment Analysis**:
    -   `textblob` & `vaderSentiment` for sentiment scoring.
    -   `emoji` for processing and analyzing emoji usage.
-   **Date/Time Utilities**: `python-dateutil`.

### Project Structure
```
.
├── app.py                 # Main Streamlit application script
├── helper.py              # Contains core analysis functions
├── preprocessor.py        # Handles chat data preprocessing and cleaning
├── bengali_stop_words.txt # Optional: Stop words for Bengali text
├── 01_whatsapp.ipynb      # Jupyter Notebook for development & exploration
├── requirements.txt       # Lists all Python dependencies
├── Dockerfile             # For containerizing the application
└── ReadMe.md              # This file: project documentation
```

### Data Processing Highlights
-   Robust parsing of various WhatsApp export formats.
-   Intelligent extraction and classification of user messages.
-   Filtering of group notifications and system messages.
-   Detection and counting of media messages.
-   Comprehensive error handling for malformed data.

## 📓 Jupyter Notebook Companion
A detailed Jupyter Notebook (`01_whatsapp.ipynb`) is included. This notebook offers:
-   Step-by-step walkthrough of data preprocessing.
-   Exploratory Data Analysis (EDA) examples.
-   Development and testing environment for new features.
-   Experiments with different visualization techniques.

## 🤝 Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📄 License
Distributed under the MIT License. See `LICENSE` file for more information (if a `LICENSE` file is present in the repository, otherwise, state that it's MIT Licensed).

This project is open source and available under the MIT License.

## 🆘 Troubleshooting

### Common Issues
1.  **"No valid chat data found" / File Processing Errors:**
    *   Ensure you exported the chat **"Without Media"** from WhatsApp.
    *   Verify the uploaded file is a `.txt` file.
    *   Check if the file contains actual message data and is not corrupted.
    *   The app expects UTF-8 encoding. If you suspect an encoding issue, try re-saving the file with UTF-8 encoding.

2.  **"Error reading stop words file" (if applicable):**
    *   Ensure `bengali_stop_words.txt` (or other custom stop word files) is present in the project's root directory if you're using features that rely on it.
    *   Check the file's encoding (should be UTF-8).

3.  **Visualization or Analysis Errors:**
    *   Confirm all libraries listed in `requirements.txt` are correctly installed in your active Python environment.
    *   Ensure your chat data has sufficient content for the selected analysis (e.g., enough messages for timeline analysis, enough text for word clouds).

### Getting Help
If you encounter persistent issues:
1.  Carefully read the error message displayed in the Streamlit interface or console.
2.  Double-check your WhatsApp export format and the uploaded file.
3.  Ensure your environment is set up correctly with all dependencies.
4.  If the problem persists, consider opening an issue on the project's GitHub repository, providing:
    *   A clear description of the issue.
    *   Steps to reproduce the error.
    *   The error message(s) you received.
    *   Information about your operating system and Python version.

---
