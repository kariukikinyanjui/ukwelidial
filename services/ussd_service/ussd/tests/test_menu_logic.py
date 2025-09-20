import pytest
from unittest.mock import patch
from ussd.menu_logic import USSDMenu


@pytest.mark.django_db
class TestUSSDReport:
    def test_report_flow(self):
        '''
        Simulate a user reporting misinformation through the USSD menu.
        '''
        # Step 1: User opens menu
        menu = USSDMenu(session_id="123", phone_number="+25470000000", text="")
        assert "CON" in menu.handle_input()

        # Step 2: User selects option 1
        menu = USSDMenu(session_id="123", phone_number="+25470000000", text="1")
        assert "CON Please describe" in menu.handle_input()

    @patch("ussd.menu_logic.requests.post")
    def test_report_submission(self, mock_post):
        '''
        Ensures a report is sent to the Report microservice.
        '''
        mock_post.return_value.status_code = 201

        menu = USSDMenu(session_id="123", phone_number="+25470000000", text="1*Fake news here")
        result = menu.handle_input()

        assert "Thank you" in result
        mock_post.assert_called_once()
