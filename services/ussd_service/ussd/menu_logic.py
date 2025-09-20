import requests
from django.conf import settings


class USSDMenu:
    '''
    Handles USSD menu navigattion and user input.
    '''
    def __init__(self, session_id, phone_number, text):
        self.session_id = session_id
        self.phone_number = phone_number
        self.text = text.strip()

    def main_menu(self):
        '''
        Display the main menu options (first page).
        '''
        return (
            "CON Welcome to UkweliDial\n"
            "1. Report Misinformation\n"
            "2. Learn about fact-checked issues\n"
            "3. Request emergency help\n"
            "4. Civici education tips\n"
            "5. More options"
        )

    def more_options_menu(self):
        '''
        Display the secondary menu.
        '''
        return (
            "CON More options:\n"
            "6. Change language\n"
            "7. Contact a moderator\n"
            "8. Exit"
        )
     
    def handle_input(self):
        '''
        Directs user input to the approprate menu option.
        '''
        if self.text == "":
            return self.main_menu()

        inputs = self.text.split('*')
        choice = inputs[0]


        if choice == "1":
            return self.report_misinformation(inputs)
        elif choice == "2":
            return self.fact_checked_info()
        elif choice == "3":
            return self.emergency_help()
        elif choice == "4":
            return self.civic_education()
        elif choice == "5":
            return.self.more_options_menu()
        elif choice == "6":
            return self.change_language(inputs)
        elif choice == "7":
            return self.contact_moderator()
        elif choice == "8":
            return "END Thank you for using UkweliDial!"
        else:
            return "END Invalid choice. Please try again."

    # ---------- Features ----------

    def report_misinformation(self, inputs):
        '''
        Handles the reporting of misinformation.
        '''
        if len(inputs) == 1:
            return "CON Please describe the misinformation you want to report:"
        else:
            report_text = inputs[1]
            try:
                response = requests.post(
                    f"{settings.REPORT_SERVICE_URL}/api/reports/",
                    json={
                        "phone_number": self.phone_number,
                        "content": report_text,
                        "session_id": self.session_id,
                    },
                    timeout=5,
                )
                if response.status_code == 201:
                    return "END Thank you! Your report has been submitted."
                else:
                    return "END Sorry, there was an issue submitting  your report."
            except requests.exceptions.RequestException:
                return "END Service unavailable. Please try again later."

    def fact_checked_info(self):
        '''
        Provide fact-checked information.
        '''
        return (
            "END Fact-checked info:\n"
            "- Fake election results are circulating online.\n"
            "- Official IEBC portal is the trusted source.\n"
            "- Visit https://www.iebc.or.ke for updates."
        )

    def emergency_help(self):
        '''
        Connects the user with emergency contacts.
        '''
        return (
            "END Emergency Help:\n"
            "Call 1199 for Red Cross\n"
            "Call 999 for Police\n"
            "Stay safe!"
        )

    def civic_education(self):
        '''
        Provices civic education tips.
        '''
        return (
            "END Civic Tip:\n"
            "Your vote is your voice!\n"
            "Verify information before sharing it."
        )
    
    def change_language(self, inputs):
        '''
        Allows user to change language.
        '''
        if len(inputs) == 1:
            return "CON Choose language:\n1. English\n2. Kiswahili\n3. Kikuyu\n4. Dholuo"
        elif len(inputs) == 2:
            lang_choice = inputs[1]
            langs = {"1": "English", "2": "Kiswahili", "3": "Kikuyu", "4": "Dholuo"}
            return f"END Language changed to {langs.get(lang_choice, 'English')}."
        else:
            return "END Invalid input."

    def contact_moderator(self):
        '''
        Provides moderator contact info.
        '''
        return "END Contact Moderator: +254772000000
