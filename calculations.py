from datetime import date, datetime
import requests
from requests.exceptions import HTTPError
import json

# converts value to standard USD format as string
def as_currency(amount):
    if amount >= 0:
        return '${:,.2f}'.format(amount)
    else:
        return '-${:,.2f}'.format(-amount)
        

# calculates the current age in years from the given date of birth
def calculate_age(date_of_birth):
    format = '%Y-%m-%d'
    date_of_birth = datetime.strptime(date_of_birth, format)
    today = date.today()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    return age, date_of_birth


# increases salary by 2% annually 
def yearly_increased_salary(income, salary_increase_rate):
    income = income * (1 + salary_increase_rate)
    return income 


# calculates how much the user makes on their final year up until they retire on there birthday
def final_salary_year(household_income, date_of_birth):
    today = datetime.now()
    retirement_day = date_of_birth.replace(year=today.year)
    new_years_day = datetime(year = today.year, month = 1, day = 1)

    delta = retirement_day - new_years_day
    daily_income = household_income / 365
    final_years_income = daily_income * float(delta.days)

    return final_years_income


# calculates the amount of the money the user will have saved by the time they retire
def calculate_saved_amount(current_savings, savings_rate, salary_increase_rate, expected_rate_of_return, household_income, age, retirement_age, date_of_birth):
    amount_saved = current_savings

    for i in range(age, retirement_age):
        amount_saved *= 1 + (expected_rate_of_return/100)
        amount_saved += household_income * (savings_rate/100)
        household_income = yearly_increased_salary(household_income, salary_increase_rate)

    amount_saved += final_salary_year(household_income, date_of_birth) * (savings_rate/100)

    return amount_saved, household_income


# calculates the net present value given a rate and cash flow list
def npv(rate, cf_list):
    sum_pv = 0
    for i, cf in enumerate(cf_list, start = 1):
        sum_pv += cf / (1 + rate) ** i

    return sum_pv


# calculates the amount a user will need to retire
def calculate_amount_you_will_need(retirement_age, life_expectancy, pre_retirement_income, inflation_rate, pre_retirement_income_percent):
    values = []

    for _ in range(retirement_age, life_expectancy):
        pre_retirement_income *= (1 + inflation_rate) 
        values.append(pre_retirement_income * (pre_retirement_income_percent/100))


    retirement_rate_of_return = .05
    pv = npv(retirement_rate_of_return, values)
    return pv


# fetch user data from api and convert to python dict
def fetch_data(user_number):
    try: 
        response = requests.get(f"https://pgf7hywzb5.execute-api.us-east-1.amazonaws.com/users/{user_number}")
        response.raise_for_status()
        json = response.json()

        return json

    except HTTPError as http_err:
        print(f'HTTP error occured: {http_err}')
    except Exception as err:
        print(f'Other error occured: {err}')

# main function that calculates retirement values
def calculate_retirment(user_id):
    user_data = fetch_data(user_id)

    ### user info
    date_of_birth =  user_data["user_info"]["date_of_birth"]
    household_income = user_data["user_info"]["household_income"]
    savings_rate = user_data["user_info"]["current_savings_rate"]
    current_savings = user_data["user_info"]["current_retirement_savings"]

    ### assumptions 
    retirement_age = user_data["assumptions"]["retirement_age"]
    life_expectancy = user_data["assumptions"]["life_expectancy"]
    pre_retirement_income_percent = user_data["assumptions"]["pre_retirement_income_percent"]
    expected_rate_of_return = user_data["assumptions"]["expected_rate_of_return"]
    inflation_rate = .03
    salary_increase_rate = .02

    age, date_of_birth = calculate_age(date_of_birth)

    amount_saved, pre_retirement_income = calculate_saved_amount(current_savings, savings_rate, salary_increase_rate, expected_rate_of_return, household_income, age, retirement_age, date_of_birth)

    amount_needed_to_retire = calculate_amount_you_will_need(retirement_age, life_expectancy, pre_retirement_income, inflation_rate, pre_retirement_income_percent)

    user_data["user_info"]["amount_needed"] = as_currency(amount_needed_to_retire)
    user_data["user_info"]["amount_saved"] = as_currency(amount_saved)

    # return json response for react app with amount needed and amount saved
    return json.dumps(user_data)

    
