from bs4 import BeautifulSoup

def extract(report_html, report_txt):
    with open(report_html, 'r', encoding='utf-8') as file:
        html_cont = file.read()

    soup = BeautifulSoup(html_cont, 'html.parser')
    
    for tag in soup.find_all(True): 
        if tag.name in ['ix:header', 'ix:hidden', 'ix:references', 'ix:resources']:
            tag.decompose()
    
    all_text = soup.get_text(separator=' ') # separator to help with chunking

    with open(report_txt, "w", encoding="utf-8") as file:
        file.write(all_text)

    #print("\nFirst 500 characters:\n", all_text[:500])
    return all_text