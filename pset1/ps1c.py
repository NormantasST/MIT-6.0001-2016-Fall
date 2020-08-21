def main():
    down_payment = 0.25
    semi_annual_raise = 0.07
    investment = 0.04
    total_cost = 1000000
    mistake_factor = 100
    months = 36
    down_payment_cost = down_payment * total_cost
    annual_salary = float(input("Enter the starting salary: "))
    if annual_salary * (months/12) < down_payment_cost:
        print("It is not possible to pay the down payment in three years.")
    else:
        find_savings_rate(down_payment_cost, annual_salary, investment, months, mistake_factor, semi_annual_raise)
    
def find_savings_rate(down_payment_cost, annual_salary, investment, months, mistake_factor, semi_annual_raise):
    low = 0
    high = 10000
    
    number_of_steps = 1
    current_rate = (low + high) // 2.0 #Position of bisection search
    current_price = calculate_savings(annual_salary, investment, months, current_rate / 10000,  semi_annual_raise)
    
    while abs(current_price - down_payment_cost) >= mistake_factor:
        number_of_steps += 1
        if current_price > down_payment_cost:
            high = current_rate
        elif current_price < down_payment_cost:
            low = current_rate
        current_rate = (low + high) // 2
        current_price = calculate_savings(annual_salary, investment, months, current_rate / 10000, semi_annual_raise)
    
    print("Best saving rate:", current_rate / 10000)
    print("Steps in bisection search:", number_of_steps)
        
def calculate_savings(annual_salary, investment, months, current_return, semi_annual_raise):
    current_savings = 0
    for i in range(months):
        current_savings += (annual_salary/12)*current_return + (current_savings/12)*investment
        if (i + 1)% 6 == 0 and i > 0:
            annual_salary += semi_annual_raise * annual_salary
            
    return current_savings

main()