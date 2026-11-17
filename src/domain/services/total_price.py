from decimal import Decimal


def calculate_total_price(
    weight_kg: Decimal,
    price_per_kg: int,
    decoration: int = 0,
) -> Decimal:
    total_price = weight_kg * price_per_kg + decoration
    return total_price.quantize(Decimal("0.01"))
