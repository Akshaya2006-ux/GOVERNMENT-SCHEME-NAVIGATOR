import requests
from bs4 import BeautifulSoup


GOVERNMENT_SCHEME_URL = "https://www.tn.gov.in/schemes.php"


def normalize_text(text):
    if not text:
        return ""

    return (
        str(text)
        .lower()
        .replace(" ", "")
        .replace("-", "")
        .replace("_", "")
    )


def scrape_government_schemes():

    print("\n🌐 Connecting to Tamil Nadu Government website...")
    print(f"🔗 {GOVERNMENT_SCHEME_URL}")

    try:

        response = requests.get(
            GOVERNMENT_SCHEME_URL,
            timeout=10,
            headers={
                "User-Agent": "Government-Scheme-Tracker/1.0"
            }
        )

        response.raise_for_status()

    except requests.RequestException as error:

        print("❌ Failed to access government website.")
        print("Error:", error)

        return []


    print("✅ Government website accessed successfully.")

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    schemes = []


    # Find headings that represent schemes
    headings = soup.find_all(
        ["h2", "h3"]
    )


    for heading in headings:

        name = heading.get_text(
            " ",
            strip=True
        )

        if not name:
            continue


        # Ignore general website headings
        ignored_headings = [
            "Government Schemes",
            "Institute Links",
            "Academics",
            "Contact Us"
        ]

        if name in ignored_headings:
            continue


        # Collect text following the heading
        description_parts = []

        current = heading.find_next_sibling()

        count = 0

        while current and count < 8:

            text = current.get_text(
                " ",
                strip=True
            )

            if text:
                description_parts.append(text)

            current = current.find_next_sibling()

            count += 1


        description = " ".join(
            description_parts
        )


        schemes.append({

            "name": name,

            "description": description,

            "official_source":
                GOVERNMENT_SCHEME_URL

        })


    return schemes


def search_schemes(
    query=None,
    state=None,
    occupation=None
):

    schemes = scrape_government_schemes()


    results = []


    normalized_query = normalize_text(
        query
    )

    normalized_state = normalize_text(
        state
    )


    for scheme in schemes:

        searchable_text = normalize_text(
            scheme.get("name", "")
            + " "
            + scheme.get("description", "")
        )


        # Query filtering
        if normalized_query:

            if normalized_query not in searchable_text:

                # Try individual words
                query_words = [
                    normalize_text(word)
                    for word in str(query).split()
                    if len(word) > 2
                ]

                if not any(
                    word in searchable_text
                    for word in query_words
                ):
                    continue


        # Currently this source is Tamil Nadu
        if normalized_state:

            if normalized_state not in [
                "tamilnadu",
                "tn"
            ]:

                continue


        results.append(scheme)


    return results