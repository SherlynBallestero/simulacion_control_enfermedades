import streamlit as st
import gpt4all as gpt
from gpt4all import GPT4All
# from simulation.main import function, factorial, contar_palabras, filtrar_lista, calcular_media, es_primo, maximo_lista, suma
import io
import sys
import re
import json
import matplotlib.pyplot as plt
import web_api
#web_api requests fuctions

# URL base de la API FastAPI
base_url = "http://localhost:8000"

#Function to initialize the simulation
def initialize_simulation(params):
    response =web_api.post(f"{base_url}/simulation/initialize", json=params)
    return response.json()

# Function to delete the simulation
def delete_simulation():
    response =web_api.get(f"{base_url}/simulation/delete")
    return response.json()

# Function to restart the simulation
def reset_simulation():
    response =web_api.get(f"{base_url}/simulation/reset")
    return response.json()

# Function to start the simulation
def start_simulation():
    response =web_api.get(f"{base_url}/simulate")
    return response.json()

#Function to get status of the simulation
def get_simulation_status():
    response =web_api.get(f"{base_url}/simulate/status")
    return response.json()


#model and prompts
model = GPT4All("C:/Users/sherl/.cache/lm-studio/models/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/mistral-7b-instruct-v0.2.Q4_K_S.gguf")


#prompt inicial, solo extrae duracion
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
#extrayendo todos los datos necesarios
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
Reply should be only the Json object with the appropiate fields.
Input:{el input del usuario}
Output:

'''
#nedded functions
def get_llm_response(query):
    # Usa el modelo cargado para generar una respuesta
    response = model.generate(query)
    return response
#parser in a dict the sim's params, return a dict, maybe i need conmtrol output for the llm if not well!
def get_dict_params(llm_extracted_params):
    result = re.search(r'\{(.*?)\}', llm_extracted_params)
    # Verificamos si encontramos un resultado
    
    input_string= result.group(1)
    print(input_string)
    # Remove the "Input:" and "Output:" parts from the string
    input_string = input_string.replace('Input:\"Output:{', '').replace('}\"', '')
    
    # Split the string into key-value pairs
    key_value_pairs = input_string.split(',')
    
    # Initialize an empty dictionary
    output_dict = {}
    
    # Iterate over the key-value pairs
    for pair in key_value_pairs:
        # Split each pair into key and value
        key, value = pair.split(':')
        # Add the key-value pair to the dictionary
        output_dict[key.strip()] = int(value.strip())
    
    # Return the dictionary
    return output_dict 
#fix the fuction, maybe is other return.
def get_simulation_return(path):
    # Abre el archivo en modo de lectura ('r')
    with open(path, 'r') as archivo:
    # Lee todo el contenido del archivo
        contenido = archivo.read()
        return contenido

def create_SimulationParameters(params:dict):
    if "days" in params:
        simulation_days_user=int(params["days"])
    else:
        simulection_days_user=0
    Simulation_params=web_api.SimulationParameters(simulation_days=simulation_days_user)
    return Simulation_params


# Streamlit
st.title("EpiDoc")

# input
user_query = st.text_input("Describa como quisiera simular una epidermia:")

# Buttom
if st.button("Obtener respuesta"):
    if user_query:
        # get  LLM-answer
        response = get_llm_response(prompt2 +' '+ user_query)
        params=get_dict_params(response)
      
         
        simulation_params=create_SimulationParameters(params)
        
        
        print(type(simulation_params))
        
        print(simulation_params)
        st.write(params)
        
    else:
        st.write("Por favor, escribe una consulta para obtener una respuesta.")

# Usar Streamlit para mostrar la gráfica
st.write("Aquí está nuestra gráfica:")

    