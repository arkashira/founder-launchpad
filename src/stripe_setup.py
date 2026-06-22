import json
from dataclasses import dataclass
from enum import Enum
from typing import Dict

class PricingPlan(str, Enum):
    FREE = "free"
    TIERED = "tiered"
    USAGE = "usage"

@dataclass
class StripeConfig:
    api_key: str
    pricing_plan: PricingPlan

class StripeSetup:
    def __init__(self, config: StripeConfig):
        self.config = config

    def generate_backend(self) -> Dict:
        backend = {
            "stripe_api_key": self.config.api_key,
            "pricing_plan": self.config.pricing_plan,
            "webhook_handling": True,
            "subscription_crud_endpoints": True
        }
        return backend

    def generate_checkout_page(self) -> str:
        return f"Checkout page for {self.config.pricing_plan} plan"

    def toggle_production_mode(self, production: bool) -> bool:
        return production

def setup_stripe(api_key: str, pricing_plan: PricingPlan) -> StripeSetup:
    if not isinstance(pricing_plan, PricingPlan):
        raise ValueError("Invalid pricing plan")
    config = StripeConfig(api_key, pricing_plan)
    return StripeSetup(config)
