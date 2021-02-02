# Anime Downloader (gogoanime.so)

This is a Python script run in a docker container that uses Selenium and Headless Chrome to allow you to download anime from gogoanime.so easily.

## Installation

1. Install Docker Desktop
2. Run Docker Desktop
3. Download the files

## Usage

OPTIONAL: Clean up your docker containers and images.

```bash
docker system prune
```

First, build the docker container. This should take 1-2 minutes depending on your internet connection and download speeds.

For testing purposes, newer build changes should apply in less than a second (everything is stored in the cache if you don't delete the image with docker system prune).

```bash
docker build -t anime-py .
```

The script may ask you for your sudo password. Enter it and continue.

Then, run the following command. Note that when specifying the directory on your host computer, use escape characters if you're on a Mac or it will give you an error.

In this Mac example, 'user' is deciding to download a season of their favorite anime to a folder titled "!anime", which is inside their "Air Video" folder on their Desktop. The backslash character '\' should precede spaces and special characters. Do not change 'home anime-py'.

### MAC
```bash
docker run --interactive --tty -v /Users/user/Desktop/Air\ Video/\!anime/:/home anime-py
```

### WINDOWS
```bash
docker run --interactive --tty -v "$("C:/Users/user/Desktop/Air Video/!anime/"):/home" anime-py
```

NOTE: Simply add "update" to the end of either of those commands to update all your anime without going through the menu first.

### results

A file titled "myAnime.txt" will be generated in the same folder you decide to store your anime, and will save all your previous downloads. This makes updating your anime list with the most recent episodes a breeze. This also means you can share this file and its contents with a friend, and run them through the same process. Then all they'll have to do is drag the "myAnime.txt" into the destination for their anime episodes, and select [1] for "Update your anime" when prompted by the script.

### Adding Anime (3 OPTIONS)

Option 1: You can also add an anime by using the 'addAnime' tag after your initial command

### MAC
```bash
docker run --interactive --tty -v /Users/user/Desktop/Air\ Video/\!anime/:/home anime-py addAnime
```

### WINDOWS
```bash
docker run --interactive --tty -v "$("C:/Users/user/Desktop/Air Video/!anime/"):/home" anime-py addAnime
```

Option 2: Run the script normally without the 'update' or 'addAnime' tags. Select 'Add a new anime [2]'. Enter in the link for the gogoanime page of the anime, and continue to give the console information such as desired name of anime, season, subs or dubs, etc.

Option 3: Run the script normally without the 'update' or 'addAnime' tags. Select 'Search for anime [3]'. Type in the name of the anime (it can be partially incomplete). For this example, lets search for the anime 'kill la kill'. 

The results should be this:

```
1: https://gogoanime.so/category/kill-la-kill
2: https://gogoanime.so/category/kill-la-kill-dub
3: https://gogoanime.so/category/kill-la-kill-special
```

Select one of the options, and continue. This bypasses the need for finding the anime page yourself!

Option 4: Add the anime MANUALLY to your myAnime.txt file. The format is as follows: 

title, url, season, sub or dubs (s or d)

Example: Kill La Kill, https://gogoanime.so/category/kill-la-kill, 1, s

NOTE: Make sure to have a newline character onto the next line.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

# extra testing stuff for later
```
brew install docker-machine-nfs
docker-machine create yourdockermachine
docker-machine start yourdockermachine # already starting?
docker-machine-nfs yourdockermachine --shared-folder=/Users --nfs-config="-alldirs -maproot=0"
```
