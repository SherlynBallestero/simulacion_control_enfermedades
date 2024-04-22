# Introducción

En el mundo actual, la propagación de enfermedades se ha convertido en un desafío global que requiere una atención urgente. La importancia de detener esta propagación no solo radica en la protección de la salud de las personas, sino también en la preservación de la estabilidad social y económica de las comunidades. En este trabajo, exploraremos las diferentes estrategias y medidas que se pueden implementar para prevenir y controlar la propagación de enfermedades, destacando la necesidad de una acción coordinada a nivel local.

# Simulación

La simulación de control de enfermedades se centra en modelar la propagación de una enfermedad ficticia en un entorno simulado, utilizando una combinación de agentes, conocimiento interno, y reglas de progresión de la enfermedad. Tenemos dos tipos de agentes, unos que representan a individuos dentro de la simulacion, con características como ubicación, estado de salud, y uso de mascarillas, y otro que representa una intitucion rectora en la ciudad. La simulación permite la interacción entre agentes y el entorno, modelando comportamientos complejos y dinámicos.

Además, la simulación permite la implementación de medidas de salud pública, como el uso de mascarillas, la cuarentena, y la adopción de prácticas de distanciamiento social, a través de la interacción entre agentes y la actualización dinámica de su conocimiento interno.

## Agentes ciudadanos

Los agentes son entidades que representan a individuos dentro de la simulación. Cada agente tiene características como su ubicación, estado de salud, y si usa mascarilla. Los agentes interactúan con el entorno y entre sí, tomando decisiones basadas en su percepción del entorno y su conocimiento interno. Estas decisiones pueden incluir moverse a diferentes ubicaciones, trabajar, usar o quitar mascarilla, entre otras acciones. La toma de decisiones se basa en una combinación de su conocimiento interno y la percepción del entorno, lo que permite modelar comportamientos complejos y dinámicos.

### Arquitectura

La arquitectura InterRRaP (Interactive Rational Planning) se centra en la interacción entre agentes en un entorno simulado, proporcionando una estructura clara y modular para el desarrollo de sistemas de inteligencia artificial autónomos y cooperativos. Esta arquitectura se compone de varias capas, cada una con responsabilidades específicas, que trabajan juntas para permitir a los agentes actuar de manera eficiente y dirigida hacia objetivos en un entorno dinámico:

- **Interfaz del Mundo**: Actúa como un intermediario entre los agentes y el entorno simulado, facilitando la interacción entre ellos. Esta interfaz no solo permite a los agentes percibir y actuar sobre su entorno, sino que también actualiza el estado del entorno en respuesta a las acciones de los agentes. A este componente se le corresponde un mapa mental que representa el conocimiento del terreno del agente, el cual se actualiza en cada paso del agente con las percepciones.

- **Capa de Comportamiento**: Gestiona el conocimiento reactivo del agente, procesa la información del entorno y toma desiciones sobre que acciones específicas realiza el agente.  

- **Capa de Planificación**: Se encarga de la planificación a corto plazo, tomando decisiones basadas en el conocimiento interno del agente y su percepción del entorno, los comportamientos rutinarios tambien se manejan en esta capa.  

- **Capa Cooperativa**: Traza planes y objetivos cooperativos, facilita la cooperación entre agentes, permitiendo que los agentes interactúen entre sí, compartan información y tomen decisiones colectivas.  

### Base de conocimiento

La base de conocimiento es responsable de almacenar y gestionar el conocimiento interno del agente. Este conocimiento se representa en una base de conocimientos herárquica dividida en tres capas implementada en Prolog, lo que permite una representación formal y lógica del conocimiento del agente.  

La base de conocimientos incluye información relevante sobre el estado de salud del agente, su ubicación, si usa mascarilla, y otros aspectos que son cruciales para la toma de decisiones del agente.  

La base de conocimientos se actualiza dinámicamente a medida que el agente interactúa con el entorno y con otros agentes. Por ejemplo, si un agente se mueve a una nueva ubicación esta información se incorpora a su base de conocimientos, permitiendo al agente actualizar su comprensión del entorno y tomar decisiones informadas.  

## Canelo

El agente especial **Canelo** juega un papel crucial en la simulación, actuando como un punto focal para la coordinación y la toma de decisiones colectivas entre los agentes en el entorno simulado.  

### Características y Propósito de Canelo

Canelo es diseñado para actuar como un líder o coordinador dentro de la simulación. Su propósito principal es tomar decisiones basadas en la información colectiva de todos los agentes y transmitir estas decisiones a los demás agentes para guiar sus acciones. Esto incluye decisiones sobre la implementación de medidas de salud pública, como el uso de mascarillas, la cuarentena, y la adopción de prácticas de distanciamiento social.

### Funcionamiento de Canelo

El funcionamiento de Canelo se basa en su capacidad para procesar y analizar la información colectiva de los agentes utilizando un *Sistema experto en Prolog*. Canelo utiliza una Interfaz del Mundo personalizada para obtener información actualizada sobre el entorno y el estado de otros agentes. Con esta información, Canelo puede tomar decisiones informadas sobre las medidas que deben implementarse para controlar la propagación de la enfermedad.

### Comunicación y Coordinación

Una de las características clave de Canelo es su capacidad para comunicarse y coordinar con los otros agentes. Utiliza la **Capa de Cooperativa** para transmitir sus decisiones a los demás agentes, facilitando la coordinación de acciones para alcanzar objetivos comunes.

# Entorno

El Entorno es una representación abstracta del espacio en el que los agentes se mueven y interactúan. Este entorno simulado es esencial para modelar la dinámica de la enfermedad y las interacciones entre agentes en un contexto urbano. El entorno se modela utilizando un Grafo. Cada nodo representa una ubicación específica dentro del entorno simulado, como un hospital, un lugar público, un espacio de trabajo, una cuadra o una parada de autobus. Las aristas representan las conexiones entre estos nodos, indicando las rutas posibles que los agentes pueden tomar para moverse entre diferentes ubicaciones. A cada nodo tambien se le calcula una probabilidad de contacto base que depende de la capacidad del nodo y la cantidad de agentes que hayan en este.

# Modelado de la Progresión del Virus

Describe cómo se desarrolla y se propaga una enfermedad ficticia en un entorno simulado.

## Cómo se propaga la enfermedad

Se tiene un grupo de personas (agentes) en la ciudad. Algunas de estas personas están infectadas con una enfermedad, pero no muestran síntomas (etapa asintomomática), mientras que otras muestran síntomas pero no son graves (etapa sintomomática). Hay personas muy enfermas (etapa crítica) y algunas que han muerto de la enfermedad (etapa terminal).

## Mecanismos de Transmisión

La transmisión de una enfermedad es el proceso mediante el cual un agente infectado pasa el patógeno (en este caso, un virus ficticio) a otro agente susceptible. En nuestro modelo, la transmisión se modela a través de la probabilidad de que un agente infectado entre en contacto con un agente susceptible y le transmita el virus.

## Progresión de la Enfermedad

La progresión de la enfermedad describe cómo un agente infectado puede pasar de una etapa de infección a otra, desde asintomomático hasta terminal. Este proceso se modela a través de una serie de reglas que describen las condiciones bajo las cuales un agente puede progresar de una etapa a otra.

### Factores de Riesgo

Existen varios factores que pueden aumentar el riesgo de infección y, por ende, la propagación de la enfermedad. Estos incluyen la densidad de población y la vulnerabilidad individual.

# IA

## Algoritmo de Búsqueda

El algoritmo **A\*** es una herramienta esencial en la planificación de rutas para los agentes dentro del entorno simulado. Este algoritmo de búsqueda informada se utiliza para encontrar el camino más corto desde un punto de inicio hasta un objetivo en un grafo, lo cual es crucial para la movilidad eficiente de los agentes dentro del entorno simulado. La implementación del algoritmo A* en este contexto implica la definición de una heurística y una función de coste. La heurística, que es una estimación de la distancia más corta posible entre dos nodos, se basa en la distancia de Manhattan, una medida adecuada para entornos urbanos. La función de coste, por otro lado, representa la distancia real entre dos nodos adyacentes.

La clase `ShortPathProblem` es fundamental para la implementación del algoritmo A*, ya que define el problema de búsqueda de la ruta más corta para un agente específico. Esta clase incluye la definición de la heurística y la función de coste, permitiendo el cálculo de la ruta más corta que un agente debe seguir para alcanzar su objetivo. Este cálculo se realiza en cada paso de la simulación, asegurando que los agentes puedan moverse de manera eficiente a través del entorno simulado.

## Interfaz de Usuario y Procesamiento de Lenguaje Natural

La interfaz de usuario, desarrollada con Streamlit, es una herramienta clave para facilitar la interacción entre los usuarios y la simulación. Esta interfaz basada en texto ofrece una forma intuitiva y accesible para que los usuarios interactúen con la simulación, consulten su estado, y realicen acciones específicas. Permite a los usuarios observar la ubicación de los agentes, su estado de salud, y las interacciones en el entorno simulado. Además, proporciona información detallada sobre el entorno, como la disponibilidad de recursos y la presencia de otros agentes con síntomas de enfermedad.

Una característica destacada de la interfaz de usuario es su capacidad para modificar parámetros de la simulación, lo que permite a los usuarios explorar diferentes escenarios y observar cómo estos cambios afectan la dinámica de la enfermedad en el entorno. Para implementar esta interfaz, se utiliza **gpt4all**, una plataforma de inteligencia artificial que integra capacidades de procesamiento de lenguaje natural (NLP). Esto facilita la creación de interfaces de usuario basadas en texto que pueden entender y responder a las consultas de los usuarios de manera natural y fluida.

El modelo **Mistral**, entrenado con **gpt4all**, juega un papel crucial en el procesamiento de lenguaje natural dentro de la interfaz de usuario. El entrenamiento del modelo implica la recolección de un conjunto de datos de entrenamiento que incluye ejemplos de consultas y respuestas esperadas. A través de este proceso, el modelo aprende a reconocer patrones en las consultas de los usuarios y a generar respuestas que se alinean con las expectativas. Una vez entrenado, el modelo se evalúa y, si su rendimiento es satisfactorio, se despliega en la interfaz de usuario para interactuar con los usuarios y responder a sus consultas de manera eficiente y precisa.

# Resultados experimentales

# Conclusiones

# Bibliografía

[1] https://towardsdatascience.com/introducing-geneal-a-genetic-algorithm-python-library-db69abfc212c  
[2] https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1009149  
[3] https://github.com/diogomatoschaves/geneal  
[4] https://jmvidal.cse.sc.edu/library/muller93a.pdf  
