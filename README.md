[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/19BwrNgF)

## Chatbot frontend

This repository now contains a simple static frontend for the Classwork Chatbot under the new Django app `chat`.

How to run (development, Windows PowerShell):

```powershell
# create a virtual env and install requirements if needed
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# run the Django development server
python manage.py runserver

# open http://127.0.0.1:8000/chat/ in your browser
```

Notes:
- The endpoint `/api/chat/` is currently a small demo that echoes messages. Replace `chat.views.chat_api` with a real model-backed implementation when ready.
- The repository also contains an earlier Streamlit prototype at `frontend/app.py` (used for auth redirect demos). The new chat UI is served by Django at `/chat/`.
