# Baraag DL

A simple Baraag media downloader, made to be a simple way of downloading all images/videos in posts made by accounts you follow.

Inspired by [PixivUtil](https://github.com/Nandaka/PixivUtil2) and [FantiaDL](https://github.com/bitbybyte/fantiadl).

Many thanks to the folks at [Mastodon.py](https://github.com/halcy/Mastodon.py) for making this implementation much easier than expected.

# Installation

## Linux/MacOS
### Recommended
- Create an environment with:
```python3 -m venv baraag_dl```

- Activate the environment:
```source baraag_dl/bin/activate```

- Download [requirements.txt](https://github.com/rizelbr/Baraag_DL/blob/main/requirements.txt) and baraag_dl.py to your current folder.

- Install dependencies:
```python3 -m pip install -r requirements.txt```

- Alternatively, install the following packages using ```python3 -m pip install```:
```
colorama
Mastodon.py
requests
```
- Run Baraag_DL:
  ```python3 baraag_dl.py```

- After done running, either close the terminal or deactivate the environment with: ```deactivate```

#### Optional additional setup
- For added convenience, I recommend either creating a shell script to execute ```baraag_dl.py``` using the Python interpreter from the environment you created above, or modifying ```baraag_dl.py``` to point to the environment's Python interpreter when executing.

- For the former, if we suppose you created the ```baraag_dl``` environment in your home folder, create a file containing the following lines in the same folder as ```baraag_dl.py```:
```
#!/bin/bash

~/baraag_dl/bin/python3 baraag_dl.py
```

- Save the file with a name of your choice (let's call it ```run.sh``` for this example), and grant it execution permissions with ```chmod +x run.sh``` .

- From this point on, you should be able to execute Baraag DL by running ```run.sh``` , without the need to activate or deactivate environments.

- For the latter, modify the first line in ```baraag_dl.py``` to ```#!~/baraag_dl/bin/python3```

- From this point on, you should be able to execute ```baraag_dl.py``` directly, without the need for activating or deactivating an environment.

- Please be aware that if you choose the latter, you **will** need to redo this modification whenever you update Baraag DL.

### Alternative 1

- Skip the virtual environment and install the requirements to the base Python install using ```pip install``` to install the required packages listed above.

### Alternative 2

- Use Anaconda/miniconda/miniforge to create an environment, install the required packages, and run ```baraag_dl.py``` from within the environment.

## Windows
### Recommended
- Download the [prepackaged binaries](https://github.com/rizelbr/Baraag_DL/releases).
- Run Baraag DL by double-clicking the executable file.

### Alternative
- Download and install Python if not already installed.

- Create an environment with:
```py -m venv baraag_dl```

- Activate the environment:
```baraag_dl\Scripts\activate```

- Download [requirements.txt](https://github.com/rizelbr/Baraag_DL/blob/main/requirements.txt) and baraag_dl.py to your current folder.

- Install dependencies:
```py -m pip install -r requirements.txt```

- Alternatively, install the following packages using ```py -m pip install```:
```
colorama
Mastodon.py
requests
```
- Run Baraag_DL:
  ```py baraag_dl.py```

- After done running, either close the terminal or deactivate the environment with: ```deactivate```

# FFMpeg Video conversion
- As of version 0.02, Baraag DL is capable of converting animations/videos posted on Baraag to APNG and GIF. **This REQUIRES [ffmpeg](https://www.ffmpeg.org) to be provided by the user (or their OS, as applicable)**
- In order to achieve this, a config file for ffmpeg settings is necessary. If this is your first time running Baraag DL, it will create it for you (`config.ini`) on the first time you run it. The file will be recreated if it is ever deleted or corrupted.
- The default file consists of the following lines:
```
use_ffmpeg = False
ffmpeg_path = System
convert_gif = True
convert_apng = True
file_size_limit = 50.0
```

- Let's go over them in a little bit more detail:
## use_ffmpeg
```use_ffmpeg = False```
- Whether or not Baraag DL will attempt to convert MP4 files as it comes across them. Set this to `True` to enable video conversion.
- This defaults to `False` as I didn't want to force a new feature onto people who don't want or need it.

## ffmpeg_path
```ffmpeg_path = System```
- Where in the system the ffmpeg executable is located.
- The default is `System`, and on Linux systems this tells Baraag DL to use `/usr/bin/ffmpeg`; On Windows, this tells Baraag DL to use `ffmpeg.exe` **in the same folder as Baraag DL**, and on Mac OSX it tells Baraag DL to use `ffmpeg` **in the same folder as Baraag DL**. 
- If using Windows, I recommend you place `ffmpeg.exe` in the same folder as `baraag_dl.py`/`baraag_dl.exe` to make things simple.
- If using a Mac, I recommend you place `ffmpeg` in the same folder as `baraag_dl.py`. 
- Alternatively, replace `System` with the **full path** to the ffmpeg executable (i.e. `/home/Downloads/ffmpeg` ; `/Users/$USER/Downloads/ffmpeg` ; `C:\Downloads\ffmpeg.exe`)
### Note for Mac users
- If the OS does not allow you to run ffmpeg due to "untrusted developer", I recommend you download ffmpeg through [Homebrew](https://brew.sh/) and then use the path provided by Homebrew as the ffmpeg path. If unsure, type `which ffmpeg` into the Terminal app and it will tell you which path to use.
## convert_gif
```convert_gif = True```
- Whether or not Baraag DL should create GIFs from MP4 files.
- Defaults to `True`
## convert_apng
```convert_apng = True```
- Whether or not Baraag DL should create APNGs from MP4 files.
- Defaults to `True`
## file_size_limit
```file_size_limit = 50.0```
- Sets the file size limit, in MB, for the **input file** to be used for video conversion.
- Defaults to 50(MB)
- This means any MP4 file over 50MB will be skipped and not converted to GIF or APNG.
- This was done because some video files on Baraag are **massive**, and:
	1. Converting these massive files takes a **very** long time
	2. The resulting filesize of the converted files is **absurd** (16GB APNG from a 67MB MP4, for example).
	3. The resulting files are unplayable/unusable due to their file size and serve no practical purpose other than take up disk space.
- If you absolutely **need** to convert larger files, do increase the limit to a value you are comfortable with; However, in that case I would suggest you raise it temporarily to convert the files from a specific creator you want (**hint:** use the search function) and then lower it to a saner value.
# Usage
## Logging in and authentication
### First run
- Baraag DL will generate a `config.ini` file with the default recommended values.
- Baraag DL will register a client with the Mastodon API used by Baraag.
- This will generate a persistent authentication token, ```client_credentials``` in the same folder baraag_dl.py is run from.
- You will be prompted for a username (e-mail) and password to log into your Baraag account.
- Alternatively, leave the login field blank to proceed as an unregistered user. This obviously won't allow for downloading media from followed accounts, but allows you to download from specific accounts by using the search function.
- Should the login be successful, Baraag DL will generate a persistent user token, ```user_credentials``` in the same folder Baraag DL is run from.

### Subsequent runs
- Settings from the `config.ini` file will be read.
- If ```client_credentials``` and ```user_credentials``` are still valid, authentication will happen without user input.
- Should either or both files become invalid or corrupted, Baraag DL will recreate the client and prompt you for username and password again.
 
## Execution
- You will then be shown a menu and asked how you'd like to proceed:
### 1. Download from all followed accounts (if logged in)
- Baraag DL will automatically:
    - Fetch all accounts you follow
    - Fetch all posts by accounts you follow that contain attachments
    - Download each attachment sequentially for all followed accounts
    - Convert all MP4 files it comes across to GIF/APNG (if enabled by the user in the `config.ini` file generated)
- This option is disabled for unregistered users.
    
### 2. Search for a specific user
- Baraag DL will then prompt you for the name of the artist/account to search. 
- Should the search be successful, it will present you with a list of the accounts matching the name you input.
- You can then choose among the options of the list for the account from which all media will be downloaded.
- If ffmpeg is present and enabled, all MP4 media will be converted to GIF/APNG, as configured in the `config.ini` file.

## Downloading and Filenames
- Files are saved as ```{Date posted}_{Post ID}_{Attachment_ID}.extension``` in a folder for each account, named in the format ```{Account name}_{Account ID}```. Keep in mind that ```Account name``` is not the same as ```Display name```, so an account's public name and Baraag registration name may differ.
- Files already downloaded and saved to disk are skipped to save time, bandwidth, and not bombard the API with requests.
- Files already converted will likewise be skipped.

:warning: The Mastodon API is limited to 300 requests every 5 minutes. This means that Baraag DL will run considerably slower after some time as to prevent being cut off by the API.

# To-Do
- Implement dry run mode (debugging)
- Implement Pawoo compatibility.
- Install script for MacOS/Linux (?)
