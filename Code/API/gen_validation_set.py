import os
import pprint
import re
import time

import billboard
import pandas as pd
import spotipy
import spotipy.util
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm

CHART = "hot-100-songs"
THROTTLE_TIME = 0.50  # Seconds


def spotipy_auth():
    load_dotenv()
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp


def test_search_query():
    sp = spotipy_auth()
    for track in unique_top_tracks_generator():
        print(track.artist)
        search_query = "artist:" + track.artist + " track:" + track.title
        results = sp.search(q=search_query)
        for i, t in enumerate(results["tracks"]["items"]):
            print(" ", i, t["name"], re.split("[']", t["name"]))
        pprint.pprint(results["id"])
        pprint.pprint(results["name"])
        pprint.pprint(results["popularity"])


def yearwise_data():
    dataset_dir = "dataset/hit predictor dataset"
    for file in os.listdir(dataset_dir):
        filename = file
        filepath = os.path.join(dataset_dir, file)
        print(filepath)
        df = pd.read_csv(filepath)
        df = df[df["target"] == 1]
        df = df[["track", "artist", "uri"]]
        df["popularity"] = [None for _ in range(len(df))]
        uris = df["uri"]
        uri_lists = [uris[x : x + 50] for x in range(0, len(uris), 50)]

        sp = spotipy_auth()
        for uri_list in uri_lists:
            tracks = sp.tracks(uri_list)
            for track in tracks["tracks"]:
                df.loc[df.uri == track["uri"], "popularity"] = track["popularity"]

        df.to_csv("dataset/processed-" + filename)


def get_track_count():
    df = pd.read_csv("dataset/data.csv")
    df = df.groupby("year", as_index=True).count()
    df = df["id"]
    track_count = {}
    for year in df.index:
        track_count[year] = df[year]
    return track_count


def unique_top_tracks_generator():
    track_dict = {}
    for year in range(1958, 2021):
        seen_tracks = set()
        chart = billboard.ChartData("hot-100", date=str(year) + "-12-31")
        while chart.previousDate[:4] == str(year):
            print(chart.previousDate)
            for track in chart:
                duplicate = track.title in seen_tracks
                if not duplicate:
                    seen_tracks.add((track.title, track.artist))
            time.sleep(THROTTLE_TIME)
            chart = billboard.ChartData("hot-100", chart.previousDate)
        track_dict[year] = list(seen_tracks)
    return track_dict
    # chart = billboard.ChartData(CHART, year="2020")

    # while len(seen_tracks) < TRACK_COUNT:
    #     top_track = chart[0]
    #     print(top_track.title)
    #     duplicate = top_track.title in seen_tracks

    #     if not duplicate:
    #         seen_tracks.add(top_track.title)
    #         yield top_track

    #     if chart.previousYear == "1999":
    #         break
    #     time.sleep(THROTTLE_TIME)
    #     chart = billboard.ChartData(CHART, year=chart.previousYear)

    # raise StopIteration


def store_billboard_tracks():
    track_dict = unique_top_tracks_generator()
    df = pd.DataFrame(columns=["year", "title", "artist"])
    for year in track_dict.keys():
        for track in track_dict[year]:
            df = df.append(
                {"year": year, "title": track[0], "artist": track[1]}, ignore_index=True
            )
    df.to_csv("dataset/billboard_tracks.csv")


def fetch_spotify_ids():
    df = pd.read_csv("dataset/billboard_tracks.csv")
    sp = spotipy_auth()
    id_list = []
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        query = "artist:" + row["artist"] + " track:" + row["title"]
        if index % 1000 == 0:
            time.sleep(2)
        results = sp.search(q=query)
        if len(results["tracks"]["items"]) != 0:
            id_list.append(results["tracks"]["items"][0]["id"])
        else:
            id_list.append(-1)
        print(id_list[-1])
    df["id"] = id_list
    df.to_csv("dataset/billboard_tracks.csv")


def fetch_popl_values():
    df = pd.read_csv("dataset/billboard_tracks.csv")
    ids = df["id"]
    df["popularity"] = [None for _ in range(len(df))]
    id_lists = [ids[x : x + 50] for x in range(0, len(ids), 50)]
    sp = spotipy_auth()
    for id_list in id_lists:
        tracks = sp.tracks(id_list)
        for track in tracks["tracks"]:
            df.loc[df.id == track["id"], "popularity"] = track["popularity"]
        time.sleep(1)

    df.to_csv("dataset/billboard_tracks.csv")


if __name__ == "__main__":
    fetch_popl_values()
