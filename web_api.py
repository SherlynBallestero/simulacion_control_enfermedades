from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Tuple
from simulation.epi_sim import Simulation
from fastapi.responses import StreamingResponse
import matplotlib.pyplot as plt
import numpy as np
import io


# Asumiendo que la clase Simulation ya está definida como en el ejemplo anterior

app = FastAPI()

# Instancia global de la simulación
simulation = None
running = False
done = False

class SimulationParameters(BaseModel):
    simulation_days: int = 31
    grid_size: int = 10
    block_capacity: int = 100
    house_amount: int = 10
    house_capacity: int = 5
    hospital_amount: int = 4
    hospital_capacity: int = 50
    hospital_hours: tuple = (8, 20)
    recreational_amount: int = 4
    recreational_capacity: int = 20
    recreational_hours: tuple = (8, 20)
    works_amount: int = 4
    works_capacity: int = 10
    work_hours: tuple = (8, 20)
    amount_of_agents: int = 20

@app.post("/simulation/initialize")
async def initialize_simulation(params: SimulationParameters):
    global simulation
    global running
    if simulation is not None:
        raise HTTPException(status_code=400, detail="Delete current simulation to initialize another one")
    simulation = Simulation(**params.model_dump())
    simulation.initialize_simulation()
    return {"message": "Simulation initialized"}

@app.get("/simulation/delete")
async def delete_simulation():
    global simulation
    global running
    global done
    if simulation is None:
        raise HTTPException(status_code=400, detail="Theres no created simulation")
    if running:
        raise HTTPException(status_code=400, detail="Wait till the simulation stops running to delete it")
    simulation = None
    done = False
    return {"message": "Simulation deleted"}

@app.get("/simulation/reset")
async def reset_simulation():
    global simulation
    global running
    global done
    if simulation is None:
        raise HTTPException(status_code=400, detail="Initialize a simulation first")
    if running:
        raise HTTPException(status_code=400, detail="Wait till the simulation is done running")
    simulation.reset_sim()
    done = False
    return {"message": "Simulation reseted"}

@app.get("/simulate")
async def start_simulation():
    global simulation
    global running
    global done
    if simulation is None:
        raise HTTPException(status_code=400, detail="Define a simulation first")
    if running:
        raise HTTPException(status_code=400, detail="The simulation is already running")
    if done:
        raise HTTPException(status_code=400, detail="Reset the simulation before running it")
    running = True
    simulation.simulate()
    running = False
    done = True
    return {"message": "Simulation started"}

@app.get("/simulate/status")
async def get_simulation_status():
    global simulation
    global running
    if simulation is None:
        return {"status": "not initialized"}
    if done:
        return {"status": "done"}
    if not running:
        return {"status": "not running"}
    if running:
        return {"status": "running"}

@app.get("/statistics")
async def stats():
    global simulation
    global done
    if simulation is None:
        raise HTTPException(status_code=400, detail="Define a simulation first")
    if not done:
        raise HTTPException(status_code=400, detail="Run the simulation first")
    sim_stats = simulation.get_stats()
    return sim_stats

@app.get("/traincanelo")
async def train_canelo():
    global simulation
    if simulation is None:
        raise HTTPException(status_code=400, detail="Define a simulation first")
    solution = simulation.train_canelo()
    return solution

@app.get("/plots/infection")
async def get_plot_infection():
    # Generate some data for plotting
    global simulation
    global done
    if simulation is None:
        raise HTTPException(status_code=400, detail="Define a simulation first")
    if not done:
        raise HTTPException(status_code=400, detail="Run the simulation first")

    sim_stats:dict = simulation.get_stats()['days_evolution']
    days = []
    infected_stats = []
    susceptible_stats = []
    inmune_stats = []
    dead_stats = []
    
    for i, stage_dist in sim_stats:
        days.append(i)
        infected_stats.append(sum_infected(stage_dist))
        susceptible_stats.append(stage_dist['susceptible'])
        inmune_stats.append(stage_dist['recovered'])
        dead_stats.append(stage_dist['dead'])

    x = days
    y = infected_stats

    # Create a plot
    plt.figure()
    plt.plot(days, infected_stats, label='Infected', color='red')
    plt.plot(days, susceptible_stats, label='Susceptible', color='blue')
    plt.plot(days, inmune_stats, label='Immune', color='green')
    plt.plot(days, dead_stats, label='Dead', color='black')
    plt.title("Epidemic Simulation")
    plt.xlabel("Days")
    plt.ylabel("Population")
    plt.legend()
    plt.grid(True)

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Return the plot as a StreamingResponse
    return StreamingResponse(buf, media_type="image/png")

@app.get("/plots/genetic/fitness")
async def get_plot_fitness():
    global simulation
    asd = 1
    genetic_algorythm = simulation.genetic_a
    
    return StreamingResponse(genetic_algorythm.get_plot_fitness(), media_type="image/png")

@app.get("/plots/genetic/genes")
async def get_plot_genes():
    global simulation
    asd  = 15
    genetic_algorythm = simulation.genetic_a
    
    return StreamingResponse(genetic_algorythm.get_plot_genes(), media_type="image/png")

def sum_infected(stage_dist):
    return sum([value for key, value in stage_dist.items() if key not in ['recovered', 'dead', 'susceptible']])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)