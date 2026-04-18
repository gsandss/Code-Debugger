# AI Code-Debugger
<img width="1496" height="745" alt="{B65FC298-85A4-4F4C-BAD1-E7E53858E467}" src="https://github.com/user-attachments/assets/e79dc242-dcd6-4a79-83a4-a66c9314457c" />

## 🧾Overview
This is a full-stack application combining web interface with a Python designed backend to help give users a clean, easy, understable solution to their coding issues.  

Users are able to:
- Write and Run Python Code
- View real-time outputs
- Recieve debugging fixes and explanations
- Ask questions about their issues

This application is hostest locally using LM Studio, which allows for privacy and offline capability

## ⚙️Technologies
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python, Flask
- **AI**: LM Studio

## 🛠️Installation & Setup

### 🚀Clone Repo
  ```bash
  git clone https://github.com/gsandss/Code-Debugger.git
  cd Code-Debugger
  ```
### ⚙️Install Backend Dependencies
  ```bash
  cd backend
  py -m pip install -r requirements.txt
  ```
### ▶️Run the Backend
  ```bash
  cd backend
  py app.py
  ```
### 🌐Run the Frontend
  ```bash
  cd frontend
  py -m http.server 5500
  ```
### 🌍Open The App
  ```text
  http://127.0.0.1:5500
  ```
### 🤖LM Studio Config
  ```python
  LM_STUDIO_API = "http://127.0.0.1:1234/v1/chat/completions"
  LM_MODEL = "your-model-name" // Replace With Your Models Name
  ```
## 👨‍💻Author
**Gavin Sands**  
Iowa State University  
Computer Science | Minors in Applied AI & Artificial Intelligence
