# 🎁 Gift Shop ERP - AI-Powered Gift Recommendation Platform

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> A modern, AI-powered e-commerce platform that helps customers find the perfect gifts through intelligent conversation and personalized recommendations.

## 🌟 Key Features

<table>
<tr>
<td width="50%">

### 🤖 **AI-Powered Gift Advisor**
- Gemini AI integration for natural conversations
- Context-aware recommendations
- Multi-turn conversation memory
- Personalized shopping assistance

### 🎯 **Smart Recommendation Engine**
- Analyzes age groups, occasions, and relationships
- Budget-conscious suggestions
- Interest-based product matching
- Diverse recommendation algorithms

</td>
<td width="50%">

### 🛒 **E-Commerce Features**  
- Dynamic product catalog with Excel import
- Real-time shopping cart management
- Gift combo packages with auto-pricing
- Mobile-responsive design

### 📊 **Admin Features**
- Excel-based product management
- Real-time system health monitoring
- Conversation analytics
- Easy product image management

</td>
</tr>
</table>

## 🚀 Quick Start

### 📋 Prerequisites

- Python 3.8+
- [Google Gemini API Key](https://makersuite.google.com/app/apikey) (Free)
- Git

### ⚡ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/gift-shop-erp.git
   cd gift-shop-erp
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Create .env file
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

5. **Launch the application**
   ```bash
   python run.py
   ```

6. **Open in browser**
   ```
   http://localhost:5000
   ```

## 🏗️ Project Architecture

```
gift-shop-erp/
├── 📁 app/
│   ├── 🔧 services/           # Business Logic Layer
│   │   ├── 🤖 gemini_chatbot_service.py    # AI Chatbot Engine
│   │   ├── 🎯 advanced_recommender.py     # Smart Recommendations
│   │   ├── 🧠 context_analyzer.py         # Conversation Analysis
│   │   ├── 🛒 cart_service.py             # Shopping Cart Logic
│   │   └── 📦 product_service.py          # Product Management
│   ├── 🎨 static/
│   │   ├── 🎨 css/style.css               # Enhanced Responsive Styles
│   │   ├── 🖼️ images/                      # Product & UI Images
│   │   └── ⚡ js/main.js                  # Frontend Interactions
│   └── 📄 templates/                      # Jinja2 Templates
├── 📊 Gift_Store_Data.xlsx               # Product Data Source
├── ⚙️ run.py                             # Application Entry Point
└── 📋 requirements.txt                   # Dependencies
```

## 🧠 AI & Machine Learning Features

### 🤖 Gemini AI Integration
Our chatbot leverages Google's Gemini AI for:

- **Natural Language Understanding**: Processes complex gift requests
- **Context Preservation**: Remembers conversation history
- **Personalized Responses**: Adapts to user preferences
- **Multi-language Support**: Handles diverse customer queries

### 🎯 Advanced Recommendation Algorithm

<details>
<summary><b>🔍 Click to see our recommendation factors</b></summary>

| Factor | Description | Weight |
|--------|-------------|--------|
| **Age Groups** | Toddler, Child, Teen, Adult | High |
| **Occasions** | Birthday, Christmas, Wedding, etc. | High |
| **Relationships** | Friend, Family, Partner, etc. | Medium |
| **Interests** | Art, Sports, Technology, etc. | Medium |
| **Budget** | Low (<$20), Medium ($20-$50), High (>$50) | High |
| **Sentiment** | Positive/Negative preferences | Low |

</details>

## 🛠️ Technology Stack

<div align="center">

| Category | Technologies |
|----------|-------------|
| **Backend** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white) |
| **AI/ML** | ![Google](https://img.shields.io/badge/Gemini_AI-4285F4?style=flat&logo=google&logoColor=white) |
| **Frontend** | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) |
| **Data** | ![Excel](https://img.shields.io/badge/Microsoft_Excel-217346?style=flat&logo=microsoft-excel&logoColor=white) |

</div>

## 📚 API Documentation

### 🛒 Shopping Cart Endpoints

```http
POST /api/cart/add
Content-Type: application/json

{
  "id": 1,
  "type": "product",
  "quantity": 1
}
```

### 🤖 Chatbot Endpoints

```http
POST /api/chatbot
Content-Type: application/json

{
  "query": "I need a gift for my 8-year-old daughter who loves art"
}
```

### 📊 System Health

```http
GET /api/health
```

<details>
<summary><b>📖 View complete API documentation</b></summary>

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/cart/add` | POST | Add item to shopping cart |
| `/api/cart/update` | POST | Update item quantity |
| `/api/cart/remove` | POST | Remove item from cart |
| `/api/chatbot` | POST | Send message to AI chatbot |
| `/api/chatbot/reset` | POST | Reset conversation context |
| `/api/health` | GET | System status and metrics |

</details>

## 🔧 Configuration

### 🌍 Environment Variables

```bash
# Required
GEMINI_API_KEY=your_gemini_api_key

# Optional
FLASK_ENV=development
SECRET_KEY=your_secret_key
DEBUG=True
```

### 📊 Excel Data Format

Your `Gift_Store_Data.xlsx` should have a sheet named **"Structured Data "** with:

| Column | Field | Example |
|--------|-------|---------|
| E | Product Name | "Art Supply Kit" |
| F | Category | "Arts & Crafts" |
| G | Price | 24.99 |

## 🚨 Troubleshooting

<details>
<summary><b>🤖 Chatbot Issues</b></summary>

**Problem**: Chatbot not responding
```bash
# Check API key
echo $GEMINI_API_KEY

# Verify service status
curl http://localhost:5000/api/health
```

**Problem**: Rate limit errors
- Wait 2-5 minutes between requests during development
- Consider upgrading to paid Gemini API tier

</details>

<details>
<summary><b>📦 Product Loading Issues</b></summary>

**Problem**: Products not displaying
```bash
# Check Excel file exists
ls -la Gift_Store_Data.xlsx

# Verify column mapping
# Ensure columns E, F, G contain: Name, Category, Price
```

</details>

<details>
<summary><b>🖼️ Image Display Issues</b></summary>

**Problem**: Product images not showing
```bash
# Check image directory
ls -la app/static/images/products/

# Images should follow naming convention:
# "Product Name" → "product_name.jpg"
```

</details>

### 📋 Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/gift-shop-erp.git

# Create development branch
git checkout -b develop

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```
