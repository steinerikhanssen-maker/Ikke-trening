FROM python:3.12-alpine
WORKDIR /app
COPY hall4_update_agent.py /app/hall4_update_agent.py
COPY stdin_dispatcher.py /app/stdin_dispatcher.py
CMD ["python3", "-u", "/app/stdin_dispatcher.py"]
