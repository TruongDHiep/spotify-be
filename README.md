# 🎵 Website Nghe Nhạc Trực Tuyến

## 📌 Giới thiệu

Dự án **"Website nghe nhạc trực tuyến"** được xây dựng với mục tiêu cung cấp một nền tảng giúp người dùng có thể truy cập, tìm kiếm và nghe nhạc mọi lúc, mọi nơi thông qua kết nối Internet.

### 🎯 Phạm vi dự án

- Hướng đến những người yêu thích âm nhạc, sử dụng nhạc vào mục đích giải trí hoặc tạo động lực trong công việc.
- Giao diện người dùng thân thiện, dễ sử dụng trên trình duyệt web.
- Cho phép người dùng:
  - Đăng ký, đăng nhập và quản lý tài khoản cá nhân.
  - Quản lý danh sách phát (playlist) và bài hát yêu thích.
  - Nghe nhạc trực tuyến từ cơ sở dữ liệu.
  - Tìm kiếm bài hát, nghệ sĩ và album.
- Hỗ trợ quản trị viên:
  - Quản lý nội dung nhạc và thông tin liên quan.
- Có thêm chatbox đơn giản để tương tác.

---

## 🛠️ Công nghệ sử dụng

| Thành phần   | Công nghệ               |
|--------------|--------------------------|
| Frontend     | React.js (Vite)          |
| Backend      | Python Django            |
| Cơ sở dữ liệu| PostgreSQL               |
| Container    | Docker, Docker Compose   |
| Triển khai   | Vercel (Frontend), AWS (Backend tùy chọn) |

---

## 📂 Cấu trúc dự án

### 🌐 Frontend (`/`)

```

.
├── public/
├── src/                  # Mã nguồn React (components, pages, v.v.)
├── index.html
├── package.json
├── vite.config.js
├── eslint.config.js
├── vercel.json
├── exit                 # Giao diện chatbox đơn giản
└── README.md

```

### ⚙️ Backend (`/server`)

```

server/
├── \[thư mục Django apps...]
├── views.py             # Xử lý logic backend
├── requirements.txt     # Danh sách thư viện Python
├── dockerfile           # Cấu hình Docker
├── docker-compose.yaml  # Cấu hình chạy nhiều service
└── .gitignore

````

---

## 🚀 Triển khai

### ▶️ 1. Truy cập trực tuyến

Frontend đã được triển khai tại:  
🔗 [https://spotify-tau-plum.vercel.app/](https://spotify-tau-plum.vercel.app/)

> Backend có thể chạy tại máy cục bộ hoặc triển khai riêng (AWS, Render, v.v.)

---

### 🐳 2. Chạy dự án bằng Docker

> Yêu cầu cài sẵn: [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

```bash
# Clone repository
git clone https://github.com/<ten-tai-khoan>/<ten-du-an>.git
cd <ten-du-an>

# Chạy toàn bộ hệ thống
docker-compose up --build
````

* Frontend chạy tại: `http://localhost:3000`
* Backend chạy tại: `http://localhost:8000`

---

## 🧪 Kiểm thử

* Đăng ký/Đăng nhập
* Thêm bài hát vào playlist
* Nghe nhạc trực tuyến
* Tìm kiếm bài hát, nghệ sĩ
* Quản lý bài hát qua trang quản trị

---

## 👨‍💻 Thành viên thực hiện

Dự án được thực hiện bởi nhóm sinh viên Trường Đại học Sài Gòn:

* **Lê Tấn Tài** – 3121410431
* **Trương Đại Hiệp** – 3121410431
* **Phạm Trung Hiếu** – 3121410431
* **Tô Minh Triết** – 3121410431
* **Phan Chí Bảo** – 3121410431
