import time
from wifi import connect_wifi
from utils import TaskQueue, new_command, sync_time, elapsed_time, ActionOne, ActionTwo, check_loop_without_events
from api import login, get_task_list, get_time, report_task_done


MAX_LOOPS_WITHOUT_EVENTS = 12 
LOOP_TIME_IN_MINUTES = 15
LOOP_TIME = 60 * LOOP_TIME_IN_MINUTES

# REMEMBER TO COMMENT THE PRINTS WHEN IN PRODUCTION

def main():
    ActionTwo.set_module()
    ActionOne.set_module()
    actions_queue = TaskQueue()
    wifi_object = connect_wifi()
    watch = sync_time(get_time())
    round_ = 0
    loops_without_events = 0

    # print("Conectado?: ", wifi_object.isconnected())
    if not wifi_object.isconnected():
        wifi_object = connect_wifi()
        if wifi_object.isconnected():
            pass
        else:
            loops_without_events = check_loop_without_events(loops_without_events, MAX_LOOPS_WITHOUT_EVENTS)
            loops_without_events += 1
            time.sleep(LOOP_TIME)
        

    while True:
        watch = sync_time(get_time())
        round_ += 1
        # print("Ronda n° ", ronda)
        # print("Revisando Wifi: ", wifi_object.isconnected())
        if not wifi_object.isconnected():
            # print("test wifi dentro del while")
            wifi_object = connect_wifi()
            if wifi_object.isconnected():
                pass
            else:
                loops_without_events = check_loop_without_events(loops_without_events, MAX_LOOPS_WITHOUT_EVENTS)
                loops_without_events += 1
                time.sleep(LOOP_TIME)
                continue
            
        token = login()
        headers = None
        if token != None:
            headers = {
                "Authorization" : f"Token {token}"
            }
        else:
            print("Login Failed")
        tasks_list = get_task_list(headers)
        # print("The List", tasks_list)
        if tasks_list:
            loops_without_events = 0
        else:
            loops_without_events += 1
        for command in tasks_list:
            n_command = new_command(command)
            actions_queue.add_command(n_command)
            # print(f"Orden n°{n_orden.ide} agregada")
        # print("Acciones ", cola_de_acciones)
        
        timer_loop = time.time()
        
        while not elapsed_time(timer_loop, LOOP_TIME_IN_MINUTES):
            timer_minutes = time.time()
            agno, mes, dia, wday, hora, minuto, segundo, microsec = watch.datetime()
            current_time = {
                "mes": mes, 
                "dia": dia,
                "hora": hora,
                "minuto": minuto
            }
            # print(f"Hora actual: {hora_actual['hora']}:{hora_actual['minuto']}")
            for command in list(actions_queue.command_queue.values()):
                if command.get_fecha() == current_time:
                    # print("Procede a ejecutar acción")
                    command.get_accion()
                    codigo_respuesta = report_task_done(command, headers)
                    # print("Acción ejecutada: ", codigo_respuesta)
                    actions_queue.delete_command(command)
            # print(cola_de_acciones)
            while not elapsed_time(timer_minutes, 1):
                time.sleep(1)
        loops_without_events = check_loop_without_events(loops_without_events, MAX_LOOPS_WITHOUT_EVENTS)
            

main()