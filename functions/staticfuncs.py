import aiohttp
import xml.etree.ElementTree as ET

def url_holder_region(region_name, query):
    return f"https://www.nationstates.net/cgi-bin/api.cgi?region={region_name}&q={query}"

def url_holder_nation(nation_name, query):
      return f"https://www.nationstates.net/cgi-bin/api.cgi?nation={nation_name}&q={query}"

def splitter(query):
    x = str(query).split('.')[0]
    return x

async def process_vote(session, url, headers, parent_element, for_element, against_element):
    async with session.get(url, headers=headers) as response:
        data = await response.text()
        root = ET.fromstring(data)
        vote_parent_element = root.find(parent_element)
        for_element = vote_parent_element.find(for_element)
        against_element = vote_parent_element.find(against_element)

        if for_element is not None:
            for_vote = for_element.text
        else:
            for_vote = 'N/A'
        
        if against_element is not None:
            against_vote = against_element.text
        else:
            against_vote = 'N/A'

        return for_vote, against_vote

async def nation_ga_vote(session, url, headers):
    async with session.get(url, headers=headers) as response:
        data = await response.text()
        root = ET.fromstring(data)
        vote = root.find('GAVOTE').text
        return vote

async def nation_sc_vote(session, url, headers):
    async with session.get(url, headers=headers) as response:
        data = await response.text()
        root = ET.fromstring(data)
        vote = root.find('SCVOTE').text
        return vote

async def get_banner(session, url, headers):
    async with session.get(url, headers=headers) as response:
        data = await response.text()
        root = ET.fromstring(data)
        _banner = root.find('BANNER').text
        return _banner

async def get_things(session, url, element, headers):
    async with session.get(url, headers=headers) as response:
        data = await response.text()
        root = ET.fromstring(data)
        _element = root.find(element).text
        return _element
    
async def get_wa_badge(session, url, headers):
    async with session.get(url, headers=headers) as response:
        data = await response.text()
        root = ET.fromstring(data)
        
        try:
            badge = root.find('.//WABADGE')
            _type = badge.get('type')
            res_id = badge.text
        except AttributeError:
            _type = None
            res_id = None
        
        return _type, res_id


async def get_census(session, headers, _type, nr, element, scale: int):
    async with session.get(f"https://www.nationstates.net/cgi-bin/api.cgi?{_type}={nr};q=census;scale={scale}", headers=headers) as response:
        data = await response.text()
        root = ET.fromstring(data)
        census = root.find('CENSUS')
        scale = census.find('SCALE')
        r = scale.find(element).text
        r = f'{float(r):,.2f}'
        return r
