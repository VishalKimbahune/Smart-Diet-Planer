# 🥗 Smart Diet Planner

A full-stack web application that generates personalized, nutritionally-balanced daily meal plans using authentic Indian cuisine. The backend employs an enhanced knapsack optimization algorithm to select optimal food combinations tailored to the user's body metrics, activity level, and dietary preferences.

## ✨ Features

- **🔐 JWT Authentication** — Register and log in with email/password; secure API access
- **📊 Personalized Meal Plans** — Age, weight, height, gender, activity level, and calorie target drive the algorithm
- **🧠 Knapsack Optimization** — Selects up to 3 dishes per meal maximizing calories and protein within limits
- **🥦 Dietary Preference** — Vegetarian / Non-Vegetarian toggle filters the food pool
- **📈 Health Metrics** — Live BMI, BMR, and recommended daily calorie calculation
- **🍽️ Per-Meal Breakdown** — Breakfast (~25%), Lunch (~45%), Dinner (~30%) with calorie progress bars
- **🔬 Detailed Nutrition** — Per-item macros & micronutrients with expandable details
- **🎲 Daily Variety** — Random subsampling from large food pools for diverse plans

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python, FastAPI, Uvicorn |
| **Database** | MongoDB (via PyMongo) |
| **Auth** | JWT (python-jose), bcrypt (passlib) |
| **Data** | Pandas (1,015-item Indian food nutrition CSV) |
| **Frontend** | React 18, TypeScript, Vite |
| **HTTP Client** | Axios |
| **Routing** | React Router DOM v6 |

## 📁 Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point, CORS, routers
│   │   ├── db.py                # MongoDB connection
│   │   ├── schemas.py           # Pydantic request/response models
│   │   ├── security.py          # JWT creation, password hashing, auth dependency
│   │   ├── routes_auth.py       # POST /api/auth/register, /api/auth/login
│   │   ├── routes_meal.py       # POST /api/meal/generate
│   │   ├── meal_logic.py        # Knapsack meal plan generation algorithm
│   │   └── data_loader.py       # CSV loading & food categorization
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── api/                 # Axios client & API wrappers
│   │   ├── auth/                # React auth context
│   │   ├── components/          # Navbar
│   │   ├── pages/               # Home, Register, Login, Planner
│   │   ├── App.tsx              # Routes & routing
│   │   ├── main.tsx             # Entry point
│   │   └── styles.css           # Dark theme (2000+ lines)
│   ├── package.json
│   └── README.md
├── Indian_Food_Nutrition_Processed.csv
└── README.md                    # ← You are here
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- MongoDB (running on `localhost:27017` by default)

### Backend Setup

```powershell
cd backend
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MONGO_URL` | `mongodb://localhost:27017/` | MongoDB connection string |
| `VITE_API_BASE` | `http://127.0.0.1:8000` | API base URL (frontend) |

## 📡 API Reference

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/` | ❌ | Health check |
| `POST` | `/api/auth/register` | ❌ | Register `{ email, password }` |
| `POST` | `/api/auth/login` | ❌ | Login (form: `username`, `password`) → JWT token |
| `POST` | `/api/meal/generate` | ✅ Bearer | Generate meal plan |

### Generate Plan Request Body

```json
{
  "age": 25,
  "weight_kg": 70,
  "height_cm": 175,
  "gender": "male",
  "activity_level": "moderate",
  "calories_limit": 2200,
  "food_type": "veg"
}
```

### Generate Plan Response (truncated)

```json
{
  "breakfast": [
    { "name": "Vegetable Poha", "calories": 250, "protein_g": 5.2, "serving_size": "1 bowl" }
  ],
  "lunch": [
    { "name": "Dal Rice", "calories": 450, "protein_g": 14.0, "serving_size": "1 plate" }
  ],
  "dinner": [
    { "name": "Roti Sabzi", "calories": 380, "protein_g": 10.5, "serving_size": "2 rotis" }
  ],
  "total_calories": 2050,
  "total_nutrition": {
    "protein_g": 68.5,
    "carbohydrates_g": 280.0,
    "fats_g": 55.0
  },
  "meal_breakdown": {
    "breakfast": { "calories": 480, "target_calories": 500, "nutrition": { ... } },
    "lunch": { "calories": 920, "target_calories": 990, "nutrition": { ... } },
    "dinner": { "calories": 650, "target_calories": 660, "nutrition": { ... } }
  },
  "nutritional_analysis": {
    "protein_percentage": 18.5,
    "carb_percentage": 55.0,
    "fat_percentage": 26.5
  }
}
```

## ⚙️ How It Works

1. **BMR Calculation** — Mifflin-St Jeor equation based on gender, weight, height, and age
2. **Activity Multiplier** — Adjusts calorie target from 1.2× (sedentary) to 1.9× (very active)
3. **Calorie Distribution** — Breakfast 25%, Lunch 45%, Dinner 30%
4. **Protein Target** — 1.0 g/kg (male) / 0.9 g/kg (female) of body weight
5. **Knapsack DP** — For each meal, selects up to 3 dishes maximizing nutrition within the calorie budget
6. **Food Pool** — 1,015 Indian dishes categorized into breakfast/lunch/dinner; veg filter excludes meat keywords

## 📊 Dataset

The meal plans are built from **`Indian_Food_Nutrition_Processed.csv`** — 1,015 authentic Indian dishes with full nutritional profiles including calories, protein, carbs, fats, fiber, calcium, iron, vitamin C, sodium, sugar, and folate.

## 📄 License

[MIT](LICENSE)
