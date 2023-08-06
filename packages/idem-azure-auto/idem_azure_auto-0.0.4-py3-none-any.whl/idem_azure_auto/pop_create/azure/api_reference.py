from typing import List

try:
    import bs4
    import requests
    import tqdm

    HAS_LIBS = (True,)
except ImportError as e:
    HAS_LIBS = False, str(e)


def __virtual__(hub):
    return HAS_LIBS


def parse_file(hub, file_path: str, base_url="https://docs.microsoft.com"):
    """
    Parse a page such as this one: https://docs.microsoft.com/en-us/rest/api/?view=Azure

    Create a pretty version of a list of Azure services"
    """
    hub.log.warning(
        "This function should be deprecated and replaced with parsing the URL directly"
    )
    with open(file_path) as f:
        html = f.read()
    soup = bs4.BeautifulSoup(html, "lxml")

    return soup


def parse_url(hub, url: str):
    """
    Parse a page such as this one: https://docs.microsoft.com/en-us/rest/api/?view=Azure

    Create a pretty version of a list of Azure services"
    """
    with requests.get(
        url, params={"textDecorations": True, "textFormat": "HTML"}
    ) as response:
        # Evaluate js on page
        html = response.text
        if response.status_code != 200:
            return {}

    assert "Advisor" in html
    soup = bs4.BeautifulSoup(html, parser="lxml")

    return soup


def parse(hub, soup: bs4.BeautifulSoup, resources: List[str] = None):
    base_url = "https://docs.microsoft.com"
    plugins = {}

    # Parse page and get links, names, and descriptions of each Azure service
    parsing_results = []
    api_table = soup.find(class_="api-search-results")
    table_body = api_table.find("tbody")
    for row in table_body.find_all("tr"):
        try:
            cols = row.find_all("td")
            name = cols[0].find("a").text
            if resources and name not in resources:
                hub.log.debug(f"Skipping resource: {name}")
                continue

            parsing_result = {
                "name": name,
                "url": base_url + cols[0].find("a")["href"],
                "description": cols[1].text,
            }
            parsing_results.append(parsing_result)
        except [AttributeError, KeyError] as parse_error:
            hub.log.error.error(
                f"Fail to parse table from url {base_url} at row {str(row)}. Error: {parse_error}"
            )

    progress = tqdm.tqdm(parsing_results)
    for api_reference_data in progress:
        name = api_reference_data["name"]
        progress.set_description(name)
        plugins[name] = hub.pop_create.azure.rest.parse(
            url=api_reference_data["url"], desc=api_reference_data["description"]
        )

    return plugins
