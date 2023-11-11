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
import xmlrpc.client as xmlrpclib
from datetime import datetime

db='odoo.plagiocefalia.com.ar'
user='bot'
pwd='bot2023'
server='45.33.16.200'
port='8069'    

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
        
class ActionTieneObraSocial(Action):

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
        #### manejo de archivo de ejemplo
        # ruta_completa = os.path.join(os.path.dirname(__file__), 'EjemplosTurnos.txt')
        # with open(ruta_completa, 'r') as archivo:
        #     lista_opciones = archivo.readlines()
        #     lista_opciones = [linea.strip() for linea in lista_opciones]
        # if lista_opciones is not None:
        #     numero_opcion = 1
        #     for opcion in lista_opciones:
        #         dispatcher.utter_message(text=str(f"Opcion {numero_opcion}: {opcion}"))
        #         numero_opcion += 1
        #     dispatcher.utter_message(text=str(f"Opcion {numero_opcion}: Consulta telefonica con un operador"))
        # else:
        #     lista_opciones[0] = str("Opcion 1: Consulta telefonica con un operador")
        
        #### conexiones
        uid = xmlrpclib.ServerProxy('http://'+server+':'+port+'/xmlrpc/2/common').authenticate(db, user, pwd, {})
        print (uid)
        odoo = xmlrpclib.ServerProxy('http://'+server+':'+port+'/xmlrpc/2/object')
        print (odoo)

        #### traigo los datos de los slots para crear el paciente
        nombre_completo_mama = tracker.get_slot("nombre")
        
        nombre_completo_bebe = tracker.get_slot("nombre_b")
        partes_nombre_bebe = nombre_completo_bebe.split(" ")
        nombre_bebe = ""
        apellido_bebe = ""
        cantidad_partes_nombre_bebe = len(partes_nombre_bebe)
        if (cantidad_partes_nombre_bebe > 0):
            nombre_bebe = partes_nombre_bebe[0]
            if (cantidad_partes_nombre_bebe == 2):
                apellido_bebe = partes_nombre_bebe[1]
            elif (cantidad_partes_nombre_bebe > 2):
                nombre_bebe = nombre_bebe + " " + partes_nombre_bebe[1]
                apellido_bebe = partes_nombre_bebe[2]
                for i in range(3, cantidad_partes_nombre_bebe):
                    apellido_bebe = apellido_bebe + " " + partes_nombre_bebe[i]

        mes_bebe = tracker.get_slot("mes_bebe")
        semanas_gestacion = int(tracker.get_slot("semanas_gestacion"))
        #fecha_nacimiento = tracker.get_slot("fecha_nacimiento")
        fecha_nacimiento= next(tracker.get_latest_entity_values("fecha_nacimiento_bebe"),None)
        fecha_nacimiento_obj = datetime.strptime(fecha_nacimiento, '%d-%m-%Y') # convierte a datetime
        fecha_nacimiento_formateada = fecha_nacimiento_obj.strftime('%Y-%m-%d') # formatea el formato al requerido por odoo

        #### creo un diccionario de paciente depediendo de la semana de gestacion (rnt o rnpt)
        if (semanas_gestacion >= 38) and (semanas_gestacion <= 41):
            paciente = {
                "nombre_madre": nombre_completo_mama,
                "firstname": nombre_bebe,
                "lastname": apellido_bebe,
                # "age": mes_bebe,
                # "rnt": semanas_gestacion,
                "birthdate_date": fecha_nacimiento_formateada
            }
        elif (semanas_gestacion < 38) and (semanas_gestacion >= 35):
            paciente = {
                "nombre_madre": nombre_completo_mama,
                "firstname": nombre_bebe,
                "lastname": apellido_bebe,
                # "age": mes_bebe,
                # "rnpt": semanas_gestacion,
                "birthdate_date": fecha_nacimiento_formateada
            }
        elif (semanas_gestacion < 35) or (semanas_gestacion > 41):
            paciente = {
                "nombre_madre": nombre_completo_mama,
                "firstname": nombre_bebe,
                "lastname": apellido_bebe,
                # "age": mes_bebe,
                # "rnpt": 'Otro',
                "birthdate_date": fecha_nacimiento_formateada
            }

        #### creo el paciente en odoo
        id_paciente = odoo.execute_kw(db, uid, pwd, 'res.partner', 'create', [paciente])
        # print(odoo.execute_kw(db, uid, pwd, 'res.partner', 'create', [{'nombre_madre': nombre_mama, 'firstname': nombre_bebe, 'birthdate_date': fecha_nacimiento_formateada}])) #falta rnt o rnpt en este ejemplo de insercion de paciente
        print(id_paciente)
        dispatcher.utter_message(text=str("creado paciente"))

        # #### compruebo si el paciente se creó buscando por su id
        # id_a_buscar = odoo.execute_kw(db, uid, pwd, 'res.partner', 'search', [[['id', '=', id]]], {'limit': 1})
        # print(odoo.execute_kw(db, uid, pwd, 'res.partner', 'read', [id_a_buscar]))

        #### consulta pacientes
        # ids = odoo.execute_kw(db, uid, pwd, 'res.partner', 'search', [[]], {'limit': 1})
        # print(odoo.execute_kw(db, uid, pwd, 'res.partner', 'read', [ids]))

        #### NO - consulta turnos calendario
        # id_turnos = odoo.execute_kw(db, uid, pwd, 'calendar.event', 'search', [[]], {'limit': 5})
        # print(odoo.execute_kw(db, uid, pwd, 'calendar.event', 'read', [id_turnos]))

        #### consulta turnos agenda
        id_turnos = odoo.execute_kw(db, uid, pwd, 'appointment.appointment', 'search', [[]], {'limit': 1})
        print(odoo.execute_kw(db, uid, pwd, 'appointment.appointment', 'read', [id_turnos]))

        ### creo un diccionario de turno
        turno = {
            "paciente": nombre_completo_bebe,
            "name": '?????',
            "motivo": '1 VEZ',
            "medico": 'Silvina Romero',
            "start": '2023-11-17 10:00:00',
            "stop": '2023-11-17 10:30:00',
            "display_time": '17/11/2023 at (07:00:00 To 07:30:00) (America/Buenos_Aires)',
            "allday": False,
        }

        #### creo el turno en odoo
        id_turno = odoo.execute_kw(db, uid, pwd, 'appointment.appointment', 'create', [turno])
        print(id_turno)
        dispatcher.utter_message(text=str("creado turno"))
        
     
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

class ActionGuardarNombre(Action):

     def name(self) -> Text:
         return "action_guardar_nombre"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        nombre_con_comillas = next(tracker.get_latest_entity_values("nombre"),None)
        nombre_sin_comillas = nombre_con_comillas.replace('"', '')
        ultima_accion_completada = None
        for event in reversed(tracker.events):
            if event.get("event") == "action" and event.get("name") != "action_guardar_nombre" and (event.get("name") == 'utter_pregunta_nombre_responsable' or event.get("name") == 'action_visito_especialista' or event.get("name") == 'utter_pregunta_nombre_bebe'):
                ultima_accion_completada = event.get("name")
                break
        if (ultima_accion_completada == 'utter_pregunta_nombre_responsable'):
            dispatcher.utter_message(text=str(f"Bienvenid@ {nombre_sin_comillas}" + "!​ ¿Ya has visitado un especialista craneal?"))
            return [SlotSet("nombre", nombre_sin_comillas)]
        elif (ultima_accion_completada == 'action_visito_especialista'):
            dispatcher.utter_message(text=str("Bien! Ahora adjunta foto de la misma. Aguardamos la foto de cada uno de los documentos emitidos😊"))
            return [SlotSet("nombre_n", nombre_sin_comillas)]
        elif (ultima_accion_completada == 'utter_pregunta_nombre_bebe'):
            dispatcher.utter_message(text=str(f"Qué lindo nombre! ¿Y con cuántas semanas de gestación nació {nombre_sin_comillas}? "))
            return [SlotSet("nombre_b", nombre_sin_comillas)]
        return []
