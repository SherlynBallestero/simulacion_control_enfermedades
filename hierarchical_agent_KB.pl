%---------------------------- Knowledge -----------------------------------------------
% week_day(week_day_k).
% month_day(month_day_k).
% hour(23).
% min(min_k).

objetives([]).

% home([2,3]).
% work_place([1,2]).
% open_place([1,2], true).
% open_hours_place([1,2],8,23).
hospitals([1,2]).

% dissease_symptoms([tos, catarro, fiebre, dolor_de_cabeza]).
my_symptoms([tos]).
% is_medical_personal(false).

% mask_knowledge(true).
% use_mask([1,2], true).
use_personal_mask(false).

% Local Plans
usar_equipos_proteccion(false).
quedarse_en_casa(false).
mantener_distanciamiento(false).
necesidad_aislamiento(false).

add_home(Node):-
    assert(home(Node)).

add_work_place(Node):-
    assert(work_place(Node)).

add_open_place(Node, Bool):-
    retract(open_place(Node,_)),
    assert(open_place(Node, Bool)).

add_open_hours_place(Node, Inicial, Final):-
    assert(open_hours_place(Node,Inicial,Final)).

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
    
add_dissease_symptoms(S):-
    assert(dissease_symptoms(S)).

add_if_is_medical_personal(Bool):-
    assert(is_medical_personal(Bool)).

add_mask_knowledge(Bool):-
    retract(mask_knowledge(_)),
    assert(mask_knowledge(Bool)).

add_place_to_use_mask(Place, Bool):
    retract(use_mask(Place,_)),
    assert(use_mask(Place, Bool)).


%---------------------------- Paterns of Behaviour -----------------------------------------------

wear_mask(Node, use_mask):-
    use_mask(Node,true),
    mask_knowledge(true),
    retract(use_personal_mask(_)),
    assert(use_personal_mask(true)).

buscar_atencion_medica(FunctionName, Args):-
    FunctionName = move,
    hospitals(Args).

detectar_sintomas(FunctionName, Args) :-
    my_symptoms( Sintomas),
    dissease_symptoms(SintomasEnfermedad),
    intersection(Sintomas, SintomasEnfermedad, SintomasComunes),
    SintomasComunes \= [],
    buscar_atencion_medica(FunctionName, Args).

%---------------------------- Local Plans --------------------------------------------------------

go_to_work(move, X):-
    work_place(X),
    open_place(X, true),
    hour(H),
    open_hours_place(X,I,_),
    H == I.

go_home_after_work(move, Y):-
    home(Y),
    work_place(X),
    open_place(X, true),
    hour(H),
    open_hours_place(X,_,F),
    H == F.

usar_mascarilla():-
    retract(mask_knowledge(_)),
    asserta(mask_knowledge(true)).

quitar_mascarilla():-
    retract(mask_knowledge(_)),
    asserta(mask_knowledge(false)).

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

contactos_riesgo_detectados( [_]).
enviar_info(_, _).

informar_contactos(_, []).
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
:-dynamic(mask_knowledge/1).
:-dynamic(necesidad_aislamiento/1).
:-dynamic(usar_equipos_proteccion/1).
:-dynamic(quedarse_en_casa/1).
:-dynamic(my_symptoms/1).
:-dynamic(hour/1).
:-dynamic(week_day/1).
:-dynamic(month_day/1).
:-dynamic(min/1).
:-dynamic(use_personal_mask/1).