import os
import googleapiclient.discovery
import csv
import re
from datetime import datetime
import re


API_FILE = "api.txt"


# Function to load or prompt for the API key
def get_api_key():
    if os.path.exists(API_FILE):
        with open(API_FILE, 'r') as f:
            api_key = f.read().strip()
            if validate_api_key(api_key):
                return api_key
            else:
                print("Invalid API key found in api.txt.")
    return prompt_for_api_key()


# Function to prompt the user for their API key and save it to a file
def prompt_for_api_key():
    api_key = input("Please enter your YouTube API key: ").strip()
    with open(API_FILE, 'w') as f:
        f.write(api_key)
    return api_key


# Function to validate the API key
def validate_api_key(api_key):
    try:
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
        youtube.videos().list(part="snippet", id="Ks-_Mh1QhMc").execute()  # Test with a valid video ID
        return True
    except Exception as e:
        return False


# Function to extract video ID from a YouTube URL
def get_video_id_from_url(url):
    video_id = None
    match = re.match(r'.*v=([a-zA-Z0-9_-]+)', url)
    if match:
        video_id = match.group(1)
    return video_id


# Function to retrieve video details (title, author)
def get_video_details(video_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

    response = youtube.videos().list(
        part="snippet",
        id=video_id
    ).execute()

    if response['items']:
        video_title = response['items'][0]['snippet']['title']
        video_author = response['items'][0]['snippet']['channelTitle']
        return video_title, video_author
    else:
        return None, None


# Function to retrieve comments from a YouTube video
def get_video_comments(video_id, max_comments=None):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)
    all_comments = []

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        textFormat="plainText"
    )

    response = request.execute()

    while response:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            author = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            published_at = item['snippet']['topLevelComment']['snippet']['publishedAt']

            all_comments.append({
                'comment_author': author,
                'comment_text': comment,
                'comment_published_at': published_at
            })

            # Stop if we have retrieved the requested number of comments
            if max_comments and len(all_comments) >= max_comments:
                return all_comments

        if 'nextPageToken' in response:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                pageToken=response['nextPageToken'],
                maxResults=100,
                textFormat="plainText"
            )
            response = request.execute()
        else:
            break

    return all_comments


# Function to sanitize the filename
def sanitize_filename(filename):
    # Replace invalid characters with an underscore or remove them
    return re.sub(r'[\/:*?"<>|]', '_', filename)


# Function to save comments to a CSV file, including video details
def save_comments_to_csv(video_title, video_author, video_url, comments):
    # Get current timestamp to append to the filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Sanitize the video title to create a valid filename
    sanitized_title = sanitize_filename(video_title.replace(' ', '_'))

    filename = f"comments_{sanitized_title}_{timestamp}.csv"

    # Add video metadata to each comment entry
    for comment in comments:
        comment['video_title'] = video_title
        comment['video_author'] = video_author
        comment['video_url'] = video_url

    # Save to CSV
    keys = comments[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(comments)

    print(f"Comments saved to {filename}")


# Function to process multiple video links from a file
def process_video_links_from_file(filepath, max_comments):
    if not os.path.exists(filepath):
        print(f"File '{filepath}' not found.")
        return

    with open(filepath, 'r') as file:
        video_links = [line.strip() for line in file.readlines() if line.strip()]

    for video_url in video_links:
        process_single_video(video_url, max_comments)


# Function to process a single video link
def process_single_video(video_url, max_comments):
    video_id = get_video_id_from_url(video_url)

    if not video_id:
        print(f"Invalid YouTube link: {video_url}")
        return

    # Fetch video details (title and author)
    video_title, video_author = get_video_details(video_id)

    if not video_title or not video_author:
        print("Could not retrieve video details. Please check the video URL.")
        return

    print(f"Video Title: {video_title}")
    print(f"Video Author: {video_author}")

    # Fetch the comments
    comments = get_video_comments(video_id, max_comments)

    # Display and save the comments
    if comments:
        save_comments_to_csv(video_title, video_author, video_url, comments)
        print(f"Successfully retrieved {len(comments)} comments.")
    else:
        print("No comments found or an error occurred.")


# Main execution flow
if __name__ == "__main__":
    API_KEY = get_api_key()

    # Ask the user whether they want to enter a single video or a file with multiple links
    choice = input("Enter '1' to input a single YouTube link or '2' to load a text file with multiple video links: ").strip()

    # Ask how many comments to retrieve for all videos
    max_comments_input = input("How many comments would you like to retrieve for each video? (Leave blank for all): ").strip()
    max_comments = int(max_comments_input) if max_comments_input else None

    if choice == '1':
        # Prompt the user for a single YouTube video link
        video_url = input("Please enter the YouTube video link: ").strip()
        process_single_video(video_url, max_comments)
    elif choice == '2':
        # Prompt the user for the file path
        file_path = input("Please enter the file path for the .txt file with YouTube video links: ").strip()
        process_video_links_from_file(file_path, max_comments)
    else:
        print("Invalid choice. Please enter '1' or '2'.")
