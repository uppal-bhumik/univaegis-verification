# UnivAegis - AI Admissions Verification Engine

A full-stack AI application that automates the verification of student admission documents. It uses a **FastAPI** backend with **EasyOCR (GPU-accelerated)** to extract data from academic transcripts and financial statements, and a **React** frontend to validate eligibility in real-time.

## 🚀 Features

* **Automated OCR Extraction:** Instantly extracts Student Name, GPA/CGPA, and Bank Balance from PDFs and Images
* **Smart Eligibility Engine:** Auto-calculates eligibility based on University criteria (GPA ≥ 8.0 AND IELTS ≥ 8.0)
* **Dual-Mode Logic:** Intelligently distinguishes between GPA (scale of 10) and Percentage (scale of 100)
* **Confidence Scoring:** Provides an AI confidence metric to flag low-quality document scans
* **Interactive Dashboard:** Clean, responsive UI built with React & Vite

## 🛠️ Tech Stack

* **Backend:** Python, FastAPI, EasyOCR (PyTorch), PyMuPDF (fitz), Regex
* **Frontend:** React.js, Vite, Axios
* **Design:** CSS Modules (Responsive & Minimalist)

## ⚙️ Installation & Setup

### Prerequisites

* Python 3.10+
* Node.js & npm

### 1. Backend Setup (Python)

```bash
cd backend
pip install -r requirements.txt

# Run the server (Auto-downloads OCR models on first run)
python -m uvicorn app.main:app --reload
```

The Backend API will start at `http://127.0.0.1:8000`

### 2. Frontend Setup (React)

```bash
cd frontend
npm install

# Start the dashboard
npm run dev
```

The Frontend will start at `http://localhost:5173`

## 🧪 Usage Guide

1. Open the dashboard
2. Upload a transcript or bank statement (PDF/JPG/PNG)
3. Click "Scan Document" to trigger the OCR engine
4. Review the extracted data (Name, GPA, Balance)
5. Enter the candidate's IELTS Score manually
6. Click "Check Eligibility" to see the Pass/Fail verdict

## 📸 Project Demo

*(Paste your video link here after recording)*

---

**Submitted by:** Bhumik Uppal