# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from typing import Text, List, Any, Dict
from rasa_sdk import Tracker
# from rasa_sdk.forms import FormAction
from rasa_sdk.forms import FormValidationAction, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from datetime import datetime
import re
import logging
from rasa_sdk.events import SlotSet


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UserDataForm(Action):
    def name(self) -> Text:
        return "user_data_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["name", "email", "mobile_number", "dob"]



class ValidateUserDataForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_user_data_form"

    def validate_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `name` value."""
        print(f"Validating name: {slot_value}") 
        name = slot_value
        if len(name) == 0:
            dispatcher.utter_message(text="The name you entered is not correct.")
            return {"name": None}
        return {"name": name}

    def validate_mobile_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `mobile_number` value."""
        mobile_number = slot_value.strip() 
        if not mobile_number.isdigit() and len(mobile_number) != 11:
            dispatcher.utter_message(text="Please enter a valid 11-digit mobile number.")
            return {"mobile_number": None}

        return {"mobile_number": mobile_number}
    
    def validate_dob(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `dob` value."""
        dob = slot_value.strip()
        expected_format = "%d-%m-%Y"

        try:
            datetime.strptime(dob, expected_format)
        except ValueError:
            dispatcher.utter_message(text="Please enter a valid date of birth in the format dd-mm-yyyy.")
            return {"dob": None}

        return {"dob": dob}

    def validate_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `email` value."""
        email = slot_value.strip()
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not re.match(email_pattern, email):
            dispatcher.utter_message(text="Please enter a valid email address.")
            return {"email": None}
        else:
            print(f"Email Validation: {email}")

        return {"email": email}

class ActionConfirmData(Action):
    def name(self) -> Text:
        return "action_confirm_data"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        user_input = tracker.latest_message.get("text")
        affirm_intent = "affirm_data"  
        deny_intent = "deny_data"      

        if affirm_intent in tracker.latest_message['intent']['name']:
            response = domain['responses']['affirmation_response']
        elif deny_intent in tracker.latest_message['intent']['name']:
            response = domain['responses']['denial_response']
        else:
            response = domain['responses']['invalid_response']

        dispatcher.utter_message(template=response)
        return []


class ActionCreatePassword(Action):
    def name(self) -> Text:
        return "action_create_password"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_name = tracker.get_slot("name")
        user_email = tracker.get_slot("email")
        user_phone = tracker.get_slot("mobile_number")
        user_dob = tracker.get_slot("dob")
        # generated_password = self.generate_password(user_name, user_email, user_phone, user_dob)

        # tracker.slots["password"] = generated_password

        # tracker.slots["USER_SIGNED_IN"] = True
        password = user_name.replace(" ", "").lower() + user_dob.replace("-","")
        dispatcher.utter_message(f"Your password is: {password}")
        

        return [SlotSet("password", password)]

    # def generate_password(self, user_name: str, user_email: str, user_phone: str, user_dob: str) -> str:
         
    #     return []
    
class ActionCreateLogin(Action):
    def name(self) -> Text:
        return "action_create_login"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        login_email = tracker.get_slot("email")
        login_password = tracker.get_slot("password")
        print(f"Email: {login_email}")
        print(f"Password: {login_password}")

        dispatcher.utter_message(f"Email: {login_email}")
        dispatcher.utter_message(f"Password: {login_password}")
        dispatcher.utter_message("You are now signed in.")
        # return []


class ValidateLoginAction(Action):
    def name(self) -> Text:
        return "validate_login"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        recognized_intent = tracker.latest_message['intent']['name']
        print(f"Recognized Intent: {recognized_intent}")

        email = tracker.get_slot("email")
        password = tracker.get_slot("password")

        if email == tracker.get_slot("email") and password == tracker.get_slot("password"):
            return [SlotSet("USER_SIGNED_IN", True)]
        else:
            return [SlotSet("USER_SIGNED_IN", False)]

class UtterLoginSuccessfulAction(Action):
    def name(self) -> Text:
        return "utter_login_successful"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        is_signed_in = tracker.get_slot("USER_SIGNED_IN")
        if is_signed_in:
            dispatcher.utter_message("You have successfully logged in!")
        else:
            dispatcher.utter_message("Login failed. Please check your credentials.")

        # return []



import psycopg2

db_connection = {
    "user": "postgres",
    "password": "1947001",
    "host": "localhost",
    "port": "5433",
    "database": "postgres"
}



def create_table():
    try:
        conn = psycopg2.connect(**db_connection)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS sign_up_data (
                id serial PRIMARY KEY,
                name VARCHAR(255),
                phone_number VARCHAR(15),  
                email VARCHAR(255),
                dob DATE
            )
        ''')
        conn.commit()
    except Exception as e:
        logger.error("Error creating table:", exc_info=True) 
        print("Error creating table:", e)
    finally:
        cur.close()
        conn.close()



def save_to_database(name, mobile_number, email, dob):
    try:
        conn = psycopg2.connect(**db_connection)
        cur = conn.cursor()

        logexec = cur.execute(f"INSERT INTO sign_up_data (name, phone_number, email, dob)\
        VALUES ('{name}', '{mobile_number}', '{email}', '{dob}')")
        logger.info(f"save_to_database: Execute SQL for inserting data: {logexec}")
        logger
        conn.commit()
    except Exception as e:
        # save_to_database: Error when trouble saving data: {e}
        logger.info(f"Exception occurred", exc_info=True)
        print("Error saving data to the database:", e)
    finally:
        cur.close()
        conn.close()






