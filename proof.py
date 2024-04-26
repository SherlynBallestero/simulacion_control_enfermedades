import web_api
# Crear una instancia de la clase SimulationParameters con valores personalizados
parameters = web_api.SimulationParameters(
    simulation_days=30,
    house_amount=15,
 
    
    works_capacity=15,
    amount_of_agents=15
)

# Acceder a los valores de los parámetros personalizados
print("hospital_capacity")

print(parameters.hospital_capacity)
