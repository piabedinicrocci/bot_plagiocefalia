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
from rasa_sdk.events import ActionExecutionRejected

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
         rta= tracker.latest_message['intent']['name']
         if str(rta) == 'afirmacion':
            message="Entiendo. ¿Con que neurocirujano te atendiste?"
            dispatcher.utter_message(text=str(message))
            return [SlotSet("visito_especialista",True)]
         elif str(rta) == 'negacion':
            message="Entiendo. ¿Y residis en el AMBA?"
            dispatcher.utter_message(text=str(message))
            return [SlotSet("visito_especialista",False)]
         

class ActionEndConversation(Action):
    def name(self) -> Text:
        return "action_finalizar_comunicacion"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Devuelve un evento de acción de finalización para finalizar la conversación
        return [ActionExecutionRejected()]
    

class ActionEdadBebe(Action):

     def name(self) -> Text:
         return "action_edad_bebe"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         rta= tracker.latest_message['entities'][0]['value']
         rta2= next(tracker.get_latest_entity_values("mes_bebe"),None)
         dispatcher.utter_message(text=str(rta))
         dispatcher.utter_message(text=str(rta2))
         if (rta >= 0) and (rta <= 1):
            message="ENTRE 0 Y 1"
            dispatcher.utter_message(text=str(message))
            return [SlotSet("mes_bebe",rta)]
         elif (rta > 1) and (rta <= 7):
            message="ENTRE 2 Y 7"
            dispatcher.utter_message(text=str(message))
            return [SlotSet("mes_bebe",rta)]
         elif (rta > 7) and (rta <= 10):
            message="ENTRE 8 Y 10"
            dispatcher.utter_message(text=str(message))
            return [SlotSet("mes_bebe",rta)]
         elif (rta > 10) and (rta <= 14):
            message="ENTRE 11 Y 14"
            dispatcher.utter_message(text=str(message))
            return [SlotSet("mes_bebe",rta)]
         elif (rta > 14):
            message="MAS DE 14"
            dispatcher.utter_message(text=str(message))
            return [SlotSet("mes_bebe",rta)]
         else:
            return dispatcher.utter_message(text=str("no entro"))