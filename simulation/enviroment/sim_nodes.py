from utils.graph import Node

class SimNode(Node):
    def __init__(self, capacity, id=None):
        super().__init__( id)
        self.capacity = capacity
        self.agent_list = []
        self.transmition_modifier = 1
        self.contact_rate = 0

class HouseHold(SimNode):
    def __init__(self, id=None):
        super().__init__( id)
        pass 
    
class Workspace(SimNode):
   def __init__(self, id=None):
        super().__init__( id)
        pass    
    
class Block(SimNode):
    def __init__(self, id=None):
        super().__init__( id)
        pass 
    
class Transport(SimNode):
    def __init__(self, id=None):
        super().__init__( id)
        pass  

class PublicPlace(SimNode):
    """
    Class representing a public place in the city.

    Attributes:
    - capacity: Maximum number of people that can be inside the place at the same time.
    - activity: Type of activity that takes place in the place (e.g., shopping, dining, etc.).
    - opening_hours: The hours during which the place is open.
    - location_type: Indicates if the place is indoor, outdoor, or a combination of both.
    - health_services_access: Indicates if the place has direct access to health services.
    - ventilation_level: For indoor places, the level of ventilation can affect the spread of diseases.
    - distance_to_outdoors: For outdoor places, the distance to the nearest outdoor space.
    - distance_to_high_risk_places: For places that are near high-risk places, such as hospitals or medical care centers.
    - daily_visitor_count: To estimate the number of people in the place during the simulation.
    - access_restrictions: To model access restrictions such as visiting hours, maximum capacity, or reservation requirements.
    """
    def __init__(self, id, capacity, activity, opening_hours, location_type, health_services_access, ventilation_level, distance_to_outdoors, distance_to_high_risk_places, daily_visitor_count, access_restrictions):
        super().__init__(id=id, capacity=capacity)
        self.capacity = capacity
        self.activity = activity
        self.opening_hours = opening_hours
        self.location_type = location_type 
        self.health_services_access = health_services_access
        self.ventilation_level = ventilation_level
        self.distance_to_outdoors = distance_to_outdoors
        self.distance_to_high_risk_places = distance_to_high_risk_places
        self.daily_visitor_count = daily_visitor_count

    def __str__(self):
        return f"PublicPlace({self.id}, capacity={self.capacity}, activity={self.activity}, opening_hours={self.opening_hours}, location_type={self.location_type}, health_services_access={self.health_services_access}, ventilation_level={self.ventilation_level}, distance_to_outdoors={self.distance_to_outdoors}, distance_to_high_risk_places={self.distance_to_high_risk_places}, daily_visitor_count={self.daily_visitor_count}, access_restrictions={self.access_restrictions})"

class School(PublicPlace):
    """
    Class representing a school in the city.

    Attributes:
    - classrooms: Number of classrooms in the school.
    - school_hours: School hours to simulate the flow of students.
    - supervision_level: Level of supervision and health control at the school.
    """

    def __init__(self, id, capacity, activity, opening_hours, location_type, health_services_access, ventilation_level, distance_to_outdoors, distance_to_high_risk_places, daily_visitor_count, access_restrictions, classrooms, school_hours, supervision_level):
        super().__init__(id=id, capacity=capacity, activity=activity, opening_hours=opening_hours, location_type=location_type, health_services_access=health_services_access, ventilation_level=ventilation_level, distance_to_outdoors=distance_to_outdoors, distance_to_high_risk_places=distance_to_high_risk_places, daily_visitor_count=daily_visitor_count, access_restrictions=access_restrictions)
        self.classrooms = classrooms
        self.school_hours = school_hours
        self.supervision_level = supervision_level

    def __str__(self):
        return f"School({self.id}, capacity={self.capacity}, activity={self.activity}, opening_hours={self.opening_hours}, location_type={self.location_type}, health_services_access={self.health_services_access}, ventilation_level={self.ventilation_level}, distance_to_outdoors={self.distance_to_outdoors}, distance_to_high_risk_places={self.distance_to_high_risk_places}, daily_visitor_count={self.daily_visitor_count}, access_restrictions={self.access_restrictions}, classrooms={self.classrooms}, school_hours={self.school_hours}, supervision_level={self.supervision_level})"

class Hospital(PublicPlace):
    """
    Class representing a hospital in the city.

    Attributes:
    - number_of_beds: Number of beds available in the hospital.
    - specialties: Specialties offered by the hospital.
    - number_of_staff: Number of medical staff available.
    """

    def __init__(self, id, capacity, activity, opening_hours, location_type, health_services_access, ventilation_level, distance_to_outdoors, distance_to_high_risk_places, daily_visitor_count, access_restrictions, number_of_beds, specialties, number_of_staff):
        super().__init__(id=id, capacity=capacity, activity=activity, opening_hours=opening_hours, location_type=location_type, health_services_access=health_services_access, ventilation_level=ventilation_level, distance_to_outdoors=distance_to_outdoors, distance_to_high_risk_places=distance_to_high_risk_places, daily_visitor_count=daily_visitor_count, access_restrictions=access_restrictions)
        self.number_of_beds = number_of_beds
        self.specialties = specialties
        self.number_of_staff = number_of_staff

    def __str__(self):
        return f"Hospital({self.id}, capacity={self.capacity}, activity={self.activity}, opening_hours={self.opening_hours}, location_type={self.location_type}, health_services_access={self.health_services_access}, ventilation_level={self.ventilation_level}, distance_to_outdoors={self.distance_to_outdoors}, distance_to_high_risk_places={self.distance_to_high_risk_places}, daily_visitor_count={self.daily_visitor_count}, access_restrictions={self.access_restrictions}, number_of_beds={self.number_of_beds}, specialties={self.specialties}, number_of_staff={self.number_of_staff})"

class Supermarket(PublicPlace):
    """
    Class representing a supermarket in the city.

    Attributes:
    - number_of_sections: Number of sections in the supermarket.
    - store_size: Size of the supermarket to model the capacity of customers.
    """

    def __init__(self, id, capacity, activity, opening_hours, location_type, health_services_access, ventilation_level, distance_to_outdoors, distance_to_high_risk_places, daily_visitor_count, access_restrictions, number_of_sections, store_size):
        super().__init__(id=id, capacity=capacity, activity=activity, opening_hours=opening_hours, location_type=location_type, health_services_access=health_services_access, ventilation_level=ventilation_level, distance_to_outdoors=distance_to_outdoors, distance_to_high_risk_places=distance_to_high_risk_places, daily_visitor_count=daily_visitor_count, access_restrictions=access_restrictions)
        self.number_of_sections = number_of_sections
        self.store_size = store_size

    def __str__(self):
        return f"Supermarket({self.id}, capacity={self.capacity}, activity={self.activity}, opening_hours={self.opening_hours}, location_type={self.location_type}, health_services_access={self.health_services_access}, ventilation_level={self.ventilation_level}, distance_to_outdoors={self.distance_to_outdoors}, distance_to_high_risk_places={self.distance_to_high_risk_places}, daily_visitor_count={self.daily_visitor_count}, access_restrictions={self.access_restrictions}, number_of_sections={self.number_of_sections}, store_size={self.store_size})"

class Park(PublicPlace):

    """
    Class representing a park in the city.

    Attributes:
    - playground_areas: Number of playground areas in the park.
    - number_of_benches: Number of benches in the park.
    - park_size: Size of the park to model the capacity of visitors.
    """

    def __init__(self, id, capacity, activity, opening_hours, location_type, health_services_access, ventilation_level, distance_to_outdoors, distance_to_high_risk_places, daily_visitor_count, access_restrictions, playground_areas, number_of_benches, park_size):
        super().__init__(id=id, capacity=capacity, activity=activity, opening_hours=opening_hours, location_type=location_type, health_services_access=health_services_access, ventilation_level=ventilation_level, distance_to_outdoors=distance_to_outdoors, distance_to_high_risk_places=distance_to_high_risk_places, daily_visitor_count=daily_visitor_count, access_restrictions=access_restrictions)
        self.playground_areas = playground_areas
        self.number_of_benches = number_of_benches
        self.park_size = park_size

    def __str__(self):
        return f"Park({self.id}, capacity={self.capacity}, activity={self.activity}, opening_hours={self.opening_hours}, location_type={self.location_type}, health_services_access={self.health_services_access}, ventilation_level={self.ventilation_level}, distance_to_outdoors={self.distance_to_outdoors}, distance_to_high_risk_places={self.distance_to_high_risk_places}, daily_visitor_count={self.daily_visitor_count}, access_restrictions={self.access_restrictions}, playground_areas={self.playground_areas}, number_of_benches={self.number_of_benches}, park_size={self.park_size})"
    
class Library(PublicPlace):
    """
    Class representing a library in the city.

    Attributes:
    - number_of_sections: Number of sections in the library.
    - number_of_computers: Number of computers available for public use.
    """

    def __init__(self, id, capacity, activity, opening_hours, location_type, health_services_access, ventilation_level, distance_to_outdoors, distance_to_high_risk_places, daily_visitor_count, access_restrictions, number_of_sections, number_of_computers):
        super().__init__(id=id, capacity=capacity, activity=activity, opening_hours=opening_hours, location_type=location_type, health_services_access=health_services_access, ventilation_level=ventilation_level, distance_to_outdoors=distance_to_outdoors, distance_to_high_risk_places=distance_to_high_risk_places, daily_visitor_count=daily_visitor_count, access_restrictions=access_restrictions)
        self.number_of_sections = number_of_sections
        self.number_of_computers = number_of_computers

    def __str__(self):
        return f"Library({self.id}, capacity={self.capacity}, activity={self.activity}, opening_hours={self.opening_hours}, location_type={self.location_type}, health_services_access={self.health_services_access}, ventilation_level={self.ventilation_level}, distance_to_outdoors={self.distance_to_outdoors}, distance_to_high_risk_places={self.distance_to_high_risk_places}, daily_visitor_count={self.daily_visitor_count}, access_restrictions={self.access_restrictions}, number_of_sections={self.number_of_sections}, number_of_computers={self.number_of_computers})"

class Restaurant(PublicPlace):
    """
    Class representing a restaurant in the city.

    Attributes:
    - number_of_tables: Number of tables in the restaurant.
    - type_of_cuisine: Type of cuisine offered by the restaurant.
    """

    def __init__(self, id, capacity, activity, opening_hours, location_type, health_services_access, ventilation_level, distance_to_outdoors, distance_to_high_risk_places, daily_visitor_count, access_restrictions, number_of_tables, type_of_cuisine):
        super().__init__(id=id, capacity=capacity, activity=activity, opening_hours=opening_hours, location_type=location_type, health_services_access=health_services_access, ventilation_level=ventilation_level, distance_to_outdoors=distance_to_outdoors, distance_to_high_risk_places=distance_to_high_risk_places, daily_visitor_count=daily_visitor_count, access_restrictions=access_restrictions)
        self.number_of_tables = number_of_tables
        self.type_of_cuisine = type_of_cuisine

    def __str__(self):
        return f"Restaurant({self.id}, capacity={self.capacity}, activity={self.activity}, opening_hours={self.opening_hours}, location_type={self.location_type}, health_services_access={self.health_services_access}, ventilation_level={self.ventilation_level}, distance_to_outdoors={self.distance_to_outdoors}, distance_to_high_risk_places={self.distance_to_high_risk_places}, daily_visitor_count={self.daily_visitor_count}, access_restrictions={self.access_restrictions}, number_of_tables={self.number_of_tables}, type_of_cuisine={self.type_of_cuisine})"

class Gym(PublicPlace):
    """
    Class representing a gym in the city.

    Attributes:
    - number_of_equipment: Number of different types of exercise equipment available.
    - number_of_trainers: Number of personal trainers available.
    """

    def __init__(self, id, capacity, activity, opening_hours, location_type, health_services_access, ventilation_level, distance_to_outdoors, distance_to_high_risk_places, daily_visitor_count, access_restrictions, number_of_equipment, number_of_trainers):
        super().__init__(id=id, capacity=capacity, activity=activity, opening_hours=opening_hours, location_type=location_type, health_services_access=health_services_access, ventilation_level=ventilation_level, distance_to_outdoors=distance_to_outdoors, distance_to_high_risk_places=distance_to_high_risk_places, daily_visitor_count=daily_visitor_count, access_restrictions=access_restrictions)
        self.number_of_equipment = number_of_equipment
        self.number_of_trainers = number_of_trainers

    def __str__(self):
        return f"Gym({self.id}, capacity={self.capacity}, activity={self.activity}, opening_hours={self.opening_hours}, location_type={self.location_type}, health_services_access={self.health_services_access}, ventilation_level={self.ventilation_level}, distance_to_outdoors={self.distance_to_outdoors}, distance_to_high_risk_places={self.distance_to_high_risk_places}, daily_visitor_count={self.daily_visitor_count}, access_restrictions={self.access_restrictions}, number_of_equipment={self.number_of_equipment}, number_of_trainers={self.number_of_trainers})"   
    
class Bar(PublicPlace):
    """
    Class representing a bar in the city.

    Attributes:
    - number_of_tables: Number of tables in the bar.
    - type_of_music: Type of music played at the bar.
    - number_of_bartenders: Number of bartenders available.
    """

    def __init__(self, id, capacity, activity, opening_hours, location_type, health_services_access, ventilation_level, distance_to_outdoors, distance_to_high_risk_places, daily_visitor_count, access_restrictions, number_of_tables, type_of_music, number_of_bartenders):
        super().__init__(id=id, capacity=capacity, activity=activity, opening_hours=opening_hours, location_type=location_type, health_services_access=health_services_access, ventilation_level=ventilation_level, distance_to_outdoors=distance_to_outdoors, distance_to_high_risk_places=distance_to_high_risk_places, daily_visitor_count=daily_visitor_count, access_restrictions=access_restrictions)
        self.number_of_tables = number_of_tables
        self.type_of_music = type_of_music
        self.number_of_bartenders = number_of_bartenders

    def __str__(self):
        return f"Bar({self.id}, capacity={self.capacity}, activity={self.activity}, opening_hours={self.opening_hours}, location_type={self.location_type}, health_services_access={self.health_services_access}, ventilation_level={self.ventilation_level}, distance_to_outdoors={self.distance_to_outdoors}, distance_to_high_risk_places={self.distance_to_high_risk_places}, daily_visitor_count={self.daily_visitor_count}, access_restrictions={self.access_restrictions}, number_of_tables={self.number_of_tables}, type_of_music={self.type_of_music}, number_of_bartenders={self.number_of_bartenders})"
    

       