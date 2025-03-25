from flask import render_template, request, redirect, url_for, session, jsonify, flash
import uuid
from sqlalchemy import or_
import logging

from app import app, db
from models import Laptop, UserPreference, Favorite
from ml_models import laptop_recommender

@app.route('/')
def index():
    """Home page route"""
    # Ensure user has a session
    if 'user_session_id' not in session:
        session['user_session_id'] = str(uuid.uuid4())
    
    with app.app_context():
        # Get some featured laptops for the home page
        laptops = Laptop.query.order_by(Laptop.user_rating.desc()).limit(6).all()
        
        # Get categories for filtering
        categories = {
            'gaming': Laptop.query.filter_by(suitable_for_gaming=True).count(),
            'business': Laptop.query.filter_by(suitable_for_business=True).count(),
            'student': Laptop.query.filter_by(suitable_for_students=True).count(),
            'content_creation': Laptop.query.filter_by(suitable_for_content_creation=True).count()
        }
    
    return render_template('index.html', laptops=laptops, categories=categories)

@app.route('/search')
def search():
    """Search laptops based on query"""
    query = request.args.get('q', '')
    
    if not query:
        return redirect(url_for('index'))
    
    with app.app_context():
        # Search laptops by brand or model
        laptops = Laptop.query.filter(
            or_(
                Laptop.brand.ilike(f'%{query}%'),
                Laptop.model.ilike(f'%{query}%')
            )
        ).all()
    
    return render_template('index.html', laptops=laptops, search_query=query)

@app.route('/questionnaire')
def questionnaire():
    """Display the questionnaire page"""
    return render_template('questionnaire.html')

@app.route('/submit_questionnaire', methods=['POST'])
def submit_questionnaire():
    """Process the questionnaire submission and generate recommendations"""
    # Ensure user has a session
    if 'user_session_id' not in session:
        session['user_session_id'] = str(uuid.uuid4())
    
    session_id = session['user_session_id']
    
    # Extract user preferences from form
    use_case = request.form.get('use_case')
    budget_min = float(request.form.get('budget_min', 0))
    budget_max = float(request.form.get('budget_max', 5000))
    
    # Extract other preferences
    priority_performance = int(request.form.get('priority_performance', 3))
    priority_battery = int(request.form.get('priority_battery', 3))
    priority_display = int(request.form.get('priority_display', 3))
    priority_portability = int(request.form.get('priority_portability', 3))
    
    with app.app_context():
        # Create user preference object
        user_pref = UserPreference(
            session_id=session_id,
            budget_min=budget_min,
            budget_max=budget_max,
            use_case_gaming=(use_case == 'gaming'),
            use_case_business=(use_case == 'business'),
            use_case_student=(use_case == 'student'),
            use_case_content_creation=(use_case == 'content_creation'),
            priority_cpu_performance=priority_performance,
            priority_gpu_performance=priority_performance if use_case == 'gaming' or use_case == 'content_creation' else 2,
            preferred_display_size='Large' if priority_display >= 4 else 'Medium',
            battery_life_importance=priority_battery,
            build_quality_importance=int(request.form.get('build_quality', 3))
        )
        
        # Save user preferences
        db.session.add(user_pref)
        db.session.commit()
        
        # Create a user preferences dictionary for the ML model
        user_prefs_dict = {
            'use_case': use_case,
            'budget_min': budget_min,
            'budget_max': budget_max,
            'performance_priority': priority_performance,
            'battery_priority': priority_battery,
            'display_priority': priority_display,
            'portability_priority': priority_portability
        }
        
        # Get recommendations from ML model
        recommended_ids = laptop_recommender.recommend_laptops(user_prefs_dict, limit=3)
        
        # Redirect to results page
        return redirect(url_for('results', pref_id=user_pref.id))

@app.route('/results/<int:pref_id>')
def results(pref_id):
    """Display the recommendation results"""
    with app.app_context():
        # Get the user preference
        user_pref = UserPreference.query.get_or_404(pref_id)
        
        # Create user preferences dictionary for the ML model
        user_prefs_dict = {
            'use_case': 'gaming' if user_pref.use_case_gaming else 
                      'business' if user_pref.use_case_business else
                      'student' if user_pref.use_case_student else
                      'content_creation' if user_pref.use_case_content_creation else 'general',
            'budget_min': user_pref.budget_min,
            'budget_max': user_pref.budget_max,
            'performance_priority': user_pref.priority_cpu_performance,
            'battery_priority': user_pref.battery_life_importance
        }
        
        # Get recommendations
        recommended_ids = laptop_recommender.recommend_laptops(user_prefs_dict, limit=3)
        
        recommended_laptops = Laptop.query.filter(Laptop.id.in_(recommended_ids)).all() if recommended_ids else []
        
        # If we don't have enough recommendations, get some based on best value
        if len(recommended_laptops) < 3:
            use_case = user_prefs_dict['use_case']
            value_ids = laptop_recommender.get_value_recommendations(
                budget=user_pref.budget_max,
                use_case=use_case,
                limit=3-len(recommended_laptops)
            )
            if value_ids:
                value_laptops = Laptop.query.filter(
                    Laptop.id.in_(value_ids),
                    ~Laptop.id.in_(recommended_ids) if recommended_ids else True  # Exclude already recommended laptops
                ).all()
                recommended_laptops.extend(value_laptops)
        
        # Get alternative suggestions
        alternatives = []
        if recommended_laptops:
            similar_ids = laptop_recommender.find_similar_laptops(recommended_laptops[0].id, limit=2)
            alternatives = Laptop.query.filter(Laptop.id.in_(similar_ids)).all() if similar_ids else []
    
    return render_template(
        'results.html',
        recommendations=recommended_laptops,
        alternatives=alternatives,
        preferences=user_pref
    )

@app.route('/laptop/<int:laptop_id>')
def laptop_detail(laptop_id):
    """Display details of a specific laptop"""
    with app.app_context():
        laptop = Laptop.query.get_or_404(laptop_id)
        
        # Get similar laptops
        similar_ids = laptop_recommender.find_similar_laptops(laptop_id, limit=3)
        similar_laptops = Laptop.query.filter(Laptop.id.in_(similar_ids)).all() if similar_ids else []
        
        # Check if laptop is in user's favorites
        is_favorite = False
        if 'user_session_id' in session:
            is_favorite = Favorite.query.filter_by(
                session_id=session['user_session_id'],
                laptop_id=laptop_id
            ).first() is not None
    
    # Extract features to JSON-safe data for the JavaScript to use
    laptop_features = {
        'id': laptop.id,
        'brand': laptop.brand,
        'model': laptop.model,
        'price': laptop.price,
        'cpu': laptop.cpu,
        'gpu': laptop.gpu if laptop.gpu else 'Integrated Graphics',
        'ram': laptop.ram,
        'storage': f"{laptop.storage_capacity} GB {laptop.storage_type}",
        'display': f"{laptop.display_size}\" {laptop.display_resolution}",
        'weight': laptop.weight,
        'battery': laptop.battery_life,
        'rating': laptop.user_rating if laptop.user_rating else 4.0,
        'cinebench': laptop.cinebench_score if laptop.cinebench_score else 0,
        'geekbench': laptop.geekbench_score if laptop.geekbench_score else 0,
        'gaming_fps': laptop.gaming_fps if laptop.gaming_fps else 0,
        'product_url': laptop.product_url
    }
    
    return render_template(
        'laptop_detail.html',
        laptop=laptop,
        laptop_json=laptop.to_dict(),
        similar_laptops=[l.to_dict() for l in similar_laptops] if similar_laptops else [],
        is_favorite=is_favorite
    )

@app.route('/laptop/redirect/<int:laptop_id>')
def laptop_redirect(laptop_id):
    """Redirect to external product page for a laptop"""
    with app.app_context():
        laptop = Laptop.query.get_or_404(laptop_id)
        
        if laptop.product_url and laptop.product_url.strip():
            return redirect(laptop.product_url)
        else:
            flash('No product link available for this laptop', 'warning')
            return redirect(url_for('laptop_detail', laptop_id=laptop_id))

@app.route('/comparison')
def comparison():
    """Display laptop comparison page"""
    # Get laptop IDs from query string
    laptop_ids = request.args.getlist('laptop_id', type=int)
    
    # If no laptops specified, redirect to home
    if not laptop_ids:
        return redirect(url_for('index'))
    
    with app.app_context():
        # Get the laptops
        laptops = Laptop.query.filter(Laptop.id.in_(laptop_ids)).all() if laptop_ids else []
    
    # Get specs to compare
    specs = [
        {'name': 'Price', 'key': 'price', 'unit': '₹', 'is_higher_better': False},
        {'name': 'CPU', 'key': 'cpu', 'unit': '', 'is_higher_better': True},
        {'name': 'GPU', 'key': 'gpu', 'unit': '', 'is_higher_better': True},
        {'name': 'RAM', 'key': 'ram', 'unit': 'GB', 'is_higher_better': True},
        {'name': 'Storage', 'key': 'storage_capacity', 'unit': 'GB', 'is_higher_better': True},
        {'name': 'Storage Type', 'key': 'storage_type', 'unit': '', 'is_higher_better': True},
        {'name': 'Display Size', 'key': 'display_size', 'unit': '"', 'is_higher_better': True},
        {'name': 'Resolution', 'key': 'display_resolution', 'unit': '', 'is_higher_better': True},
        {'name': 'Refresh Rate', 'key': 'display_refresh_rate', 'unit': 'Hz', 'is_higher_better': True},
        {'name': 'Battery Life', 'key': 'battery_life', 'unit': 'hours', 'is_higher_better': True},
        {'name': 'Weight', 'key': 'weight', 'unit': 'kg', 'is_higher_better': False},
        {'name': 'Cinebench Score', 'key': 'cinebench_score', 'unit': '', 'is_higher_better': True},
        {'name': 'Geekbench Score', 'key': 'geekbench_score', 'unit': '', 'is_higher_better': True},
        {'name': 'Gaming FPS', 'key': 'gaming_fps', 'unit': 'FPS', 'is_higher_better': True},
        {'name': 'User Rating', 'key': 'user_rating', 'unit': '/5', 'is_higher_better': True}
    ]
    
    laptop_dicts = [laptop.to_dict() for laptop in laptops]
    return render_template('comparison.html', laptops=laptop_dicts, specs=specs)

@app.route('/add_to_favorites/<int:laptop_id>', methods=['POST'])
def add_to_favorites(laptop_id):
    """Add a laptop to user's favorites"""
    # Ensure user has a session
    if 'user_session_id' not in session:
        session['user_session_id'] = str(uuid.uuid4())
    
    session_id = session['user_session_id']
    
    try:
        with app.app_context():
            # Check if laptop exists
            laptop = Laptop.query.get_or_404(laptop_id)
            
            # Check if already in favorites
            existing = Favorite.query.filter_by(
                session_id=session_id,
                laptop_id=laptop_id
            ).first()
            
            if not existing:
                # Add to favorites
                favorite = Favorite(session_id=session_id, laptop_id=laptop_id)
                db.session.add(favorite)
                db.session.commit()
                flash('Laptop added to favorites!', 'success')
            else:
                flash('Laptop already in favorites!', 'info')
    except Exception as e:
        db.session.rollback()
        flash('Error adding to favorites!', 'error')
        logging.error(f"Error adding favorite: {str(e)}")
    
    # Redirect back to laptop detail page
    return redirect(url_for('laptop_detail', laptop_id=laptop_id))

@app.route('/remove_from_favorites/<int:laptop_id>', methods=['POST'])
def remove_from_favorites(laptop_id):
    """Remove a laptop from user's favorites"""
    if 'user_session_id' not in session:
        return redirect(url_for('laptop_detail', laptop_id=laptop_id))
    
    session_id = session['user_session_id']
    
    with app.app_context():
        # Find and delete the favorite
        favorite = Favorite.query.filter_by(
            session_id=session_id,
            laptop_id=laptop_id
        ).first()
        
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            flash('Laptop removed from favorites!', 'success')
    
    # Redirect back to laptop detail page
    return redirect(url_for('laptop_detail', laptop_id=laptop_id))

@app.route('/favorites')
def favorites():
    """Display user's favorite laptops"""
    if 'user_session_id' not in session:
        session['user_session_id'] = str(uuid.uuid4())
        return render_template('favorites.html', favorites=[])
    
    session_id = session['user_session_id']
    
    with app.app_context():
        # Get user's favorites
        favorites = Favorite.query.filter_by(session_id=session_id).all()
        
        # Get the corresponding laptops
        laptop_ids = [fav.laptop_id for fav in favorites]
        laptops = Laptop.query.filter(Laptop.id.in_(laptop_ids)).all() if laptop_ids else []
    
    return render_template('favorites.html', favorites=laptops)

@app.route('/api/laptop/<int:laptop_id>')
def api_laptop_detail(laptop_id):
    """API endpoint to get laptop details"""
    with app.app_context():
        laptop = Laptop.query.get_or_404(laptop_id)
        
        # Convert laptop to dictionary
        laptop_dict = {
            'id': laptop.id,
            'brand': laptop.brand,
            'model': laptop.model,
            'price': laptop.price,
            'product_url': laptop.product_url,
            'cpu': laptop.cpu,
            'gpu': laptop.gpu,
            'ram': laptop.ram,
            'storage_type': laptop.storage_type,
            'storage_capacity': laptop.storage_capacity,
            'display_size': laptop.display_size,
            'display_resolution': laptop.display_resolution,
            'display_refresh_rate': laptop.display_refresh_rate,
            'weight': laptop.weight,
            'battery_life': laptop.battery_life,
            'operating_system': laptop.operating_system,
            'cinebench_score': laptop.cinebench_score,
            'geekbench_score': laptop.geekbench_score,
            'gaming_fps': laptop.gaming_fps,
            'user_rating': laptop.user_rating,
            'build_quality': laptop.build_quality,
            'value_category': laptop.value_category,
            'price_performance_ratio': laptop.price_performance_ratio
        }
    
    return jsonify(laptop_dict)
