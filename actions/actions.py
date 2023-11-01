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
import os

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
            message="Muchas gracias por contactarnos! Por favor ingresa el nombre completo del Neurocirujano que les emitió la orden médica solicitando el uso de la Ortesis Craneal entre comillas dobles: "
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
        
class ActionVisitoEspecialista(Action):

     def name(self) -> Text:
         return "action_tiene_os"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         rta= tracker.latest_message['intent']['name']
         if str(rta) == 'afirmacion':
            message="Genial! Te pedimos que nos adjuntes foto del carnet de la misma"
            dispatcher.utter_message(text=str(message))
            return [SlotSet("tiene_os",True)]
         elif str(rta) == 'negacion':
            message="Bueno! Entonces te pido que nos adjuntes foto de frente y dorso de tu DNI"
            dispatcher.utter_message(text=str(message))
            return [SlotSet("tiene_os",False)]

class ActionMostrarTurnos(Action):

     def name(self) -> Text:
         return "action_mostrar_turnos"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=str("Para proceder con la agenda de un turno, seleccione alguna de las siguientes opciones: "))
        ruta_completa = os.path.join(os.path.dirname(__file__), 'EjemplosTurnos.txt')
        with open(ruta_completa, 'r') as archivo:
            lista_opciones = archivo.readlines()
            lista_opciones = [linea.strip() for linea in lista_opciones]
        if lista_opciones is not None:
            numero_opcion = 1
            for opcion in lista_opciones:
                dispatcher.utter_message(text=str(f"Opcion {numero_opcion}: {opcion}"))
                numero_opcion += 1
            dispatcher.utter_message(text=str(f"Opcion {numero_opcion}: Consulta telefonica con un operador"))
        else:
            lista_opciones[0] = str("Opcion 1: Consulta telefonica con un operador")
        return []
     
class ActionConfirmacionTurno(Action):

     def name(self) -> Text:
         return "action_confirmacion_turno"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        opcion_seleccionada = float(next(tracker.get_latest_entity_values("opcion"),None))
        ruta_completa = os.path.join(os.path.dirname(__file__), 'EjemplosTurnos.txt')
        with open(ruta_completa, 'r') as archivo:
            lista_opciones = archivo.readlines()
            lista_opciones = [linea.strip() for linea in lista_opciones]
        cantidad_opciones = len(lista_opciones)
        if (opcion_seleccionada == cantidad_opciones+1): #esto es porque está la opción adicional de derivación a un operador
            dispatcher.utter_message(text=str("Ya te derivé al sector correspondiente en el transcurso del día se estarán contactando con vos!☺️"))
        elif(opcion_seleccionada > 0) and (opcion_seleccionada <= cantidad_opciones):
            datos_turno = lista_opciones[int(opcion_seleccionada)-1].split(" - ")
            fecha, horario, doctor, honorarios = datos_turno
            posicion = fecha.rfind('d')-1
            fecha_sin_anio = fecha[:posicion]
            nombre_bebe = tracker.get_slot("nombre_b")
            dispatcher.utter_message(text=str(f"Bien,👌 ya queda agendada la visita de {nombre_bebe} para el día {fecha_sin_anio} con dr {doctor} a las {horario}, en nuestros consultorios ubicados en 📍Av. Callao 384, Piso 4º 9, Capital Federal. Los honorarios son {honorarios}\nhttps://g.page/PlagiocefaliaArgentina?share\nEl equipo de Plagiocefalia Argentina https://youtu.be/wrfBgNa0shY"))
        else:
            dispatcher.utter_message(text=str("Perdón, ingresaste una opción inválida, por favor intentalo devuelta y asegurate que el número de opción esté en el listado"))
        return []

class ActionGuardarNombreResponsable(Action):
    def name(self) -> Text:
        return "action_guardar_nombre_responsable"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        nombre_con_comillas = next(tracker.get_latest_entity_values("nombre"),None)
        dispatcher.utter_message(f"{nombre_con_comillas}")
        if nombre_con_comillas:
            nombre_sin_comillas = nombre_con_comillas.replace('"', '')  # Elimina las comillas dobles
            dispatcher.utter_message(f"Bienvenid@ {nombre_sin_comillas}" + "!​ ¿Ya has visitado un especialista craneal?")
            return [SlotSet("nombre", nombre_sin_comillas)]
        else:
            dispatcher.utter_message("No has proporcionado un nombre R")
            return []

class ActionGuardarNombreNeurocirujano(Action):
    def name(self) -> Text:
        return "action_guardar_nombre_neurocirujano"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        nombre_con_comillas = next(tracker.get_latest_entity_values("nombre_n"),None)
        if nombre_con_comillas:
            nombre_sin_comillas = nombre_con_comillas.replace('"', '')  # Elimina las comillas dobles
            dispatcher.utter_message(f"Bien! Ahora adjunta foto de la misma. Aguardamos la foto de cada uno de los documentos emitidos😊")
            return [SlotSet("nombre_n", nombre_sin_comillas)]
        else:
            dispatcher.utter_message("No has proporcionado un nombre N")
            return []
        
class ActionGuardarNombreBebe(Action):
    def name(self) -> Text:
        return "action_guardar_nombre_bebe"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        nombre_con_comillas = next(tracker.get_latest_entity_values("nombre_b"),None)
        if nombre_con_comillas:
            nombre_sin_comillas = nombre_con_comillas.replace('"', '')  # Elimina las comillas dobles
            dispatcher.utter_message(f"Las semanas de gestación de tu bebé: ")
            return [SlotSet("nombre_b", nombre_sin_comillas)]
        else:
            dispatcher.utter_message("No has proporcionado un nombre B")
            return []
