#!/bin/bash
# Render.com build script - Simple install
echo "🔧 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Build complete!"
