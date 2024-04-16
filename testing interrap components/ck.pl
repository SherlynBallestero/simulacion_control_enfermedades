
% Definición de predicados auxiliares
necesidad_coordinacion(Agente1, Agente2).
establecer_canal_comunicacion(Agente1, Agente2).
coordinar_acciones(Agente1, Agente2).

necesidad_planificacion(Agente1, Agente2, Objetivo).
definir_plan_accion(Agente1, Agente2, Objetivo).
implementar_plan_accion(Agente1, Agente2, Objetivo).

necesidad_intercambio(Agente1, Agente2).
seleccionar_informacion(Agente1, Agente2).
enviar_informacion(Agente1, Agente2).

necesidad_medida(Agente1, Agente2, Medida).
coordinar_implementacion(Agente1, Agente2, Medida).
ejecutar_medida(Agente1, Agente2, Medida).

% Definición de los patrones de comportamiento
comunicacion_coordinacion(Agente1, Agente2) :-
    necesidad_coordinacion(Agente1, Agente2),
    establecer_canal_comunicacion(Agente1, Agente2),
    coordinar_acciones(Agente1, Agente2).

planificacion_conjunta(Agente1, Agente2, Objetivo) :-
    necesidad_planificacion(Agente1, Agente2, Objetivo),
    definir_plan_accion(Agente1, Agente2, Objetivo),
    implementar_plan_accion(Agente1, Agente2, Objetivo).

intercambio_informacion(Agente1, Agente2) :-
    necesidad_intercambio(Agente1, Agente2),
    seleccionar_informacion(Agente1, Agente2),
    enviar_informacion(Agente1, Agente2).

implementar_medidas_salud_publica_conjunta(Agente1, Agente2, Medida) :-
    necesidad_medida(Agente1, Agente2, Medida),
    coordinar_implementacion(Agente1, Agente2, Medida),
    ejecutar_medida(Agente1, Agente2, Medida).
