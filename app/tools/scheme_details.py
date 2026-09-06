def get_scheme_details(scheme):

    return {
        "name": scheme["name"],
        "benefit": scheme["benefit"],
        "income_limit": scheme["income_limit"],
        "age_range": (
            scheme["min_age"],
            scheme["max_age"]
        ),
        "documents": scheme["documents"]
    }