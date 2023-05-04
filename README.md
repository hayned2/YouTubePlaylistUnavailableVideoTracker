# **YouTube Playlist Unavailable Video Tracker**

*Do you have a YouTube playlist with videos that keep getting deleted or hidden, and find yourself scraping around trying to figure out which video it was?*

*This code attempts to assist in reducing the pain of maintaining your playlists by tracking the names of your videos, and alerting you WHEN a video is removed, and WHAT video was removed.*

*When you run this script for the first time, a record will be made of your playlist videos and their IDs. This record is then used on any subsequent run of the script to alert you of any unavailable videos.*

## **Setup**

### **Setting your playlists**

To track a playlist, you need to provide the script with two things: your name for the playlist, and the YouTube ID.

1. The name can be anything that is valid for a filename in Windows (So some special characters might be invalid).
2. The ID can be found in the URL of the playlist page on YouTube.

![Playlist ID](https://imgur.com/gBFFWKx.jpg)

Once you have this information, you insert it into your ```playlists.json``` file in the following json format:

```
{
    "certified_bangers": "PLFmSz1cm0-ouuhx1-HOr-6pwlZCSpblf3",
    "best_game_music": "PLrnb8c3hFJatjyJ-wFMuFGANNoo7-LZsG"
}
```

*Note that this file needs to be in valid JSON format. See [here](https://www.w3schools.com/js/js_json_intro.asp) for more information if needed. The script can handle as many playlists you would like, one per line.*

### **Getting your Google API Key**

In order to communicate with the Google servers to get the information for your playlists, you need an access key, which can be given to anyone with a valid Google account.

There is a guide on getting API Keys [here](https://cloud.google.com/docs/authentication/api-keys).

Once you have your API Key, it needs to be placed in the ```googleAPIKey.txt``` file on a single line.

## Running the Script

You can run the script through Python, or by double-clicking on the ```Snapshot.sh``` file.

The user will be prompted with a list of their inputted playlists from ```playlists.json```, and asked to either provide the number for a single playlist, or simply press enter to process all of the playlists.

![user_prompt](https://imgur.com/udg0DNb.jpg)

The script will then go through the playlists, getting the information and the statuses for each video, providing a summary of the number of available videos and the number of unavailable videos. Additionally, it will provide the names and the IDs of any unavailable videos, for you to address.

*Note 1: Google will only return information for 50 videos in a single call, so if your playlist is longer than 50 videos, The script will need to make multiple calls. This is shown to the user from the  "Getting page number ___" outputs*

*Note 2: If you run this script for the first time on a playlist that currently has unavailable videos, the names of those videos will be unknown (i.e. Deleted Video), and those videos will need to be removed or replaced manually. On subsequent runs of the script, any previously available videos that are made unavailable will have their proper names.*

![output](https://imgur.com/wnohD38.jpg)

## Extra Notes

- I recommend running this script once you have your playlist in a good state (no current unavailable videos), and every time that you modify your playlist. After that, you can run it on a regular schedule to stay on top of the status of your videos or run it whenever you notice a video has been made unavailable to identify the video(s) in question.
- The Google API has a limit to its calls, but that limit is not something this script should come remotely close to hitting. (50,000 calls per day, 10 calls per second)
