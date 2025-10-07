#!/bin/bash
# Render.com build script - Binary wheels only!
echo "🔧 Installing dependencies with binary wheels..."
pip install --upgrade pip
pip install --only-binary=:all: -r requirements.txt || pip install -r requirements.txt
echo "✅ Build complete!"
