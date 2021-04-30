# Returns a link that redirects to the first result from DuckDuckGo
def feeling_ducky(search_terms):
    # print(f'Searching "{search_terms}"')
    search_terms.replace('+', '')
    search_terms = f'\\{"+".join(search_terms.split())}'
    return f'https://duckduckgo.com/?q={search_terms}&t=TransferHero'
