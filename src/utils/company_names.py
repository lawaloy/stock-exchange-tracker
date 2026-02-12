"""
Shared company name resolution (pytickersymbols).
Used when saving data so names are stored at write time.
"""
from typing import Dict

# Cached symbol->name lookup - built once, reused
_name_cache: Dict[str, str] = {}


def resolve_company_name(symbol: str, fallback: str = "") -> str:
    """
    Resolve company name when API returns symbol. Uses pytickersymbols.
    Returns real name for S&P 500, NASDAQ 100, Dow Jones symbols.
    """
    if fallback and fallback != symbol:
        return fallback
    if symbol in _name_cache:
        return _name_cache[symbol]
    try:
        from pytickersymbols import PyTickerSymbols
        data = PyTickerSymbols()
        for index_name in ["S&P 500", "NASDAQ 100", "Dow Jones"]:
            try:
                for s in data.get_stocks_by_index(index_name):
                    if s.get("symbol") == symbol and s.get("name"):
                        _name_cache[symbol] = s["name"]
                        return s["name"]
            except Exception:
                continue
    except Exception:
        pass
    _name_cache[symbol] = symbol
    return symbol


def enrich_stock_data_with_names(data: list) -> list:
    """
    Enrich each stock dict with resolved company name when name is missing or equals symbol.
    Modifies in place and returns the same list.
    """
    for row in data:
        symbol = row.get("symbol")
        if not symbol:
            continue
        raw_name = row.get("name", symbol)
        if not raw_name or raw_name == symbol:
            row["name"] = resolve_company_name(symbol, raw_name or symbol)
    return data
