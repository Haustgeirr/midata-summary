import csv
import operator
import re


class Payee:
    string = ''
    count = 0
    spend = 0

    def __init__(self, string):
        self.string = string


def clean_charge(charge):
    clean = re.sub('[^A-Za-z0-9.]+', '', charge)

    return float(clean)


def inc_payee(payee, amount):
    payee.spend += clean_charge(amount)
    payee.count += 1


payees = []

with open('midata.csv', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    payee_names = []

    for row in csv_reader:
        first4 = row["Merchant/Description"][0:5]
        x = re.sub('[A-Za-z0-9]', '', first4)

        if len(x) == 0:
            if first4 in payee_names:
                inc_payee(payees[payee_names.index(first4)],
                          row["Debit/Credit"])
            else:
                payee_names.append(first4)
                payees.append(Payee(row["Merchant/Description"]))
                inc_payee(payees[payee_names.index(first4)],
                          row["Debit/Credit"])
    print(
        f'{"Payee".ljust(12, " ")}',
        f'{"Count".rjust(7, " ")}',
        f'{"Spend".rjust(12, " ")}',
        f'{"Per Month".rjust(12, " ")}',
        f'{"Avg Spend".rjust(12, " ")}')

    payees.sort(key=operator.attrgetter('spend'), reverse=True)
    for payee in payees:
        if payee.count > 1:

            print(
                f'{payee.string[0:8].ljust(12, " ")}',
                f'{str(payee.count).rjust(7, " ")}',
                f'{str(round(payee.spend, 2)).rjust(12, " ")}',
                f'{str(round(payee.spend / 12, 2)).rjust(12, " ")}',
                f'{str(round(payee.spend / payee.count, 2)).rjust(12, " ")}')
