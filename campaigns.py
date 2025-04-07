"""
Mock campaigns: fake API.
"""

def create_campaign(campaign_id, name, level_min=1, level_max=float('inf'), countries=[], 
                   required_items=[], excluded_items=[], enabled=True):

    if countries is None:
        countries = ["US", "RO", "CA"]
    
    if required_items is None:
        required_items = ["item_1"]
        
    if excluded_items is None:
        excluded_items = ["item_4"]
    
    return {
        "id": campaign_id,
        "game": "mygame",
        "name": name,
        "priority": 10.5,
        "matchers": {
            "level": {
                "min": level_min,
                "max": level_max
            },
            "has": {
                "country": countries,
                "items": required_items
            },
            "does_not_have": {
                "items": excluded_items
            },
        },
        "start_date": "2024-01-25 00:00:00Z",
        "end_date": "2026-02-25 00:00:00Z",
        "enabled": enabled,
        "last_updated": "2024-07-13 11:46:58Z"
    }

def get_active_campaigns():
    """
    Return a list of currently active campaigns.
    This is a mock function simulating a call to an external API service.
    """
    return [
        create_campaign(
            campaign_id="campaign-005",
            name="mycampaign",
            level_min=1,
            level_max=3,
            countries=["US", "RO", "CA"],
            required_items=["item_1"],
            excluded_items=["item_4"]
        )
    ]