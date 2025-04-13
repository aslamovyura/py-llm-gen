import os
import random
import sys
import asyncio
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Add the project root to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))))
sys.path.append(project_root)

# Load environment variables from the root directory
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path, override=True)

from src.infrastructure.database.models import User, Client, Equipment, Request, Offer
from src.infrastructure.database.config import Base

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Project root: {project_root}")
print(f"Env file path: {dotenv_path}")
print(f"Attempting to connect to database with URL: {DATABASE_URL}")

engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Initialize Faker
fake = Faker()

def create_fake_user():
    username = fake.user_name()[:20]  # Limit username to 20 characters
    email = fake.email()[:50]  # Limit email to 50 characters
    full_name = fake.name()[:50]  # Limit full name to 50 characters
    hashed_password = fake.password()[:72]  # Limit password to 72 characters (bcrypt max)
    phone_number = fake.phone_number()[:20]  # Limit phone number to 20 characters
    
    return User(
        username=username,
        email=email,
        full_name=full_name,
        hashed_password=hashed_password,
        role=random.choice(["admin", "manager", "user"]),
        phone_number=phone_number
    )

def create_fake_client():
    return Client(
        name=fake.company(),
        email=fake.company_email(),
        phone_number=fake.phone_number(),
        address=fake.address(),
        company_name=fake.company(),
        contact_person=fake.name(),
        notes=fake.text(max_nb_chars=200),
        tags={"industry": fake.word(), "size": random.choice(["small", "medium", "large"])}
    )

def create_fake_equipment():
    categories = ["medical", "industrial", "laboratory", "office", "safety"]
    statuses = ["available", "in_use", "maintenance", "reserved"]
    manufacturers = ["Siemens", "GE Healthcare", "Philips", "Roche", "Thermo Fisher"]
    
    purchase_date = fake.date_between(start_date="-5y", end_date="today")
    warranty_end_date = purchase_date + timedelta(days=random.randint(365, 1095))
    
    return Equipment(
        name=fake.word(),
        model=fake.bothify(text="MOD-###"),
        serial_number=fake.bothify(text="SN-########"),
        manufacturer=random.choice(manufacturers),
        category=random.choice(categories),
        status=random.choice(statuses),
        purchase_date=purchase_date,
        warranty_end_date=warranty_end_date,
        location=fake.city(),
        specifications={
            "power": f"{random.randint(100, 1000)}W",
            "weight": f"{random.randint(10, 100)}kg",
            "dimensions": f"{random.randint(50, 200)}x{random.randint(50, 200)}x{random.randint(50, 200)}mm"
        },
        tags={"type": fake.word(), "condition": random.choice(["new", "used", "refurbished"])}
    )

def create_fake_request(client_id):
    priorities = ["low", "medium", "high", "urgent"]
    statuses = ["pending", "in_progress", "completed", "cancelled"]
    currencies = ["USD", "EUR", "GBP"]
    
    return Request(
        title=fake.sentence(nb_words=6),
        description=fake.text(max_nb_chars=500),
        client_id=client_id,
        equipment_category=random.choice(["medical", "industrial", "laboratory", "office", "safety"]),
        required_specifications={
            "power": f"{random.randint(100, 1000)}W",
            "weight": f"max {random.randint(10, 100)}kg"
        },
        quantity=random.randint(1, 10),
        priority=random.choice(priorities),
        status=random.choice(statuses),
        budget_min=random.uniform(1000, 5000),
        budget_max=random.uniform(5000, 20000),
        currency=random.choice(currencies),
        desired_delivery_date=fake.date_between(start_date="+30d", end_date="+180d"),
        notes=fake.text(max_nb_chars=200),
        tags={"urgency": random.choice(["normal", "urgent"]), "type": fake.word()}
    )

def create_fake_offer(request_id, equipment_id):
    statuses = ["pending", "accepted", "rejected", "expired"]
    currencies = ["USD", "EUR", "GBP"]
    payment_terms = ["immediate", "30_days", "60_days", "custom"]
    
    return Offer(
        request_id=request_id,
        equipment_id=equipment_id,
        price=random.uniform(1000, 20000),
        currency=random.choice(currencies),
        quantity=random.randint(1, 10),
        delivery_date=fake.date_between(start_date="+30d", end_date="+180d"),
        warranty_period_months=random.randint(12, 36),
        status=random.choice(statuses),
        terms_and_conditions=fake.text(max_nb_chars=500),
        notes=fake.text(max_nb_chars=200),
        additional_services={
            "installation": random.choice([True, False]),
            "training": random.choice([True, False]),
            "maintenance": random.choice([True, False])
        },
        discount_percentage=random.uniform(0, 20),
        payment_terms=random.choice(payment_terms),
        custom_payment_terms=fake.text(max_nb_chars=100) if random.choice([True, False]) else None
    )

async def populate_database():
    async with async_session() as session:
        try:
            # Create users
            users = [create_fake_user() for _ in range(10)]
            session.add_all(users)
            await session.commit()
            
            # Create clients
            clients = [create_fake_client() for _ in range(20)]
            session.add_all(clients)
            await session.commit()
            
            # Create equipment
            equipment = [create_fake_equipment() for _ in range(30)]
            session.add_all(equipment)
            await session.commit()
            
            # Create requests
            requests = []
            for client in clients:
                for _ in range(random.randint(1, 3)):
                    requests.append(create_fake_request(client.id))
            session.add_all(requests)
            await session.commit()
            
            # Create offers
            offers = []
            for request in requests:
                for _ in range(random.randint(1, 3)):
                    equipment_id = random.choice(equipment).id
                    offers.append(create_fake_offer(request.id, equipment_id))
            session.add_all(offers)
            await session.commit()
            
            print("Database populated successfully!")
            
        except Exception as e:
            await session.rollback()
            print(f"Error populating database: {str(e)}")

if __name__ == "__main__":
    asyncio.run(populate_database()) 