# SMTP Bulk Email Sender (Dockerized)

A lightweight **Python + Flask** web app to send a fixed email message to multiple recipients using **SMTP**, with configurable delay/throttling between sends.

This project was built as a hands-on DevOps + deployment exercise and is **containerized with Docker** . It was also deployed on an **AWS EC2 instance** and exposed on **port 5000**.

---

## Features

- Web UI to paste multiple recipient emails (comma or newline separated)
- Sends a fixed message to all valid recipients
- Configurable delay between emails (default: **10 seconds**)
- SMTP-based sending (Gmail SMTP supported)
- Environment-based configuration (`.env`)
- Dockerized for easy deployment
- Basic authentication support for UI access (recommended)

---

## Tech Stack

- **Backend:** Python, Flask
- **Email:** SMTP (`smtplib`, `email.message`)
- **Config:** `python-dotenv`
- **Containerization:** Docker, Docker Compose
- **Deployment:** AWS EC2 (Port 5000)

---

## Project Structure

```bash
.
├── app.py                  # Flask app + UI routes
├── send_mail_update.py     # Bulk SMTP sender logic
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container image build
├── .env                    # Environment variables (NOT committed)
└── README.md
