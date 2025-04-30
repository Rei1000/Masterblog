

# Masterblog – A Simple Flask Blog

This is a learning project built with Python and the Flask web framework.  
It’s a simple blog application with basic CRUD functionality.

## 🔧 Features

- View all posts (homepage)
- Add new posts
- Edit existing posts
- Delete posts
- Data stored in a JSON file
- Clean, responsive styling with CSS
- No database required

## 🛠️ Installation & Running

### Requirements

- Python 3.x
- Flask (see `requirements.txt`)

### Run Locally

```bash
git clone https://github.com/Rei1000/Masterblog.git
cd Masterblog
pip install -r requirements.txt
python app.py
```

Then open in your browser:  
[http://localhost:5000](http://localhost:5000)

## 📁 Project Structure

```
Masterblog/
│
├── app.py              # Main Flask app
├── posts.json          # Data storage
├── requirements.txt    # Dependencies
├── static/
│   └── style.css       # Styling
├── templates/
│   ├── index.html      # Homepage
│   ├── add.html        # Form: Add post
│   └── update.html     # Form: Edit post
```

## 🧠 Purpose

This project is designed to help you learn Flask fundamentals:
- Routing
- Template rendering with Jinja2
- Form handling
- JSON file processing
- Error handling with `try/except`

## 📌 Note

This project deliberately avoids JavaScript, databases, or user authentication  
— it is meant to be as simple and educational as possible.

---
**Have fun exploring Flask!**