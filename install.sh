#!/bin/bash

if [ ! -d "./crawl-venv" ]; then
  echo "[*] Venv missing, creating it now..."
  python -m venv crawl-venv
  source crawl-venv/bin/activate
else
  source crawl-venv/bin/activate
fi

pip install -r requirements.txt

sudo setcap cap_net_raw,cap_net_admin=eip "$(readlink -f "$(which python3)")"

if [ ! -f ".env" ]; then
  echo "[!] .env file not found. Creating one now..."
  echo 'GEMINI_API_KEY="YOURKEY"' > .env
  echo "[*] Please update the .env file with your actual GEMINI_API_KEY."
else
  source .env
  if [ -z "$GEMINI_API_KEY" ]; then
    echo "[!] GEMINI_API_KEY is missing or empty in your .env file."
    echo "[*] Please update the .env file with your actual GEMINI_API_KEY."
  fi
fi

echo "[*] Setup complete."
