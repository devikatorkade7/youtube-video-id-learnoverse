from pymongo import MongoClient
from django.http import JsonResponse

# Connect to MongoDB
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["youtube_db"]   # database name
collection = db["videos"]   # collection name

def get_videos(request):
    videos = list(collection.find({}, {"_id": 0, "title": 1, "youtube_id": 1}))
    return JsonResponse(videos, safe=False)
