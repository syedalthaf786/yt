from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import yt_dlp as youtube_dl
import os

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with the specific origins you want to allow
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the homepage (index.html)
@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        with open("templates/index.html") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Homepage not found")

# Serve the Privacy Policy page
@app.get("/privacy-policy.html", response_class=HTMLResponse)
async def privacy_policy():
    try:
        with open("static/privacy-policy.html") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Privacy Policy page not found")

class VideoURL(BaseModel):
    url: str

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import yt_dlp as youtube_dl
import os
import uuid 
import subprocess  # For generating unique file names

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with the specific origins you want to allow
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the homepage (index.html)
@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        with open("templates/index.html") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Homepage not found")

class VideoURL(BaseModel):
    url: str

@app.post("/download")
async def download_video(video_url: VideoURL):
    try:
        # Generate a unique filename using uuid
        unique_filename = str(uuid.uuid4())  # Generate a unique UUID

        ydl_opts = {
            'outtmpl': f'static/downloads/{unique_filename}.%(ext)s',  # Use the unique filename
            'format': 'mp4',
        }
        
        # Ensure the downloads directory exists
        download_dir = "static/downloads"
        os.makedirs(download_dir, exist_ok=True)

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url.url, download=True)
            filename = ydl.prepare_filename(info_dict)
            download_link = f"/static/downloads/{os.path.basename(filename)}"
        
        return {"success": True, "download_link": download_link}
    except Exception as e:
        print(f"Error: {str(e)}")  # Print error details for debugging
        return {"success": False, "message": str(e)}
