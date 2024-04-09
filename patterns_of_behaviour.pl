% Define los hechos
% name(cambiar_ubicacion, '').
capacity_place(place1, 100).
capacity_place(place3, 300).


behavior_pattern(CurrentNode, move_to_next_location):-
    % Verifica la capacidad del nodo actual
    capacity_place(CurrentNode, Capacity),
    Capacity > 100.

    behavior_pattern(CurrentNode, a):-
    % Verifica la capacidad del nodo actual
    capacity_place(CurrentNode, Capacity),
    Capacity > 100.
    
    

:-dynamic capacity_place/2.

