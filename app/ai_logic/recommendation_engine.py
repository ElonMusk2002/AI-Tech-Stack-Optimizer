# recommendation_engine.py

from flask import current_app
import json
import google.generativeai as genai
from app import db
from app.models import Recommendation, TechStack


def get_recommendations(analysis):
    genai.configure(api_key=current_app.config["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")

    recommendations = {}
    overall_opinion = {}

    for tech, details in analysis.items():
        prompt = f"""
        Analyze the following technology: {tech}
        Category: {details.get('category', 'N/A')} 
        Popularity: {details.get('popularity', 'N/A')} 
        Description: {details.get('description', 'N/A')}

        Provide 3 alternative technologies that might be better suited for a project using {tech}.
        For each alternative, give a reason why it might be better and a score from 0 to 1.
        Format the response as a JSON object with the following structure:
        {{
            "alternatives": [
                {{
                    "name": "Alternative1",
                    "reason": "Reason for recommending Alternative1",
                    "score": 0.9 
                }},
                // ... more alternatives
            ]
        }}
        """

        try:
            response = model.generate_content(prompt)
            result = response.text

            json_start = result.find("{")
            json_end = result.rfind("}") + 1
            if json_start != -1 and json_end != -1:
                json_str = result[json_start:json_end]
                result_json = json.loads(json_str)
            else:
                raise ValueError("No valid JSON object found in the response")

            recommendations[tech] = result_json["alternatives"]
            tech_stack = TechStack.query.filter_by(name=tech).first()
            if not tech_stack:
                tech_stack = TechStack(
                    name=tech,
                    category=details.get("category"),
                    popularity=details.get("popularity"),
                    description=details.get("description"),
                )
                db.session.add(tech_stack)
                db.session.flush()

            for alt in result_json["alternatives"]:
                recommendation = Recommendation(
                    tech_stack_id=tech_stack.id,
                    recommendation=f"Consider using {alt['name']} instead of {tech}",
                    reason=alt["reason"],
                    score=alt["score"],
                )
                db.session.add(recommendation)

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error processing recommendations for {tech}: {e}")
            print(f"Received response: {result}")
            recommendations[tech] = []
        except Exception as e:
            print(f"Unexpected error processing recommendations: {e}")
            recommendations[tech] = []

    tech_stack_str = ", ".join(analysis.keys())
    overall_prompt = f"""
    Analyze the following technology stack: {tech_stack_str}

    Provide an overall opinion about this stack, including its strengths and weaknesses.
    Format the response as a JSON object with the following structure:
    {{
        "opinion": "Overall opinion about the stack",
        "strengths": ["Strength 1", "Strength 2", "Strength 3"],
        "weaknesses": ["Weakness 1", "Weakness 2", "Weakness 3"]
    }}
    """

    try:
        response = model.generate_content(overall_prompt)
        result = response.text

        json_start = result.find("{")
        json_end = result.rfind("}") + 1
        if json_start != -1 and json_end != -1:
            json_str = result[json_start:json_end]
            overall_opinion = json.loads(json_str)
        else:
            raise ValueError("No valid JSON object found in the response")

    except Exception as e:
        print(f"Error processing overall opinion: {e}")
        overall_opinion = {
            "opinion": "Unable to generate overall opinion",
            "strengths": [],
            "weaknesses": [],
        }
    db.session.commit()

    return recommendations, overall_opinion
