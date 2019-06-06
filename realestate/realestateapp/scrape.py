from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
# from models import (Livability)

def getLivability(cityProp, stateProp):
    my_url = 'https://www.areavibes.com/search/'
    my_domain = 'https://www.areavibes.com'
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    container = page_soup.findAll("ul", {"class":"stacked-place-list"})
    for a in container[0].findAll("a"):
        link = my_domain + a['href']
        state2 = a['href'][1:-1]
        if state2.lower() == stateProp.lower():
            uClientState = uReq(link)
            page_html_state = uClientState.read()
            uClientState.close()
            page_soup_state = soup(page_html_state, "html.parser")
            container_city = page_soup_state.findAll("ul", {"id":"all-cities"})
            for a_city in container_city[0].findAll("a"):
                link_city = my_domain + a_city['href']
                cityString = a_city.string
                if cityString.lower() == cityProp.lower():
                    uClientCity = uReq(link_city)
                    page_html_city = uClientCity.read()
                    uClientCity.close()
                    page_soup_city = soup(page_html_city, "html.parser")
                    container_score = page_soup_city.find("div", {"class":"score-hero-info"})
                    bc = page_soup_city.find("div",{"class":"bc"})
                    all_a = bc.findAll("a")
                    state = all_a[1].string
                    score = container_score.em.string
                    city = container_score.h2.string
                    return (int(score))
                    # livability = Livability()
                    # livability.city = city
                    # livability.state = state
                    # livability.score = score
                    # livability.save()