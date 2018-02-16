

# -----------------main function that starts computation ----------------------
# 1. takes input from the percentile.txt and itcont.txt file in input directory
# 2. dissects all the necessary data from the given file
# 3. stores the data in a data structure
# 4. processes the data
def main():
    file = open("../input/itcont.txt", "r")             # data file
    file_p = open("../input/percentile.txt", "r")       # percentile file
    percentile = int(file_p.read())
    file_p.close()

    # initial record that will contain everything taken from file,
    # this is a list of lists
    record = []

    with file as file_obj:
        for line in file_obj:
            lst = []            # temporary list that stores data of each line
            counter = 0         # counts the number of '|' encounters('|' is the separator)
            s = ""              # temporary string

            # read characters from the file one by one
            for ch in line:
                if ch == "|":       # if separator encountered i.e. a string is completed
                    counter += 1    # increment counter
                    lst.append(s)   # append the string to temporary list
                    s = ""          # clear s for next iteration
                else:
                    s += ch         # keep building string
                if counter == 21 or ch == '\n':     # total separators for one record is 21
                                                    # if counter turns 21 or its eof, that means end of record reached
                    record.append(lst)              # append the list to record
                    lst = []                        # reset list
                    counter = 0                     # reset counter

    file.close()

    # this record will hold the relevant record,
    # this is a list of dictionary
    r_record = []

    # a temporary dictionary to hold one record
    dic = {}

    # for each record in record[[]] list,
    #       position 0   gives   id
    #       position 7   gives   name
    #       position 10  gives   zip code
    #       position 13  gives   date
    #       position 14  gives   amount
    #       position 15  gives   other id
    # this loop runs through all the records in record[[]]
    for data in record:
        if is_id(data[0]):                          # is valid id
            if is_name(data[7]):                    # is valid name
                if is_zip(data[10][0:5]):           # if first five letters makes a valid zip code
                    if is_date(data[13]):           # is valid date
                        if is_amount(data[14]):     # is valid amount
                            if is_other(data[15]):  # is valid other id
                                # if all the above checks passes

                                # checking for repeat donors
                                found = False                   # flag to indicate repeat found or not
                                for r in r_record:              # checking all records in relevant record
                                    if data[7] in r.values():
                                        if data[10][0:5] in r.values():
                                            # name and zip code is matching, that means donor repeats
                                            found = True                    # raise a flag

                                            # update the recipient id, date and amount for that specific donor
                                            r['id'].append(data[0])
                                            r['date'].append(data[13])
                                            r['amount'].append(data[14])

                                # if flag returns false, that means it is a new donor
                                if found is False:
                                    # create a dictionary
                                    dic['id'] = [data[0]]
                                    dic['name'] = data[7]
                                    dic['zip'] = data[10][0:5]
                                    dic['date'] = [data[13]]
                                    dic['amount'] = [data[14]]

                                    # add that dictionary in relevant record
                                    r_record.append(dic)
                                    dic = {}                # clear temporary dictionary

    record.clear()          # releasing useless memory

    # open the file to write output
    file = open("../output/repeat_donors.txt", "w")

    # list that holds the contribution amount
    contribution_list = []
    for r in r_record:                          # loop through all records in relevant record

        # if dictionary r has more than one date, that means repeat donations
        if len(r['date']) > 1:
            for i in range(len(r['date'])):     # loop through all dates
                year = get_year(r['date'][i])
                if year == "2018":              # if the year is 2018(as given in the question)
                    # get the amount donated
                    contribution = int(r['amount'][i])
                    # add that amount to the contribution amount list
                    contribution_list.append(contribution)
                    # get the percentile index
                    index = int((percentile / 100) * len(contribution_list))

                    # write output to file in specified format
                    file.write("{}|{}|{}|{}|{}|{}\n".
                               format(r['id'][i], r['zip'], year, contribution_list[index],
                                      sum(contribution_list), len(contribution_list)))

    # housekeeping
    file.close()
    r_record.clear()


# function that returns the year for a given date
def get_year(date):
    return date[4]+date[5]+date[6]+date[7]


# function to check if date is valid
def is_date(date):
    if len(date) != 8 or date.isdigit() is False:       # if string is non numeric or less than 8, invalid date
        return False
    else:
        month = int(date[0]+date[1])                    # get month
        day = int(date[2]+date[3])                      # get date

        # check validity of month
        if month > 12 or month < 1:
            return False

        # check validity of day
        if month == 2:                                  # for february
            if day > 29 or day < 1:
                return False
        else:                                           # for others
            if day > 31 or day < 1:
                return False
    return True


# returns true if the zip code is in valid format
def is_zip(code):
    if len(code) < 5 or code.isdigit() is False:
        return False
    return True


# returns true if the name is in valid format
def is_name(name):
    if len(name) == 0:
        return False
    return True


# returns true if the id is in valid format
def is_id(_id):
    if len(_id) == 0:
        return False
    return True


# returns true if the amount is in valid format
def is_amount(amount):
    if len(amount) == 0 or amount.isdigit() is False:
        return False
    return True


# returns true if the other is in valid format
def is_other(other):
    if len(other) == 0:
        return True
    return False


if __name__ == "__main__":
    main()
