import json
import random

db = open('./data/members.json', 'r')
band_db = open('./data/bands.json', 'w')
db_manage = json.loads(db.read())

# The max number of bands
band_amount = int(len(db_manage) / 6)

# initialize the data
band_list,singer_list,guitar_list,drummer_list = [],[],[],[]
bassist_list,keyboardist_list,instrument_list = [],[],[]

# grade the gender, male=0, female=1


def male_female_grade(type_list):
    total = []
    for i in range(len(type_list)):
        if type_list[i].get('gender') == 'male':
            total.append(0)
        elif type_list[i].get('gender') == 'female':
            total.append(1)
    return total

# judge whether the female or male is free to choose. free=2, If not free,male=0,female=1. If no data = -1


def male_female_judge(type_list):
    j = 0
    for i in type_list:
        j = j + i
    if len(type_list) == 0:
        judge_result = -1
    elif j == len(type_list):
        judge_result = 1
    elif j == 0:
        judge_result = 0
    elif j < len(type_list):
        judge_result = 2
    return judge_result

# create the list to judge whether the talent rank is free to choose in each gender


def type_ruler(member, gender):
    if gender == 'male':
        g = 0
    else:
        g = 1
    ruler = [[0, 0, 0, 0, g], [0, 0, 0, 0, g], [0, 0, 0, 0, g],
             [0, 0, 0, 0, g], [0, 0, 0, 0, g], [0, 0, 0, 0, g]]
    for i in range(len(member)):
        for j in range(len(member[i])):
            if member[i][j].get('gender') == gender:
                templ = member[i][j].get('trank')
                ruler[i][templ - 1] = templ
    return ruler

# gender choose & remove


def member_result(type_member, gender, rank):
    for i in range(len(type_member)):
        if type_member[i].get('gender') == gender and type_member[i].get('trank') == rank:
            temp_member = type_member[i].get('member_info')
            del type_member[i]
            break
    return temp_member

# Average


def average(list):
    sum = 0
    length = 0
    for i in list:
        if i != 0:
            sum = sum + i
            length += 1
    if length != 0:
        return sum / length
    else:
        return 0

# input band by their talent rank


def band_rank(ruler_boy, ruler_girl, result):
    talent_list = []
    talent_grade = 0
    for i in range(6):
        talent_list.append(0)
        if result[i] == 0:
            for j in range(4):
                if i == 0 and ruler_boy[i][j] != 0:
                    talent_list[i] = ruler_boy[i][j]
                    break
                if ruler_boy[i][j] != 0:
                    talent_list[i] = ruler_boy[i][j]
                    ave_add = average(talent_list)
                    var_add = variance(talent_list, ave_add)
                    var_balance = abs(var_add - 1.25)
                    if var_balance < 0.35:
                        if len(talent_list) > 3:
                            if ave_add >2.7:
                                talent_list[-1] = 0
                            else:
                                break
                        else:
                            break
                    else:
                        talent_list[-1] = 0
        if result[i] == 1:
            for j in range(4):
                if i == 0 and ruler_girl[i][j] != 0:
                    talent_list[i] = ruler_girl[i][j]
                    break
                if ruler_girl[i][j] != 0:
                    talent_list[i] = ruler_girl[i][j]
                    ave_add = average(talent_list)
                    var_add = variance(talent_list, ave_add)
                    var_balance = abs(var_add - 1.25)
                    if var_balance < 0.35:
                        if len(talent_list) > 3:
                            if ave_add >2.7:
                                talent_list[-1] = 0
                            else:
                                break
                        else:
                            break
                    else:
                        talent_list[-1] = 0
        if result[i] == 'null':
            talent_list[i] = 'null'
            break
        if talent_list[i] == 0:
            talent_grade+=1
    talent_list.append(talent_grade)
    return talent_list

# variance


def variance(list, average):
    sum = 0
    length = 0
    for i in list:
        if i != 0:
            sum = sum + (i - average)**2
            length += 1
    if length != 0:
        return sum / length
    else:
        return 0

# input the gender result


def result_list(best_number, judge_list):
    result = []
    for j in range(len(judge_list) - 1):
        if judge_list[j] == 2:
            if best_number < 1:
                result.append(0)
            else:
                result.append(1)
                best_number -= 1
        if judge_list[j] == 0:
            result.append(0)
        if judge_list[j] == 1:
            result.append(1)
        if judge_list[j] == -1:
            result.append('null')
    result.append(judge_list[-1])
    return result


# input data into each dataset type. Change this will change the input to achieve that each semester get the different result
for i in range(len(db_manage)):
    id_name = db_manage[i].get('memberId') + " || " + \
        db_manage[i].get('gender')
    temp = {'gender': db_manage[i].get('gender'), 'trank': db_manage[i].get('trank'), 'member_info': id_name + " || " +
            db_manage[i].get('firstName') + " " + db_manage[i].get('lastName') + " || " + str(db_manage[i].get('trank'))}
    if db_manage[i].get('talent') == 'Singer':
        singer_list.append(temp)
    elif db_manage[i].get('talent') == 'Guitarist':
        guitar_list.append(temp)
    elif db_manage[i].get('talent') == 'Drummer':
        drummer_list.append(temp)
    elif db_manage[i].get('talent') == 'Bassist':
        bassist_list.append(temp)
    elif db_manage[i].get('talent') == 'Keyboardist':
        keyboardist_list.append(temp)
    elif db_manage[i].get('talent') == 'Instrumentalist':
        instrument_list.append(temp)

# list random input
random.shuffle(singer_list)
random.shuffle(guitar_list)
random.shuffle(drummer_list)
random.shuffle(bassist_list)
random.shuffle(keyboardist_list)
random.shuffle(instrument_list)
all_member = [singer_list, guitar_list, drummer_list,
              bassist_list, keyboardist_list, instrument_list]
key = ['singer', 'guitarist', 'drummer',
       'bassist', 'keyboardist', 'instrumentalist']


# generate the result
for i in range(band_amount):
    m = str(i)
    balance_number = 6
    band_name = "band " + m
    band_list.append({"name": band_name, "type": "band"})
    final_result = []

    # find the balance_number(current people can choose) and best_number(the best number of girl to choose)
    # then input the judge list
    judge_list_f = []
    for n in all_member:
        temp_list = male_female_grade(n)
        temp_number = male_female_judge(temp_list)
        if temp_number == -1:
            balance_number -= 1
        if temp_number == 1:
            balance_number -= 2
        judge_list_f.append(temp_number)
    if balance_number < 1:
        balance_number = 0
    best_number = int(balance_number / 2)

    # input the number of how many times that judge_list can change(each 2 get 1)
    change_grade = 0
    for grade_judge in judge_list_f:
        if grade_judge == 2:
            change_grade += 1
    judge_list_f.append(change_grade)
    print(judge_list_f)

    # first run
    ruler_boy = type_ruler(all_member, 'male')
    ruler_girl = type_ruler(all_member, 'female')
    result = result_list(best_number, judge_list_f)
    talent_list = band_rank(ruler_boy, ruler_girl, result)

    # if the first talent result doesn't reasonable, then do a loop to find the best reasonable talent list
    # talent_list[-1] means: the amount of 0, which people's talent rank doesn't match the whole list
    # result[-1] means: the amount of 2, which the number of gender can change
    if talent_list[-1] == 0:
        final_result = result + talent_list
    elif result[-1] == 0:
        final_result = result + talent_list
    else:
        nofree = []
        char_val = 0
        for char in judge_list_f[:-1]:
            if char != 2:
                nofree.append(char_val)
            char_val += 1
        free_num = int(result[-1] / 2)
        talent_min = talent_list
        result_min = result
        small = talent_list[-1]

        # start the loop for each judge_list
        for num in range(2**free_num):
            change_list = bin(num)[2:]
            if len(change_list) < free_num:
                change_list = '0'*(free_num-len(change_list)) + change_list
            change_list = change_list + '0' * int((6 - len(nofree))/2)
            result_R = []
            best_number_temp = best_number
            state = 0

            # by using the change list to change the gender judge list, if value ==0, don't change. If value ==1,change
            for small_extra in range(6):
                if small_extra in nofree:
                    if judge_list_f[small_extra] == 0:
                        result_R.append(0)
                    elif judge_list_f[small_extra] == 1:
                        result_R.append(1)
                    elif judge_list_f[small_extra] == 'null':
                        result_R.append('null')
                else:
                    if change_list[state] == '0':
                        state += 1
                        if best_number_temp < 1:
                            result_R.append(0)
                        else:
                            result_R.append(1)
                            best_number_temp -= 1
                    elif change_list[state] == '1':
                        state += 1
                        if best_number_temp < 1:
                            result_R.append(1)
                            best_number_temp -= 1
                        else:
                            result_R.append(0)
            talent_list_R = band_rank(ruler_boy, ruler_girl, result_R)
            if small > talent_list_R[-1]:
                talent_min = talent_list_R
                small = talent_list_R[-1]
                result_min = result_R
                if small == 0:
                    result_min.append(0)
                    final_result = result_min + talent_min
                    break
        if len(result_min) == 6:
            result_min.append(0)
        final_result = result_min + talent_min

    print(final_result)

    # write the whole result into band_list, which will write into the json file after all done
    for ti in range(6):
        if final_result[ti] == 0:
            if final_result[ti + 7] == 0:
                band_list[i][key[ti]] = 'null, need Male'
            else:
                band_list[i][key[ti]] = member_result(
                    all_member[ti], 'male', final_result[ti + 7])
        else:
            if final_result[ti + 7] == 0:
                band_list[i][key[ti]] = 'null, need Female'
            else:
                band_list[i][key[ti]] = member_result(
                    all_member[ti], 'female', final_result[ti + 7])


# result input
band_list = json.dumps(band_list)
band_db.write(band_list)
band_db.close()
db.close()
