"""Rule-based crop suggestions from the crop knowledge table.

This is an educational matcher. It is not a validated agronomic prediction.
"""

from app.data.crops import CROPS
from app.data.library import DISCLAIMER

REGIONS = {
    "punjab": "Punjab commonly grows wheat in rabi and rice in kharif where irrigation is available.",
    "kerala": "Kerala is typically humid and tropical, so rice, banana, and spices are common.",
    "andhra": "Andhra Pradesh grows rice, groundnut, cotton, chilli, and turmeric in different zones.",
    "telangana": "Telangana commonly grows cotton, rice, and maize depending on irrigation.",
    "tamil": "Tamil Nadu has both irrigated rice systems and dryland groundnut areas.",
    "maharashtra": "Maharashtra has major cotton, sugarcane, and sorghum areas.",
    "gujarat": "Gujarat is an important groundnut and cotton region, much of it semi-arid.",
    "karnataka": "Karnataka includes dryland groundnut and cotton as well as humid plantation areas.",
}


def _norm(value: str) -> str:
    return " ".join(value.lower().replace("-", " ").split())


def recommend(soil_type: str, season: str, water: str, location: str, climate: str) -> dict:
    soil = _norm(soil_type)
    season_value = _norm(season)
    water_value = _norm(water)
    climate_value = _norm(climate)
    note = None
    for key, text in REGIONS.items():
        if key in _norm(location):
            note = text
            break
    suggestions = []
    for crop in CROPS:
        score = 0
        reasons = []
        if any(item in soil or soil in item for item in crop["soils"]):
            score += 2
            reasons.append(f"soil matches {crop['soil_type']}")
        if season_value in crop["seasons"] or any(item in season_value for item in crop["seasons"]):
            score += 2
            reasons.append(f"season matches {crop['season']}")
        if water_value == crop["water_need"] or water_value in crop["water_need"]:
            score += 2
            reasons.append(f"water need is {crop['water_need']}")
        if climate_value and any(item in climate_value for item in crop["climates"]):
            score += 1
            reasons.append(f"climate is broadly compatible with {crop['climate']}")
        if score < 3:
            continue
        suggestions.append(
            {
                "crop_name": crop["crop_name"],
                "score": score,
                "explanation": "Matched because " + "; ".join(reasons) + ".",
                "guidance": crop["organic_fertilizers"],
            }
        )
    suggestions.sort(key=lambda item: item["score"], reverse=True)
    return {
        "disclaimer": DISCLAIMER + " Scores only reflect how many of your stated conditions match this crop table.",
        "location_note": note,
        "suggestions": suggestions[:4],
    }
