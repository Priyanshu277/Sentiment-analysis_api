# Django Sentiment Analysis API

This project is a Django-based API for sentiment analysis using the Groq API.

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the project root and add your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

## 📝 Note

This project uses environment variables for sensitive information. Make sure to keep your `.env` file private and never commit it to the repository.

## 🚀 Quick Start

1. Set up the project following the steps above
2. Make your first API request to `http://localhost:8000/api/analyze_sentiment/` (adjust if your endpoint is different)
3. Enjoy sentiment analysis powered by Groq!

## 🤝 Support

If you encounter any problems or have suggestions, please open an issue on the GitHub repository.


---

**Happy coding! 🎉**
