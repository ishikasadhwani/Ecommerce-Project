# seed_products.py

from app.core.database import SessionLocal
from app.products.models import Product
from sqlalchemy.exc import IntegrityError

def seed_products():
    db = SessionLocal()

    sample_products = [
        Product(
            name="iPhone 15 Pro Max",
            category="Mobile",
            price=139999.0,
            description="Latest Apple flagship with A17 chip",
            stock=25,
            image_url="https://example.com/images/iphone15.jpg"
        ),
        Product(
            name="Samsung Galaxy S24",
            category="Mobile",
            price=99999.0,
            description="Samsung's top-tier Android phone",
            stock=40,
            image_url="https://example.com/images/s24.jpg"
        ),
        Product(
            name="Sony WH-1000XM5",
            category="Headphones",
            price=29999.0,
            description="Industry-leading noise-canceling headphones",
            stock=15,
            image_url="https://example.com/images/sony-headphones.jpg"
        ),
        Product(
            name="MacBook Air M3",
            category="Laptop",
            price=124999.0,
            description="Apple's lightweight laptop with M3 chip",
            stock=20,
            image_url="https://example.com/images/macbook-air.jpg"
        ),
    ]

    try:
        db.add_all(sample_products)
        db.commit()
        print("✅ Seed data inserted successfully.")
    except IntegrityError:
        db.rollback()
        print("⚠️  Duplicate data detected. Seeding skipped.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_products()
