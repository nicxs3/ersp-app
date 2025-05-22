
class Course:
    def __init__(self, id, attributes,  ta_req_nbr, pref_tas =[]):
        self.id = id
        self.attributes = attributes
        self.ta_req_nbr = ta_req_nbr
        self.pref_tas = pref_tas

    def unique_id(self):
        return str(self.id) + "-" + str(self.ta_req_nbr)
    
    def key_str(self):
        return f"Course={self.id}, Instance={self.ta_req_nbr}"

    def __hash__(self):
        return hash(self.id + str(self.ta_req_nbr))

    def __eq__(self, other):
        return isinstance(other, Course) and self.id == other.id # and self.ta_req_nbr == other.ta_req_nbr 

class Applicant:
    def __init__(self, id, gpa, class_level, courses_taken, skills, prev_exp, pref_courses):
        self.id = id
        self.gpa = gpa
        self.class_level = class_level
        self.courses_taken = courses_taken
        self.skills = skills
        self.prev_exp = prev_exp
        self.pref_courses = pref_courses
    
    def unique_id(self):
        return str(self.id)
    
    def key_str(self):
        return f"TA={self.id}"
    
    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Applicant) and self.id == other.id


class Edge:
    def __init__(self, ta_app, course: Course):
        self.ta = ta_app
        self.course = course
    
    def edge_course(self):
        return self.course
    
    def edge_ta(self):
        return self.ta

class Graph:
    def __init__(self, courses, tas, edges):
        self.tas = tas
        self.courses = courses
        self.adj_list = {course: [] for course in courses}
        self.adj_list.update({ta: [] for ta in tas})
        for e in edges:
            self.add_edge(e)
    
    def add_edge(self, e):
        if e.course not in self.adj_list[e.ta] and e.ta not in self.adj_list[e.course]:
            self.adj_list[e.ta].append(e.course)
            self.adj_list[e.course].append(e.ta)
     
    def remove_edge(self, edge):
        if edge.course in self.ta_adj_list[edge.ta] and edge.ta in self.course_adj_list[edge.course]:
            self.adj_list[edge.ta].remove(edge.course)  
            self.adj_list[edge.course].remove(edge.ta)


class MatchingGraph(Graph):
    def __init__(self, courses, tas, edges):
        super().__init__(courses, tas, edges)
        self.curr_match = dict.fromkeys(self.adj_list.keys(), None)
        self.visited = dict.fromkeys(self.adj_list.keys(), False)

    def reset_visited(self):
        self.visited = dict.fromkeys(self.adj_list.keys(), False)

    def print_matches(self):
        print("-- Matches --")
        for key in self.curr_match.keys():
            if self.curr_match[key] != None:
                #print(key.id + " " + self.curr_match[key].id)
                print(key.key_str() + " --matches-- " + self.curr_match[key].key_str())
        print("-- Unmatched --")
        for key in self.curr_match.keys():
            if self.curr_match[key] == None:
                #print(key.id)
                print(key.key_str())

    def add_node(self, node):
        self.adj_list.update({node: []})
        self.curr_match.update({node: None})
        self.visited.update({node: False})
        
        if isinstance(node, Applicant):
            self.tas.append(node)
        if isinstance(node, Course):
            self.courses.append(node)

    def check_phd_matched(self):
        for ta in self.tas:
            if ta.class_level and self.curr_match[ta] is None:
                return False
        return True
    
    def check_courses_matched(self):
        for course in self.courses:
            if self.curr_match[course] is None:
                return False
        return True


# represents the course requirement as specified by the dept/prof
class CourseRequirement: 
    def __init__(self, id, attributes, required_ta_count, pref_tas):
        self.id = id
        self.attributes = attributes
        self.required_ta_count = required_ta_count
        self.pref_tas = pref_tas if pref_tas is not None else []