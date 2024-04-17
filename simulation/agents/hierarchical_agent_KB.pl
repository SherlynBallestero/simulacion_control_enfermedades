%---------------------------- Knowledge -----------------------------------------------

% week_day(WeekDay).
% month_day(MonthDay).
% hour(Hour).
% min(Min).
% home(Id).
% work_place(Id).
% open_place(Id, Bool).
% open_hours_place(ID, OH, CH).
% dissease_symptoms(SymptomList).
% my_symptoms(SymptomList).
% is_medical_personal(Bool).
% mask_necesity(Bool).
% mask_requirement(PlaceID, Bool).
% goal(Goal1).
% goal(Goal2).
% public_space(Id, Adress).
% space_capacity_state(Id, CapacityState).
% hospital(Id, Adress).
% hospital_overrun(Id, OverrunBool).
% public_transportation_working(Id, Bool).
% public_transportation_schedule(Id, AddrList).

my_symptoms([]).

use_personal_mask(false).

add_public_space(Id, Address):-
    retractall(public_space(Id, _)),
    assert(public_space(Id, Address)).

add_home(Node):-
    retractall(home(_)),
    assert(home(Node)).

add_work_place(Node):-
    retractall(work_place(_)),
    assert(work_place(Node)).

add_open_place(Node, Bool):-
    retract(open_place(Node,_)),
    assert(open_place(Node, Bool)).

add_open_hours_place(Node, Initial, Final):-
    retractall(open_hours_place(Node, Initial, Final)),
    assert(open_hours_place(Node,Initial,Final)).

add_date(WeekDayK, MonthDayK, HourK, MinK):-
    retract(week_day(_)),
    retract(month_day(_)),
    retract(min(_)),
    retractall(hour(_)),
    asserta(week_day(WeekDayK)),
    asserta(month_day(MonthDayK)),
    assert(hour(HourK)),
    asserta(min(MinK)).

add_symptom(Symptom):-
    my_symptoms(S),
    Symptom_list_result = [Symptom| S],
    retract(my_symptoms(_)),
    asserta(my_symptoms(Symptom_list_result)).
    
add_hospital(HospitalId, Address):-
    retract(hospital(HospitalId, _)),
    asserta(hospital(HospitalId, Address)).
    
add_dissease_symptoms(S):-
    assert(dissease_symptoms(S)).

add_if_is_medical_personal(Bool):-
    assert(is_medical_personal(_)),
    assert(is_medical_personal(Bool)).

add_mask_necesity(Bool):-
    retract(mask_knowledge(_)),
    assert(mask_knowledge(Bool)).

add_place_to_use_mask(Place, Bool):-
    retract(mask_requirement(Place,_)),
    assert(mask_requirement(Place, Bool)).


%---------------------------- Paterns of Behaviour -----------------------------------------------

wear_mask(Node, use_mask):-
    mask_requirement(Node,true),
    mask_necesity(true),
    retract(use_personal_mask(_)),
    assert(use_personal_mask(true)).

buscar_atencion_medica(FunctionName, Args):-
    FunctionName = move,
    hospitals(Args).

detectar_sintomas(FunctionName, Args) :-
    my_symptoms(Sintomas),
    dissease_symptoms(SintomasEnfermedad),
    intersection(Sintomas, SintomasEnfermedad, SintomasComunes),
    SintomasComunes \= [],
    buscar_atencion_medica(FunctionName, Args).

%---------------------------- Local Plans --------------------------------------------------------

% Facts
usar_equipos_proteccion(false).
quedarse_en_casa(false).
mantener_distanciamiento(false).
necesidad_aislamiento(false).

% Rules

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