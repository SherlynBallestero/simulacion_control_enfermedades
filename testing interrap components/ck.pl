% % Hechos que representan las relaciones de cooperación
% cooperan(juan, maria).
% cooperan(juan, pedro).
% cooperan(maria, pedro).

% % Hechos que representan los roles o responsabilidades de los agentes
% rol(juan, lider).
% rol(maria, analista).
% rol(pedro, desarrollador).

% % Reglas que definen cómo se puede formar un equipo de cooperación
% equipo_cooperativo(Equipo) :-
%     findall(X, cooperan(X, _), Equipo),
%     length(Equipo, N),
%     N > 1.

% % Regla que define un equipo de cooperación basado en roles específicos
% equipo_especializado(Equipo, Rol) :-
%     findall(X, (cooperan(X, _), rol(X, Rol)), Equipo),
%     length(Equipo, N),
%     N > 1.

% % Ejemplo de uso
% ?- equipo_cooperativo(Equipo).
% ?- equipo_especializado(EquipoDeDesarrolladores, desarrollador).
