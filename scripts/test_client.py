# scripts/test_client.py
import requests
import json

BASE_URL = "http://localhost:8000/api"  # Change this to your deployment URL

def list_clips():
    """List all available clips"""
    response = requests.get(f"{BASE_URL}/clips")
    if response.status_code == 200:
        clips = response.json()
        print("\n=== AVAILABLE CLIPS ===")
        for clip in clips:
            print(f"ID: {clip['id']}")
            print(f"Title: {clip['title']}")
            print(f"Genre: {clip['genre']}")
            print(f"Duration: {clip['duration']}s")
            print(f"Play Count: {clip['play_count']}")
            print("-" * 30)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def stream_clip(clip_id):
    """Stream a specific clip"""
    print(f"\n=== STREAMING CLIP {clip_id} ===")
    # In a real client, this would download and play the file
    response = requests.get(f"{BASE_URL}/clips/{clip_id}/stream", stream=True)
    if response.status_code == 200:
        # Save to a temporary file to demonstrate streaming
        filename = response.headers.get('Content-Disposition', '').split('filename=')[1].strip('"')
        with open(f"downloaded_{filename}", "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"Downloaded clip to downloaded_{filename}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def get_clip_stats(clip_id):
    """Get play statistics for a clip"""
    response = requests.get(f"{BASE_URL}/clips/{clip_id}/stats")
    if response.status_code == 200:
        stats = response.json()
        print(f"\n=== STATS FOR CLIP {clip_id} ===")
        print(f"Title: {stats['title']}")
        print(f"Play Count: {stats['play_count']}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def add_new_clip():
    """Add a new clip to the database"""
    new_clip = {
        "title": "Custom User Clip",
        "description": "A clip added by the test client",
        "genre": "Test",
        "duration": 25.0,
        "audio_url": "https://cdn.pixabay.com/download/audio/2021/08/08/audio_dc39bbc88c.mp3"
    }
    
    response = requests.post(f"{BASE_URL}/clips/", json=new_clip)
    if response.status_code == 201:
        clip = response.json()
        print("\n=== NEW CLIP ADDED ===")
        print(f"ID: {clip['id']}")
        print(f"Title: {clip['title']}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def main():
    print("Sound Clip API Client")
    print("1. List all clips")
    print("2. Stream a clip")
    print("3. Get clip statistics")
    print("4. Add a new clip")
    print("5. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == "1":
            list_clips()
        elif choice == "2":
            clip_id = input("Enter clip ID to stream: ")
            stream_clip(clip_id)
        elif choice == "3":
            clip_id = input("Enter clip ID to get stats: ")
            get_clip_stats(clip_id)
        elif choice == "4":
            add_new_clip()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()