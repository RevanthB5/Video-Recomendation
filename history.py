import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the scopes required for accessing YouTube data
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

# Function to authenticate with YouTube Data API
def authenticate(client_id, client_secret):
    flow = InstalledAppFlow.from_client_config(
        {"installed": {"client_id": client_id, "client_secret": client_secret}},
        SCOPES
    )

    # Perform authorization flow to obtain initial credentials
    credentials = flow.run_local_server()

    # Build the YouTube service using the authenticated credentials
    youtube_service = build("youtube", "v3", credentials=credentials)
    return youtube_service

# Function to retrieve user's watch history
def get_watch_history(youtube_service):
    # Make API request to retrieve user's watch history
    history_response = youtube_service.activities().list(
        part="snippet",
        maxResults=50,  # Adjust maxResults as needed
        mine=True,
        fields="items/snippet(title, resourceId/videoId)",
        publishedAfter="1970-01-01T00:00:00Z"  # Adjust publishedAfter as needed
    ).execute()

    # Extract relevant information from the response
    watch_history = []
    for item in history_response["items"]:
        title = item["snippet"]["title"]
        video_id = item["snippet"]["resourceId"]["videoId"]
        watch_history.append({"title": title, "video_id": video_id})

    return watch_history

def main():
    # Manually enter client ID and client secret
    client_id = input("Enter your client ID: ")
    client_secret = input("Enter your client secret: ")

    # Authenticate with YouTube Data API
    youtube_service = authenticate(client_id, client_secret)

    # Retrieve user's watch history
    watch_history = get_watch_history(youtube_service)

    # Print the titles and video IDs of the watched videos
    for video in watch_history:
        print("Title:", video["title"])
        print("Video ID:", video["video_id"])
        print()

if __name__ == "__main__":
    main()
