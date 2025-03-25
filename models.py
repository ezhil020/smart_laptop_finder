from app import db
from datetime import datetime

# Laptop model
class Laptop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(500), nullable=False)  # Increased length for longer model names
    price = db.Column(db.Float, nullable=False)
    product_url = db.Column(db.String(1000), nullable=True)  # URL to the product page
    
    # Basic specifications
    cpu = db.Column(db.String(200), nullable=False)  # Increased length for CPU descriptions
    gpu = db.Column(db.String(200), nullable=True)   # Increased length for GPU descriptions
    ram = db.Column(db.Integer, nullable=False)  # In GB
    storage_type = db.Column(db.String(50), nullable=False)  # SSD, HDD, Hybrid
    storage_capacity = db.Column(db.Integer, nullable=False)  # In GB
    
    # Display
    display_size = db.Column(db.Float, nullable=False)  # In inches
    display_resolution = db.Column(db.String(50), nullable=False)  # e.g., 1920x1080
    display_refresh_rate = db.Column(db.Integer, nullable=True)  # In Hz
    
    # Other specifications
    weight = db.Column(db.Float, nullable=True)  # In kg
    battery_life = db.Column(db.Float, nullable=True)  # In hours
    operating_system = db.Column(db.String(100), nullable=True)
    
    # Performance benchmarks
    cinebench_score = db.Column(db.Integer, nullable=True)
    geekbench_score = db.Column(db.Integer, nullable=True)
    gaming_fps = db.Column(db.Float, nullable=True)  # Average FPS in common games
    
    # User ratings and categorization
    user_rating = db.Column(db.Float, nullable=True)  # 1-5 scale
    build_quality = db.Column(db.String(100), nullable=True)  # Poor, Average, Good, Excellent
    value_category = db.Column(db.String(50), nullable=True)  # Budget, Mid-Range, High-End
    
    # Use cases
    suitable_for_gaming = db.Column(db.Boolean, default=False)
    suitable_for_business = db.Column(db.Boolean, default=False)
    suitable_for_students = db.Column(db.Boolean, default=False)
    suitable_for_content_creation = db.Column(db.Boolean, default=False)
    
    # Calculated metrics
    price_performance_ratio = db.Column(db.Float, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Laptop {self.brand} {self.model}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'brand': self.brand,
        'model': self.model,
        'price': self.price,
        'cpu': self.cpu,
        'gpu': self.gpu,
        'ram': self.ram,
        'storage_type': self.storage_type,
        'storage_capacity': self.storage_capacity,
        'display_size': self.display_size,
        'display_resolution': self.display_resolution,
        'display_refresh_rate': self.display_refresh_rate,
        'weight': self.weight,
        'battery_life': self.battery_life,
        'cinebench_score': self.cinebench_score,
        'geekbench_score': self.geekbench_score,
        'gaming_fps': self.gaming_fps,
        'user_rating': self.user_rating,
        'build_quality': self.build_quality,
        'price_performance_ratio': self.price_performance_ratio
    }

# UserPreference model to store questionnaire responses
class UserPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(50), nullable=False)
    
    # Budget preference
    budget_min = db.Column(db.Float, nullable=True)
    budget_max = db.Column(db.Float, nullable=True)
    
    # Use case preferences
    use_case_gaming = db.Column(db.Boolean, default=False)
    use_case_business = db.Column(db.Boolean, default=False)
    use_case_student = db.Column(db.Boolean, default=False)
    use_case_content_creation = db.Column(db.Boolean, default=False)
    
    # Performance priorities (scale 1-5)
    priority_cpu_performance = db.Column(db.Integer, nullable=True)
    priority_gpu_performance = db.Column(db.Integer, nullable=True)
    priority_ram = db.Column(db.Integer, nullable=True)
    priority_storage = db.Column(db.Integer, nullable=True)
    
    # Other preferences
    preferred_display_size = db.Column(db.String(20), nullable=True)  # Small, Medium, Large
    preferred_weight = db.Column(db.String(20), nullable=True)  # Light, Medium, Heavy
    battery_life_importance = db.Column(db.Integer, nullable=True)  # 1-5 scale
    build_quality_importance = db.Column(db.Integer, nullable=True)  # 1-5 scale
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<UserPreference {self.id} for session {self.session_id}>"

# Favorite model to store user's saved laptops
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(50), nullable=False)
    laptop_id = db.Column(db.Integer, db.ForeignKey('laptop.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Define relationship
    laptop = db.relationship('Laptop', backref=db.backref('favorites', lazy=True))
    
    def __repr__(self):
        return f"<Favorite {self.id} for laptop {self.laptop_id}>"
