#!/usr/bin/env python3

from app import app
from models import db, Plant

# Seed the database
with app.app_context():
    print("🧹 Clearing existing data...")
    Plant.query.delete()

    print("🌱 Creating new seed data...")
    aloe = Plant(
        name="Aloe",
        image="./images/aloe.jpg",
        price=11.50,
        is_in_stock=True,
    )

    zz_plant = Plant(
        name="ZZ Plant",
        image="./images/zz-plant.jpg",
        price=25.98,
        is_in_stock=False,
    )

    db.session.add_all([aloe, zz_plant])
    db.session.commit()
    print("✅ 🌱 Database successfully seeded!")
