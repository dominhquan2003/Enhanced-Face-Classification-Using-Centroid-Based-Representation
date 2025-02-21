#!/bin/bash

# Dừng quy trình đang chạy trên cổng 8081
PIDS=$(netstat -ano | findstr :8081 | awk '{print $5}')

if [ -n "$PIDS" ]; then
    echo "Dừng quy trình đang chạy trên cổng 8081 với PID $PIDS..."
    for PID in $PIDS; do
        taskkill //PID $PID //F
    done
fi

# Khởi động server React Native
echo "Khởi động server React Native..."
cd ./frontend
npm run android &

echo "Frontend đã khởi động thành công."