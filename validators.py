def validate_input(revenue, expenses, assets, liabilities, equity):
    """Basic validation: all numeric, non-negative, accounting equation check"""
    if any(x < 0 for x in [revenue, expenses, assets, liabilities, equity]):
        return False
    # Accounting equation: Assets = Liabilities + Equity (± tolerance for input error)
    return abs(assets - (liabilities + equity)) < 1.0  # $1 tolerance