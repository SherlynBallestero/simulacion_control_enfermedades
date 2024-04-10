import pyswip

# Initialize the Prolog engine
prolog = pyswip.Prolog()

# Load the behavior patterns
prolog.consult('bbc.pl')

# Function to add a new citizen's health status
def add_citizen(name, health_status):
    prolog.assertz(f"{health_status}({name})")

# Function to query a citizen's behavior
def query_behavior(name):
    return list(prolog.query(f"behavior({name}, Behavior)"))

# Example usage
add_citizen("Alice", "healthy")
add_citizen("Bob", "infected")

# Query behaviors
print(query_behavior("Alice"))
print(query_behavior("Bob"))

# Dynamically update the knowledge base
# For example, to update Alice's status to infected
prolog.retract(f"healthy(Alice)")
prolog.assertz(f"infected(Alice)")

# Query behaviors after update
print(query_behavior("Alice"))
# import pyswip

# # Initialize the Prolog engine
# prolog = pyswip.Prolog()

# # Load the knowledge base
# prolog.consult('knowledge_base.pl')

# # Remove a fact
# prolog.retract('likes(john, pizza)')
# def remove_fact(fact):
#     prolog.retract(fact)

# def add_fact(fact):
#     prolog.assertz(fact)

# # Example usage
# remove_fact('likes(john, pizza)')
# add_fact('likes(john, burger)')