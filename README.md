# Anime Downloader (gogoanime.so)

This is a Python script run in a docker container that uses Selenium and Headless Chrome to allow you to download anime from gogoanime.so easily.

## Installation

1. Install Docker Desktop
2. Run Docker Desktop
3. Simply download the files.

## Usage

OPTIONAL: Clean up your docker containers and images.

```bash
docker system prune
```

First, build the docker container. This should take a minute or two, and is a one time build until this script is updated again.

For testing purposes, newer build changes should apply in less than a second (everything is stored in the cache).

```bash
docker build -t anime-py .
```

The script may ask you for your sudo password. Simply enter it and continue.

Then, simply run the following command. Note that when specifying the directory on your host computer, use escape characters where necessary or it will give you an error.

For this following example, 'user' is deciding to download a season of their favorite anime to a folder titled "Air Video" on their Desktop, inside the '!anime' folder. The backslash character '\' should precede spaces and special characters. Do not change 'home anime-py'.

MAC
```bash
docker run --interactive --tty -v /Users/user/Desktop/Air\ Video/\!anime/:/home anime-py
```

WINDOWS
```bash
docker run --interactive --tty -v "$("C:/Users/user/Desktop/Air Video/!anime/"):/home" anime-py
```

A file titled "myAnime.txt" will be generated in the same folder you decide to store your anime, and will save all your previous downloads. This makes it very simple to check for new episodes and install them for all your favorite anime!

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

# extra testing stuff for later
brew install docker-machine-nfs
docker-machine create yourdockermachine
docker-machine start yourdockermachine # already starting?
docker-machine-nfs yourdockermachine --shared-folder=/Users --nfs-config="-alldirs -maproot=0"
