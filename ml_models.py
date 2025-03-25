import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import logging

from models import Laptop
from app import db, app


class LaptopRecommender:

    def __init__(self):
        self.decision_tree = None
        self.random_forest = None
        self.kmeans = None
        self.scaler = StandardScaler()
        self.laptop_features = None
        self.laptop_ids = None

    def initialize_models(self):
        """Initialize and train all ML models"""
        logging.info("Initializing ML models...")

        # Check if models are already initialized
        if self.laptop_features is not None:
            return

        # Get all laptops from the database using app context
        with app.app_context():
            laptops = Laptop.query.all()

            if not laptops:
                logging.warning(
                    "No laptops found in database. Models not initialized.")
                return

        # Create a DataFrame from the laptop data
        laptop_data = []
        for laptop in laptops:
            laptop_data.append({
                'id':
                laptop.id,
                'price':
                laptop.price,
                'ram':
                laptop.ram,
                'storage_capacity':
                laptop.storage_capacity,
                'display_size':
                laptop.display_size,
                'refresh_rate':
                laptop.display_refresh_rate or 60,
                'battery_life':
                laptop.battery_life or 0,
                'cinebench_score':
                laptop.cinebench_score or 0,
                'geekbench_score':
                laptop.geekbench_score or 0,
                'gaming_fps':
                laptop.gaming_fps or 0,
                'user_rating':
                laptop.user_rating or 3.0,
                'for_gaming':
                1 if laptop.suitable_for_gaming else 0,
                'for_business':
                1 if laptop.suitable_for_business else 0,
                'for_students':
                1 if laptop.suitable_for_students else 0,
                'for_content_creation':
                1 if laptop.suitable_for_content_creation else 0,
                'is_ssd':
                1 if laptop.storage_type == 'SSD' else 0,
                'weight':
                laptop.weight or 2.0,
                'price_performance_ratio':
                laptop.price_performance_ratio or 0.8
            })

        df = pd.DataFrame(laptop_data)
        self.laptop_ids = df['id'].values

        # Create feature matrix for content-based filtering
        features = [
            'price', 'ram', 'storage_capacity', 'display_size', 'refresh_rate',
            'battery_life', 'cinebench_score', 'geekbench_score', 'gaming_fps',
            'user_rating', 'for_gaming', 'for_business', 'for_students',
            'for_content_creation', 'is_ssd', 'weight',
            'price_performance_ratio'
        ]

        # Store scaled features for content-based filtering
        X = df[features].values
        self.laptop_features = self.scaler.fit_transform(X)

        # Create labels for use case classification
        y_gaming = df['for_gaming'].values
        y_business = df['for_business'].values
        y_student = df['for_students'].values
        y_content = df['for_content_creation'].values

        # Create labels for price category (budget, mid-range, high-end)
        df['price_category'] = pd.qcut(df['price'], q=3, labels=[0, 1, 2])
        y_price = df['price_category'].values

        # Train Decision Tree for use case classification
        self.decision_tree = DecisionTreeClassifier(max_depth=5,
                                                    random_state=42)
        use_case_features = [
            'price', 'ram', 'gaming_fps', 'battery_life', 'cinebench_score'
        ]
        self.decision_tree.fit(df[use_case_features],
                               y_gaming)  # Just for gaming as example

        # Train Random Forest for more complex recommendation
        self.random_forest = RandomForestClassifier(n_estimators=100,
                                                    random_state=42)
        self.random_forest.fit(self.laptop_features, y_price)

        # Train K-Means for laptop clustering by price-performance
        kmeans_features = [
            'price', 'cinebench_score', 'geekbench_score', 'gaming_fps',
            'price_performance_ratio'
        ]
        kmeans_scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=3, random_state=42)
        self.kmeans.fit(kmeans_scaler.fit_transform(df[kmeans_features]))

        logging.info("ML models successfully initialized!")

    def recommend_laptops(self, user_preferences, limit=3):
        """Recommend laptops based on user preferences, prioritizing brand preference properly."""

        if self.laptop_features is None:
            self.initialize_models()
            if self.laptop_features is None:
                return []

        with app.app_context():
            laptops = Laptop.query.all()
            if not laptops:
                return []

            # Extract user preferences
            brand_prefs = user_preferences.get('brand_pref', [])  # User preferred brands
            budget_max = user_preferences.get('budget_max', 5000)

            # Apply brand preference filtering FIRST
            if brand_prefs:
                laptops = [laptop for laptop in laptops if laptop.brand in brand_prefs]

            # If brand filtering removed all options, revert to all laptops
            if not laptops:
                laptops = Laptop.query.all()

            # Create user preference vector
            user_vector = self._create_user_vector(user_preferences)
            user_vector_scaled = self.scaler.transform([user_vector])

            # Compute similarity scores
            similarity_scores = cosine_similarity(user_vector_scaled, self.laptop_features)[0]

            # Sort based on similarity
            sorted_indices = similarity_scores.argsort()[::-1]
            sorted_laptop_ids = [int(self.laptop_ids[i]) for i in sorted_indices]

            # Apply budget filtering
            filtered_laptops = [l for l in laptops if l.id in sorted_laptop_ids and l.price <= budget_max]

            # Return the top `limit` recommendations
            return [l.id for l in filtered_laptops[:limit]]


    def find_similar_laptops(self, laptop_id, limit=3):
        """
        Find laptops similar to the given laptop ID.

        Args:
            laptop_id: ID of the reference laptop
            limit: Maximum number of similar laptops to return

        Returns:
            List of similar laptop IDs
        """
        if self.laptop_features is None:
            self.initialize_models()
            if self.laptop_features is None:
                logging.warning("Failed to initialize models")
                return []

        try:
            ref_idx = np.where(self.laptop_ids == laptop_id)[0][0]
        except (IndexError, TypeError):
            logging.warning(f"Laptop ID {laptop_id} not found in model data")
            return []

        ref_features = self.laptop_features[ref_idx].reshape(1, -1)
        similarity_scores = cosine_similarity(ref_features,
                                              self.laptop_features)[0]

        if len(similarity_scores) > 0:
            top_indices = similarity_scores.argsort()[-(limit + 1):][::-1]
            top_indices = [
                idx for idx in top_indices if self.laptop_ids[idx] != laptop_id
            ]
            similar_laptop_ids = [
                int(self.laptop_ids[i]) for i in top_indices[:limit]
            ]
        else:
            logging.warning(
                "No similarity scores calculated for similar laptop finding")
            return []

        return similar_laptop_ids

    def get_value_recommendations(self, budget, use_case, limit=3):
        """
        Get best value for money recommendations within a budget.

        Args:
            budget: Maximum price
            use_case: Primary use case (gaming, business, student, content_creation)
            limit: Maximum number of recommendations

        Returns:
            List of recommended laptop IDs
        """
        with app.app_context():
            laptops = Laptop.query.filter(Laptop.price <= budget).all()

            if not laptops:
                logging.warning(f"No laptops found within budget {budget}")
                return []

            laptop_scores = []
            for laptop in laptops:
                score = laptop.price_performance_ratio or 0.5
                if use_case == 'gaming' and laptop.suitable_for_gaming:
                    score += 0.2
                elif use_case == 'business' and laptop.suitable_for_business:
                    score += 0.2
                elif use_case == 'student' and laptop.suitable_for_students:
                    score += 0.2
                elif use_case == 'content_creation' and laptop.suitable_for_content_creation:
                    score += 0.2

                laptop_scores.append((laptop.id, score))

            laptop_scores.sort(key=lambda x: x[1], reverse=True)
            top_laptop_ids = [
                laptop_id for laptop_id, _ in laptop_scores[:limit]
            ]

            return top_laptop_ids


# Create global instance of the recommender
laptop_recommender = LaptopRecommender()
