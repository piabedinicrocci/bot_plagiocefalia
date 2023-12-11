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
import time

db='odoo.plagiocefalia.com.ar'
user='plagiobot'
pwd='plagio2023+-*'
server='odoo.plagiocefalia.com.ar'
port='8069'   

# Definir información de los médicos
medicos = {
    31: {'nombre': 'Emanuel Ortiz', 'dias': ['Thursday'], 'inicio': '09:30:00', 'fin': '14:30:00'},
    32: {'nombre': 'Silvina Romero', 'dias': ['Friday'], 'inicio': '09:00:00', 'fin': '16:30:00'},
    33: {'nombre': 'Gaston Dech', 'dias': ['Monday'], 'inicio': '10:00:00', 'fin': '15:30:00'},
}

fechas_disponibles = []

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
            message="Genial! Te pedimos que nos adjuntes foto del carnet de la misma y posteriormente foto de frente y dorso de tu DNI"
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
        if dia == "Monday" or dia == "monday":
            return "Lunes"
        elif dia == "Tuesday" or dia == "tuesday":
            return "Martes"
        elif dia == "Wednesday" or dia == "wednesday":
            return "Miércoles"
        elif dia == "Thursday" or dia == "thursday":
            return "Jueves"
        elif dia == "Friday" or dia == "friday":
            return "Viernes"
        elif dia == "Saturday" or dia == "saturday":
            return "Sábado"
        elif dia == "Sunday" or dia == "sunday":
            return "Domingo"
        else:
            return "Dia invalido"
        
     def obtenerMesEnCastellano(self, mes):
        if mes == "January" or mes == "january":
            return "Enero"
        elif mes == "February" or mes == "february":
            return "Febrero"
        elif mes == "March" or mes == "march":
            return "Marzo"
        elif mes == "April" or mes == "april":
            return "Abril"
        elif mes == "May" or mes == "may":
            return "Mayo"
        elif mes == "June" or mes == "june":
            return "Junio"
        elif mes == "July" or mes == "july":
            return "Julio"
        elif mes == "August" or mes == "august":
            return "Agosto"
        elif mes == "September" or mes == "september":
            return "Septiembre"
        elif mes == "October" or mes == "october":
            return "Octubre"
        elif mes == "November" or mes == "november":
            return "Noviembre"
        elif mes == "December" or mes == "december":
            return "Diciembre"
        else:
            return "Mes invalido"
    
     def obtenerDiaEnIngles(self, dia):
        if dia == "Lunes" or dia == "lunes":
            return "Monday"
        elif dia == "Martes" or dia == "martes":
            return "Tuesday"
        elif dia == "Miercoles" or dia == "miercoles":
            return "Wednesday"
        elif dia == "Jueves" or dia == "jueves":
            return "Thursday"
        elif dia == "Viernes" or dia == "viernes":
            return "Friday"
        elif dia == "Sabado" or dia == "sabado":
            return "Saturday"
        elif dia == "Domingo" or dia == "domingo":
            return "Sunday"
        else:
            return "Dia invalido"
    
     def obtenerMesEnIngles(self, mes):
        if mes == "Enero" or mes == "enero":
            return "January"
        elif mes == "Febrero" or mes == "febrero":
            return "February"
        elif mes == "Marzo" or mes == "marzo":
            return "March"
        elif mes == "Abril" or mes == "abril":
            return "April"
        elif mes == "Mayo" or mes == "mayo":
            return "May"
        elif mes == "Junio" or mes == "junio":
            return "June"
        elif mes == "Julio" or mes == "julio":
            return "July"
        elif mes == "Agosto" or mes == "agosto":
            return "August"
        elif mes == "Septiembre" or mes == "septiembre":
            return "September"
        elif mes == "Octubre" or mes == "octubre":
            return "October"
        elif mes == "Noviembre" or mes == "noviembre":
            return "November"
        elif mes == "Diciembre" or mes == "diciembre":
            return "December"
        else:
            return "Mes invalido"
     
     def noSeCruzaConOtroTurno(self, fecha_inicio, fecha_fin, turnos_ocupados):
        for i, turno in enumerate(turnos_ocupados):
            print(i)
            fecha_inicio_turno = datetime.strptime(turno['appointment_date'], '%Y-%m-%d %H:%M:%S') - timedelta(hours=3)
            fecha_fin_turno = datetime.strptime(turno['appointment_stop_date'], '%Y-%m-%d %H:%M:%S') - timedelta(hours=3)
            print (fecha_inicio)
            print(fecha_inicio_turno)
            print(fecha_fin)
            print(fecha_fin_turno)
            if fecha_inicio < fecha_fin_turno and fecha_fin > fecha_inicio_turno:
                return False
        return True

     def obtenerTurnosDisponibles(self, fecha_inicio, fecha_fin, turnos_ocupados, medico_id, turnos_disponibles):
        while fecha_inicio < fecha_fin:
            final_actual = fecha_inicio + timedelta(minutes=30)
            if final_actual <= fecha_fin and self.noSeCruzaConOtroTurno(fecha_inicio, final_actual, turnos_ocupados):
                opcion_turno = {
                    "technician_id": medico_id,
                    "appointment_date": fecha_inicio.strftime('%Y-%m-%d %H:%M:%S'),
                    "appointment_stop_date": final_actual.strftime('%Y-%m-%d %H:%M:%S'),
                }
                turnos_disponibles.append(opcion_turno)
            fecha_inicio += timedelta(minutes=15)  

     def obtenerPosicionTurnoMedico(self, turnos_disponibles, medico_id, debe_ser_maniana, debe_ser_tarde):
        posicion_turno_parcial = -1
        for i, turno in enumerate(turnos_disponibles):
            fecha_inicio = turno['appointment_date']
            if (datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M:%S').strftime('%A').lower() == 'lunes') or (datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M:%S').strftime('%A').lower() == 'martes') or (datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M:%S').strftime('%A').lower() == 'miercoles') or (datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M:%S').strftime('%A').lower() == 'jueves') or (datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M:%S').strftime('%A').lower() == 'viernes') or (datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M:%S').strftime('%A').lower() == 'sabado') or (datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M:%S').strftime('%A').lower() == 'domingo'):
                if (self.obtenerDiaEnIngles(datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M:%S').strftime('%A')) == medicos[medico_id]['dias'][0]) and medicos[medico_id]['inicio'] <= fecha_inicio[-8:] <= medicos[medico_id]['fin'] and ((datetime.strptime(fecha_inicio[-8:], '%H:%M:%S') > datetime.strptime('12:00:00', '%H:%M:%S') and debe_ser_tarde == True) or (datetime.strptime(fecha_inicio[-8:], '%H:%M:%S') <= datetime.strptime('12:00:00', '%H:%M:%S') and debe_ser_maniana == True)):
                    return i
                elif (self.obtenerDiaEnIngles(datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M:%S').strftime('%A')) == medicos[medico_id]['dias'][0]) and medicos[medico_id]['inicio'] <= fecha_inicio[-8:] <= medicos[medico_id]['fin'] and posicion_turno_parcial == -1:
                    posicion_turno_parcial = i
            else:
                if datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M:%S').strftime('%A').lower() == medicos[medico_id]['dias'][0].lower() and medicos[medico_id]['inicio'] <= fecha_inicio[-8:] <= medicos[medico_id]['fin'] and ((datetime.strptime(fecha_inicio[-8:], '%H:%M:%S') > datetime.strptime('12:00:00', '%H:%M:%S') and debe_ser_tarde == True) or (datetime.strptime(fecha_inicio[-8:], '%H:%M:%S') <= datetime.strptime('12:00:00', '%H:%M:%S') and debe_ser_maniana == True)):
                    return i
                elif datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M:%S').strftime('%A').lower() == medicos[medico_id]['dias'][0].lower() and medicos[medico_id]['inicio'] <= fecha_inicio[-8:] <= medicos[medico_id]['fin'] and posicion_turno_parcial == -1:
                    posicion_turno_parcial = i
        return posicion_turno_parcial

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=str("Para proceder con la agenda de un turno, seleccione alguna de las siguientes opciones: "))

        fecha_nacimiento= next(tracker.get_latest_entity_values("fecha_nacimiento_bebe"),None)
        [SlotSet("fecha_nacimiento_bebe", fecha_nacimiento)]

        #### conexiones
        uid = xmlrpclib.ServerProxy('http://'+server+':'+port+'/xmlrpc/2/common').authenticate(db, user, pwd, {})
        print (uid)
        odoo = xmlrpclib.ServerProxy('http://'+server+':'+port+'/xmlrpc/2/object')
        print (odoo)

        today = datetime.now()
        # Calcular la fecha de inicio y fin de la próxima semana
        start_date = today
        end_date = (today + timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
        # Consultar los turnos disponibles en el rango de una semana

        opcion = 1
        medico_ids = [33,31,32]

        global fechas_disponibles

        global debe_ser_maniana
        global debe_ser_tarde
        debe_ser_maniana = True
        debe_ser_tarde = True

        for medico_id in medico_ids:
            turno_ids = []
            turno_ids = odoo.execute_kw(
                db, uid, pwd, 'appointment.appointment', 'search',
                [[
                    ('appointment_date', '>=', start_date.strftime('%Y-%m-%d %H:%M:%S')),
                    ('appointment_date', '<', end_date.strftime('%Y-%m-%d %H:%M:%S')),
                    ('technician_id', '=', int(medico_id))
                ]],
                {'order': 'technician_id ASC, appointment_date ASC'}
            )
            turnos_ocupados = []
            turnos_ocupados = odoo.execute_kw(
                db, uid, pwd, 'appointment.appointment', 'read', [turno_ids],
                {'fields': ['id', 'appointment_date', 'appointment_stop_date', 'technician_id']}
            )
            turnos_disponibles = []
            print(turnos_ocupados)
            dia = medicos[medico_id]['dias'][0]
            if (dia == "Monday"):
                proxima_fecha_asociada = (today + timedelta(days=((7 - today.weekday()) % 7))).replace(hour=0, minute=0, second=0, microsecond=0)
            elif (dia == "Tuesday"):
                proxima_fecha_asociada = (today + timedelta(days=((1 - today.weekday()) % 7))).replace(hour=0, minute=0, second=0, microsecond=0)
            elif (dia == "Wednesday"):
                proxima_fecha_asociada = (today + timedelta(days=((2 - today.weekday()) % 7))).replace(hour=0, minute=0, second=0, microsecond=0)
            elif (dia == "Thursday"):
                proxima_fecha_asociada = (today + timedelta(days=((3 - today.weekday()) % 7))).replace(hour=0, minute=0, second=0, microsecond=0)
            elif (dia == "Friday"):
                proxima_fecha_asociada = (today + timedelta(days=((4 - today.weekday()) % 7))).replace(hour=0, minute=0, second=0, microsecond=0)
            elif (dia == "Saturday"):
                proxima_fecha_asociada = (today + timedelta(days=((5 - today.weekday()) % 7))).replace(hour=0, minute=0, second=0, microsecond=0)
            elif (dia == "Sunday"):
                proxima_fecha_asociada = (today + timedelta(days=((6 - today.weekday()) % 7))).replace(hour=0, minute=0, second=0, microsecond=0)
            horario_inicio = datetime.strptime(medicos[medico_id]['inicio'], '%H:%M:%S').time()
            fecha_hora_completa_inicio = datetime.combine(proxima_fecha_asociada.date(), horario_inicio)
            print(f'Fecha y Hora completa inicio: {fecha_hora_completa_inicio}')
            horario_final = datetime.strptime(medicos[medico_id]['fin'], '%H:%M:%S').time()
            fecha_hora_completa_final = datetime.combine(proxima_fecha_asociada.date(), horario_final)
            print(f'Fecha y Hora completa final: {fecha_hora_completa_final}')
            self.obtenerTurnosDisponibles(fecha_hora_completa_inicio, fecha_hora_completa_final, turnos_ocupados, medico_id, turnos_disponibles)
            print(turnos_disponibles)
            posicion_turno_medico = self.obtenerPosicionTurnoMedico(turnos_disponibles, medico_id, debe_ser_maniana, debe_ser_tarde)
            print(posicion_turno_medico)
            if (posicion_turno_medico > -1):
                turno = list(turnos_disponibles)[posicion_turno_medico]
                fecha_inicio = turno['appointment_date']
                fecha_fin = turno['appointment_stop_date']
                fechas_disponibles.append((fecha_inicio, fecha_fin, medico_id))
                dia= datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M:%S').strftime('%A')
                numero_dia= datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M:%S').strftime('%d')
                mes= datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M:%S').strftime('%B')
                hora = datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M:%S').strftime('%H:%M')
                if (dia.lower() == 'monday') or (dia.lower() == 'tuesday') or (dia.lower() == 'wednesday') or (dia.lower() == 'thursday') or (dia.lower() == 'friday') or (dia.lower() == 'saturday') or (dia.lower() == 'sunday'):
                    if (mes.lower() == 'january') or (mes.lower() == 'february') or (mes.lower() == 'march') or (mes.lower() == 'april') or (mes.lower() == 'may') or (mes.lower() == 'june') or (mes.lower() == 'july') or (mes.lower() == 'august') or (mes.lower() == 'september') or (mes.lower() == 'october') or (mes.lower() == 'november') or (mes.lower() == 'december'):
                        dispatcher.utter_message(text=str(f"*Opción {opcion}:* Médico: {medicos[medico_id]['nombre']} - Fecha y Hora: {self.obtenerDiaEnCastellano(dia)} {numero_dia} de {self.obtenerMesEnCastellano(mes)} a las {hora}hs"))
                    else:
                        dispatcher.utter_message(text=str(f"*Opción {opcion}:* Médico: {medicos[medico_id]['nombre']} - Fecha y Hora: {self.obtenerDiaEnCastellano(dia)} {numero_dia} de {mes.capitalize()} a las {hora}hs"))
                else:
                    if (mes.lower() == 'january') or (mes.lower() == 'february') or (mes.lower() == 'march') or (mes.lower() == 'april') or (mes.lower() == 'may') or (mes.lower() == 'june') or (mes.lower() == 'july') or (mes.lower() == 'august') or (mes.lower() == 'september') or (mes.lower() == 'october') or (mes.lower() == 'november') or (mes.lower() == 'december'):
                        dispatcher.utter_message(text=str(f"*Opción {opcion}:* Médico: {medicos[medico_id]['nombre']} - Fecha y Hora: {dia.capitalize()} {numero_dia} de {self.obtenerMesEnCastellano(mes)} a las {hora}hs"))
                    else:
                        dispatcher.utter_message(text=str(f"*Opción {opcion}:* Médico: {medicos[medico_id]['nombre']} - Fecha y Hora: {dia.capitalize()} {numero_dia} de {mes.capitalize()} a las {hora}hs"))
                opcion += 1
                if datetime.strptime(fecha_inicio[-8:], '%H:%M:%S') > datetime.strptime('12:00:00', '%H:%M:%S'):
                    debe_ser_maniana = True
                    debe_ser_tarde = False
                else:
                    debe_ser_maniana = False
                    debe_ser_tarde = True

        dispatcher.utter_message(text=str(f"*Opción {opcion}:* Consulta telefónica con un operador"))

        #### TURNO HARDCODEADO
        # turno = {
        #     "partner_id": id_paciente, #id de paciente recien agregado
        #     "motivo": '1 VEZ',
        #     "technician_id": 32, # 32=id silvina romero y 33=gaston dech y 31=emanuel ortiz
        #     "appointment_date": '2023-11-14 12:30:00', # la hora real es 3 horas menos
        #     "appointment_stop_date": '2023-11-14 13:00:00', # la hora real es 3 horas menos
        # }

        # #### Busco el id del paciente con el nombre = x
        # id_paciente_a_buscar= odoo.execute_kw(db, uid, pwd, 'res.partner', 'search', [[['lastname', '=','crocci']]])
        # print(f"el id del paciente X es: {id_paciente_a_buscar}")
        # print(odoo.execute_kw(db, uid, pwd, 'res.partner', 'read', [id_paciente_a_buscar]))
        # #### Borrar paciente
        # odoo.execute_kw(db, uid, pwd, 'res.partner', 'unlink', [[id_paciente_a_buscar]])
        # # chequeo si el registro que acabo de eliminar existe
        # odoo.execute_kw(db, uid, pwd, 'res.partner', 'search', [[['id', '=', id_paciente_a_buscar]]])

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

        semanas_gestacion = str(tracker.get_slot("semanas_gestacion"))
        #fecha_nacimiento= next(tracker.get_latest_entity_values("fecha_nacimiento_bebe"),None)
        fecha_nacimiento = tracker.get_slot("fecha_nacimiento_bebe")
        fecha_nacimiento_obj = datetime.strptime(fecha_nacimiento, '%d-%m-%Y') # convierte a datetime
        fecha_nacimiento_formateada = fecha_nacimiento_obj.strftime('%Y-%m-%d') # formatea el formato al requerido por odoo

        #### creo un diccionario de paciente depediendo de la semana de gestacion (rnt o rnpt)
        if (semanas_gestacion >= '38') and (semanas_gestacion <= '41'):
            paciente = {
                "paciente": True,
                "nombre_madre": nombre_completo_mama.title(),
                "firstname": nombre_bebe.title(),
                "lastname": apellido_bebe.title(),
                "rnt": semanas_gestacion,
                "rnpt_otro": False,
                "birthdate_date": fecha_nacimiento_formateada
            }
        elif (semanas_gestacion < '38') and (semanas_gestacion >= '35'):
            paciente = {
                "paciente": True,
                "nombre_madre": nombre_completo_mama.title(),
                "firstname": nombre_bebe.title(),
                "lastname": apellido_bebe.title(),
                "rnpt": semanas_gestacion,
                "rnpt_otro": False,
                "birthdate_date": fecha_nacimiento_formateada
            }
        elif (semanas_gestacion < '35') or (semanas_gestacion > '41'):
            paciente = {
                "paciente": True,
                "nombre_madre": nombre_completo_mama.title(),
                "firstname": nombre_bebe.title(),
                "lastname": apellido_bebe.title(),
                "rnpt": 'otro',
                "rnpt_otro": True,
                "birthdate_date": fecha_nacimiento_formateada
            }

        #### creo el paciente en odoo
        id_paciente = odoo.execute_kw(db, uid, pwd, 'res.partner', 'create', [paciente])
        print("id paciente recien agregado: {id_paciente}")
        # dispatcher.utter_message(text=str("creado paciente"))

        print(f"fechas disponibles: {fechas_disponibles}")                
        if fechas_disponibles:
                opcion_elegida = int(next(tracker.get_latest_entity_values("opcion"),None))
                if opcion_elegida == 4:
                    dispatcher.utter_message(text=str(f"Ya te derivé al sector correspondiente en el transcurso del día se estarán contactando con vos!☺️"))
                elif 1 <= opcion_elegida <= len(fechas_disponibles):
                    turno_seleccionado = fechas_disponibles[opcion_elegida - 1]
                    inicio_seleccionado, fin_seleccionado, medico_id_seleccionado = turno_seleccionado
                    print(f"Ha seleccionado la opción {opcion_elegida}: Médico: {medicos[medico_id_seleccionado]['nombre']} - Fecha y Hora: {inicio_seleccionado} - {fin_seleccionado}")
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
                    #### BORRAR TURNO DE MÁS
                    if id_turno:
                        id_turno_a_borrar= id_turno+1
                        odoo.execute_kw(db, uid, pwd, 'appointment.appointment', 'unlink', [[id_turno_a_borrar]])
                        # chequea que se haya eliminado correctamente:
                        # odoo.execute_kw(db, uid, pwd, 'appointment.appointment', 'search', [[['id', '=', id_turno_a_borrar]]])
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
                        dispatcher.utter_message(text=str(f"Bien,👌 ya queda agendada la visita de {nombre_completo_bebe.title()} para el día {dia.title()} {numero_dia} de {mes.title()} a las {hora}hs con la Neurocirujana Pediátrica la Dra. {medicos[medico_id_seleccionado]['nombre']}, en nuestros consultorios ubicados en 📍Av. Callao 384, Piso 4º 9, Capital Federal.\nhttps://g.page/PlagiocefaliaArgentina?share\nEl equipo de Plagiocefalia Argentina\nhttps://youtu.be/wrfBgNa0shY")) 
                    else:
                        dispatcher.utter_message(text=str(f"Bien,👌 ya queda agendada la visita de {nombre_completo_bebe.title()} para el día {dia.title()} {numero_dia} de {mes.title()} a las {hora}hs con el Neurocirujano Pediátrico el Dr. {medicos[medico_id_seleccionado]['nombre']}, en nuestros consultorios ubicados en 📍Av. Callao 384, Piso 4º 9, Capital Federal.\nhttps://g.page/PlagiocefaliaArgentina?share\nEl equipo de Plagiocefalia Argentina\nhttps://youtu.be/wrfBgNa0shY")) 
                else:
                    print("Opción no válida. Por favor, ingrese un número de opción válido.")
        else:
            print("No hay turnos disponibles en el rango de la próxima semana.")

        
class ActionFotos(Action):

     def name(self) -> Text:
         return "action_fotos"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #  print("Antes de sleep:", time.time())
        #  time.sleep(10)
        #  print("Después de sleep:", time.time())
         message="¡Perfecto! Para poder derivarte al sector de presupuesto y coordinación de turno para la toma de molde, vamos a solicitarle los siguientes datos:"
         dispatcher.utter_message(text=str(message))
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
            time.sleep(10)
            return [SlotSet("nombre_n", nombre_sin_comillas)]
        elif (ultima_accion_completada == 'utter_pregunta_nombre_bebe'):
            dispatcher.utter_message(text=str(f"Qué lindo nombre! ¿Y con cuántas semanas de gestación nació {nombre_sin_comillas}? "))
            return [SlotSet("nombre_b", nombre_sin_comillas)]
        return []
