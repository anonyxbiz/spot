# Views.py
from django.shortcuts import render
from spotifydata import song_data
from os import environ
from random import randint
from django.http import JsonResponse

p = print

def home(request):
    if request.method == 'POST':
        song_url = request.POST.get('song_url')

        if not song_url.startswith('https://open.spotify.com/album/'):
            error_message = "Please enter a valid Spotify album link."
            return render(request, 'analytics_app/home.html', {'error_message': error_message})

        Bearer_token ="BQBx0MOZVvPpnfxa07QhJqMqnyWWNGsukIpP48oeSnN8DQThlbWhfDpz6SkwPQ2hEx866i9oj08BNvwJPmqxLlKRovhsd3912NhOPFwUoM43VqiQxhTQ1yC3QHK6tgCgPKg1cvvVl3Yra2eOn3vDs6kWwkviGWa6kF500FKvc2CD4WmRaWVJ7HssRsJZXID2jx5W-If-upbZEuafvRmatB_DhhFkzR0KCdMrln6Y8HZs_4g__20kwMw-gt7-swgH5H_QEyIdTP35b1eSaFG66fe2Rc2DV0vk2eyJmqUjcTDpIMzjM1GX7LKP9b_oZUFXdQuToHD-k5CIkAhfAVi3erTnXtr0f-CB"

        streams_or_tracks = song_data(song_url, Bearer_token)

        if isinstance(streams_or_tracks, int):
            streams = streams_or_tracks
            return render(request, 'analytics_app/home.html', {'streams': streams})

        elif isinstance(streams_or_tracks, list):
            streams = None
            total_album_streams = streams_or_tracks.pop(-1)['total_album_streams']  # Extract total album streams
            release_name = streams_or_tracks.pop(-1)['release_name']  # Extract release name
            return render(request, 'analytics_app/home.html', {'streams': streams_or_tracks, 'total_album_streams': total_album_streams, 'release_name': release_name})

    return render(request, 'analytics_app/home.html')
