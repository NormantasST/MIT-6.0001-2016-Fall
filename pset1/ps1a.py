annual_salary = float(input("Enter your annual salary: "))
portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost = float(input("Enter the cost of your dream home: "))

portion_down_payment = 0.25
current_savings = float(0);
r = 0.04
months = 0;

while current_savings < total_cost * portion_down_payment:
    months = months + 1
    current_savings = current_savings + (annual_salary/12)*portion_saved + current_savings/12*r
     
print(months)