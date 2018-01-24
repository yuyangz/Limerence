# Limerence
Irene Lam: API Expert

Arif Roktim: Flask Expect

Anish Shenoy: Database Expert/Flask Assistant

Yuyang Zhang: PM/Frontend Expert

Welcome to our lifestyle app, where users will be able to monitor and receive suggestions in regards to their dietary choices and exercise plan! After creating an account, you will be prompted to insert information about your music choice, basic profile information (e.g. age, weight), exercise preferences, etc. so that our schedule will be tailored to your needs. For example, we will be suggesting music, food choices, and exercise sets, listed in both a recommendations page and a user-specific schedule. If you come across any recommendations you like, you may also insert them into your profile or save them for future reference. Without further ado, please enjoy the health benefits of our app!

Frontend is primarily managed through HTML and CSS.

Backend is managed through SQLite for databases. Various APIs (below) are used to retrieve information to create a custom-made schedule for the user. 

## Keys to procure in advance

[Spotify](https://www.spotify.com/us/) 

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
6. Copy the Application ID into a new line under "#Edamam ID - Key"
7. Copy the Application Key into a new line under the Application ID

[FourSquare](https://foursquare.com/) - Our location API
1. Create an account by clicking "Sign Up" [here](https://foursquare.com/)
2. Sign in [here](https://foursquare.com/login?continue=%2F&clicked=true)
3. Navigate to your apps [here](https://foursquare.com/developers/apps)
4. Copy the Client ID into a new line under "#FourSquare - Key"
5. Copy the Client Secret into a new line under the Client ID

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


