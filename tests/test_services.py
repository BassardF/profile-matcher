"""
Tests for the services module functions
"""
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch
from app.services import (
    filter_eligible_campaigns,
    check_player_matches_campaign_criteria,
    check_campaign_is_active
)

class TestFilterEligibleCampaigns:
    """Tests for the filter_eligible_campaigns function"""
    
    def test_returns_false_when_player_already_has_campaign(self):
        # Arrange
        player = MagicMock()
        player.has_campaign.return_value = True
        campaign = {"id": "campaign-001"}
        
        # Act
        result = filter_eligible_campaigns(player, campaign)
        
        # Assert
        assert result is False
        player.has_campaign.assert_called_once_with("campaign-001")

    @patch('app.services.check_campaign_is_active')
    def test_returns_false_when_campaign_not_active(self, mock_check_active):
        # Arrange
        player = MagicMock()
        player.has_campaign.return_value = False
        mock_check_active.return_value = False
        campaign = {"id": "campaign-001"}
        
        # Act
        result = filter_eligible_campaigns(player, campaign)
        
        # Assert
        assert result is False
        mock_check_active.assert_called_once_with(campaign)
    
    @patch('app.services.check_campaign_is_active')
    @patch('app.services.check_player_matches_campaign_criteria')
    def test_returns_false_when_player_does_not_match_criteria(self, mock_check_criteria, mock_check_active):
        # Arrange
        player = MagicMock()
        player.has_campaign.return_value = False
        mock_check_active.return_value = True
        mock_check_criteria.return_value = False
        campaign = {"id": "campaign-001"}
        
        # Act
        result = filter_eligible_campaigns(player, campaign)
        
        # Assert
        assert result is False
        mock_check_criteria.assert_called_once_with(player, campaign)
    
    @patch('app.services.check_campaign_is_active')
    @patch('app.services.check_player_matches_campaign_criteria')
    def test_returns_true_when_all_conditions_met(self, mock_check_criteria, mock_check_active):
        # Arrange
        player = MagicMock()
        player.has_campaign.return_value = False
        mock_check_active.return_value = True
        mock_check_criteria.return_value = True
        campaign = {"id": "campaign-001"}
        
        # Act
        result = filter_eligible_campaigns(player, campaign)
        
        # Assert
        assert result is True


class TestCheckPlayerMatchesCampaignCriteria:
    """Tests for the check_player_matches_campaign_criteria function"""
    
    def test_returns_true_when_no_matchers_defined(self):
        # Arrange
        player = MagicMock()
        campaign = {"id": "campaign-001"}  # No matchers defined
        
        # Act
        result = check_player_matches_campaign_criteria(player, campaign)
        
        # Assert
        assert result is True
    
    def test_level_requirements_min_only(self):
        # Arrange
        player = MagicMock()
        player.level = 5
        campaign = {
            "matchers": {
                "level": {
                    "min": 3
                }
            }
        }
        
        # Act
        result = check_player_matches_campaign_criteria(player, campaign)
        
        # Assert
        assert result is True
        
        # Test with player below min level
        player.level = 2
        result = check_player_matches_campaign_criteria(player, campaign)
        assert result is False
    
    def test_level_requirements_max_only(self):
        # Arrange
        player = MagicMock()
        player.level = 5
        campaign = {
            "matchers": {
                "level": {
                    "max": 10
                }
            }
        }
        
        # Act
        result = check_player_matches_campaign_criteria(player, campaign)
        
        # Assert
        assert result is True
        
        # Test with player above max level
        player.level = 15
        result = check_player_matches_campaign_criteria(player, campaign)
        assert result is False
    
    def test_level_requirements_min_and_max(self):
        # Arrange
        player = MagicMock()
        player.level = 5
        campaign = {
            "matchers": {
                "level": {
                    "min": 3,
                    "max": 10
                }
            }
        }
        
        # Act
        result = check_player_matches_campaign_criteria(player, campaign)
        
        # Assert
        assert result is True
        
        # Test with player below range
        player.level = 2
        result = check_player_matches_campaign_criteria(player, campaign)
        assert result is False
        
        # Test with player above range
        player.level = 11
        result = check_player_matches_campaign_criteria(player, campaign)
        assert result is False
    
    def test_country_requirements(self):
        # Arrange
        player = MagicMock()
        player.country = "US"
        campaign = {
            "matchers": {
                "has": {
                    "country": ["US", "CA", "UK"]
                }
            }
        }
        
        # Act
        result = check_player_matches_campaign_criteria(player, campaign)
        
        # Assert
        assert result is True
        
        # Test with player from non-matching country
        player.country = "FR"
        result = check_player_matches_campaign_criteria(player, campaign)
        assert result is False
    
    def test_required_items(self):
        # Arrange
        player = MagicMock()
        player.has_all_items.return_value = True
        campaign = {
            "matchers": {
                "has": {
                    "items": ["Item 1", "Item 2"]
                }
            }
        }
        
        # Act
        result = check_player_matches_campaign_criteria(player, campaign)
        
        # Assert
        assert result is True
        player.has_all_items.assert_called_once_with(["Item 1", "Item 2"])
        
        # Test with player missing required items
        player.has_all_items.return_value = False
        result = check_player_matches_campaign_criteria(player, campaign)
        assert result is False
    
    def test_excluded_items(self):
        # Arrange
        player = MagicMock()
        player.has_any_items.return_value = False
        campaign = {
            "matchers": {
                "does_not_have": {
                    "items": ["Item 3", "Item 4"]
                }
            }
        }
        
        # Act
        result = check_player_matches_campaign_criteria(player, campaign)
        
        # Assert
        assert result is True
        player.has_any_items.assert_called_once_with(["Item 3", "Item 4"])
        
        # Test with player having excluded items
        player.has_any_items.return_value = True
        result = check_player_matches_campaign_criteria(player, campaign)
        assert result is False
    
    def test_combined_requirements(self):
        # Arrange
        player = MagicMock()
        player.level = 5
        player.country = "US"
        player.has_all_items.return_value = True
        player.has_any_items.return_value = False
        
        campaign = {
            "matchers": {
                "level": {
                    "min": 3,
                    "max": 10
                },
                "has": {
                    "country": ["US", "CA"],
                    "items": ["Item 1", "Item 2"]
                },
                "does_not_have": {
                    "items": ["Item 3", "Item 4"]
                }
            }
        }
        
        # Act
        result = check_player_matches_campaign_criteria(player, campaign)
        
        # Assert
        assert result is True
        
        # Test with one failing condition (level)
        player.level = 2
        result = check_player_matches_campaign_criteria(player, campaign)
        assert result is False
        
        # Reset level and test with another failing condition (country)
        player.level = 5
        player.country = "FR"
        result = check_player_matches_campaign_criteria(player, campaign)
        assert result is False
        
        # Reset country and test with another failing condition (required items)
        player.country = "US"
        player.has_all_items.return_value = False
        result = check_player_matches_campaign_criteria(player, campaign)
        assert result is False
        
        # Reset required items and test with another failing condition (excluded items)
        player.has_all_items.return_value = True
        player.has_any_items.return_value = True
        result = check_player_matches_campaign_criteria(player, campaign)
        assert result is False


class TestCheckCampaignIsActive:
    """Tests for the check_campaign_is_active function"""
    
    def test_returns_false_when_campaign_not_enabled(self):
        # Arrange
        campaign = {"enabled": False}
        
        # Act
        result = check_campaign_is_active(campaign)
        
        # Assert
        assert result is False
    
    def test_returns_true_when_campaign_enabled_no_dates(self):
        # Arrange
        campaign = {"enabled": True}
        
        # Act
        result = check_campaign_is_active(campaign)
        
        # Assert
        assert result is True
    
    @patch('app.services.datetime')
    def test_returns_false_when_current_time_before_start_date(self, mock_datetime):
        # Arrange
        current_time = datetime(2024, 1, 1, tzinfo=timezone.utc)
        mock_datetime.now.return_value = current_time
        
        start_date = datetime(2024, 2, 1, tzinfo=timezone.utc)
        end_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        
        campaign = {
            "enabled": True,
            "start_date": start_date,
            "end_date": end_date
        }
        
        # Act
        result = check_campaign_is_active(campaign)
        
        # Assert
        assert result is False
        mock_datetime.now.assert_called_once_with(timezone.utc)
    
    @patch('app.services.datetime')
    def test_returns_false_when_current_time_after_end_date(self, mock_datetime):
        # Arrange
        current_time = datetime(2024, 4, 1, tzinfo=timezone.utc)
        mock_datetime.now.return_value = current_time
        
        start_date = datetime(2024, 2, 1, tzinfo=timezone.utc)
        end_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        
        campaign = {
            "enabled": True,
            "start_date": start_date,
            "end_date": end_date
        }
        
        # Act
        result = check_campaign_is_active(campaign)
        
        # Assert
        assert result is False
        mock_datetime.now.assert_called_once_with(timezone.utc)
    
    @patch('app.services.datetime')
    def test_returns_true_when_current_time_within_date_range(self, mock_datetime):
        # Arrange
        current_time = datetime(2024, 2, 15, tzinfo=timezone.utc)
        mock_datetime.now.return_value = current_time
        
        start_date = datetime(2024, 2, 1, tzinfo=timezone.utc)
        end_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        
        campaign = {
            "enabled": True,
            "start_date": start_date,
            "end_date": end_date
        }
        
        # Act
        result = check_campaign_is_active(campaign)
        
        # Assert
        assert result is True
        mock_datetime.now.assert_called_once_with(timezone.utc)
