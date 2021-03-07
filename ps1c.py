####################################
# Goal is to figure out how much you need to save
#  in order to afford a down-payment on a $1MM house in 36 months
#  variable inputs will be salary, output will be %-of-income saved
#
# Assignment States the required use of "Bisection Search"
# Youtube: https://www.youtube.com/watch?v=mqaf7vj1AdA
# Rookies Lab: https://www.rookieslab.com/posts/linear-search-vs-bisection-search-in-python
# Creating an Array : http://people.bu.edu/andasari/courses/basicpython/basicpython.html
#
####################################
# Import "Bisection Search" module may be a fast way to do this, we should first try writing our own.
#import bisect
#
#
#
# Here is an example, from Rookies Lab link above, of a Linear Search
# def linear_search(x, search_list):
#     """
#     Returns the index of the x if found in search_list
#     Else returns -1
#     """
#     iterations = 0
#     idx = 0
#     while idx < len(search_list):
#         iterations += 1
#         if x == search_list[idx]:
#             print('iterations = ' + str(iterations))
#             return idx
#         idx += 1
#     return -1
#
# # The print statement has to come second, after the function definition
# print(linear_search(14,[1,2,3,4,5,6,14]))
# print(linear_search(14,[100,2,3,8,14,6,1]))


"""
Linear Search does not require a sorted list, as you can see. 
Binary search by contrast needs a sorted list. This can be done afterward too.
The idea is basic. Look half-way down your list each time until you find what you're looking for
"""

####################################
# def binary_search(x,current_savings,search_list):
#     iterations = 1
#     left = 0
#     right = len(search_list)
#     mid = (left + right)//2
#     print("Searching for value",x)
#     while current_savings != x:
#         print(
#             "Left, " + str(left) + ", Right, " + str(right) + ", Mid, " + str(mid) + ", Iteration # " + str(iterations))
#         if search_list[mid] < x:
#             left = mid + 1
#             mid = (right + left)//2
#         else:
#             right = mid - 1
#             mid = (right + left)//2
#         iterations += 1
#     print("Iteration # "+str(iterations))
#     return mid
####################################

"""
So now let's apply this to our assignment
"""
####################################
# Gather Salary Information
####################################
annual_salary = float(input("Enter Starting Salary:"))
####################################
# Initialize Variables for Calculation
####################################
semi_annual_raise = 0.07
r = 0.04                  #r is a variable used as Annual Rate of Return on Savings. Hard-coding to 4% Annual
total_cost = 1000000.0
portion_down_payment = 250000.0
current_savings = 0.0
iterations = 1            #Total Number of Iterations, Start at 1


def calc_savings_after_36_months(guess,m_salary,bonus,int):
    """
    Inputs: guess, an integer betweeon 0 and 10,000 representing savings rate
            m_salary, a float representing monthly salary
            bonus, a float representing the semi-annual raise expected
            int, a float representing the monthly interest rate
    This function calculates the $ user would saved after 36 months with the given inputs using a for loop
    Returns: a float of calculated savings after 36 months
    """
    savings = 0.0
    for imonths in range(1,37):
        if imonths % 6 == 0:
            m_salary = m_salary * (1 + bonus)
        m_savings = guess/10000 * m_salary
        savings = savings + m_savings + (savings * int)
    return savings


def bisection_find_best_savings_rate(left,right,mid,savings_rate,current_savings,portion_down_payment):
    """
    Inputs
    This function uses a bisection search to determine which savings rate user should apply in order to
    put a downpayment on their desired house after 36 months of saving.
    Output is integer
    """
    print("In Bisection: Left is",left,"Right is",right,"Mid is",mid)
    if current_savings < portion_down_payment - 100:
        if mid == 10000:
            print("It is not possible to pay the down payment in three years")
            return 999
        left = mid + 1
        mid = savings_rate[(left + right)//2]
        print("Savings Rate Increased to", mid / 10000)
    elif current_savings > portion_down_payment + 100:
        right = mid - 1
        mid = savings_rate[(left + right)//2]
        print("Savings Rate Decreased to", mid / 10000)
    else:
        print("Steps in Bisection Search:", iterations)
        print("Best Savings Rate:", mid / 10000)
    return left,right,mid


####################################
# Create an Array to represent the savings rate between 0% and 100%
# This will include two decimal points (5 total sig-figs)
####################################
savings_rate = []
for i in range(10001):
    savings_rate.append(i)
####################################

# left_right_mid = []
# left_right_mid.append(0) = 0
# left_right_mid.append(1) = len(savings_rate)-1
# left_right_mid.append(2) = savings_rate[(left_right_mid[0] + left_right_mid[1])//2]

left = 0
right = len(savings_rate)-1
mid = savings_rate[(left + right) // 2]
print("Left is",left,"Right is",right,"Mid is",mid)


while abs(current_savings - portion_down_payment) > 100:
    iterations += 1
    print()
    print("Savings Rate is", mid / 10000)
    monthly_salary = annual_salary / 12  # Monthly Amount Set-Aside.

    # Function Call to Determine Your 36-month Savings
    current_savings = calc_savings_after_36_months(mid, monthly_salary, semi_annual_raise, r / 12)
    print("Savings after 36 months is", current_savings)

    # Function Call to Determine New Bisection Result for Savings Rate
    left,right,mid = bisection_find_best_savings_rate(left,right,mid,savings_rate,current_savings,portion_down_payment)
    print("Savings Rate in While Loop Updated to",mid / 10000)

answer = mid/10000
print("Best Savings Rate:", answer)




