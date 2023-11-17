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
import locale
from datetime import datetime, timedelta

db='odoo.plagiocefalia.com.ar'
user='bot'
pwd='bot2023'
server='45.33.16.200'
port='8069'   

# Definir información de los médicos
medicos = {
    31: {'nombre': 'Emanuel Ortiz', 'dias': ['Thursday'], 'inicio': '09:30:00', 'fin': '14:30:00'},
    32: {'nombre': 'Silvina Romero', 'dias': ['Friday'], 'inicio': '09:00:00', 'fin': '16:30:00'},
    33: {'nombre': 'Gaston Dech', 'dias': ['Monday'], 'inicio': '10:00:00', 'fin': '15:30:00'},
}

fechas_disponibles = []

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
     
     def obtenerDiaEnCastellano(self, dia):
        if dia == "Monday":
            return "Lunes"
        elif dia == "Tuesday":
            return "Martes"
        elif dia == "Wednesday":
            return "Miércoles"
        elif dia == "Thursday":
            return "Jueves"
        elif dia == "Friday":
            return "Viernes"
        elif dia == "Saturday":
            return "Sábado"
        elif dia == "Sunday":
            return "Domingo"
        else:
            return "Dia invalido"
        
     def obtenerMesEnCastellano(self, mes):
        if mes == "January":
            return "Enero"
        elif mes == "February":
            return "Febrero"
        elif mes == "March":
            return "Marzo"
        elif mes == "April":
            return "Abril"
        elif mes == "May":
            return "Mayo"
        elif mes == "June":
            return "Junio"
        elif mes == "July":
            return "Julio"
        elif mes == "August":
            return "Agosto"
        elif mes == "September":
            return "Septiembre"
        elif mes == "October":
            return "Octubre"
        elif mes == "November":
            return "Noviembre"
        elif mes == "December":
            return "Diciembre"
        else:
            return "Mes invalido"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=str("Para proceder con la agenda de un turno, seleccione alguna de las siguientes opciones: "))

        fecha_nacimiento= next(tracker.get_latest_entity_values("fecha_nacimiento_bebe"),None)
        [SlotSet("fecha_nacimiento_bebe", fecha_nacimiento)]
        print(f"fecha nac en mostrar turnos: {fecha_nacimiento}")

        #### conexiones
        uid = xmlrpclib.ServerProxy('http://'+server+':'+port+'/xmlrpc/2/common').authenticate(db, user, pwd, {})
        print (uid)
        odoo = xmlrpclib.ServerProxy('http://'+server+':'+port+'/xmlrpc/2/object')
        print (odoo)

        #### consulta pacientes
        # ids = odoo.execute_kw(db, uid, pwd, 'res.partner', 'search', [[]], {'limit': 1})
        # print(odoo.execute_kw(db, uid, pwd, 'res.partner', 'read', [ids]))

        #### consulta turnos agenda
        # id_turnos = odoo.execute_kw(db, uid, pwd, 'appointment.appointment', 'search', [[]], {'limit': 1})
        # print(odoo.execute_kw(db, uid, pwd, 'appointment.appointment', 'read', [id_turnos]))

        today = datetime.now()
        # Calcular la fecha de inicio y fin de la próxima semana
        start_date = today
        end_date = today + timedelta(days=7)
        # Consultar los turnos disponibles en el rango de una semana
        # CORREGIR CONSULTA: ESTA DEVOLVIENDO LOS ESPACIOS OCUPADOS CON TURNOS EN VEZ DE LOS ESPACIOS LIBRES
        turno_ids = odoo.execute_kw(
            db, uid, pwd, 'appointment.appointment', 'search',
            [[
                ('appointment_date', '>=', start_date.strftime('%Y-%m-%d %H:%M:%S')),
                ('appointment_date', '<', end_date.strftime('%Y-%m-%d %H:%M:%S'))
            ]],
            {'order': 'technician_id ASC, appointment_date ASC'}
        )

        opcion = 1
        medicos_procesados = [] 
        medico_ids = [31,32,33]

        global fechas_disponibles

        if turno_ids:
            turnos_disponibles = odoo.execute_kw(
                db, uid, pwd, 'appointment.appointment', 'read', [turno_ids],
                {'fields': ['id', 'appointment_date', 'appointment_stop_date', 'technician_id']}
            )
            for i, turno in enumerate(turnos_disponibles):
                fecha_inicio = turno['appointment_date']
                fecha_fin = turno['appointment_stop_date']
                medico_id = int(turno['technician_id'][0]) if turno['technician_id'] else None

                print(medico_id)
                print(medico_ids)
                print(medicos_procesados)

                # Iterar sobre los médicos asociados a un turno
                for medico_id in medico_ids:
                    # Verificar si el médico ya ha sido procesado
                    if medico_id in medicos_procesados:
                        continue
                    # Verificar si el turno está dentro del horario del médico
                    if medico_id is not None and medico_id in medicos and datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M:%S').strftime('%A').lower() == medicos[medico_id]['dias'][0].lower() and medicos[medico_id]['inicio'] <= fecha_inicio[-8:] <= medicos[medico_id]['fin']:
                        fechas_disponibles.append((turno['id'], fecha_inicio, fecha_fin, medico_id))
                        dia= datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M:%S').strftime('%A')
                        numero_dia= datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M:%S').strftime('%d')
                        mes= datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M:%S').strftime('%B')
                        hora = datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M:%S').strftime('%H:%M')
                        dispatcher.utter_message(text=str(f"*Opción {opcion}:* Médico: {medicos[medico_id]['nombre']} - Fecha y Hora: {self.obtenerDiaEnCastellano(dia)} {numero_dia} de {self.obtenerMesEnCastellano(mes)} a las {hora}hs"))
                        opcion += 1 
                        medicos_procesados.append(medico_id)
                        break  # Romper el bucle interno después de agregar un turno para el médico
            dispatcher.utter_message(text=str(f"*Opción 4:* Consulta telefonica con un operador"))

        #### TURNO HARDCODEADO
        # turno = {
        #     "partner_id": id_paciente, #id de paciente recien agregado
        #     "motivo": '1 VEZ',
        #     "technician_id": 32, # 32=id silvina romero y 33=gaston dech y 31=emanuel ortiz
        #     "appointment_date": '2023-11-14 12:30:00', # la hora real es 3 horas menos
        #     "appointment_stop_date": '2023-11-14 13:00:00', # la hora real es 3 horas menos
        # }

        # #### Borrar paciente
        # odoo.execute_kw(db, uid, pwd, 'res.partner', 'unlink', [[id]])
        # # check if the deleted record is still in the database
        # odoo.execute_kw(db, uid, pwd, 'res.partner', 'search', [[['id', '=', id]]])

        # #### busco el id del paciente con el nombre = x
        # id_paciente= odoo.execute_kw(db, uid, pwd, 'res.partner', 'search', [[['firstname', '=','ximena']]])
        # print(f"el id del paciente X es: {id_paciente}")
        # #### busco los ids de los turnos asociados al paciente = x
        # id_turnoo= odoo.execute_kw(db, uid, pwd, 'appointment.appointment', 'search', [[['partner_id', '=',id_paciente]]])
        # print(f"el id del turno de X es: {id_turnoo}")
        # #### busco todos los datos del turno que yo ingreso por el input
        # id_a_consultar = int(input("Ingrese el id del turno por el cual quiere saber sus datos: "))
        # id_medico= odoo.execute_kw(db, uid, pwd, 'appointment.appointment', 'search', [[['id', '=',id_a_consultar]]])
        # print(odoo.execute_kw(db, uid, pwd, 'appointment.appointment', 'read', [id_medico]))


     
class ActionConfirmacionTurno(Action):

     def name(self) -> Text:
         return "action_confirmacion_turno"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        uid = xmlrpclib.ServerProxy('http://'+server+':'+port+'/xmlrpc/2/common').authenticate(db, user, pwd, {})
        odoo = xmlrpclib.ServerProxy('http://'+server+':'+port+'/xmlrpc/2/object')

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

        semanas_gestacion = int(tracker.get_slot("semanas_gestacion"))
        #fecha_nacimiento= next(tracker.get_latest_entity_values("fecha_nacimiento_bebe"),None)
        fecha_nacimiento = tracker.get_slot("fecha_nacimiento_bebe")
        fecha_nacimiento_obj = datetime.strptime(fecha_nacimiento, '%d-%m-%Y') # convierte a datetime
        fecha_nacimiento_formateada = fecha_nacimiento_obj.strftime('%Y-%m-%d') # formatea el formato al requerido por odoo

        #### creo un diccionario de paciente depediendo de la semana de gestacion (rnt o rnpt)
        if (semanas_gestacion >= 38) and (semanas_gestacion <= 41):
            paciente = {
                "nombre_madre": nombre_completo_mama,
                "firstname": nombre_bebe,
                "lastname": apellido_bebe,
                # "rnt": semanas_gestacion,
                "birthdate_date": fecha_nacimiento_formateada
            }
        elif (semanas_gestacion < 38) and (semanas_gestacion >= 35):
            paciente = {
                "nombre_madre": nombre_completo_mama,
                "firstname": nombre_bebe,
                "lastname": apellido_bebe,
                # "rnpt": semanas_gestacion,
                "birthdate_date": fecha_nacimiento_formateada
            }
        elif (semanas_gestacion < 35) or (semanas_gestacion > 41):
            paciente = {
                "nombre_madre": nombre_completo_mama,
                "firstname": nombre_bebe,
                "lastname": apellido_bebe,
                # "rnpt": 'Otro',
                "birthdate_date": fecha_nacimiento_formateada
            }

        #### creo el paciente en odoo
        id_paciente = odoo.execute_kw(db, uid, pwd, 'res.partner', 'create', [paciente])
        # print(id_paciente)
        # dispatcher.utter_message(text=str("creado paciente"))

        print(f"fechas disponibles: {fechas_disponibles}")                
        if fechas_disponibles:
                opcion_elegida = int(next(tracker.get_latest_entity_values("opcion"),None))
                if opcion_elegida == 4:
                    dispatcher.utter_message(text=str(f"Ya te derivé al sector correspondiente en el transcurso del día se estarán contactando con vos!☺️"))
                elif 1 <= opcion_elegida <= len(fechas_disponibles):
                    turno_seleccionado = fechas_disponibles[opcion_elegida - 1]
                    id_seleccionado, inicio_seleccionado, fin_seleccionado, medico_id_seleccionado = turno_seleccionado
                    print(f"Ha seleccionado la opción {opcion_elegida}: ID: {id_seleccionado} - Médico: {medicos[medico_id_seleccionado]['nombre']} - Fecha y Hora: {inicio_seleccionado} - {fin_seleccionado}")
                    # Sumar 3 horas a las fechas seleccionadas
                    inicio_seleccionado = (datetime.strptime(inicio_seleccionado, '%Y-%m-%d %H:%M:%S') + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
                    fin_seleccionado = (datetime.strptime(fin_seleccionado, '%Y-%m-%d %H:%M:%S') + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
                    #### CREO UN DICCIONARIO DE TURNO ---------------------------------------------------------------------------------------
                    turno = {
                        "partner_id": id_paciente, #id de paciente recien agregado
                        "motivo": '1 VEZ',
                        "technician_id": medico_id_seleccionado,
                        "appointment_date": inicio_seleccionado, # la hora real es 3 horas menos
                        "appointment_stop_date": fin_seleccionado, # la hora real es 3 horas menos
                    }
                    #### CREO EL TURNO EN ODOO ----------------------------------------------------------------------------------------------
                    id_turno = odoo.execute_kw(db, uid, pwd, 'appointment.appointment', 'create', [turno])
                    # Restar 3 horas a las fechas seleccionadas
                    inicio_seleccionado = (datetime.strptime(inicio_seleccionado, '%Y-%m-%d %H:%M:%S') - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
                    fin_seleccionado = (datetime.strptime(fin_seleccionado, '%Y-%m-%d %H:%M:%S') - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
                    # Establecer la configuración regional a español
                    locale.setlocale(locale.LC_TIME, 'es_ES.utf8')
                    dia= datetime.strptime(inicio_seleccionado, '%Y-%m-%d %H:%M:%S').strftime('%A')
                    numero_dia= datetime.strptime(inicio_seleccionado, '%Y-%m-%d %H:%M:%S').strftime('%d')
                    mes= datetime.strptime(inicio_seleccionado, '%Y-%m-%d %H:%M:%S').strftime('%B')
                    hora = datetime.strptime(inicio_seleccionado, '%Y-%m-%d %H:%M:%S').strftime('%H:%M')
                    if medico_id_seleccionado == 32:
                        dispatcher.utter_message(text=str(f"Bien,👌 ya queda agendada la visita de {nombre_completo_bebe} para el día {dia} {numero_dia} de {mes} a las {hora}hs con la Neurocirujana Pediátrica la Dra. {medicos[medico_id_seleccionado]['nombre']}, en nuestros consultorios ubicados en 📍Av. Callao 384, Piso 4º 9, Capital Federal.\nhttps://g.page/PlagiocefaliaArgentina?share\nEl equipo de Plagiocefalia Argentina\nhttps://youtu.be/wrfBgNa0shY")) 
                    else:
                        dispatcher.utter_message(text=str(f"Bien,👌 ya queda agendada la visita de {nombre_completo_bebe} para el día {dia} {numero_dia} de {mes} a las {hora}hs con el Neurocirujano Pediátrico el Dr. {medicos[medico_id_seleccionado]['nombre']}, en nuestros consultorios ubicados en 📍Av. Callao 384, Piso 4º 9, Capital Federal.\nhttps://g.page/PlagiocefaliaArgentina?share\nEl equipo de Plagiocefalia Argentina\nhttps://youtu.be/wrfBgNa0shY")) 
                else:
                    print("Opción no válida. Por favor, ingrese un número de opción válido.")
        else:
            print("No hay turnos disponibles en el rango de la próxima semana.")

        #### BORRAR TURNO DE MÁS
        if id_turno:
            id_turno_a_borrar= id_turno+1
            odoo.execute_kw(db, uid, pwd, 'appointment.appointment', 'unlink', [[id_turno_a_borrar]])
            # chequea que se haya eliminado correctamente:
            # odoo.execute_kw(db, uid, pwd, 'appointment.appointment', 'search', [[['id', '=', id_turno_a_borrar]]])

        
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
