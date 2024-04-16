from pyswip import Prolog

# Initialize Prolog engine
prolog = Prolog()

# Load your Prolog code
prolog.consult('./simulation/epidemic/chony_virus_progression.pl')

# Define your test cases as Prolog queries
test_cases_query = ["test_case_1.", "test_case_2.", "test_case_3.", "test_case_4.", "test_case_5.", "test_case_6.", "test_case_7"]

# Run the test cases
for query in test_cases_query:
    try:
        result = list(prolog.query(query))
        if result:
            print(f'query:{query}\nresult{result}')
        else:
            print(f'query{query} failed')
    except:
        print('query:{query} failed with error')