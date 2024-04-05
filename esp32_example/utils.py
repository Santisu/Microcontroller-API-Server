import time
from servo import Servo
from machine import RTC, Pin

class TaskQueue:
    def __init__(self):
        self.command_queue = {}

    def add_command(self, command):
        command_id = command.ide
        self.command_queue[command_id] = command

    def delete_command(self, command):
        command_id = command.ide
        if command_id in self.command_queue:
            del self.command_queue[command_id]
            return f"Command with ID {command_id} deleted from the queue."
        else:
            return f"Command with ID {command_id} not found in the queue."

    def __str__(self) -> str:
        return str(self.command_queue)

class Command:
    def __init__(self, ide, mes, dia, hora, minuto, accion):
        self.ide = ide
        self.mes = mes
        self.dia = dia
        self.hora = hora
        self.minuto = minuto
        self.accion = accion
        self.hora_ejecucion = f"{mes}-{dia}-{hora}-{minuto}"

    def get_accion(self):
        return self.accion()

    def get_fecha(self):
        return {
            "mes": self.mes,
            "dia": self.dia,
            "hora": self.hora,
            "minuto": self.minuto
        }
    def __str__(self) -> str:
        return f"{self.ide} - {self.mes}/{self.dia} - {self.hora}:{self.minuto} - {self.accion}"


class ActionTwo():
    rele = Pin(4, Pin.OUT)
    rele.on()

    @staticmethod
    def set_module():
        ActionTwo.rele.off()
        time.sleep(2)
        ActionTwo.rele.on()
        

    @staticmethod
    def execute():
        ActionTwo.rele.off()
        time.sleep(20)
        ActionTwo.rele.on()

class ActionOne():
    MOVEMENT_DEGREE = 13
    servo = Servo(pin=2)
    servo.move(MOVEMENT_DEGREE)
    
    @staticmethod
    def set_module():
        ActionOne.servo.move(ActionOne.MOVEMENT_DEGREE)
        time.sleep(0.5)
        ActionOne.servo.move(45)
        time.sleep(0.5)
        ActionOne.servo.move(ActionOne.MOVEMENT_DEGREE)
        time.sleep(0.5)
        ActionOne.servo.stop()

    @staticmethod
    def execute():
        ActionOne.servo.move(45)
        time.sleep(0.8)
        ActionOne.servo.move(ActionOne.MOVEMENT_DEGREE)
        time.sleep(0.5)
        ActionOne.servo.stop()


def new_command(command):
    """
    Receives a dictionary with information to create an object Order and returns the object

    Args:
        orden (dict): Diccionario con información para crear objeto orden.
            Ejemplo:
            {
                "id" : 1,
                "mes" : 12,
                "dia" : 15,
                "hora" : 22,
                "minuto" : 3,
                "accion" : "dar_comida"
            }

    Returns:
        Orden: Objeto orden.
    """ 
    command_action = asign_command(command["accion"])
    n_orden = Command(
        ide=command["id"],
        mes=command["mes"],
        dia=command["dia"],
        hora=command["hora"],
        minuto=command["minuto"],
        accion=command_action
    )
    return n_orden

def asign_command(action:str) -> Any:
    """
    Receives a string with the action to assign to the object,
    and returns the action to store in its attributes.

    Args:
        accion (str): String with the action "action_2"|"action_1".

    Returns:
        func: .execute method of the class ActionTwo or ActionOne.
    """
    if action == "action_2":
        return ActionTwo.execute
    elif action == "action_1":
        return ActionOne.execute
    else:
        return None


def sync_time(time_dict:dict) -> object:
    """
    Create a RTC with the time received in the dictionary

    Args:
        time_dict (dict): Dict with parsed time.
            Used Values:
                {
                    "year": 2023, 
                    "month": 12, 
                    "day": 15, 
                    "hour": 11, 
                    "min": 47, 
                    "sec": 6, 
                    "wday": 4, 
                }

    Returns:
        object: Objeto RTC - Real Time Clock
    """
    watch = RTC()
    if time_dict:
        watch.datetime((
                time_dict["year"],
                time_dict["month"],
                time_dict["day"],
                time_dict["wday"],
                time_dict["hour"],
                time_dict["min"],
                time_dict["sec"],
                0
            )
        )
    return watch

def elapsed_time(timer:int, minutes:int) -> bool:
    current_time = time.time()
    elapsed = current_time - timer
    if elapsed >= (minutes * 60):
        return True
    return False


def check_loop_without_events(loops:int, max_loops:int):
    """
    Set the quantity of loops that can be executed without events,
    if the loops is greater than max_loops, it executes the actions.
    """
    if loops >= max_loops:
        ActionOne.execute()
        time.sleep(1)
        ActionTwo.execute()
        time.sleep(1)
        return 0
    else:
        return loops
