from langchain.tools import tool
from backend.services.currency_api import get_conversion_rate

@tool
def get_currency_rate_tool(base_currency: str, target_currency: str) -> float:
    """
    Returns ONLY the exchange rate between two currencies.
    Example:
    base_currency='USD', target_currency='NPR   '
    """
    return get_conversion_rate(base_currency, target_currency)


@tool
def convert_currency_tool(
    amount: float,
    base_currency: str,
    target_currency: str
) -> str:
    """
    Converts amount from base_currency to target_currency.
    Uses real exchange rate and Python math.
    """
    rate = get_conversion_rate(base_currency, target_currency)
    converted = amount * rate
    return f"{amount} {base_currency} = {converted:.2f} {target_currency}"
