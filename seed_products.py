from app.core.database import SessionLocal
from app.products.models import Product
from sqlalchemy.exc import IntegrityError
from app.products.models import Product
from app.auth.models import User

def seed_products():
    db = SessionLocal()

    admin = db.query(User).filter(User.role == "admin").first()
    if not admin:
        print("❌ No admin found. Please create an admin user before seeding products.")
        return

    sample_products = [
        Product(
            name="iPhone 15 Pro Max",
            category="Mobile",
            price=139999.0,
            stock=25,
            description="Latest Apple flagship with A17 chip",
            image_url="https://example.com/images/iphone15.jpg",
            created_by=admin.id  # ✅ associate with admin
        ),
        Product(
            name="MacBook Air M3",
            category="Laptop",
            price=124999.0,
            stock=20,
            description="Apple's lightweight laptop with M3 chip",
            image_url="https://example.com/images/macbook-air.jpg",
            created_by=admin.id
        ),
            Product(
            name="Samsung Galaxy S24",
            category="Mobile",
            price=99999.0,
            description="Samsung's top-tier Android phone",
            stock=40,
            image_url="https://example.com/images/s24.jpg",
            created_by=admin.id
        ),
        Product(
            name="Sony WH-1000XM5",
            category="Headphones",
            price=29999.0,
            description="Industry-leading noise-canceling headphones",
            stock=15,
            image_url="https://example.com/images/sony-headphones.jpg",
            created_by=admin.id
        ),
        # Add more products similarly...
    ]

    try:
        db.add_all(sample_products)
        db.commit()
        print("✅ Sample products seeded successfully.")
    except IntegrityError:
        db.rollback()
        print("⚠️  Duplicate entries or foreign key error.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_products()


# from app.core.database import SessionLocal
# from app.products.models import Product
# from app.auth.models import User
# from sqlalchemy.exc import IntegrityError

# def seed_products():
#     db = SessionLocal()

#     # ✅ Get an admin user (make sure at least one exists)
    