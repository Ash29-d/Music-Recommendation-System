import pickle 
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd


Client_ID = "c905b9e812e14b31be8e8cd838001ecb"
Client_secret = "e99bea4af8ed4ef5a27dd89c9ea09bde"

# Initialize the spotify client
client_credentials_manager = SpotifyClientCredentials(client_id = Client_ID,client_secret=Client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name , artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query ,type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        print(album_cover_url)
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend(song):
    print(music[music["song"]==song])
    if music[music["song"]==song].shape[0] > 0:
        index = music[music["song"]==song].index[0]
        distance = sorted(list(enumerate(similarity[index])),reverse=True , key=lambda x : x[1])
        recommended_music_names = []
        recommended_music_posters = []
        for i in distance[1:6]:
            artist = music.iloc[i[0]].artist
            print(artist)
            print(music.iloc[i[0]].song)
            recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song,artist))
            recommended_music_names.append(music.iloc[i[0]].song)
            
        return recommended_music_names, recommended_music_posters
    else:
        return [],[]


st.header("Music Recommender System")

music = pickle.load(open("df.pkl", "rb"))
music = pd.DataFrame(music)
music.reset_index(inplace=True,drop=True)
print(music)
similarity = pickle.load(open("similarity.pkl", "rb"))

music_list = music['song'].values
selected_movie = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)

print("selected_movie", selected_movie)

if st.button('Show Recommendation'):
    recommended_music_names,recommended_music_posters = recommend(selected_movie)

    if recommended_music_names:
        col1, col2, col3, col4, col5= st.columns(5)
        with col1:
            st.text(recommended_music_names[0])
            st.image(recommended_music_posters[0])
        with col2:
            st.text(recommended_music_names[1])
            st.image(recommended_music_posters[1])

        with col3:
            st.text(recommended_music_names[2])
            st.image(recommended_music_posters[2])
        with col4:
            st.text(recommended_music_names[3])
            st.image(recommended_music_posters[3])
        with col5:
            st.text(recommended_music_names[4])
            st.image(recommended_music_posters[4])

    else:
        st.text("Music not found")