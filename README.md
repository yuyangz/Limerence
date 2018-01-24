# Limerence
Irene Lam: API Expert

Arif Roktim: Flask Expert

Anish Shenoy: Database Expert/Flask Assistant

Yuyang Zhang: PM/Frontend Expert

Welcome to our lifestyle app, where users will be able to monitor and receive suggestions in regards to their dietary choices and exercise plan! After creating an account, you will be prompted to insert information about your music choice and location so that our schedule will be tailored to your needs. For example, we will be suggesting music, food choices, and exercise sets, listed in both a recommendations page and a user-specific schedule. Recommendations will be tailored to the user and will change depending on the time of day, weather, and the user's preferences. If you come across any recommendations you like, you may also insert them into your schedule. Without further ado, please enjoy the health benefits of our app!

Frontend is primarily managed through HTML and CSS.

Backend is managed through SQLite for databases. Various APIs (below) are used to retrieve information to create a custom-made schedule for the user.

[Watch out Demo here](https://youtu.be/WDz5c8pCyVQ)

## Keys to procure in advance

Be sure that keys.txt is in the root of the repository!

[Spotify](https://www.spotify.com/us/)
1. Create an by signing up [here](https://beta.developer.spotify.com/dashboard/)
2. Now that you are greeted by the dashboard, create a new app
3. Copy the client ID and paste it under the line "#Spotify ID - Secret" in keys.txt
4. Copy the client secret and paste it under the client ID

[OpenWeatherMap](https://openweathermap.org/api) - Our weather API
1. Create an account [here](https://home.openweathermap.org/users/sign_up)
2. Sign in [here](https://home.openweathermap.org/users/sign_in)
3. View your profile by clicking on your username
4. Navigate to the section titled "API keys"
5. Create a key by naming your key and clicking "Generate"
6. Copy the resulting key into keys.txt into a new line under "#OpenWeatherMap - Key"

[Edamam](https://www.edamam.com/) - Our food and nutrition API
1. Create an account [here](https://www.edamam.com/signup)
2. Sign in [here](https://www.edamam.com/login?return=/) if you are not yet logged in
3. Sign up for the Nutrition Analysis API and choose the Developer plan
4. Navigate your mouse to the tab labeled "Get an API key now!"
5. Create an application by filling in necessary information
6. Copy the Application ID into a new line under "#Edamam ID - Key" in keys.txt
7. Copy the Application Key into a new line under the Application ID in keys.txt

[Eventbrite](https://eventbrite.com/) - Our location API
1. Create an account by clicking sign in in the top right corner [here](https://www.eventbrite.com/developer/v3/)
2. Once you are signed in, head over to "my apps" [here](https://www.eventbrite.com/myaccount/apps/)
3. Create a new app
4. Expand the dropdown
5. Copy the key labeled "Your personal OAuth token"
6. Place this under the line labeled "#Eventbrite - Key" in keys.txt

## Instructions to run the application
- Pull repository

- Enter virtual environment

```
. <.name>\bin\activate
```

- Install necessary packages

```python
  pip install requests
```

- Run application.

```python
  python app.py
```

*App should now be running!*
