"""
Mock campaigns: fake API.
"""

def get_active_campaigns():
    """
    Return a list of currently active campaigns.
    This is a mock function simulating a call to an external API service.
    """
    return [
        {
            "id": "campaign-004",
            "game": "mygame",
            "name": "mycampaign",
            "priority": 10.5,
            "matchers": {
                "level": {
                    "min": 1,
                    "max": 3
                },
                "has": {
                    "country": ["US", "RO", "CA"],
                    "items": ["item_1"]
                },
                "does_not_have": {
                    "items": ["item_4"]
                },
            },
            "start_date": "2024-01-25 00:00:00Z",
            "end_date": "2026-02-25 00:00:00Z",
            "enabled": True,
            "last_updated": "2024-07-13 11:46:58Z"
        }
    ]