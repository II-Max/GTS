# Sử dụng Python 3.10 slim làm hệ điều hành cơ sở
FROM python:3.10-slim

# Thiết lập thư mục làm việc trong Docker
WORKDIR /app

# Cài đặt các trình biên dịch (C++, Java, Node.js, Pascal)
RUN apt-get update && apt-get install -y \
    g++ \
    gcc \
    default-jdk \
    nodejs \
    fpc \
    && rm -rf /var/lib/apt/lists/*

# Copy file requirements.txt vào Docker
COPY requirements.txt .

# Cài đặt các thư viện Python
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn dự án vào Docker
COPY . .

# Lệnh khởi chạy ứng dụng
CMD ["python", "-m", "backend.app"]
