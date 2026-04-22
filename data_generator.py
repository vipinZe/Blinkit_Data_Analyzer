import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_blinkit_data(num_records=5000):
    """
    Generate synthetic Blinkit data for analysis
    """
    np.random.seed(42)
    random.seed(42)
    
    # Product categories and their details
    categories = {
        'Groceries': {'products': ['Rice', 'Wheat', 'Pulses', 'Cooking Oil', 'Salt', 'Sugar'], 'price_range': (50, 500)},
        'Snacks': {'products': ['Chips', 'Biscuits', 'Chocolates', 'Noodles', 'Cookies'], 'price_range': (10, 200)},
        'Beverages': {'products': ['Soft Drinks', 'Juice', 'Tea', 'Coffee', 'Energy Drinks'], 'price_range': (20, 300)},
        'Dairy': {'products': ['Milk', 'Curd', 'Cheese', 'Butter', 'Paneer'], 'price_range': (25, 400)},
        'Personal Care': {'products': ['Shampoo', 'Soap', 'Toothpaste', 'Deodorant', 'Face Cream'], 'price_range': (30, 600)},
        'Fruits & Vegetables': {'products': ['Apples', 'Bananas', 'Tomatoes', 'Potatoes', 'Onions'], 'price_range': (20, 150)}
    }
    
    # Cities and their delivery time characteristics
    cities = {
        'Delhi': {'avg_delivery_time': 25, 'peak_hours': [18, 19, 20]},
        'Mumbai': {'avg_delivery_time': 30, 'peak_hours': [19, 20, 21]},
        'Bangalore': {'avg_delivery_time': 28, 'peak_hours': [18, 19, 20]},
        'Chennai': {'avg_delivery_time': 32, 'peak_hours': [19, 20, 21]},
        'Kolkata': {'avg_delivery_time': 35, 'peak_hours': [18, 19, 20]}
    }
    
    data = []
    start_date = datetime(2024, 1, 1)
    
    for i in range(num_records):
        # Random date within 2024
        days_offset = random.randint(0, 364)
        order_date = start_date + timedelta(days=days_offset)
        
        # Random time
        hour = random.randint(8, 23)  # 8 AM to 11 PM
        minute = random.randint(0, 59)
        order_time = order_date.replace(hour=hour, minute=minute)
        
        # Select random category and product
        category = random.choice(list(categories.keys()))
        product = random.choice(categories[category]['products'])
        
        # Select random city
        city = random.choice(list(cities.keys()))
        
        # Generate order details
        quantity = random.randint(1, 5)
        base_price = random.randint(*categories[category]['price_range'])
        total_amount = quantity * base_price
        
        # Delivery time based on city and time of day
        base_delivery_time = cities[city]['avg_delivery_time']
        if hour in cities[city]['peak_hours']:
            delivery_time = base_delivery_time + random.randint(5, 15)
        else:
            delivery_time = base_delivery_time + random.randint(-5, 5)
        delivery_time = max(10, delivery_time)  # Minimum 10 minutes
        
        # Rating (slightly biased towards higher ratings)
        rating = random.choices([1, 2, 3, 4, 5], weights=[0.02, 0.03, 0.15, 0.3, 0.5])[0]
        
        # Discount (some orders have discounts)
        has_discount = random.random() < 0.3
        discount_percent = random.randint(5, 25) if has_discount else 0
        discount_amount = (total_amount * discount_percent) / 100
        final_amount = total_amount - discount_amount
        
        # Order type
        order_type = random.choices(['Instant', 'Scheduled'], weights=[0.8, 0.2])[0]
        
        data.append({
            'order_id': f'BLK{10000 + i}',
            'order_date': order_date.date(),
            'order_time': order_time.time(),
            'order_datetime': order_time,
            'category': category,
            'product': product,
            'quantity': quantity,
            'unit_price': base_price,
            'total_amount': total_amount,
            'discount_percent': discount_percent,
            'discount_amount': discount_amount,
            'final_amount': final_amount,
            'city': city,
            'delivery_time_minutes': delivery_time,
            'customer_rating': rating,
            'order_type': order_type,
            'day_of_week': order_time.strftime('%A'),
            'is_weekend': order_time.weekday() >= 5,
            'month': order_time.strftime('%B')
        })
    
    return pd.DataFrame(data)

def save_sample_data():
    """
    Generate and save sample data to CSV
    """
    df = generate_blinkit_data(5000)
    df.to_csv('blinkit_data.csv', index=False)
    print("Sample data generated and saved as 'blinkit_data.csv'")
    print(f"Dataset shape: {df.shape}")
    print("\nFirst few records:")
    print(df.head())
    
    return df

if __name__ == "__main__":
    df = save_sample_data()