from datetime import datetime, timezone
from typing import Dict, Any, Optional
from .models import Player


def filter_eligible_campaigns(
        player: Player, campaign: Dict[str, Any]) -> bool:
    """
    Check if a player is eligible to a new campaign.

    Args:
        player: Player object containing the player data
        campaign: Dictionary containing the campaign configuration and matcher rules

    Returns:
        bool: True if the player is eligible for the campaign, False otherwise
    """

    # Filter out campaigns already assigned to the player
    if player.has_campaign(campaign['id']):
        return False

    # Check if campaign is active
    if not check_campaign_is_active(campaign):
        return False

    # Check matchers against player profile
    if not check_player_matches_campaign_criteria(player, campaign):
        return False

    return True


def check_player_matches_campaign_criteria(
        player: Player, campaign: Dict[str, Any]) -> bool:
    """
    Check if a player matches the criteria defined in a campaign's matchers.

    Args:
        player: Player object containing the player data
        campaign: Dictionary containing the campaign configuration and matcher rules

    Returns:
        bool: True if the player matches all criteria, False otherwise
    """
    matchers: Dict[str, Any] = campaign.get("matchers", {})

    # Check level requirements
    if level_requirements := matchers.get("level"):
        min_level = level_requirements.get("min", 1)
        max_level = level_requirements.get("max", float('inf'))

        if not (min_level <= player.level <= max_level):
            return False

    # Check 'has' requirements
    if has_requirements := matchers.get("has"):
        # Check country
        if required_countries := has_requirements.get("country"):
            if player.country not in required_countries:
                return False

        # Check items
        if required_items := has_requirements.get("items"):
            # Check if player has all required items
            if not player.has_all_items(required_items):
                return False

    # Check 'does_not_have' requirements
    if exclusion_requirements := matchers.get("does_not_have"):
        if excluded_items := exclusion_requirements.get("items"):
            # Check if player has any excluded items
            if player.has_any_items(excluded_items):
                return False

    return True


def check_campaign_is_active(campaign: Dict[str, Any]) -> bool:
    """
    Check if a campaign is currently active based on enabled status and date range.

    Args:
        campaign: Dictionary containing the campaign configuration

    Returns:
        bool: True if the campaign is active, False otherwise
    """
    # Check if campaign is enabled
    if not campaign.get("enabled", False):
        return False

    # Check campaign dates
    current_time: datetime = datetime.now(timezone.utc)
    start_date: Optional[datetime] = campaign.get("start_date")
    end_date: Optional[datetime] = campaign.get("end_date")

    if start_date and end_date:
        if current_time < start_date or current_time > end_date:
            return False

    return True