import streamlit as st
import gpt4all as gpt
from gpt4all import GPT4All
# from simulation.main import function, factorial, contar_palabras, filtrar_lista, calcular_media, es_primo, maximo_lista, suma
import io
import sys
import re
import json
import matplotlib.pyplot as plt

model = GPT4All("C:/Users/sherl/.cache/lm-studio/models/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/mistral-7b-instruct-v0.2.Q4_K_S.gguf")


#Para extraer los dias de duracion...
prompt='''Given the fallowig user query:
{msg}
Tell me the duration in days of the epidemic he wants.
Reply with a JSON object with thw fallowing structure:
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

#grafic
# Crear una gráfica de muestra usando Matplotlib
fig, ax = plt.subplots()
ax.plot([0, 1, 2, 3], [10, 20, 30, 40])

# Streamlit
st.title("EpiDoc")

# input
user_query = st.text_input("Describa como quisiera simular una epidermia:")

# Buttom
if st.button("Obtener respuesta"):
    if user_query:
        # get  LLM-answer
        response = get_llm_response(prompt +' '+ user_query)
        #get-param-duration
        number_days = get_number_of_days(response)
        print(type(number_days))
        # show answer
        st.write(number_days)
    else:
        st.write("Por favor, escribe una consulta para obtener una respuesta.")

# Usar Streamlit para mostrar la gráfica
st.write("Aquí está nuestra gráfica:")
st.pyplot(fig)
    