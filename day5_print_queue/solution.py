from functools import cmp_to_key

def read_input(filename):
    with open(filename) as file:
        rules, updates = file.read().split("\n\n")

        rules = rules.split("\n")
        rules_final = []

        for rule in rules:
            first, second = rule.split("|")
            rules_final.append((int(first), int(second)))

        updates = updates.split("\n")
        updates_final = []

        for update in updates:
            update_final = [int(page) for page in update.split(",")]
            updates_final.append(update_final)

        return rules_final, updates_final

def build_rule_dictionary(rules):
    rule_dict = {}
    for rule in rules:
        if rule[0] in rule_dict:
            rule_dict[rule[0]].append(rule[1])
        else:
            rule_dict[rule[0]] = [rule[1]]
    return rule_dict

def check_update_ordering(update, rule_dict):
    for i in range(len(update)):
        page = update[i]
        pages_before = update[:i]
        for page_before in pages_before:
            if page in rule_dict and page_before in rule_dict[page]:
                return False
    return True

def get_sum_of_middle_pages(updates, rule_dict):
    return sum(update[len(update)//2] for update in updates if check_update_ordering(update, rule_dict))

def rule_dict_for_update(update, rule_dict):
    new_rule_dict = {}
    for i in range(len(update)):
        if update[i] not in new_rule_dict:
            pages_after = set()
            if update[i] in rule_dict:
                pages_after = set(rule_dict[update[i]])
            new_pages_after = set(update).intersection(pages_after)
            new_rule_dict[update[i]] = list(new_pages_after)
    return new_rule_dict


if __name__ == '__main__':
    rules, updates = read_input("input.txt")
    rule_dict = build_rule_dictionary(rules)

    def compare(x, y):
        if x in rule_dict and y in rule_dict and x in rule_dict[y] and y in rule_dict[x]:
            raise ValueError("Rules must be consistent")
        if x in rule_dict and y in rule_dict[x]:
            return -1
        if y in rule_dict and x in rule_dict[y]:
            return 1
        else:
            return 0

    sum_correct = get_sum_of_middle_pages(updates, rule_dict)

    sum_total = 0
    for update in updates:
        # new_rule_dict = rule_dict_for_update(update, rule_dict)
        sorted_update = sorted(update, key=cmp_to_key(compare))
        sum_total += sorted_update[len(sorted_update)//2]

    print(sum_total - sum_correct)
        