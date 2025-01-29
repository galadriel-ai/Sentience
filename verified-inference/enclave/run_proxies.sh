#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

nohup vsock-proxy 8001 api.openai.com 443 \
  --config "$SCRIPT_DIR/vsock/vsock_proxy_openai.yaml" -w 20 \
  &> "$SCRIPT_DIR/vsock_proxy_openai.log" &
nohup vsock-proxy 8002 discord.com 443 \
  --config "$SCRIPT_DIR/vsock/vsock_proxy_discord.yaml" -w 20 \
  &> "$SCRIPT_DIR/vsock_proxy_discord.log" &
nohup vsock-proxy 8003 api.galadriel.com 443 \
  --config "$SCRIPT_DIR/vsock/vsock_proxy_galadriel.yaml" -w 20 \
  &> "$SCRIPT_DIR/vsock_proxy_galadriel.log" &
nohup vsock-proxy 8004 api.preplexity.ai 443 \
  --config "$SCRIPT_DIR/vsock/vsock_proxy_preplexity.yaml" -w 20 \
  &> "$SCRIPT_DIR/vsock_proxy_preplexity.log" &
nohup vsock-proxy 8005 api.telegram.org 443 \
  --config "$SCRIPT_DIR/vsock/vsock_proxy_telegram.yaml" -w 20 \
  &> "$SCRIPT_DIR/vsock_proxy_telegram.log" &  
nohup vsock-proxy 8006 api.twitter.com 443 \
  --config "$SCRIPT_DIR/vsock/vsock_proxy_twitter.yaml" -w 20 \
  &> "$SCRIPT_DIR/vsock_proxy_twitter.log" &  
nohup vsock-proxy 8007 agents-memory-storage.s3.us-east-1.amazonaws.com 443 \
  --config "$SCRIPT_DIR/vsock/vsock_proxy_s3.yaml" -w 20 \
  &> "$SCRIPT_DIR/vsock_proxy_s3.log" &
nohup vsock-proxy 8008 api.coingecko.com 443 \
  --config "$SCRIPT_DIR/vsock/vsock_proxy_coingecko.yaml" -w 20 \
  &> "$SCRIPT_DIR/vsock_proxy_coingecko.log" &
nohup vsock-proxy 8009 api.dexscreener.com 443 \
  --config "$SCRIPT_DIR/vsock/vsock_proxy_dexscreener.yaml" -w 20 \
  &> "$SCRIPT_DIR/vsock_proxy_dexscreener.log" &