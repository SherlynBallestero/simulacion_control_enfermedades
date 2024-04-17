%---------------------------- Knowledge -----------------------------------------------

% week_day(WeekDay).
% month_day(MonthDay).
% hour(Hour).
% min(Min).
% home(Id).
% work_place(Id).
% open_place(Id, Bool).
% open_hours_place(ID, OH, CH).
% disease_symptoms(SymptomList).
% my_symptoms(SymptomList).
% is_medical_personal(Bool).
% mask_necessity(Bool).
% mask_requirement(PlaceID, Bool).
% goal(Goal1).
% goal(Goal2).
% public_space(Id, Address).
% space_capacity_state(Id, CapacityState).
% hospital(Id, Address).
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
    
add_disease_symptoms(S):-
    assert(disease_symptoms(S)).

add_if_is_medical_personal(Bool):-
    assert(is_medical_personal(_)),
    assert(is_medical_personal(Bool)).

add_mask_necessity(Bool):-
    retract(mask_knowledge(_)),
    assert(mask_knowledge(Bool)).

add_place_to_use_mask(Place, Bool):-
    retract(mask_requirement(Place,_)),
    assert(mask_requirement(Place, Bool)).


%---------------------------- Patterns of Behaviour -----------------------------------------------

wear_mask(Node, use_mask):-
    mask_requirement(Node,true),
    mask_necessity(true),
    retract(use_personal_mask(_)),
    assert(use_personal_mask(true)).

search_medical_attention(FunctionName, Args):-
    FunctionName = move,
    hospitals(Args).

detect_symptoms(FunctionName, Args) :-
    my_symptoms(Symptoms),
    disease_symptoms(DiseaseSymptoms),
    intersection(Symptoms, DiseaseSymptoms, CommonSymptoms),
    CommonSymptoms \= [],
    search_medical_attention(FunctionName, Args).

%---------------------------- Local Plans --------------------------------------------------------

% Facts
use_protection_equipment(false).
stay_at_home(false).
maintain_distancing(false).
need_isolation(false).

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

use_mask():-
    retract(mask_knowledge(_)),
    asserta(mask_knowledge(true)).

remove_mask():-
    retract(mask_knowledge(_)),
    asserta(mask_knowledge(false)).

establish_need_isolation():-
    retract(need_isolation(_)),
    asserta(need_isolation(true)).

remove_need_isolation():-
    retract(need_isolation(_)),
    asserta(need_isolation(false)).

establish_use_protection_equipment():-
    retract(use_protection_equipment(_)),
    asserta(use_protection_equipment(true)).

establish_stay_at_home():-
    retract(stay_at_home(_)),
    asserta(stay_at_home(true)).

leave_home():-
    retract(stay_at_home(_)),
    asserta(stay_at_home(false)).

establish_distancing():-
    retract(maintain_distancing(_)),
    asserta(maintain_distancing(true)).

remove_distancing():-
    retract(maintain_distancing(_)),
    asserta(maintain_distancing(false)).

implement_isolation_measures() :-
    establish_need_isolation(),
    establish_use_protection_equipment(),
    establish_stay_at_home().


%---------------------------- Cooperation Knowledge -----------------------------------------------

risk_contacts_detected( [_]).
send_info(_, _).

inform_contacts(_, []).
inform_contacts(Info, [A|[Contacts]]):-
    send_info(Info, A),
    inform_contacts(Info, Contacts).

track_risk_contacts() :-
    risk_contacts_detected(Contacts),
    inform_contacts(infected_agent, Contacts).


%--------------------------- Auxiliary Methods -----------------------------------------

intersection([], _, []).
intersection([H|T], L, [H|R]) :-
    member(H, L),
    intersection(T, L, R).
intersection([H|T], L, R) :-
    \+ member(H, L),
    intersection(T, L, R).

:-dynamic(maintain_distancing/1).
:-dynamic(mask_knowledge/1).
:-dynamic(need_isolation/1).
:-dynamic(use_protection_equipment/1).
:-dynamic(stay_at_home/1).
:-dynamic(my_symptoms/1).
:-dynamic(hour/1).
:-dynamic(week_day/1).
:-dynamic(month_day/1).
:-dynamic(min/1).
:-dynamic(use_personal_mask/1).