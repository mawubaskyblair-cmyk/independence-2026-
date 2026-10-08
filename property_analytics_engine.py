import json
import logging
import math
from datetime import datetime
from typing import Dict, List, Optional, Union

# Configure logging for tracking operations
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

class StructuralSpecs:
    """Defines physical build and structural metrics for construction estimation."""
    def __init__(self, total_sqm: float, floors: int, bedrooms: int, bathrooms: int, has_pool: bool = False):
        if total_sqm <= 0:
            raise ValueError("Total square meters must be greater than 0.")
        self.total_sqm = total_sqm
        self.floors = floors
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.has_pool = has_pool

    def calculate_concrete_requirement(self) -> float:
        """Estimates structural concrete volume needed in cubic meters."""
        base_slab = self.total_sqm * 0.25  # 25cm slab thickness
        pillar_volume = (self.floors * 12) * 0.4  # Approx 12 pillars per floor
        pool_volume = 45.0 if self.has_pool else 0.0
        return round(base_slab + pillar_volume + pool_volume, 2)

class ValuationEngine:
    """Calculates property market estimation based on location and build costs."""
    def __init__(self, base_cost_per_sqm: float, location_factor: float):
        self.base_cost_per_sqm = base_cost_per_sqm
        self.location_factor = location_factor

    def compute_valuation(self, specs: StructuralSpecs) -> Dict[str, float]:
        base_build_cost = specs.total_sqm * self.base_cost_per_sqm
        pool_cost = 35000.0 if specs.has_pool else 0.0
        total_construction_cost = base_build_cost + pool_cost
        
        estimated_market_value = total_construction_cost * self.location_factor
        estimated_profit_margin = estimated_market_value - total_construction_cost

        return {
            "construction_cost": round(total_construction_cost, 2),
            "market_valuation": round(estimated_market_value, 2),
            "estimated_profit": round(estimated_profit_margin, 2)
        }

class ContentGenerator:
    """Automates social media video scripts and listing headlines for content creators."""
    def __init__(self, property_title: str):
        self.property_title = property_title

    def generate_social_caption(self, specs: StructuralSpecs, valuation: Dict[str, float]) -> str:
        caption = (
            f"🏡 JUST BUILT: {self.property_title}!\n\n"
            f"✨ Features:\n"
            f"• {specs.total_sqm} SqM Luxury Living Space\n"
            f"• {specs.bedrooms} Beds | {specs.bathrooms} Baths\n"
            f"• {specs.floors} Modern Floors\n"
            f"{'• Custom Concrete Infinity Pool included! 🏊' if specs.has_pool else ''}\n\n"
            f"💰 Estimated Value: ${valuation['market_valuation']:,.2f}\n"
            f"#RealEstate #Architecture #ConstructionUpdate #LuxuryHomes"
        )
        return caption

    def generate_video_voiceover_script(self, specs: StructuralSpecs) -> List[Dict[str, str]]:
        return [
            {"scene": 1, "duration": "0-3s", "script": f"Welcome to the walkthrough of {self.property_title}."},
            {"scene": 2, "duration": "3-7s", "script": f"Spanning over {specs.total_sqm} square meters, built with reinforced structural framing."},
            {"scene": 3, "duration": "7-12s", "script": f"Featuring {specs.bedrooms} bedrooms and premium architectural finishing throughout."},
            {"scene": 4, "duration": "12-15s", "script": "Comment below if you would live here!"}
        ]

class PropertyPipelineManager:
    """Coordinates calculation, media creation, and report export."""
    def __init__(self, title: str, base_sqm_cost: float, location_multiplier: float):
        self.title = title
        self.valuation_engine = ValuationEngine(base_sqm_cost, location_multiplier)
        self.content_gen = ContentGenerator(title)

    def process_property(self, specs: StructuralSpecs) -> str:
        logging.info(f"Processing property analysis for: {self.title}")
        valuation = self.valuation_engine.compute_valuation(specs)
        concrete_needed = specs.calculate_concrete_requirement()
        caption = self.content_gen.generate_social_caption(specs, valuation)
        script = self.content_gen.generate_video_voiceover_script(specs)

        report = {
            "property_name": self.title,
            "timestamp": datetime.utcnow().isoformat(),
            "structural_metrics": {
                "total_area_sqm": specs.total_sqm,
                "floors": specs.floors,
                "concrete_cubic_meters": concrete_needed
            },
            "financials": valuation,
            "creator_assets": {
                "social_caption": caption,
                "voiceover_script": script
            }
        }
        return json.dumps(report, indent=4)

if __name__ == "__main__":
    try:
        house_specs = StructuralSpecs(total_sqm=450.0, floors=2, bedrooms=5, bathrooms=4, has_pool=True)
        manager = PropertyPipelineManager("Skyline Luxury Villa", base_sqm_cost=1100.0, location_multiplier=1.45)
        json_output = manager.process_property(house_specs)
        print(json_output)
    except Exception as e:
        logging.error(f"Error executing pipeline: {e}")