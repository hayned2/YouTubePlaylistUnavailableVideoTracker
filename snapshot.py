import requests
import ast
import json
import os

def getPlaylistsFromUser():
    knownPlaylists = None
    with open(f'{os.path.dirname(os.path.realpath(__file__))}/playlists.json', mode="r", encoding='utf-8') as jsonFile:
        knownPlaylists = json.load(jsonFile)
    if knownPlaylists != None:
        playlistIndices = {}
        print("Enter which playlist number you want to snapshot, or leave blank for all:")
        for index, playlist in enumerate(knownPlaylists):
            print(f'\t({index + 1}): {playlist}')
            playlistIndices[str(index + 1)] = playlist
        index = input()
        if index in playlistIndices:
            playlist = playlistIndices[index]
            return {playlist: knownPlaylists[playlist]}
        elif index == '':
            return knownPlaylists
        else:
            print("Unknown input:", index)

def getAPIKey():
    with open(f'{os.path.dirname(os.path.realpath(__file__))}/googleAPIKey.txt', mode="r", encoding='utf-8') as keyFile:
        return keyFile.readline().strip()
    
def updateSnapshotFile(videos, playlistName):
    snapshotFilePath = f'{os.path.dirname(os.path.realpath(__file__))}/Snapshots/{playlistName}.json'
    knownPlaylistVideos = {}
    if os.path.isfile(snapshotFilePath):
        with open(snapshotFilePath, mode="r", encoding='utf-8') as jsonFile:
            knownPlaylistVideos = json.load(jsonFile)

    knownPlaylistVideos.update(videos)
    with open(snapshotFilePath, mode="w+", encoding='utf-8') as jsonFile:
        json.dump(knownPlaylistVideos, jsonFile, indent='\t')

    return knownPlaylistVideos

def alertForUnavailableVideos(videos, unavailableVideos):
    if len(unavailableVideos) > 0:
        print("\t--Listing out unavailable videos--")
        for video in unavailableVideos:
            if unavailableVideos[video] in [ 'Deleted video', 'Private video'] and video in videos:
                unavailableVideos[video] = videos[video]
            print(f"\t\t{unavailableVideos[video]} ({video})")

def snapshotPlaylist(playlistName, playlistId):
    
    # Set parameters for the GET request
    params = {
        "playlistId": playlistId,
        "key": getAPIKey(),
        "part": "snippet,status",
        "maxResults": 50,
        "pageToken": None
    }

    moreVideos = True
    videos = {}
    unavailableVideos = {}
    pageNumber = 0

    # Keep making calls while there are videos to grab. Google API allows up to 50 items per page.
    while moreVideos:

        print("\tGetting page number", pageNumber)
        pageNumber += 1

        retryCount = 0
        response = None
        while retryCount < 3:
            # Make the API call
            response = requests.get("https://www.googleapis.com/youtube/v3/playlistItems", params)
            if response.status_code != 200:
                retryCount += 1
            else:
                break

        # Make sure we get a 200.
        if response.status_code == 200:

            # Convert from bytes to a dictionary
            responseContent = ast.literal_eval(response.content.decode('utf-8'))

            # Check if there is another page of content to GET, or if this is the last page.
            if 'nextPageToken' in responseContent:
                params["pageToken"] = responseContent['nextPageToken']
            else:
                moreVideos = False

            # Iterate over the retrieved videos. Grab their URL and title, then sort them by their status.
            if 'items' in responseContent:
                for video in responseContent['items']:
                    videoId = video.get("snippet", {}).get("resourceId", {}).get("videoId", None)
                    videoTitle = video.get("snippet", {}).get("title", None)
                    if not videoId or not videoTitle:
                        print("Video", video, "was found without a title or an id")
                        continue
                    if video.get("status", {}).get("privacyStatus", {}) in ['public', 'unlisted']:
                        videos[videoId] = videoTitle
                    else:
                        unavailableVideos[videoId] = videoTitle
        else:
            print("\tResponse returned with code: ", response.status_code)
            print(response.content)
            break

    print("\tNumber of available videos:", len(videos))
    print("\tNumber of unavailable videos:", len(unavailableVideos))

    videos = updateSnapshotFile(videos, playlistName)
    alertForUnavailableVideos(videos, unavailableVideos)

def main():
    playlists = getPlaylistsFromUser()
    if not playlists:
        exit()
    for playlistName in playlists:
        print(f"Processing {playlistName}...")
        snapshotPlaylist(playlistName, playlists[playlistName])
    print("Finished!")

if __name__ == "__main__":
    main()