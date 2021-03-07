####################################
# Gather Salary Information
annual_salary = float(input("How much $ do you make a year?"))
portion_saved = float(input("How much can you set aside to save for down-payment?\n(Enter value in range of 0.0 to 1.0)"))
current_savings = 0.0
semi_annual_raise = float(input("What percentage increase is your raise?\n(Enter value in range of 0.0 to 1.0"))
####################################
#  Gather Information on the Dream House
total_cost = float(input("How much does the house cost?"))
portion_down_payment = 0.25 * total_cost
# print(portion_down_payment)
####################################
# Alternatively, maybe since you're moving to the Bay Area you have a Trust Fund.
# current_savings = float(input("How much money are you getting from your family/trust fund?"))
# if current_savings >= total_cost:
#     print("Lucky Day, Go Buy That House!")
# else:
#     print("Keep saving, Champ")
####################################
# Initialize Variables
r = 0.04 # r is a variable used as Annual Rate of Return on Savings. Hard-coding to 4% Annual ROI
i = 0 #Total Number of Months
monthly_salary = annual_salary / 12
monthly_saved = portion_saved * monthly_salary

while current_savings < portion_down_payment:
    i += 1
    if i % 6 == 0:
        monthly_salary = monthly_salary + (monthly_salary*semi_annual_raise)
        monthly_saved = portion_saved * monthly_salary
    current_savings = current_savings + monthly_saved + ( current_savings * (r / 12))
    print("After",i,"months, you've saved",str(int(current_savings))+". You need",int(portion_down_payment))

print("Number of months:",i)