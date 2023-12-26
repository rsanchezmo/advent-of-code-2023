from pprint import pprint
import re
import copy


def main():
    with open("./december_19/test.txt", 'r') as f:
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
        workflow = workflows[next_]
        for rule in workflow:
            type_, comparison, value, next_ = rule
            
            if type_ is None:
                if next_.isupper():
                    if next_ == 'A':
                        x_combi = ranges['x'][1] - ranges['x'][0]
                        m_combi = ranges['m'][1] - ranges['m'][0]
                        a_combi = ranges['a'][1] - ranges['a'][0]
                        s_combi = ranges['s'][1] - ranges['s'][0]
                        return x_combi * m_combi * a_combi * s_combi  # we got accepted
                    else:
                        return 0 # we got rejected
                
                else:
                    break  # move onto the next workflow, keep ranges as they were

            else:
                if comparison == '>':
                    # create two new nodes from upper or lower
                    ranges_lower = copy.deepcopy(ranges)
                    ranges_upper = copy.deepcopy(ranges)

                    # modify lower

                    # modify higher
                    

                    count_lower = process_node_tree(next_, ranges_lower)
                    count_upper = process_node_tree(next_, ranges_upper)

                    return count_lower + count_upper

                else:
                    # create two new nodes from upper or lower
                    ranges_lower = copy.deepcopy(ranges)
                    ranges_upper = copy.deepcopy(ranges)
                    

                    count_lower = process_node_tree(next_, ranges_lower)
                    count_upper = process_node_tree(next_, ranges_upper)

                    return count_lower + count_upper


    print(f'Part 2: {process_node_tree(next_, ranges)}')



if __name__ == "__main__":
    main()