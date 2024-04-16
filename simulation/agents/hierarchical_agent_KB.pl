
%---------------------------- Paterns of Behaviour -----------------------------------------------

sintomas_enfermedad([tos, catarro, fiebre, dolor_de_cabeza]).
mis_sintomas([tos]).
hospitals([1,2]).

comunicar_informacion( OtroAgente, Informacion).
sintomas_presentes(Agente, [Sintomas]).

buscar_atencion_medica(Agente, move, Id):-
    hospitals(Id).

detectar_sintomas(Agente, Sintomas, X) :-
    sintomas_presentes(Agente, Sintomas),
    sintomas_enfermedad(SintomasEnfermedad),
    intersection(Sintomas, SintomasEnfermedad, SintomasComunes),
    SintomasComunes \= [],
    buscar_atencion_medica(Agente, X, Id).

%---------------------------- Local Plans --------------------------------------------------------

mascarilla(false).
necesidad_aislamiento(false),
usar_equipos_proteccion(false),
quedarse_en_casa(false).
mantener_distanciamiento(false).

usar_mascarilla():-
    retract(mascarilla(_)),
    asserta(mascarilla(true)).

quitar_mascarilla():-
    retract(mascarilla(_)),
    asserta(mascarilla(false)).

establecer_necesidad_aislamiento():-
    retract(necesidad_aislamiento(_)),
    asserta(necesidad_aislamiento(true)).

quitar_necesidad_aislamiento():-
    retract(necesidad_aislamiento(_)),
    asserta(necesidad_aislamiento(false)).

usar_equipos_proteccion():-
    retract(usar_equipos_proteccion(_)),
    asserta(usar_equipos_proteccion(true)).

establecer_quedarse_en_casa():-
    retract(quedarse_en_casa(_)),
    asserta(quedarse_en_casa(true)).

salir_de_casa():-
    retract(quedarse_en_casa(_)),
    asserta(quedarse_en_casa(false)).

establecer_distanciamiento():-
    retract(mantener_distanciamiento(_)).
    asserta(mantener_distanciamiento(true)).

eliminar_distanciamiento():-
    retract(mantener_distanciamiento(_)).
    asserta(mantener_distanciamiento(false)).

implementar_medidas_aislamiento() :-
    establecer_necesidad_aislamiento(),
    usar_equipos_proteccion(),
    establecer_quedarse_en_casa().



%---------------------------- Cooperation Knowledge -----------------------------------------------


contactos_riesgo_detectados( Contactos).
informar_contactos(Contactos).

enviar_info(Info, Agente).

informar_contactos(Info, []).
informar_contactos(Info, [A|[Contactos]]):-
    enviar_info(Info, A),
    informar_contactos(Info, Contactos).

seguimiento_contactos_riesgo() :-
    contactos_riesgo_detectados(Contactos),
    informar_contactos(Contactos).


%--------------------------- Medotos auxiliares -----------------------------------------

intersection([], _, []).
intersection([H|T], L, [H|R]) :-
    member(H, L),
    intersection(T, L, R).
intersection([H|T], L, R) :-
    \+ member(H, L),
    intersection(T, L, R).
