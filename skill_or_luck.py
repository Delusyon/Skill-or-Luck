import random
import math

bootstrap_value = 1000
sample_value = 18300
top_nth = 11

def person(i):
    index = i

    skill = random.randrange(0, 101)
    luck = random.randrange(0, 101)

    total_score = (0.95 * skill) + (0.05 * luck)

    # print(skill, luck, total_score)

    return [skill, luck, total_score, index]


result = []
diff_chosen_people = []

def bootstraping(iteration):
    # Reports the progression
    print("Calculating values")
    for bootstrap_value in range(iteration):
        if (bootstrap_value == round(iteration / 4)):
            print("25% done")
        elif (bootstrap_value == round(iteration / 2)):
            print("50% done")
        elif (bootstrap_value == round(iteration * 3 / 4)):
            print("75% done")
        elif (bootstrap_value == iteration):
            print("100% done")

        # Sort the "all_people" array to find the 10 best people
        all_people = []
        all_sorted_people = []
        all_sorted_people_onSkill = []

        for i in range(sample_value):
            new_person = person(i)
            all_people.append(new_person)
            all_sorted_people = sorted(all_people, key=lambda x: x[2])
            all_sorted_people_onSkill = sorted(all_people, key=lambda x: x[0])

        # print(all_people)
        # print(all_sorted_people)
        # print(all_sorted_people_onSkill)

        # Calculating skills and luck of 10 best people
        # Take note on the index of people chosen as the best 10 based on Skill+Luck and Skill only
        total_skill = 0
        total_luck = 0

        people_skillLuck = []
        people_onlySkill = []

        for j in range(top_nth):
            total_skill += all_sorted_people[len(all_sorted_people) - j - 1][0]
            total_luck += all_sorted_people[len(all_sorted_people) - j - 1][1]

            people_skillLuck.append(all_sorted_people[len(all_sorted_people) - j - 1][3])
            people_onlySkill.append(all_sorted_people_onSkill[len(all_sorted_people_onSkill) - j - 1][3])

        average_skill = total_skill / top_nth
        average_luck = total_luck / top_nth

        # print(total_skill, total_luck)
        # print(average_skill, average_luck)
        # print(people_skillLuck, people_onlySkill)

        # Make an array that reports the chance that a person is chosen only because they had the skills)
        diff_chosen_people.append(len((set(people_skillLuck) & set(people_onlySkill))) / top_nth)

        # Calculating deviation
        sum_pow_deviation_skill = 0
        sum_pow_deviation_luck = 0

        for k in range(top_nth):
            sum_pow_deviation_skill += pow(abs(average_skill - all_sorted_people[len(all_sorted_people) - k - 1][0]), 2)
            sum_pow_deviation_luck += pow(abs(average_luck - all_sorted_people[len(all_sorted_people) - k - 1][1]), 2)

        sd_skill = math.sqrt(sum_pow_deviation_skill / (top_nth - 1))
        sd_luck = math.sqrt(sum_pow_deviation_luck / (top_nth - 1))

        # add all results (skill and luck) into an array
        result.append([average_skill, sd_skill, average_luck, sd_luck])

bootstraping(bootstrap_value)

print("writing results")
with open('avg_data.csv', 'w') as f:
    for i in range(bootstrap_value):
        f.write(str(result[i][0]) + "," + str(result[i][1]) + "," + str(result[i][2]) + "," + str(result[i][3]) + "\n")
with open('skillOnly_data.csv', 'w') as f:
    for i in range(bootstrap_value):
        f.write(str(diff_chosen_people[i]) + "\n")
