from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import USSDUser, USSDSession
from report.models import Report


class USSDGatewayView(APIView):
    '''
    Handles USSD requests:
    - If new session: create a USSDSession and greets the user.
    - If exisiting session: processes user input and returns next menu.
    '''
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phoneNumber')
        session_id = request.data.get('sessionId')
        text = request.data.get('text', '')

        if not phone_number or not session_id:
            return Response({'error': 'Missing phoneNumber or sessionId'}, status=status.HTTP_400_BAD_REQUEST)

        # Get or create user
        user, _ USSDUser.objects.get_or_create(phone_number=phone_number)

        # Get or create session
        session, _ = USSDSession.objects.get_or_create(
            session_id=session_id, user=user, defaults={'last_input': text}
        )

        # Split text into steps
        inputs = text.split('*')

        if text == '':
            menu = "Welcome to UkweliDial\n1. Report Misinformation\n2. Fact-check a claim"

        elif inputs[0] == '1':
            # Option 1: Report misinformation
            if len(inputs) == 1:
                # User just pressed 1, ask for input
                menu = "Please enter the misinformation you want to report:"
            elif len(inputs) == 2:
                # User entered misinformation -> Save to Report DB
                report_content = inputs[1]
                Report.objects.create(user=user, content=report_content)
                menu = "Thank you! Your report has been submitted for review."
            else:
                menu = "Invalid input. Please try again."

        elif inputs[0] == '2':
            # Option 2: Fact-check
            if len(inputs) == 1:
                menu = "Enter the claim you want verified:"
            elif len(inputs) == 2:
                claim = inputs[1]
                menu = f"Your claim '{claim}' has been submitted for fact-checking."
            else:
                menu = "Invalid input. Please try again."
        else:
            menu = "Invalid choice. Please try again."

        # Update session
        session.last_input = text
        session.save()

        return Response({"response": menu}, status=status.HTTP_200_OK)
