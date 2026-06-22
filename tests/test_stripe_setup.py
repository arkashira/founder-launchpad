from src.stripe_setup import setup_stripe, PricingPlan, StripeSetup
import pytest

def test_setup_stripe():
    api_key = "test_api_key"
    pricing_plan = PricingPlan.FREE
    stripe_setup = setup_stripe(api_key, pricing_plan)
    assert isinstance(stripe_setup, StripeSetup)

def test_generate_backend():
    api_key = "test_api_key"
    pricing_plan = PricingPlan.FREE
    stripe_setup = setup_stripe(api_key, pricing_plan)
    backend = stripe_setup.generate_backend()
    assert backend["stripe_api_key"] == api_key
    assert backend["pricing_plan"] == pricing_plan

def test_generate_checkout_page():
    api_key = "test_api_key"
    pricing_plan = PricingPlan.FREE
    stripe_setup = setup_stripe(api_key, pricing_plan)
    checkout_page = stripe_setup.generate_checkout_page()
    assert checkout_page == f"Checkout page for {pricing_plan} plan"

def test_toggle_production_mode():
    api_key = "test_api_key"
    pricing_plan = PricingPlan.FREE
    stripe_setup = setup_stripe(api_key, pricing_plan)
    production_mode = stripe_setup.toggle_production_mode(True)
    assert production_mode

def test_invalid_pricing_plan():
    api_key = "test_api_key"
    pricing_plan = "invalid_plan"
    with pytest.raises(ValueError):
        setup_stripe(api_key, pricing_plan)
