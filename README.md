# Arr Stack Media Manager


## Maintainerr
recently i have found this new project that does the same as my script but better. feel free to use this script but i advise to check the following repo

[https://github.com/jorenn92/Maintainerr](https://github.com/jorenn92/Maintainerr).




**Disclaimer:**

**Use at your own risk! This project has the potential to delete data. Please ensure proper backups and take necessary precautions before running any commands. The author and contributors of this project are not responsible for any data loss or damage caused by the usage of this software.**


## Desciption
This Python script is designed to manage media content in a media center. It interacts with various APIs such as Tautulli and Overseerr to fetch, process, and delete media content based on the number of days that passed since the first request and the last activity on it before deletion.

This was made to manage a stack like the one I built [here](https://github.com/Rick45/quick-arr-Stack).

## Requirements
1. Overseer - Get the media requests from the users
2. Tautulli - Used to check the activity history for the media in the Overseerr requests
3. Sonarr - Used to delete the requested Shows media
4. Radarr - Used to delete the requested Movie media




## Configuration

The `config.json.example` file contains the following settings:

- `TESTING_MODE`: A boolean value indicating whether the application is in testing mode. (1 = Testing, 0 = Prod) In testing mode, no data will be deleted.
- `USERS_TO_IGNORE`: An array of usernames to ignore. Media requested by these users will be excluded from deletions.
- `NUMBER_OF_DAYS`: The number of days to purge the data.
- `NUMBER_OF_DAYS_IF_ONLY_REQUESTER`: The number of days to purge the data if the only person that has seen the media was the requester. This applies only to seen media.
- `WEBHOOK`: The URL for the webhook to be called. If left empty, no webhook will be called
- `OVERSEER_BASEURL`: The URL for the Overseer API.
- `OVERSEER_TOKEN`: The token for authentication with the Overseer.
- `RADARR_BASEURL`: The URL for the Radarr API.
- `RADARR_APIKEY`: The API key for authentication with the Radarr.
- `TAUTULLI_BASEURL`: The URL for the Tautulli API.
- `TAUTULLI_APIKEY`: The API key for authentication with the Tautulli.
- `SONARR_BASEURL`: The URL for the Sonarr API.
- `SONARR_APIKEY`: The API key for authentication with the Sonarr.


## How To run

### Run directly
1. Make sure you have Python installed on your system.
3. Update the configuration in the 'config.json' file with your desired settings.
4. Run the script using the following command:

    ```bash
    python mediacenterManager.py
    ```

### Run Using Docker:

1. Update the `crontab` file with the desired interval for checking the Media, this file will be used by the container to schedule the actions. The current configuration will check every day at midnight:
    
    ```bash
    0 0 * * * /usr/local/bin/python3 /app/mediacenterManager.py > /proc/1/fd/1 2>/proc/1/fd/2 
    ```

2. Build the Docker image:

    ```bash
    docker build -t arr_stack_manager .
    ```

3. Run the Docker container:

    ```bash
    docker run -d --name arr_stack_manager arr_stack_manager
    ```

