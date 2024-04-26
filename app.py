import streamlit as st
import web_api

# URL base de la API FastAPI
base_url = "http://localhost:8000"

# Función para inicializar la simulación
def initialize_simulation(params):
    response =web_api.post(f"{base_url}/simulation/initialize", json=params)
    return response.json()

# Función para eliminar la simulación
def delete_simulation():
    response =web_api.get(f"{base_url}/simulation/delete")
    return response.json()

# Función para reiniciar la simulación
def reset_simulation():
    response =web_api.get(f"{base_url}/simulation/reset")
    return response.json()

# Función para iniciar la simulación
def start_simulation():
    response =web_api.get(f"{base_url}/simulate")
    return response.json()

# Función para obtener el estado de la simulación
def get_simulation_status():
    response =web_api.get(f"{base_url}/simulate/status")
    return response.json()

# Interfaz de usuario con Streamlit
st.title("Simulación de Epidemias")

# Botones para interactuar con la simulación
if st.button("Inicializar simulación"):
    params = {
        "simulation_days": 31,
        "grid_size": 10,
        "block_capacity": 100,
        "house_amount": 10,
        "house_capacity": 5,
        "hospital_amount": 4,
        "hospital_capacity": 50,
        "hospital_hours": [8, 20],
        "recreational_amount": 4,
        "recreational_capacity": 20,
        "recreational_hours": [8, 20],
        "works_amount": 4,
        "works_capacity": 10,
        "work_hours": [8, 20],
        "amount_of_agents": 10
    }
    result = initialize_simulation(params)
    st.write(result)

if st.button("Eliminar simulación"):
    result = delete_simulation()
    st.write(result)

if st.button("Reiniciar simulación"):
    result = reset_simulation()
    st.write(result)

if st.button("Iniciar simulación"):
    result = start_simulation()
    st.write(result)

status = get_simulation_status()
st.write("Estado de la simulación:", status["status"])