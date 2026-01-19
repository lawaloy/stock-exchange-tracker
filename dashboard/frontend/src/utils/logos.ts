export const getCompanyLogoUrl = (symbol: string): string => {
  const cleanSymbol = symbol?.trim().toUpperCase();
  return `https://assets.parqet.com/logos/symbol/${encodeURIComponent(cleanSymbol)}?format=png`;
};
