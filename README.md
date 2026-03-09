# 🔗 Link Analytics Shortener

A simple **URL Shortening and Click Analytics Web Application** built using **Python and Streamlit**.

This application converts long URLs into unique short links and tracks the number of clicks each shortened link receives. It also provides a dashboard showing analytics for all generated links.

---

## 🚀 Features

* Accepts **long URLs** (Google, Amazon, YouTube, etc.)
* Generates a **unique shortened URL**
* **Redirects users** from the short link to the original URL
* Tracks **click count analytics**
* Displays a **dashboard of all links**
* **Persistent storage** using SQLite (data remains after refresh)
* **Input validation** for empty or invalid URLs

---

## 🧠 How It Works

1. User enters a long URL.
2. The system generates a **random short code**.
3. The short code is stored with the original URL in the database.
4. Opening the short link:

   * increments the click counter
   * redirects the user to the original URL.
5. The dashboard displays analytics for every generated link.

---

## 🏗 Tech Stack

* **Python**
* **Streamlit** (Web App Framework)
* **SQLite** (Persistent Database)
* **Pandas** (Dashboard display)

---

## 📂 Project Structure

```
link_analytics_shortener/
│
├── app.py                # Main Streamlit application
├── db.py                 # Database functions
├── utils.py              # URL validation and short code generation
├── requirements.txt      # Python dependencies
├── runtime.txt           # Python runtime for deployment
├── README.md             # Project documentation
│
├── data/
│   └── links.db          # SQLite database
│
└── .streamlit/
    └── config.toml       # Streamlit configuration
```

---

## 🔗 URL Shortening Format

Short URLs follow this format:

```
https://<deployed-app-url>.streamlit.app/?code=<short_code>
```

Example:

```
https://vibeathon-url-shortener.streamlit.app/?code=aB93Kx
```

Opening this link redirects the user to the stored original URL.

---

## 💾 Data Storage

All link data is stored using **SQLite**.

Each record stores:

* Original URL
* Short code
* Click count
* Creation timestamp

This ensures that analytics remain available even after refreshing the application.

---

## 🧪 Example URLs Supported

The system supports shortening links such as:

```
https://google.com
https://youtube.com/watch?v=abc123
https://amazon.in/s?k=headphones
https://github.com
https://wikipedia.org
```

---

## ⚙ Installation (Local Development)

Install dependencies:

```
pip install -r requirements.txt
```

Run the application:

```
streamlit run app.py
```

---

## 🌐 Deployment

This application is designed to be deployed using **Streamlit Community Cloud**.

Steps:

1. Push project to GitHub.
2. Create a new app on Streamlit Cloud.
3. Select:

   * repository
   * branch (`main`)
   * main file (`app.py`)
4. Deploy.

After deployment, the generated short URLs will use the **public Streamlit app link**.

---

## 🏆 VIBEATHON 2026

This project was developed as part of the **VIBEATHON Build & Ship competition**.

The goal was to create a **fully functional URL shortener with analytics under time constraints**.

---

## 📜 License

This project is intended for educational and demonstration purposes.
