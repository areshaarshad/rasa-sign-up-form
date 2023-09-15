import ftplib
from typing import Text, List, Any, Dict
from rasa_sdk import Tracker
# from rasa_sdk.forms import FormAction
from rasa_sdk.forms import Action
from rasa_sdk.executor import CollectingDispatcher
from actions.actions import save_to_database
class SubmitUserData(Action):

      def name(self) -> Text:
        return "action_submit_data"

      def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        name = tracker.get_slot("name")
        email = tracker.get_slot("email")
        mobile_number = tracker.get_slot("mobile_number")
        dob = tracker.get_slot("dob")
        password = tracker.get_slot("password")

        confirmation_message = f"Please confirm the following details:\n" \
                               f"Name: {name}\n" \
                               f"Email: {email}\n" \
                               f"Mobile Number: {mobile_number}\n" \
                               f"Date of Birth: {dob}\n" \
                               f"User Password: {password}\n" \
                               f"Is this information correct?"

        dispatcher.utter_message(text=confirmation_message)

        return []


import logging

class ActionHandleAffirmation(Action):
    def name(self) -> Text:
        return "action_handle_affirmation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       
        # INFO log level
        logging.basicConfig(level=logging.INFO) 

        logging.info("The data you entered is confirmed.")

        dispatcher.utter_message("The data you entered is confirmed.")
        return []

class ActionHandleDenial(Action):
    def name(self) -> Text:
        return "action_handle_denial"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        logging.basicConfig(level=logging.INFO) 

        logging.info("Kindly provide more information.")
        dispatcher.utter_message("Can you provide more information?")
        return []


class ActionSubmitData(Action):
    def name(self) -> Text:
        return "action_submit_data"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot("name") 
        phone_number = tracker.get_slot("mobile_number")
        email = tracker.get_slot("email")
        dob = tracker.get_slot("dob")

        save_to_database(name, phone_number, email, dob)
        dispatcher.utter_message("Your data has been submitted.")

        return []



