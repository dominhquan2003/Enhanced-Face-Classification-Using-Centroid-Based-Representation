#!/bin/bash

# Lấy địa chỉ IPv4
IP=$(ipconfig | grep "IPv4" | awk '{print $NF}')

# Nếu không tìm thấy địa chỉ IP, thoát
if [ -z "$IP" ]; then
    echo "Không thể tìm thấy địa chỉ IPv4."
    exit 1
fi

# Khởi động server Django
echo "Khởi động server Django tại http://$IP:8000..."
cd backendapi
python manage.py runserver $IP:8000 &

# Đợi một chút để server Django khởi động
sleep 5

# Cập nhật file .env cho React Native
ENV_FILE="../frontend/.env" # Đường dẫn tới file .env
if [ -f "$ENV_FILE" ]; then
    echo "Cập nhật file .env với địa chỉ mới..."
    sed -i "s|EXPO_PUBLIC_API_URL=.*|EXPO_PUBLIC_API_URL=http://$IP:8000/facedetect/api/v1/|" $ENV_FILE
else
    echo "File .env không tồn tại tại $ENV_FILE."
    exit 1
fi

echo "Backend đã khởi động thành công."