# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

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

class ActionVisitoEspecialista(Action):

     def name(self) -> Text:
         return "action_visito_especialista"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         #rta= tracker.latest_message['entities'][0]['value']
         #rta= next(tracker.get_latest_entity_values("visito_especialista"),None)
         rta= tracker.latest_message['intent']['name']
         if str(rta) == 'afirmacion':
            message="Entiendo. ¿Con que neurocirujano te atendiste?"
            dispatcher.utter_message(text=str(message))
            return [SlotSet("visito_especialista",True)]
         elif str(rta) == 'negacion':
            message="Entiendo. ¿Y residis en el AMBA?"
            dispatcher.utter_message(text=str(message))
            return [SlotSet("visito_especialista",False)]