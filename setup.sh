#!/usr/bin/env bash

set -eio pipefail

if [[ -d venv ]]; then
    echo "⏭️ Virtual environment already exists. Skipping setup."
    exit 0
fi

echo "🌱 Creating virtual environment..."
python3 -m venv venv

echo "📦 Activating virtual environment and installing dependencies..."
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Setup complete. Virtual environment created and dependencies installed."
