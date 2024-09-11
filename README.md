# YouTube Comments Scraper

This script allows you to retrieve comments from YouTube videos using the YouTube Data API v3. You can input a single video link or provide a text file containing multiple video links. The script will fetch the specified number of comments for each video and save them to CSV files.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [1. Install Python](#1-install-python)
  - [2. Get a YouTube Data API Key](#2-get-a-youtube-data-api-key)
  - [3. Download the Script](#3-download-the-script)
  - [4. Install Required Python Packages](#4-install-required-python-packages)
- [Usage](#usage)
  - [Option 1: Single YouTube Video Link](#option-1-single-youtube-video-link)
  - [Option 2: Multiple YouTube Video Links from a File](#option-2-multiple-youtube-video-links-from-a-file)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Features

- Retrieve comments from YouTube videos.
- Support for single or multiple video links.
- Save comments to CSV files with video metadata (title, author, and link).
- Specify the number of comments to retrieve for each video.

## Prerequisites

- A computer with an internet connection.
- **Python 3.6 or higher** installed on your system.
- A **YouTube Data API v3 key** from Google Cloud Console.

## Installation

### 1. Install Python

If you don't have Python installed on your computer, follow these steps:

#### For Windows:

1. Go to the [Python Downloads](https://www.python.org/downloads/windows/) page.
2. Download the latest version of Python for Windows.
3. Run the installer. During installation, make sure to check the box "Add Python to PATH".
4. Follow the prompts to complete the installation.

#### For macOS:

1. Go to the [Python Downloads](https://www.python.org/downloads/mac-osx/) page.
2. Download the latest version of Python for macOS.
3. Run the installer and follow the prompts.

#### For Linux:

Python is usually pre-installed on most Linux distributions. If not, you can install it via your terminal:

```bash
sudo apt update
sudo apt install python3
```
 ### 2. Get a YouTube Data API Key

1. Visit the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Go to the **API & Services Dashboard** and enable the **YouTube Data API v3**.
4. Navigate to **Credentials** and click **Create Credentials** -> **API Key**.
5. Copy the API key and keep it handy. You will use it in the script.

### 3. Download the Script

1. Download the `youtubecomments.py` script from the repository or wherever it's hosted.
2. Place it in a folder on your computer where you want to run the script.

### 4. Install Required Python Packages

Once Python is installed, you need to install the required packages for the script:

1. Open a terminal or command prompt.
2. Navigate to the folder where the `youtubecomments.py` script is located.
3. Run the following command to install the required packages:

```bash
pip install google-api-python-client
```
This will install the necessary libraries to interact with the YouTube API.

## Usage

After setting up Python and the necessary libraries, you can now run the script.

### Option 1: Single YouTube Video Link

1. Open a terminal or command prompt.
2. Navigate to the directory where the script is located.
3. Run the script with:

    ```bash
    python youtubecomments.py
    ```

4. Select **Option 1** to enter a single YouTube link.
5. Provide the YouTube video link when prompted.
6. Specify how many comments you want to retrieve, or leave blank to retrieve all comments.
7. The comments will be saved in a CSV file in the same directory, with the video title and metadata included.

### Option 2: Multiple YouTube Video Links from a File

1. Prepare a text file (`.txt`) containing one YouTube video link per line.
2. Open a terminal or command prompt.
3. Run the script with:

    ```bash
    python youtubecomments.py
    

4. Select **Option 2** to load a text file with multiple video links.
5. Enter the path to the text file.
6. Specify how many comments to retrieve for each video.
7. The script will process each video and save the comments in separate CSV files.
