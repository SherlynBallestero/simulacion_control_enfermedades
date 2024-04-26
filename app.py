import streamlit as st
import gpt4all as gpt
from gpt4all import GPT4All
# from simulation.main import function, factorial, contar_palabras, filtrar_lista, calcular_media, es_primo, maximo_lista, suma
import io
import sys
import re
import json
import matplotlib.pyplot as plt
import text_interface

model = GPT4All("C:/Users/sherl/.cache/lm-studio/models/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/mistral-7b-instruct-v0.2.Q4_K_S.gguf")


#Para extraer los dias de duracion...
prompt='''Given the fallowig user query:
{msg}
Tell me the duration in days of the epidemic he wants.
Reply with a JSON object with the fallowing structure:
{{
    "days":"" exacly one int object of the query user, wich describe the duration in days
}}
Raply should be only the Json object with the appropiate fields.
#EXAMPLES
Input: Quiero que dure la epidermia cerca de 567 dias
Output: {days: 567};
Input: Me gustaria llevar a cabo un analisis relacionado al covid desarrollado por 62 dias
Output:{days: 62}
Input: {el input del usuario}
Output:
'''
prompt2='''Given the fallowig user query:
{msg}
Extract information properly.
Reply with a JSON object with the following structure:
{{
    "days":"exacly one int object of the query user, wich describe the duration in days"
    "block_capacity":"exacly one int of capacity of the envairoment"
    "house_amount":"exacly the amount of houses in the envairoment"
    
    "house_capacity":"exacly capacity of the houses"
    "hospital_amount":"exacly amount of hospitals in the envairoment"
    "hospital_capacity":"exacly the amount of people can be in the hospital at the same time"
    "recreational_amount":"exacly the amount of recreatrionals centers of the envairoment"
    "recreational_capacity":"exacly the amount of agents can be in the recreational center at the same time"
}}
Reply should be only the Json object with the appropiate fields.
#EXAMPLES
Input: Quiero una epidermia que dure 342 dias en una ciudad cuya capacidad es 456, deben haber 32 casas,
cada casa acepta 5 personas y hay 45 hospitales cuyas capacidades son 9,existen 97 centros de recreacion y aceptan 20 
personas cada uno

Output:{days:342, block_capacity:456, house_amount:32,house_capacity:5,hospital_amount:45,hospital_capacity:9,recreational_amount:97, recreational_capacity:20}
Input: Genara una epidermia durante 67 dias en una capacidad de 89, con 42 casas con capacidad 2.Deben haber 32 hospitales donde caben 43 personas.Las recreaciones se hacen en 67 centros cuyas capacidades son 90.
Output:{days:67, block_capacity:89, house_amount:42,house_capacity:2,hospital_amount:32,hospital_capacity:43,recreational_amount:67, recreational_capacity:90}
Input: Genara una epidermia durante un anno  en una capacidad de 8, donde hayan 2 casas y caben 5 personas en cada una. Existen 54 centros donde los ciudadanos pueden divertirse y caben en cada uno 76 personas y hay 32 hospitales con capacidad 21
Output:{days:365, block_capacity:8, house_amount:2,house_capacity:5,hospital_amount325,hospital_capacity:21,recreational_amount:54, recreational_capacity:76}
Input:{el input del usuario}
Output:
'''
#with the llm answer about duration get the int wich is number of days the costum want simulate the epidemic
def get_number_of_days(text_input):
    pattern = r'\d+'  # Patrón que coincide con uno o más dígitos
    # Search for the pattern in the text input
    match = re.search(pattern, text_input)
    if match:
    # Extract the number of days from the matched pattern
        days = int(match.group())
        return days

    else:
        print("Number of days not found in the text input.")
        return None
    
         
# abswer of llm
def get_llm_response(query):
    # Usa el modelo cargado para generar una respuesta
    response = model.generate(query)
    return response

def get_simulation_return(path):
    # Abre el archivo en modo de lectura ('r')
    with open(path, 'r') as archivo:
    # Lee todo el contenido del archivo
        contenido = archivo.read()
        return contenido

 
#grafic
# Crear una gráfica de muestra usando Matplotlib
# fig, ax = plt.subplots()
# ax.plot([0, 1, 2, 3], [10, 20, 30, 40])

# Streamlit
st.title("EpiDoc")

# input
user_query = st.text_input("Describa como quisiera simular una epidermia:")

# Buttom
if st.button("Obtener respuesta"):
    if user_query:
        # get  LLM-answer
        response = get_llm_response(prompt2 +' '+ user_query)
        sim_returns=get_simulation_return("simulation.log")
        print(type(sim_returns))
        st.write(response)
        
    else:
        st.write("Por favor, escribe una consulta para obtener una respuesta.")

# Usar Streamlit para mostrar la gráfica
st.write("Aquí está nuestra gráfica:")

    