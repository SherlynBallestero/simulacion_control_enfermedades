import streamlit as st
import gpt4all as gpt
from gpt4all import GPT4All
# from simulation.main import function, factorial, contar_palabras, filtrar_lista, calcular_media, es_primo, maximo_lista, suma
import io
import sys

model = GPT4All("/home/chony/LLM/Mistral-7B-Instruct-v0.1-GGUF/mistral-7b-instruct-v0.1.Q4_K_S.gguf")

st.title("EpiDoc")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "user",
        "content": """
                    Dado que he solicitado que las respuestas a mis preguntas sean exclusivamente llamadas a funciones específicas, sin incluir texto adicional o comentarios, y considerando las funciones que has mencionado (function, factorial, contar_palabras, filtrar_lista, calcular_media), me gustaría que me proporcionaras una respuesta que cumpla con estos criterios.

                    En particular, me interesa obtener el factorial de 5. Entiendo que el factorial de un número es el producto de todos los números enteros positivos desde 1 hasta ese número. Por lo tanto, espero que la respuesta sea una llamada a la función `factorial` con el argumento 5.

                    Además, me gustaría que esta respuesta se ajuste a la estructura de las respuestas anteriores que has proporcionado, donde cada respuesta es una llamada a una función específica sin texto adicional.

                    Por favor, proporciona una respuesta que cumpla con estos requisitos,que tus respuestas sean solamente funciones de python.$
                    """
    })
    st.session_state.messages.append({
        "role": "user",
        "content": """Quiero que mi chatbot responda únicamente con llamados a las siguientes funciones de Python, sin ningún texto ni comentario adicional:
                    - function(nombre_funcion, *args, **kwargs): llama a la función con el nombre especificado y los argumentos proporcionados.
                    - factorial(n): calcula el factorial de un número entero n.
                    - contar_palabras(frase): cuenta el número de palabras en una frase.
                    - filtrar_lista(funcion_filtro, lista): filtra una lista utilizando una función de filtro.
                    - calcular_media(numeros): calcula la media aritmética de una lista de números.

                    Por favor, asegúrate de que tus respuestas sean únicamente llamados a estas funciones.$
                    """
    })
    st.session_state.messages.append({
        "role": "user",
        "content": """El simbolo $ al final de mis prompts significa que ya terminde de escribir no me sigas autocompletando"""
    })
    st.session_state.messages.append({
        "role": "user",
        "content": "cual es el factorial de 5 ?$"
    })
    st.session_state.messages.append({
        "role": "assistent",
        "content": "factorial(5)"
    })
    st.session_state.messages.append({
        "role": "user",
        "content": "cuantas palabras tiene la oracion: hola mundo$"
    })
    st.session_state.messages.append({
        "role": "assistent",
        "content": "contar_palabras([hola, mundo])"
    })
    st.session_state.messages.append({
        "role": "user",
        "content": "calcula la media de 5 numeros primos cualesquiera$"
    })
    st.session_state.messages.append({
        "role": "assistent",
        "content": "calcular_media([3,3,3,5,7])"
    })
    st.session_state.messages.append({
        "role": "user",
        "content": "5 es un numero primo?$"
    })
    st.session_state.messages.append({
        "role": "assistent",
        "content": "es_primo(5)"
    })
    st.session_state.messages.append({
        "role": "user",
        "content": "cual es el maximo de esta lista [2,3]$"
    })
    st.session_state.messages.append({
        "role": "assistent",
        "content": "maximo_lista([2,3])"
    })
    st.session_state.messages.append({
        "role": "user",
        "content": "suma 2 y 3$"
    })
    st.session_state.messages.append({
        "role": "assistent",
        "content": "suma(2,3)"
    })
    
# Convertir el historial en una cadena de texto
historial_texto = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])

print(historial_texto)


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
# Assigning and determining the messages that the user will enter from the prompt
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Pasar el historial y el mensaje del usuario al modelo
    # Suponiendo que 'model' es tu modelo de lenguaje y que tiene un método 'generate'
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        
        
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        response = model.generate(historial_texto + "\n" + "user: " + prompt + "$")
        content = message_placeholder.markdown(response)
        
        res = response.replace("assistant:", "", 1)
        res = res.replace(" ", "")
        
        print(res)
        result = eval(res)
        print(result)

        
        # Finalmente, agregamos al asistente y al usuario al historial.
        st.session_state.messages.append({"role": "assistent", "content": response})
    
    
