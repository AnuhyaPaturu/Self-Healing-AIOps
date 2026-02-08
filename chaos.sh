#!/bin/bash

# --- CONFIGURATION ---
DURATION=60
CORES=$(nproc)

echo "-----------------------------------------------"
echo "☢️  AIOPS CHAOS AGENT: TOTAL SYSTEM STRESS"
echo "-----------------------------------------------"
echo "🎯 Stressing $CORES cores + Memory + Disk I/O..."

# 1. STRESS CPU: Run 'yes' on all cores
for i in $(seq 1 $CORES); do
    yes > /dev/null &
done

# 2. STRESS MEMORY: Allocate a large chunk of RAM (adjust 512M if needed)
# This uses the 'stress' tool if installed, or a python one-liner if not
python3 -c "a = bytearray(1024*1024*512); import time; time.sleep(60)" &
MEM_PID=$!

# 3. STRESS I/O: Force heavy disk writing
dd if=/dev/zero of=temp_chaos_file bs=1M count=1024 conv=fdatasync &
IO_PID=$!

echo "🔥 STATUS: SYSTEM UNDER HEAVY MULTI-VECTOR ATTACK"
echo "📡 ACTION: Check the 'AI Confidence' score on your Dashboard!"
echo "⏳ Time remaining: $DURATION seconds..."

# 2. Wait for the duration
sleep $DURATION

# 3. Clean up
echo "-----------------------------------------------"
echo "🩹 CHAOS ENDED: Cleaning up all stress vectors..."
pkill yes
kill $MEM_PID
rm temp_chaos_file
echo "✅ STATUS: Resources released. Baseline recovery starting."
echo "-----------------------------------------------"