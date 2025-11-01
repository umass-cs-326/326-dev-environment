#! /usr/bin/env bash

echo -e "POST /api/artifact/create"
curl -sS -X POST http://localhost:8000/api/artifact/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -d '{
    "name": "Trail Camera",
    "description": "Solar powered, motion-activated camera",
    "location": { "lat": 42.391, "lon": -72.526, "alt": 92.5 },
    "parent_id": 0 
  }' | jq

echo -e "\nPOST /api/artifact/create"
curl -sS -X POST http://localhost:8000/api/artifact/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -d '{
    "name": "Spare Battery",
    "description": "Lithium pack for the trail cam",
    "location": { "lat": 42.392, "lon": -72.527 },
    "parent_id": 1
  }' | jq

echo -e "\nGET /api/artifact/1"
curl -sS "http://localhost:8000/api/artifact/1" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer <YOUR_TOKEN>" | jq
