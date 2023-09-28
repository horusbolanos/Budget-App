class Category:
    def __init__(self, category):
        self.category = category
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        return sum(item["amount"] for item in self.ledger)

    def transfer(self, amount, budget_category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {budget_category.category}")
            budget_category.deposit(amount, f"Transfer from {self.category}")
            return True
        return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def __str__(self):
        title = f"{self.category:*^30}\n"
        items = ""
        total = 0
        for item in self.ledger:
            items += f"{item['description'][:23]:<23}{item['amount']:7.2f}\n"
            total += item['amount']
        output = title + items + f"Total: {total:.2f}"
        return output


def create_spend_chart(categories):
    chart = "Percentage spent by category\n"
    spendings = []
    total_spent = 0

    for category in categories:
        spent = sum(item["amount"] for item in category.ledger if item["amount"] < 0)
        spendings.append(spent)
        total_spent += spent

    percentages = [int(spent / total_spent * 100) for spent in spendings]

    for i in range(100, -1, -10):
        chart += str(i).rjust(3) + "| "
        for percent in percentages:
            chart += "o" if percent >= i else " "
            chart += "  "
        chart += "\n"

    chart += "    ----------\n"

    max_len = max(len(category.category) for category in categories)
    categories_str = [category.category.ljust(max_len) for category in categories]

    for i in range(max_len):
        chart += "     "
        for category in categories_str:
            chart += category[i] + "  "
        chart += "\n"

    return chart.rstrip("\n")

# Crear categorías y realizar transacciones
food_category = Category("Food")
clothing_category = Category("Clothing")

food_category.deposit(1000, "Initial deposit")
food_category.withdraw(10.15, "Groceries")
food_category.withdraw(15.89, "Restaurant and more foo")
food_category.transfer(50, clothing_category)

# Imprimir resumen de categoría
print(food_category)
print(clothing_category)

# Crear una lista de categorías
categories = [food_category, clothing_category]

# Imprimir gráfico de gastos
print(create_spend_chart(categories))

