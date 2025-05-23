from collections.abc import Iterable
from classes import *

def complete_matching(applicant_list, course_list, edge_list):
    #--------- phd applicants----------------
    phd_applicant_list = [student for student in applicant_list if student.class_level]
    edge_list_temp = [edge for edge in edge_list if edge.ta.class_level]

    final_graph = MatchingGraph(course_list, phd_applicant_list, edge_list_temp)
    
    print('Running PhD...')
    final_graph = find_maximum_matching(final_graph)
    
    if not final_graph.check_phd_matched():
        print('No valid matching, phd')
        return None

    #-------------masters applicants -----------------
    masters_applicant_list = [student for student in applicant_list if student.class_level is False]
    masters_edge_list = [edge for edge in edge_list if edge.ta.class_level is False]


    for student in masters_applicant_list: 
        final_graph.add_node(student)
    
    for edge in masters_edge_list: 
        final_graph.add_edge(edge)

    final_graph.visited = dict.fromkeys(final_graph.visited.keys(), False)

    
    print('Running masters...')
    final_graph = find_maximum_matching(final_graph)

    
    if not final_graph.check_courses_matched():
        print('No valid matching, courses')
        return None

    return final_graph




def get_courses_and_edges(course_requirement_list, ta_list):
    courses = []
    edges = []

    ta_lookup = {ta.id: ta for ta in ta_list}  # Use .id if you set Applicant(id=ta.name)

    for cr in course_requirement_list:
        for i in range(cr.required_ta_count):
            new_course = Course(cr.id + ' ' + str(i), cr.attributes, i + 1)
            courses.append(new_course)
            '''
            for ta in ta_list:
                if cr.id in ta.pref_courses:
                    edges.append(Edge(ta, new_course))
            '''
            for ta_name in getattr(cr, 'pref_tas', []):
                ta = ta_lookup.get(ta_name)
                if ta:
                    edges.append(Edge(ta, new_course))

    return courses, edges, ta_list


def get_processed_data(course_requirement_list, ta_list):
    courses = []
    edges = []
    
    
    for cr in course_requirement_list:
        for i in range(cr.required_ta_count):
            new_course = Course(cr.id, cr.attributes, i + 1)
            courses.append(new_course)
            for ta in ta_list:
                if cr.id in ta.pref_courses and ta.id in cr.pref_tas:
                    edges.append(Edge(ta, new_course))

def flip_edges(graph, v):
    iter_v = v
    while iter_v in graph.parent_map:
        p = graph.parent_map[iter_v]
        graph.curr_match[p], graph.curr_match[iter_v] = iter_v, p
        iter_v = p


def try_augmenting_path_bfs(graph, start_ta):
    queue = [start_ta]
    graph.reset_visited()
    graph.visited[start_ta] = True
    graph.parent_map = {}

    while queue:
        u = queue.pop(0)

        if u in graph.courses:  
            if graph.curr_match.get(u) is not None:
                w = graph.curr_match[u]
                if not graph.visited.get(w, False):
                    graph.visited[w] = True
                    queue.append(w)
                    graph.parent_map[w] = u 
            else: 
                flip_edges(graph, u)
                return True

        elif u in graph.tas: 
            if graph.curr_match.get(u) is not None:
                for w in graph.adj_list[u]:
                    if graph.curr_match.get(u) != w and not graph.visited.get(w, False):
                        graph.visited[w] = True
                        graph.parent_map[w] = u
                        queue.append(w)
            else:  
                for w in graph.adj_list[u]:
                    if not graph.visited.get(w, False):
                        graph.visited[w] = True
                        queue.append(w)
                        graph.parent_map[w] = u 

    return False 


def find_maximum_matching(graph):
    found_augmenting_path = True
    while found_augmenting_path is True:
        found_augmenting_path = False

        for ta in graph.tas:
            if graph.curr_match.get(ta) is None: 
                if try_augmenting_path_bfs(graph, ta):
                    found_augmenting_path = True

    return graph





# ta_1 = Applicant("1", 3.5, True, ["CS 225", "CS 173", "CS173"], ["Python", "Java"], ["CS 173"], ["CS 225", "CS 173"])
# ta_2 = Applicant("2", 3.8, True, ["CS 225", "CS 173"], ["Python", "Java"],  ["CS 225"], ["CS 225", "CS 173"])
# ta_3 = Applicant("3", 3.6, True, ["CS 225", "CS 173"], ["Python", "Java"],  [], ["CS 225", "CS 173"])

# CourseRequirement - holds Course Information and number of TAs required for the course
# Eventually, for every TA required an instance of this Course will be created 
# Each instance of Course then qualifies as a node/vertex in the graph
# course_1 = CourseRequirement("CS 225", ["Python", "Java"], 2) # will result in 1 instance of Course object
# course_2 = CourseRequirement("CS 173", ["Python", "Java"], 4)  # will result in 3 instance of Course object

# course_list, edge_list, ta_list_incl_dummies = get_courses_and_edges ([course_1, course_2], [ta_1, ta_2, ta_3])


#course_list, edge_list = get_courses_edges ([course_1, course_2], [edge_1, edge_2, edge_3, edge_4, edge_5, edge_6])
#print ('course list', [x for x in course_list])
#print ('edge list', edge_list)



# graph = MatchingGraph(course_list, ta_list_incl_dummies, edge_list)
# matching(graph)
# graph.print_matches()
# print('---')
# final_graph = complete_matching(ta_list_incl_dummies, course_list, edge_list)

# try:
#     final_graph.print_matches()
# except:
#     print(final_graph)