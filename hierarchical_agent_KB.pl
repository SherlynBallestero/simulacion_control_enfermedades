%---------------------------- Knowledge -----------------------------------------------
% week_day(week_day_k).
% month_day(month_day_k).
% hour(23).
% min(min_k).

objetives([]).

home([2,3]).
work_place([1,2]).
open_place([1,2], true).
open_hours_place([1,2],8,23).
hospitals([1,2]).

sintomas_enfermedad([tos, catarro, fiebre, dolor_de_cabeza]).
my_symptoms([tos]).
is_medical_personal(false).

mascarilla(true).
use_mask([1,2], true).
use_personal_mask(false).

usar_equipos_proteccion(false).
quedarse_en_casa(false).
mantener_distanciamiento(false).
necesidad_aislamiento(false).

add_date(Week_day_k, Month_day_k, Hour_k, Min_k):-
    retract(week_day(_)),
    retract(month_day(_)),
    retract(min(_)),
    retractall(hour(_)),
    asserta(week_day(Week_day_k)),
    asserta(month_day(Month_day_k)),
    assert(hour(Hour_k)),
    asserta(min(Min_k)).

add_symptom(Symptom):-
    my_symptoms(S),
    Symptom_list_result = [Symptom| S],
    retract(my_symptoms(_)),
    asserta(my_symptoms(Symptom_list_result)).
    
add_hospital(Hospital):-
    hospitals(H),
    Hospitals_list_result = [Hospital| H],
    retract(hospitals(_)),
    asserta(hospitals(Hospitals_list_result)).
    

%---------------------------- Paterns of Behaviour -----------------------------------------------

wear_mask(Node, use_mask):-
    use_mask(Node,true),
    mascarilla(true),
    retract(use_personal_mask(_)),
    assert(use_personal_mask(true)).

buscar_atencion_medica(FunctionName, Args):-
    FunctionName = move,
    hospitals(Args).

detectar_sintomas(FunctionName, Args) :-
    my_symptoms( Sintomas),
    sintomas_enfermedad(SintomasEnfermedad),
    intersection(Sintomas, SintomasEnfermedad, SintomasComunes),
    SintomasComunes \= [],
    buscar_atencion_medica(FunctionName, Args).

%---------------------------- Local Plans --------------------------------------------------------

go_to_work(move, X):-
    work_place(X),
    open_place(X, true),
    hour(H),
    open_hours_place(X,I,F),
    H == I.

go_home_after_work(move, Y):-
    home(Y),
    work_place(X),
    open_place(X, true),
    hour(H),
    open_hours_place(X,I,F),
    H == F.

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

establecer_usar_equipos_proteccion():-
    retract(usar_equipos_proteccion(_)),
    asserta(usar_equipos_proteccion(true)).

establecer_quedarse_en_casa():-
    retract(quedarse_en_casa(_)),
    asserta(quedarse_en_casa(true)).

salir_de_casa():-
    retract(quedarse_en_casa(_)),
    asserta(quedarse_en_casa(false)).

establecer_distanciamiento():-
    retract(mantener_distanciamiento(_)),
    asserta(mantener_distanciamiento(true)).

eliminar_distanciamiento():-
    retract(mantener_distanciamiento(_)),
    asserta(mantener_distanciamiento(false)).

implementar_medidas_aislamiento() :-
    establecer_necesidad_aislamiento(),
    establecer_usar_equipos_proteccion(),
    establecer_quedarse_en_casa().


%---------------------------- Cooperation Knowledge -----------------------------------------------

contactos_riesgo_detectados( [Contactos]).
enviar_info(Info, Agente).

informar_contactos(Info, []).
informar_contactos(Info, [A|[Contactos]]):-
    enviar_info(Info, A),
    informar_contactos(Info, Contactos).

seguimiento_contactos_riesgo() :-
    contactos_riesgo_detectados(Contactos),
    informar_contactos(agente_enfermo, Contactos).


%--------------------------- Medotos auxiliares -----------------------------------------

intersection([], _, []).
intersection([H|T], L, [H|R]) :-
    member(H, L),
    intersection(T, L, R).
intersection([H|T], L, R) :-
    \+ member(H, L),
    intersection(T, L, R).

:-dynamic(mantener_distanciamiento/1).
:-dynamic(mascarilla/1).
:-dynamic(necesidad_aislamiento/1).
:-dynamic(usar_equipos_proteccion/1).
:-dynamic(quedarse_en_casa/1).
:-dynamic(my_symptoms/1).
:-dynamic(hour/1).
:-dynamic(week_day/1).
:-dynamic(month_day/1).
:-dynamic(min/1).
:-dynamic(use_personal_mask/1).