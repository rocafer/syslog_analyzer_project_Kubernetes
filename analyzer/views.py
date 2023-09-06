from django.shortcuts import render

# Create your views here.

# analyzer/views.py
#import pdb

from django.http import HttpResponse

import os
import datetime
import sqlite3

import re
import openai
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UploadFileForm, ShowAnswerForm
from .models import UploadedFile, FoundError
from .models import Logs

import json
from django.http import JsonResponse



current_time = datetime.datetime.now()

#conn = sqlite3.connect('Linuxtrbl.db')
#c = conn.cursor()




openai.api_key = "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"  # Reemplaza con tu API key





# ... (otros códigos)



# ... (otros códigos)


def chat_consult():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",
                   "content": "I have the following problem in Linux: " + "file not found" + " My question is: How to fix the problem?"}]
    )
    answer = response.choices[0].message.content
    print("Respuesta del Chat GPT:  ", answer)



def hola(request):
    with open('registro_seleccionado.txt', 'r') as file:
        data = file.read()

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",
                   "content": "I have the following problem in Linux: " + data + " My question is: How to fix the problem?"}]
    )
    answer = response.choices[0].message.content

    #print("Hola!")
    #message = 'Hola a Todos!'
    #message2 = 'Hola a Todos, Hi!'
    #return HttpResponse("Proceso Terminado!")
    #return render(request, 'analyzer/chat_consulta.html', {'message': message})


    return render(request, 'analyzer/chat_consulta.html', {'message': data, 'message2': answer})



def get_selected_registro(request):
    try:
        with open('registro_seleccionado.txt', 'r') as file:
            data = file.read()



            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user",
                           "content": "I have the following problem in Linux: " + data + " My question is: How to fix the problem?"}]
            )
            answer = response.choices[0].message.content
            print("Respuesta del Chat GPT:  ", answer)



            return HttpResponse(data, content_type='text/plain')
    except Exception as e:
        return HttpResponse('Error al cargar el archivo.', content_type='text/plain', status=500)



def seleccionar_registro(request):
    if request.method == 'POST':
        registro_id = request.POST.get('registro_id')
        if registro_id:
            try:
                registro = Logs.objects.get(ID=registro_id)
                message = registro.message




                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user",
                               "content": "I have the following problem in Linux: " + message + " My question is: How to fix the problem?"}]
                )
                answer = response.choices[0].message.content

                return render(request, 'analyzer/chat_consulta.html', {'message': message, 'message2': answer})

                # Guardar el contenido del campo "message" en el archivo texto
                #with open('registro_seleccionado.txt', 'w') as file:
                 #   file.write(message)

                # Puedes agregar un mensaje de éxito si lo deseas
                messages.success(request, "Registro seleccionado y guardado en el archivo 'registro_seleccionado.txt'.")

            except Logs.DoesNotExist:
                # Puedes agregar un mensaje de error si el registro no se encuentra
                messages.error(request, "El registro seleccionado no existe.")

        else:
            # Puedes agregar un mensaje de error si no se ha seleccionado ningún registro
            messages.error(request, "Por favor, seleccione un registro antes de continuar.")

        return redirect('consulta_registros')  # Redirigir a la página de consulta de registros
    else:
        # Si se intenta acceder directamente a esta vista sin un POST, redirigir a la página de consulta de registros
        return redirect('consulta_registros')

# ... (otros códigos)






def get_db_connection():
    return sqlite3.connect('db.sqlite3')


def ver_un_registro(request):
    registro_id = 34926
    try:
        registro = Logs.objects.filter(ID=registro_id).values('message').first()
        if registro:
            message = registro['message']
        else:
            message = "No se encontró el registro con ID=34926"
    except Exception as e:
        error_message = f"Error al obtener el registro: {str(e)}"
        message = f"Error: {error_message}"

    return render(request, 'analyzer/un_registro.html', {'message': message})


def agrupar_registros(registro):
    try:
        #print("Funcion clasificar_registro....")
        #print("Registro.-  ", registro)
        #print("Presiona Enter para continuar...")
        #input()  # El prog

        # Clasificar el registro y retornar la clasificación
        palabras_clave = ['networkmanager', 'kernel']

        # Check if registro is of type bytes
        if isinstance(registro, bytes):
            valor = registro.decode('utf-8').lower()
        else:
            valor = registro.lower()

        for keyword in palabras_clave:
            if keyword in valor:
                return keyword.capitalize()  # Devolver la palabra clave con la primera letra en mayúscula

        return "Linux"  # Si no se encuentra ninguna palabra clave, se clasifica como "General"
    except Exception as e:
        # Capturar cualquier excepción que pueda ocurrir durante la lectura
        error_message = f"Error al Clasificar Registros: {str(e)}"
        print("Funcion Clasificar Registros.- Error:  ", error_message)
        print("Presiona Enter para continuar...")
        input()  # El prog


def inicio_proyecto(request, form):
    try:
        #print("Funcion inicio_proyecto....")
        create_table()
        #pdb.set_trace()
        delete_all()
    except Exception as e:
        # Capturar cualquier excepción que pueda ocurrir durante la lectura
        error_message = f"Error al analizar el archivo: {str(e)}"
        print("Funcion inicio_proyecto.- Error:  ", error_message)
        return render(request, 'analyzer/upload.html', {'form': form, 'error_message': error_message})


def delete_all():
    conn = get_db_connection()  # Obtener una nueva conexión local
    c = conn.cursor()  # Obtener un nuevo cursor

    c.execute("DELETE FROM analyzer_logs")
    conn.commit()


def update_data():
    conn = get_db_connection()  # Obtener una nueva conexión local
    c = conn.cursor()  # Obtener un nuevo cursor

    c.execute("UPDATE analyzer_logs SET type='ERROR' WHERE type='fail' OR type='err' OR type='error' OR type='Fail' OR type='Err'")
    #c.execute("UPDATE logs SET type='ERROR' WHERE type='Could' OR type='could'")
    c.execute("UPDATE analyzer_logs SET type='ERROR' WHERE type IN ('Could', 'could')")

    conn.commit()


def create_table():
    conn = get_db_connection()  # Obtener una nueva conexión local
    c = conn.cursor()  # Obtener un nuevo cursor
    c.execute('CREATE TABLE IF NOT EXISTS analyzer_logs (ID INTEGER PRIMARY KEY AUTOINCREMENT, group_name TEXT, type TEXT, message TEXT, currdate TIMESTAMP)')
    conn.commit()
    conn.close()  # Cerrar la conexión al finalizar



def clasificar_registro(registro):
    try:
        #print("Funcion clasificar_registro....")
        #print("Registro.-  ", registro)
        #print("Presiona Enter para continuar...")
        #input()  # El prog

        # Clasificar el registro y retornar la clasificación
        palabras_clave = ['err', 'fail', 'error', 'warning', 'info', 'could']

        # Check if registro is of type bytes
        if isinstance(registro, bytes):
            valor = registro.decode('utf-8').lower()
        else:
            valor = registro.lower()

        for keyword in palabras_clave:
            if keyword in valor:
                return keyword.capitalize()  # Devolver la palabra clave con la primera letra en mayúscula

        return "General"  # Si no se encuentra ninguna palabra clave, se clasifica como "General"
    except Exception as e:
        # Capturar cualquier excepción que pueda ocurrir durante la lectura
        error_message = f"Error al Clasificar Registros: {str(e)}"
        print("Funcion Clasificar Registros.- Error:  ", error_message)
        print("Presiona Enter para continuar...")
        input()  # El prog


def nueva_agrupacion(registro):
    try:

        # Clasificar el registro y retornar la clasificación
        palabras_clave = ['err', 'fail', 'error', 'warning', 'info', 'could']

        # Check if registro is of type bytes
        if isinstance(registro, bytes):
            valor = registro.decode('utf-8').lower()
        else:
            valor = registro.lower()

        for keyword in palabras_clave:
            if keyword in valor:
                return keyword.capitalize()  # Devolver la palabra clave con la primera letra en mayúscula

        return "General"  # Si no se encuentra ninguna palabra clave, se clasifica como "General"
    except Exception as e:
        # Capturar cualquier excepción que pueda ocurrir durante la lectura
        error_message = f"Error al Clasificar Registros: {str(e)}"
        print("Funcion Clasificar Registros.- Error:  ", error_message)
        print("Presiona Enter para continuar...")
        input()  # El prog




def mostrar_registro(registro):
    try:
        #print("Funcion mostrar_registro...")
        #print("Registro.- ", registro)

        #return HttpResponse("Pregunta en mostrar_registro!")
        # Convert registro to a string if it is a list
        if isinstance(registro, list):
            registro = " ".join(registro)

        # Agregar una columna con la clasificación al registro completo
        #return HttpResponse("Empieza clasificacion!")
        clasificacion = clasificar_registro(registro)

        #return HttpResponse("Empieza registro_con_clasificacion!")
        registro_con_clasificacion = [clasificacion] + registro.split()

        #return HttpResponse("Empieza agrupacion!")
        agrupacion = agrupar_registros(registro)

        # Obtener una nueva conexión local

        #return HttpResponse("Obtener conexion!")

        conn = get_db_connection()
        c = conn.cursor()

        #return HttpResponse("Se termino de obtener la conexion!!")

        # Insertar datos en la base de datos
        group = agrupacion
        tipo = clasificacion
        message = " ".join(registro)
        #print("Imprimiendo: Grupo:  ", group)
        #print("Imprimiendo: Tipo:  ", tipo)
        #print("Imprimiendo: Tipo:  ", message)

        #print("Insertando Registro.-")
        #print("Presiona Enter para continuar...")
        #input()  # El prog

        #return HttpResponse("Se ejecuta el Insert!")

        c.execute("INSERT INTO analyzer_logs (group_name, type, message, currdate) VALUES (?, ?, ?, ?)", (group, tipo, message, current_time))
        conn.commit()  # Guardar los cambios en la base de datos

        #return HttpResponse("Se inserto el registro!")


        # Cerrar la conexión al finalizar
        conn.close()

        # Resto del código...
    except Exception as e:
        # Capturar cualquier excepción que pueda ocurrir durante la lectura
        error_message = f"Error al Mostrar o Insertar Registros: {str(e)}"
        print("Funcion Mostrar Registros.- Error:  ", error_message)



# analyzer/views.py

def upload_action(request):
    #print("Funcion upload_action...")
    form = UploadFileForm()
    inicio_proyecto(request, form)  # Llamada a la función inicio_proyecto

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            try:
                # Leer el archivo línea por línea y procesar cada línea
                for line in uploaded_file:
                    # Procesar la línea aquí
                    # Hacemos el split de la línea
                    datos_registro = [elemento.decode('utf-8') for elemento in line.split()]

                    #print("Imprimiendo...",datos_registro)
                    # Mostramos el registro
                    #return HttpResponse("Se ejecuta mostrar Registro!")
                    mostrar_registro(datos_registro)
                    pass

                # Si llegamos hasta aquí, el análisis del archivo fue exitoso

               # return HttpResponse("Se termina el ciclo de Leer el archivo linea por linea!")
                update_data()

                #return HttpResponse("Se ejecuto el update_data!")

                registros = Logs.objects.order_by('group_name', 'type')


                #return HttpResponse("Se ejecuto registros!")


                #return HttpResponse("Analisis del Archivo exitoso!")

                #print("Proceso terminado.....")
                #print("Presiona Enter para continuar...")
                #input()  # El prog

                return render(request, 'analyzer/consulta.html', {'registros': registros})
                #return render(request, 'analyzer/results.html', {'file_path': uploaded_file.name})
            except Exception as e:
                # Capturar cualquier excepción que pueda ocurrir durante la lectura
                error_message = f"Error al analizar el archivo: {str(e)}"
                return render(request, 'analyzer/upload.html', {'form': form, 'error_message': error_message})
    else:
        form = UploadFileForm()
    return render(request, 'analyzer/upload.html', {'form': form})

# analyzer/views.py

# ... (código anterior)

def consulta_registros(request):
    if request.method == 'POST':
        # Realizar el select a la tabla logs y ordenar por group_name y type
        registros = Logs.objects.order_by('group_name', 'type')
        return render(request, 'analyzer/consulta.html', {'registros': registros})
    else:
        return render(request, 'analyzer/consulta.html')


def show_results(request, file_id):
    uploaded_file = UploadedFile.objects.get(id=file_id)
    found_errors = FoundError.objects.filter(file=uploaded_file)

    if request.method == 'POST':
        form = ShowAnswerForm(request.POST)
        if form.is_valid():
            selected_error_id = form.cleaned_data['error_choices']
            selected_error = FoundError.objects.get(id=selected_error_id)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "I have the following problem in Linux: " + selected_error.error_message + " My question is: How to fix the problem?"}]
            )
            answer = response.choices[0].message.content

            messages.success(request, "Respuesta generada con éxito.")
            return render(request, 'analyzer/results.html', {'file': uploaded_file, 'found_errors': found_errors, 'form': form, 'answer': answer})

    else:
        form = ShowAnswerForm()

    return render(request, 'analyzer/results.html', {'file': uploaded_file, 'found_errors': found_errors, 'form': form})



def chat_gpt(request):
    if request.method == 'POST':
        try:
            message = request.POST.get('message', '')
            if not message.strip():
                return JsonResponse({'error': 'Por favor ingrese un mensaje antes de usar Chat-GPT.'}, status=400)

            # Llamar a la API de GPT-3.5 Turbo
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "I have the following problem in Linux: " + message + " My question is: How to fix the problem?"}]
            )
            answer = response.choices[0].message.content

            return JsonResponse({'answer': answer})
        except Exception as e:
            return JsonResponse({'error': 'Error al obtener la respuesta de Chat-GPT.'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)

# Fin de archivo views.py


