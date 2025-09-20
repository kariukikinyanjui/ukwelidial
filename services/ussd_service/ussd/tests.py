from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import USSDUser, USSDSession
from report.models import Report


class USSDGatewayTests(TestCase):
    '''
    Tests the USSD service workflow.
    '''
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('ussd-gateway')
        self.phone = '254722000000'
        self.session_id = '12334'

    def test_start_new_session(self):
        response = self.client.post(self.url, {
            'phoneNumber': self.phone,
            'sessionId': self.session_id,
            'text': ''
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Welcome to UkweliDial', response.data['response'])

    def test_continue_session(self):
        # Start sessioin
        self.client.post(self.url, {'phoneNumber': self.phone, 'sessionId': self.session_id, 'text': ''}, format='json')

        # Continue with option 1
        response = self.client.post(self.url, {'phoneNumber': self.phone, 'sessionId': self.session_id, 'text':'1'}, format='json')
        self.assertIn("Please enter the misinformation", response.data['response'])

    def test_submit_report(self):
        # Step 1: Start session
        self.client.post(self.url, {"phoneNumber": self.phone, "sessionId": self.session_id, "text": ''}, format='json')

        # Step 2: Select option 1
        self.client.post(self.url, {"phoneNumber": self.phone, "sessionId": self.session_id, "text": '1'}, format='json')

        # Step 3: Submit misinformation
        response = self.client.post(self.url, {
            "phoneNumber": self.phone,
            "sessionId": self.session_id,
            "text": "1*Fake news about election"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Thank you! Your report has been submitted", response.data["response"])

        # Verify report is saved
        user = USSDUser.objects.get(phone_number=self.phone)
        report = Report.objects.filter(user=user).first()
        self.assertIsNotNone(report)
        self.assertEqual(report.content, "Fake news about election")
