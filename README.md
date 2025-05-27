## Project Structure

```
ERP_PROJECT/
├── .vscode/
├── .env                            # NEW: Gemini API key configuration
├── ERP/
│   ├── __pycache__/
│   ├── app/
│   │   ├── __pycache__/
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── cart_service.py
│   │   │   ├── gemini_chatbot_service.py
│   │   │   ├── context_analyzer.py
│   │   │   ├── advanced_recommender.py
│   │   │   └── product_service.py 
│   │   ├── static/
│   │   │   ├── css/
│   │   │   │   └── style.css
│   │   │   ├── images/
│   │   │   │   ├── about/
│   │   │   │   ├── products/
│   │   │   │   └── hero-bg.jpg
│   │   │   └── js/
│   │   │       └── main.js
│   │   └── templates/
│   │       ├── about.html
│   │       ├── base.html
│   │       ├── cart.html
│   │       ├── combos.html
│   │       ├── index.html
│   │       └── products.html
│   └── ...
├── venv/
├── Gift_Store_Data.xlsx
├── README.md
├── requirements.txt
└── run.py

```
python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python run.py