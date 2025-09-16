import os
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.conf import settings

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

client = MongoClient(MONGO_URI)
db = client.youtubeDB  # database
collection = db.videos   # collection

@api_view(['GET'])
def get_videos(request):
    # Fetch video IDs from MongoDB
    video_ids = [doc['videoId'] for doc in collection.find()]
    ids_str = ",".join(video_ids)

    # Fetch metadata from YouTube API
    youtube_url = (
        f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={ids_str}&key={YOUTUBE_API_KEY}"
    )

    print("YouTube URL:", youtube_url)

    response = requests.get(youtube_url)
    data = response.json()

    # Extract necessary fields
    enriched_videos = []
    for item in data.get('items', []):
        enriched_videos.append({
            "videoId": item["id"],
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
            "duration": item["contentDetails"]["duration"]
        })

    return Response(enriched_videos)

def get_youtube_videos(request):
    # Access the collection
    collection = settings.mongo_db["videos"]
    
    # Fetch all documents
    videos = list(collection.find({}, {"_id": 0}))  # exclude _id

    return JsonResponse(videos, safe=False)
