# Microcontroller API Server

Web application to set commands for microcontrollers.

Through a loop, the microcontroller fetch the API to get commands to be executed by it. 

The example script for microcontroller, made with MicroPython, includes a Servomotor Adapter Class. The two basic commands loaded on the microcontroller can move a Servomotor or activate a Reele.

New commands can be added to the microcontroller and the API on the Comando model on the app_comando. It can be used any microcontroller with internet connection.

## API Server

The web application is made with django and django rest framework, it is setted to post two different instructions to be fetched by the microcontroller.

The microcontroller client must have an username and password to connect to the server, the same way that the user client also needs an account to login on the app.
