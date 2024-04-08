% Define el estado inicial de la enfermedad
disease_state(susceptible).

% Define los patrones de comportamiento
behavior_pattern(susceptible, exposed) :-
    % El agente se expone si entra en contacto con un individuo infectado
    contact_with_infected.

behavior_pattern(exposed, infected) :-
    % El agente se infecta después de un cierto período de exposición
    exposure_time_passed.

behavior_pattern(infected, recovered) :-
    % El agente se recupera después de un cierto período de infección
    infection_time_passed.

% Define predicados para simular el contacto con un individuo infectado y el paso del tiempo
contact_with_infected :-
    % Simula el contacto con un individuo infectado
    write('El agente entró en contacto con un individuo infectado.'), nl.

exposure_time_passed :-
    % Simula el paso del tiempo para la exposición
    write('El tiempo de exposición ha pasado.'), nl.

infection_time_passed :-
    % Simula el paso del tiempo para la infección
    write('El tiempo de infección ha pasado.'), nl.

% Predicado principal para simular el comportamiento de un agente
simulate_agent :-
    % Obtiene el estado actual de la enfermedad
    disease_state(CurrentState),
    % Determina el siguiente patrón de comportamiento basado en el estado actual
    behavior_pattern(CurrentState, NextState),
    % Actualiza el estado de la enfermedad
    retract(disease_state(_)),
    assert(disease_state(NextState)),
    % Imprime el nuevo estado
    write('El estado del agente cambió a: '), write(NextState), nl.

% Ejemplo de consulta para simular el comportamiento del agente
% ?- simulate_agent.