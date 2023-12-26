from pprint import pprint
import re
import copy


def main():
    with open("./december_19/input.txt", 'r') as f:
        lines = f.readlines()

    workflows = {}
    parts = []
    getting_workflows = True
    for line in lines:
        if line == '\n':
            getting_workflows = False
            continue

        if getting_workflows:
            split_line = line.split('{')
            name = split_line[0]
            rules = split_line[1].split('}')[0].split(',')

            # wanna transform rules into tuple with (type, comparison, value, next)
            new_rules = []
            for rule in rules:
                type_ = None
                comparison = None
                value = None
                next_ = None
                if '<' in rule:
                    type_ = rule.split('<')[0]
                    comparison = '<'
                    value = int(rule.split('<')[1].split(':')[0])
                    next_ = rule.split(':')[1]
                elif '>' in rule:
                    type_ = rule.split('>')[0]
                    comparison = '>'
                    value = int(rule.split('>')[1].split(':')[0])
                    next_ = rule.split(':')[1]
                else:
                    next_ = rule

                new_rules.append((type_, comparison, value, next_))
            workflows[name] = new_rules

        else:
            component = line.strip().replace('}', '').replace('{', '')
            x = int(re.findall('x=(\d+)', component)[0])
            m = int(re.findall('m=(\d+)', component)[0])
            a = int(re.findall('a=(\d+)', component)[0])
            s = int(re.findall('s=(\d+)', component)[0])
            parts.append({'x': x, 
                          'm': m,
                          'a': a,
                          's': s})

    organization = {'A': [], 'R': []}
    def process_part(part, workflow):
        for rule in workflow:
            type_, comparison, value, next_ = rule

            # first check if there is no condition
            if type_ is None:
                if next_.isupper():
                    organization[next_].append(part)
                else:
                    process_part(part, workflows[next_])
                return
            
            if (comparison == '<' and part[type_] < value) or (comparison == '>' and part[type_] > value):
                if next_.isupper():  # if next is a final state (A or R)
                    organization[next_].append(part)
                    return
                else:
                    process_part(part, workflows[next_])
                    return
        

    # Part 1
    for part in parts:
        workflow = workflows['in']
        process_part(part, workflow)

    sum_accepted = sum(sum(val.values()) for val in organization['A'])
    sum_rejected = sum(sum(val.values()) for val in organization['R'])
    print(f'Part 1: A {sum_accepted} R {sum_rejected}')

    # Part 2
    total_combinations = 0
    next_ = 'in'
    x_range = [1, 4000]
    m_range = [1, 4000]
    a_range = [1, 4000]
    s_range = [1, 4000]
    ranges = {'x': x_range, 
              'm': m_range, 
              'a': a_range,
              's': s_range}

    def process_node_tree(next_, ranges):
        """ Binary Tree Search """

        if next_.isupper():
            if next_ == 'A':
                x_combi = ranges['x'][1] - ranges['x'][0] + 1
                m_combi = ranges['m'][1] - ranges['m'][0] + 1
                a_combi = ranges['a'][1] - ranges['a'][0] + 1
                s_combi = ranges['s'][1] - ranges['s'][0] + 1
                return x_combi * m_combi * a_combi * s_combi  # we got accepted
            else:
                return 0 # we got rejected
        
        workflow = workflows[next_]
        count = 0
        for i, rule in enumerate(workflow):
            type_, comparison, value, next_ = rule
    
            if type_ is None:
                if next_.isupper():
                    if next_ == 'A':
                        x_combi = ranges['x'][1] - ranges['x'][0] + 1
                        m_combi = ranges['m'][1] - ranges['m'][0] + 1
                        a_combi = ranges['a'][1] - ranges['a'][0] + 1
                        s_combi = ranges['s'][1] - ranges['s'][0] + 1
                        return x_combi * m_combi * a_combi * s_combi + count  # we got accepted
                    else:
                        return count # we got rejected, return the branches that were closed before
                else:
                    count += process_node_tree(next_, ranges)
                    return count  # we are moving forced to the next_ workflow
            
            if comparison == '>':
                # create two new nodes from upper or lower
                ranges_lower = copy.deepcopy(ranges)
                ranges_upper = copy.deepcopy(ranges)

                # modify lower
                ranges_lower[type_][1] = value if value < ranges_lower[type_][1] else ranges_lower[type_][1]
                # modify higher
                ranges_upper[type_][0] = value + 1 if value + 1 > ranges_upper[type_][0] else ranges_upper[type_][0]
                
                if ranges_upper[type_][0] <= ranges_upper[type_][1]:
                    count += process_node_tree(next_, ranges_upper)  # if matches the > rule, move onto the next_ workflow
                
                if ranges_lower[type_][0] > ranges_lower[type_][1]:
                    # this way is not possible so we can stop
                    return count  # return count as this value is from the other branch

                ranges = ranges_lower # if upper should move onto the next rule

            else:
                # create two new nodes from upper or lower
                ranges_lower = copy.deepcopy(ranges)
                ranges_upper = copy.deepcopy(ranges)

                # modify lower
                ranges_lower[type_][1] = value - 1 if value - 1 < ranges_lower[type_][1] else ranges_lower[type_][1]
                # modify higher
                ranges_upper[type_][0] = value if value > ranges_upper[type_][0] else ranges_upper[type_][0]

                if ranges_lower[type_][0] <= ranges_lower[type_][1]:
                    count += process_node_tree(next_, ranges_lower)  # if lower should move onto the next_ workflow
                
                if ranges_upper[type_][0] > ranges_upper[type_][1]:
                    # this way is not possible so we can stop
                    return count
                
                ranges = ranges_upper # if lower should move onto the next rule

        return count

    solution = process_node_tree(next_, ranges)
    # assert solution == 167409079868000, f'Wrong solution: {solution}'
    print(f'Part 2: {solution}')


if __name__ == "__main__":
    main()