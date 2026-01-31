#!/bin/bash

echo "------------------------------------------"
echo "🛠 AIOPS HEALER TRIGGERED AT: $(date)"
echo "Action: Clearing temporary system caches and identifying heavy processes..."

# 1. Simulate a fix by clearing a (safe) temp folder
rm -rf ./temp_cache/*
echo "✅ Temp cache cleared."

# 2. Log the top 3 CPU consuming processes for the record
echo "📊 Top CPU Consumers at time of event:"
ps -eo pcpu,comm -r | head -n 4

echo "✅ Healing process complete. System should stabilize shortly."
echo "------------------------------------------"