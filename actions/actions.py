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
        rta = float(next(tracker.get_latest_entity_values("mes_bebe"),None))
        # dispatcher.utter_message(text=str(rta))
        if (rta >= 0) and (rta <= 1):
            message = "Que bueno que nos contactes a tiempo 👍 ya que tu bebé al estar en sus primeros días de vida está en la edad ideal para corregir la asimetría craneal con ejercicios posicionales y si crees necesario puedes escribirnos y coordinar una visita con unos de nuestros Neurocirujanos Pediátricos.\nNuestros consultorios están ubicados en la Av. Callao y Av. Corrientes, a 5 cuadras del Obelisco en Capital Federal.\nhttps://g.page/PlagiocefaliaArgentina?share\nPara agendar una consulta es necesario que nos brindes por este medio: "
            dispatcher.utter_message(text=str(message))
            return [SlotSet("mes_bebe", rta)]
        elif (rta > 1) and (rta <= 7):
            message = f"Que bueno que nos contactes a tiempo 👍 ya que tu bebé al tener {int(rta)} meses de edad está en la edad ideal para corregir la asimetría craneal.\nEn este caso lo más adecuado es que nos visites con tu bebé en nuestra clínica.\nNuestros consultorios están ubicados en la Av. Callao y Av. Corrientes, a 5 cuadras del Obelisco en Capital Federal.\nhttps://g.page/PlagiocefaliaArgentina?share\nPara agendar una consulta es necesario que nos brindes por este medio: "
            dispatcher.utter_message(text=str(message))
            return [SlotSet("mes_bebe", rta)]
        elif (rta > 7) and (rta <= 10):
            message = f"Que bueno que nos contactes! 👍 Como tu bebé tiene {int(rta)} meses estamos en una edad avanzada pero a tiempo para corregir la asimetría craneal\nEn este caso lo más adecuado es que nos visites con tu bebé en nuestra clínica.\n*Te recomendamos coordinar un turno para una evaluación, el tiempo es determinante para obtener buenos resultados.*\nNuestros consultorios están ubicados en la Av. Callao y Av. Corrientes, a 5 cuadras del Obelisco en Capital Federal.\nhttps://g.page/PlagiocefaliaArgentina?share\nPara agendar una consulta es necesario que nos brindes por este medio: "
            dispatcher.utter_message(text=str(message))
            return [SlotSet("mes_bebe", rta)]
        elif (rta > 10) and (rta <= 14):
            message = f"Que bueno que nos contactes! 👍 Como tu bebé tiene {int(rta)} meses estamos en una MUY edad avanzada pero a tiempo para corregir la asimetría craneal\nEn este caso lo más adecuado es que nos visites con tu bebé en nuestra clínica.\n*Te recomendamos coordinar un turno para una evaluación, el tiempo es determinante para obtener buenos resultados.*\nNuestros consultorios están ubicados en la Av. Callao y Av. Corrientes, a 5 cuadras del Obelisco en Capital Federal.\nhttps://g.page/PlagiocefaliaArgentina?share\nPara agendar una consulta es necesario que nos brindes por este medio: "
            dispatcher.utter_message(text=str(message))
            return [SlotSet("mes_bebe", rta)]
        elif (rta > 14):
            message = f"Nosotros somos técnicos ortopédicos y nuestro tratamiento para corregir las asimetrías craneales tiene que iniciarse antes de los 12 meses de edad. Luego de esta edad no es efectivo.\nEn este caso, lo que te recomendamos es visitar a un *Neurocirujano Pediátrico*, él podrá evacuar todas tus dudas.\nQuedamos a tu disposición, Plagiocefalia Argentina👍\nTe dejo dos videos para que conozcas sobre Plagiocefalia!\n⏯️ https://youtu.be/XzTgTgPC7Xw\n⏯️ https://youtu.be/Oh0TF_ze-hI"
            dispatcher.utter_message(text=str(message))
            return [SlotSet("mes_bebe", rta)]
        else:
            dispatcher.utter_message(text=str("No entendí, ¿me repetis cuantos meses tiene tu bebe?"))
            return []