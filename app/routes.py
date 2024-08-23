# routes.py

from flask import Blueprint, render_template, request, jsonify, current_app
from app.forms import TechStackForm
from app.ai_logic.stack_analyzer import analyze_stack
from app.ai_logic.recommendation_engine import get_recommendations
from app.models import TechStack

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
def index():
    form = TechStackForm()
    technologies = TechStack.query.all()
    form.tech_stack.choices = [(tech.name, tech.name) for tech in technologies]
    return render_template("index.html", form=form, technologies=technologies)


@main.route("/api/analyze", methods=["POST"])
def api_analyze():
    data = request.json
    tech_stack = data.get("tech_stack")
    if not tech_stack:
        return jsonify({"error": "No technologies selected"}), 400

    analysis = analyze_stack(tech_stack)
    try:
        recommendations, overall_opinion = get_recommendations(analysis)
        return jsonify(
            {
                "analysis": analysis,
                "recommendations": recommendations,
                "overall_opinion": overall_opinion,
            }
        )
    except Exception as e:
        current_app.logger.error(f"Error generating recommendations: {e}")
        return (
            jsonify({"error": "An error occurred while generating recommendations"}),
            500,
        )
