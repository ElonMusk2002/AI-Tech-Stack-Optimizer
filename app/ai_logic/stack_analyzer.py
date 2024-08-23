# stack_analyzer.py

from sqlalchemy import func
from app.models import TechStack


def analyze_stack(tech_stack_list):
    analysis = {}

    for tech in tech_stack_list:
        tech = tech.strip()
        db_tech = TechStack.query.filter(
            func.lower(TechStack.name) == func.lower(tech)
        ).first()
        if db_tech:
            analysis[tech] = {
                "category": db_tech.category,
                "popularity": db_tech.popularity,
                "description": db_tech.description,
            }
        else:
            analysis[tech] = {
                "category": "Unknown",
                "popularity": 0,
                "description": "Technology not found in our database",
            }

    return analysis
