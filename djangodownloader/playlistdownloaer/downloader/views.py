from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
import yt_dlp as youtube_dl
import time
from .forms import InputForm
# Create your views here.

def index(request):
    context = {}
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        vid_downloader(user_input)
        titles = extract_video_title(user_input)
        context['titles'] = titles
        context['user_input'] = user_input

    form = InputForm()
    context['form'] = form
    return render(request, "downloader/index.html", context)



def extract_video_title(playlist_url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(playlist_url, download=False)
        if 'entries' in result:
            return [entry['title'] for entry in result['entries']]
        else:
            return [result['title']]
        

import os
from datetime import datetime

def vid_downloader(yt_link):
    try:
        video_urls = extract_video_urls(yt_link)
        
        # Get the path to the user's Downloads folder
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(downloads_path, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'forcefilename': True,
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            counter = 0
            for video_url in video_urls:
                ydl.download([video_url])
                current_time = datetime.now().timestamp()
                os.utime(extract_video_title(video_url)[0], (current_time, current_time))
                counter += 1
    except Exception as e:
        return "unable to complete download"

def extract_video_urls(playlist_url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(playlist_url, download=False)
        if 'entries' in result:
            return [entry['url'] for entry in result['entries']]
        else:
            return [playlist_url]
