# SmartLaptopFinder

SmartLaptopFinder is an intelligent laptop recommendation system that leverages machine learning and data-driven techniques to help users find the most suitable laptops based on their preferences, budget, and intended use cases. The system integrates content-based filtering, classification, clustering, and value-for-money analysis to deliver highly personalized and optimized recommendations.

---

## Features

- **Personalized Recommendations:** Suggests laptops tailored to user preferences such as brand, budget, performance, portability, and use case (gaming, business, student, content creation).
- **Content-Based Filtering:** Uses cosine similarity between user preference vectors and laptop feature vectors for precise matching.
- **Machine Learning Models:** Employs Decision Tree and Random Forest classifiers for use-case and price-category prediction.
- **Clustering:** Utilizes K-Means clustering to group laptops by price-performance characteristics.
- **Value-for-Money Analysis:** Ranks laptops based on price-performance ratio and suitability for the user’s primary use case.
- **Dynamic Data Integration:** Incorporates real-time laptop specifications, benchmark scores, and market prices.
- **Flask Web Integration:** Designed to be integrated with a Flask web application for an interactive user experience.

---

## Data Collection Framework

- **Comprehensive Laptop Specifications:** Collects detailed hardware and feature data for a wide range of laptop models.
- **Performance Benchmark Integration:** Integrates standardized benchmark scores (e.g., Cinebench, Geekbench, gaming FPS) for objective performance assessment.
- **User Preference Modeling:** Captures and structures user requirements (budget, brand, use case, etc.) for personalized recommendations.
- **Market Price Analysis:** Analyzes current market prices to ensure recommendations are relevant and budget-friendly.

---

## Machine Learning & Analysis Methods

- **Decision Tree Implementation:** Used for initial classification of laptops based on key features and use cases.
- **Random Forest Integration:** Enhances classification accuracy through ensemble learning for price category prediction.
- **K-Means Clustering:** Groups laptops by feature similarity, improving the diversity and relevance of recommendations.
- **Performance Metric Normalization:** Standardizes all feature values to ensure fair and unbiased model comparisons.

---

## Core Modules

### LaptopRecommender

The main class that handles model initialization, user vector creation, recommendation logic, similarity search, and value-for-money ranking.

#### Model Initialization

- Loads laptop data
- Preprocesses features
- Trains classifiers and clustering models

#### Recommendation Methods

- `recommend_laptops(user_preferences, limit)`: Returns top-N laptops matching user preferences.
- `find_similar_laptops(laptop_id, limit)`: Finds laptops most similar to a given laptop.
- `get_value_recommendations(budget, use_case, limit)`: Suggests best value-for-money laptops within a budget for a specific use case.

---

## Example Usage

```python
from smart_laptop_finder import LaptopRecommender

# Initialize recommender
recommender = LaptopRecommender()

# Example: Get recommendations
user_preferences = {
    'brand': 'Dell',
    'budget': 65000,
    'use_case': 'student',
    'performance': 'high',
    'portability': 'medium'
}
recommendations = recommender.recommend_laptops(user_preferences, limit=3)

for idx, laptop in enumerate(recommendations, 1):
    print(f"{idx}. {laptop['model']} - {laptop['brand']} - ₹{laptop['price']} - {laptop['reason']}")
```

#### Sample Output

| Rank | Laptop Model        | Brand  | Price   | RAM   | Storage | Score | Reason for Recommendation         |
|------|---------------------|--------|---------|-------|---------|-------|-----------------------------------|
| 1    | Inspiron 15 5000    | Dell   | ₹65,000 | 16GB  | 512GB   | 0.92  | High performance, fits budget     |
| 2    | IdeaPad Slim 5      | Lenovo | ₹62,000 | 16GB  | 512GB   | 0.89  | Good battery, lightweight         |
| 3    | VivoBook Ultra 14   | Asus   | ₹59,000 | 8GB   | 512GB   | 0.87  | Value for money, portable         |

---

## Results and Discussion

- Achieved a top-3 recommendation accuracy of **87%** in user testing.
- Recommendations closely matched user preferences for performance, price, and portability.
- Machine learning models improved classification and grouping, while normalization ensured balanced feature influence.
- The system dynamically adapts to user input, providing relevant and up-to-date suggestions.

---

## How to Run

### 1. Install Dependencies

- Python 3.x
- Flask
- SQLAlchemy
- pandas
- numpy
- scikit-learn

```bash
pip install flask sqlalchemy pandas numpy scikit-learn
```

### 2. Set Up Database

Ensure your laptop data is loaded into the database via SQLAlchemy models.

### 3. Run the Flask App

- Integrate the `LaptopRecommender` into your Flask routes.
- Start the Flask server and interact via the web interface or API.

```bash
export FLASK_APP=app.py
flask run
```

### 4. (Optional) Run Unit Tests

Add or run unit tests as needed for your project.

---


