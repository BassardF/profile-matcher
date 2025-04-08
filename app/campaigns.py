"""
Mock campaigns: fake API.
"""
from typing import Dict, Any, List, Union


def create_campaign(
    campaign_id: str,
    name: str,
    level_min: int = 1,
    level_max: Union[int, float] = float('inf'),
    countries: List[str] = [],
    required_items: List[str] = [],
    excluded_items: List[str] = [],
    enabled: bool = True
) -> Dict[str, Any]:
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


def get_active_campaigns() -> List[Dict[str, Any]]:
    """
    Return a list of currently active campaigns.
    This is a mock function simulating a call to an external API service.
    """
    return [
        create_campaign(
            campaign_id="campaign-001",
            name="mycampaign",
            level_min=1,
            level_max=3,
            countries=["US", "RO", "CA"],
            required_items=["Item 1"],
            excluded_items=["Item 4"]
        )
    ]
