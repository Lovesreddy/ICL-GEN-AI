"""Educational organic fertilizer quantities. These are configurable guidance rates."""

from app.data.crops import CROPS
from app.data.library import DISCLAIMER

# Quantities are common teaching rates per acre, not universal prescriptions.
RATES = {
    "vermicompost": {"per_acre": 2000, "unit": "kg", "note": "Use with a basal compost dressing. Nurseries need much less."},
    "farmyard_manure": {"per_acre": 4000, "unit": "kg", "note": "Apply only well-decomposed manure before sowing."},
    "green_manure": {"per_acre": 20, "unit": "kg of seed", "note": "This is a seed rate for raising the green-manure crop, not a manure weight."},
    "jeevamrutham": {"per_acre": 200, "unit": "litres", "note": "A traditional soil-drench volume. It supplements organic matter; it does not replace it."},
    "panchagavya": {"per_acre": 12, "unit": "litres of concentrate before dilution", "note": "Dilute to about 3 percent before spraying, and confirm the recipe with your trainer."},
    "neem_cake": {"per_acre": 200, "unit": "kg", "note": "Mix into soil. Do not leave a thick band against germinating seed."},
    "compost": {"per_acre": 3000, "unit": "kg", "note": "Spread and incorporate during land preparation."},
    "biofertilizers": {"per_acre": 8, "unit": "kg or the packet dose on the label", "note": "Prefer the packet label. This figure is only a planning placeholder for carrier-based products."},
}

CROP_FACTORS = {
    "rice": 1.0,
    "wheat": 0.9,
    "tomato": 0.8,
    "chilli": 0.8,
    "cotton": 1.0,
    "groundnut": 0.7,
    "banana": 1.4,
    "mango": 1.1,
    "turmeric": 1.0,
    "sugarcane": 1.5,
}

ALIASES = {
    "farmyard manure": "farmyard_manure",
    "fym": "farmyard_manure",
    "green manure": "green_manure",
    "neem cake": "neem_cake",
    "vermi compost": "vermicompost",
    "biofertilizer": "biofertilizers",
}


def calculate(crop: str, land_area: float, area_unit: str, fertilizer_type: str) -> dict:
    key = fertilizer_type.strip().lower().replace("-", " ")
    key = ALIASES.get(key, key.replace(" ", "_"))
    if key not in RATES:
        known = ", ".join(sorted(RATES))
        raise ValueError(f"Unknown fertilizer type. Choose one of: {known}.")
    crop_key = crop.strip().lower()
    if crop_key not in CROP_FACTORS and not any(item["crop_name"].lower() == crop_key for item in CROPS):
        raise ValueError("Choose a crop from the crop guide.")
    factor = CROP_FACTORS.get(crop_key, 1.0)
    acres = land_area * 2.47105 if area_unit == "hectare" else land_area
    hectares = acres / 2.47105
    rate = RATES[key]
    per_acre = round(rate["per_acre"] * factor, 2)
    quantity = round(per_acre * acres, 2)
    per_hectare = round(per_acre * 2.47105, 2)
    return {
        "crop": crop,
        "fertilizer_type": key.replace("_", " "),
        "land_area_acres": round(acres, 3),
        "land_area_hectares": round(hectares, 3),
        "quantity": quantity,
        "unit": rate["unit"],
        "per_acre": per_acre,
        "per_hectare": per_hectare,
        "guidance": rate["note"] + f" The crop factor for {crop} is {factor}.",
        "disclaimer": DISCLAIMER,
    }
