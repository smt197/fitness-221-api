#!/bin/sh

# 1. Start Cloudflare Tunnel
if [ -n "$CLOUDFLARE_TUNNEL_TOKEN" ]; then
    echo "--- Starting Cloudflare Tunnel with Token ---"
    cloudflared tunnel --no-autoupdate run --token "$CLOUDFLARE_TUNNEL_TOKEN" &
else
    echo "--- Starting Cloudflare Tunnel (Anonymous Quick Tunnel) ---"
    cloudflared tunnel --url http://localhost:8000 &
fi

# 2. Start the Application
echo "--- Starting Python FastAPI Application ---"
uvicorn api:app --host 0.0.0.0 --port 8000
