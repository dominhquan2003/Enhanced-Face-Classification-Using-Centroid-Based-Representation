#!/bin/bash

# Dừng quy trình đang chạy trên cổng 8081
PID=$(netstat -ano | findstr :8081 | awk '{print $5}')

if [ -n "$PID" ]; then
    echo "Dừng quy trình đang chạy trên cổng 8081 với PID $PID..."
    taskkill /PID $PID /F
fi

# Khởi động server React Native
echo "Khởi động server React Native..."
cd ./frontend
npm run android &

echo "Frontend đã khởi động thành công."