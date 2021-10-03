from random import choice

# Gets main parent paths
def get_reduced_data(major_data):
    reduced_data_names = []
    lower_division = set()
    # for each class
    for c in major_data:
        # add to reduced_data if not blacklisted
        if c['name'] not in lower_division:
            reduced_data_names.append(c['name'])
        current_prereqs = c['prereqs']
        # while have current prereqs, remove from reduced_data and add to blacklist 
        while current_prereqs:
            prereq = current_prereqs[0]
            if prereq['name'] in reduced_data_names:
                reduced_data_names.remove(prereq['name'])
            lower_division.add(prereq['name'])
            current_prereqs = prereq['prereqs']

    return [c_obj for c_obj in major_data if c_obj['name'] in reduced_data_names]

# Gets ordered class list: [last ... first]
def get_class_path(class_dict):
    class_path = [class_dict['name']]
    current_prereqs = class_dict['prereqs']
    while current_prereqs:
        prereq = current_prereqs[0]
        class_path.append(prereq['name'])
        current_prereqs = prereq['prereqs']
    return class_path
    

# Gets a random semester number that is not in exclude
def get_random_semester(start, end, exclude):
    choices = [i for i in range(start, end) if i not in exclude]
    return choice(choices)

# Gets a random schedule fulfilling the class order requirements of major_data
def get_schedule(major_data):
    NUM_SEMESTERS = 4
    NUM_CLASSES = 4
    schedule = [[] for i in range(NUM_SEMESTERS)]
    filled_semesters = set()
    # get highest order parent classes
    reduced_data = get_reduced_data(major_data)
    for track in reduced_data:
        class_path = get_class_path(track)
        # choose random last path semester from len(path) to NUM_SEMESTERS and add
        semester_num = get_random_semester(len(class_path) - 1, NUM_SEMESTERS, filled_semesters)
        schedule[semester_num].append(class_path[0])
        # if filled semester, add it to filled_semesters
        if len(schedule[semester_num]) == NUM_CLASSES:
            filled_semesters.add(semester_num)
        # add each class in path to the semester, reassign semester_num
        for c_i in range(1, len(class_path)):
            # offset by classes left (current - total) to allow for room
            semester_num = get_random_semester(len(class_path) - c_i - 1, semester_num, filled_semesters)
            schedule[semester_num].append(class_path[c_i])
            # if filled semester, add it to filled_semesters
            if len(schedule[semester_num]) == NUM_CLASSES:
                filled_semesters.add(semester_num)

    return schedule

def test():
    # Gov UT Transfer example
    CLASS_DATA = [{'name': 'ENGL 1301', 'prereqs': []}, 
                  {'name': 'ENGL 1302', 'prereqs': [ {'name': 'ENGL 1301', 'prereqs': []} ]},
                  {'name': 'ENGL 23**','prereqs': [ {'name': 'ENGL 1302', 'prereqs': [ {'name': 'ENGL 1301', 'prereqs': []} ]} ]},
                  {'name': 'SPAN 1411', 'prereqs': []},
                  {'name': 'SPAN 1412', 'prereqs': [ {'name': 'SPAN 1411', 'prereqs': []} ]}, 
                  {'name': 'SPAN 2311', 'prereqs': [ {'name': 'SPAN 1412', 'prereqs': [ {'name': 'SPAN 1411', 'prereqs': []} ]} ]},
                  {'name': 'SPAN 2312', 'prereqs': [ {'name': 'SPAN 2311', 'prereqs': [ {'name': 'SPAN 1412', 'prereqs': [ {'name': 'SPAN 1411', 'prereqs': []} ]} ]} ]},
                  {'name': 'HIST I', 'prereqs': []},
                  {'name': 'HIST II', 'prereqs': [ {'name': 'HIST I', 'prereqs': []} ]},
                  {'name': 'SCI I', 'prereqs': []},
                  {'name': 'SCI II', 'prereqs': [ {'name': 'SCI I', 'prereqs': []} ]},
                  {'name': 'SCI III', 'prereqs': []},
                  {'name': 'ARTS', 'prereqs': []}]

    for i in range(5):
        schedule = get_schedule(CLASS_DATA)
        for semester in schedule:
            print(semester)
        print()
    
#########
# NOTES #
#########
# This will work as long as each class only has ONE prereq path, should be fine for MVP. 

# Need to have students select the "tracks" they are interested in taking
# Ex: Which science track? Which history track?

# Next: 1. Integrate option prompts to get path choices.
#       2. Add check for impossible schedules.

if __name__ == '__main__':
    test()