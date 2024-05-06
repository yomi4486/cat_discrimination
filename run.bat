cd /d %~dp0
start uvicorn api:app --host 0.0.0.0 --port 8008 --reload