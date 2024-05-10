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

### Alternative 1

- Skip the virtual environment and install the requirements to the base Python install using ```pip install```

### Alternative 2

- Use Anaconda/miniconda/miniforge to create an environment, and run baraag_dl.py from within the environment.

## Windows
### Recommended
- Download the [prepackaged binaries](https://github.com/rizelbr/Baraag_DL/releases).

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

# Usage
## Logging in and authentication
### First run
- Baraag DL will register a client with the Mastodon API used by Baraag.
- This will generate a persistent authentication token, ```client_credentials``` in the same folder baraag_dl.py is run from.
- You will be prompted for a username (e-mail) and password to log into your Baraag account.
- Should the login be successful, Baraag DL will generate a persistent user token, ```user_credentials``` in the same folder baraag_dl.py is run from.

### Subsequent runs
- If ```client_credentials``` and ```user_credentials``` are still valid, authentication will happen without user input.
- Should either or both files become invalid or corrupted, Baraag DL will recreate the client and prompt you for username and password again.
 
## Execution
- Baraag DL will then automatically:
    - Fetch all accounts you follow
    - Fetch all posts by accounts you follow that contain attachments
    - Download each attachment sequentially for all followed accounts
- Files are saved as ```{Date posted}_{Post ID}_{Attachment_ID}.extension``` in a folder for each account, named in the format ```{Account name}_{Account ID}```. Keep in mind that ```Account name``` is not the same as ```Display name```, so an account's public name and Baraag registration name may differ.
- Files already downloaded and saved to disk are skipped to save time, bandwidth, and not bombard the API with requests.

:warning: The Mastodon API is limited to 300 requests every 5 minutes. This means that Baraag DL will run considerably slower after some time as to prevent being cut off by the API.

# To-Do
- Implement search function.
- Implement downloading from specific users.
- Implement Pawoo compatibility.
  

  
