# Lab 1: Minimal Flask app + deploy to Render

Replace `SURNAME` and `GH_USER`. Windows shell; on Linux/macOS activate with `source .venv/bin/activate`.

## Part 1: Local project

1. Create dir `flask_app_SURNAME`, `cd` into it.
2. Create and activate venv: `python -m venv .venv`, then `.venv\Scripts\activate`.
3. `pip list`, then `python -m pip install --upgrade pip`.
4. `pip install flask`, then `pip show flask`.
5. `git init`. Create `.gitignore` ignoring `.venv/`, `__pycache__/`, `*.pyc`.
6. Create `app.py` (no comments):
   ```python
   from flask import Flask
   app = Flask(__name__)

   @app.route('/')
   def main():
       return 'Hello, world!'

   if __name__ == '__main__':
       app.run(debug=True)
   ```
7. Run both ways, check http://127.0.0.1:5000/ (note: `python app.py` has Debug on, `flask run` has Debug off):
   - `python app.py`
   - `flask run`
8. Commit: `git add . && git commit -m "Initial commit: created Flask app and set up env"`
9. **[Manual]** Create empty GitHub repo `flask-app-lab`. Then:
   ```
   git branch -M main
   git remote add origin https://github.com/GH_USER/flask-app-lab.git
   git push -u origin main
   ```
10. `pip install python-dotenv`
11. Create `.flaskenv`:
    ```
    FLASK_DEBUG=1
    FLASK_APP=app.py
    FLASK_RUN_PORT=8080
    ```
12. Run `flask run`, confirm "Debug mode: on" and port 8080.
13. `pip freeze > requirements.txt` (ensure UTF-8 encoding, not UTF-16). Verify with `pip install -r requirements.txt`.
14. Commit and push: `git add . && git commit -m "Add dotenv and requirements" && git push`

## Part 2: Deploy

1. `pip install gunicorn`, `pip freeze > requirements.txt`, commit `"add gunicorn"`, push.
2. **[Manual, browser]** On render.com: sign up, New -> Web Service, connect repo `flask-app-lab`.
   - Language: Python 3
   - Branch: main
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Instance: Free
   - Click Deploy Web Service, wait for "Live".
3. **[Manual]** Open the `https://<name>.onrender.com` URL, confirm "Hello, world!" (free tier may take ~50s to wake).
4. **[Manual]** Check service shows "Deployed" on dashboard.render.com.

## Report deliverables (all manual screenshots)

- Screenshot: local browser page (Hello, world!)
- Screenshot: Render dashboard with service list
- Screenshot: deployed app in browser (onrender.com URL visible)
- Link: `https://github.com/GH_USER/flask-app-lab`
