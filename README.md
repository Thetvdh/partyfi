# PartyFi

# Usage:

**REQUIRES SPOTIFY PREMIUM FOR FULL USE OF FEATURES!**

1) Clone repo `git clone https://github.com/Thetvdh/partyfi`
2) Rename .env.example to .env
3) Configure .env with your details from your spotify dashboard
4) Create a venv `python3 -m venv venv`
5) Enter the venv `source venv/bin/activate`
6) Install dependencies `pip3 install -r requirements.txt`
7) Run gen_token.py `python3 gen_token.py`
8) Run app.py `python3 app.py`
9) Go to http://127.0.0.1:5000/
10) Done


Common mistakes:

- Ensure the redirect URI set in the .env file is the same as the redirect URI on your spotify dashboard.
- Use Python 3.11+
- If running on a server configure Gunicorn as a part of your deployment rather than just running app.py


# Todo

- Add way of resetting the number of people currently in a room
- Add skip button to Queue as well as search.