def normalize_text(text):
    """
    Convert text into a standard format.

    Example:
        Tamil Nadu -> tamilnadu
        TAMIL NADU -> tamilnadu
        Female -> female
    """

    if text is None:
        return ""

    return (
        str(text)
        .lower()
        .replace(" ", "")
        .replace("-", "")
        .replace("_", "")
    )


def check_eligibility(scheme, user_profile):

    eligibility_rules = scheme.get("eligibility", {})

    reasons = []
    eligible = True

    # --------------------------------
    # STATE
    # --------------------------------

    required_states = eligibility_rules.get("state", [])

    if required_states:

        user_state = normalize_text(
            user_profile.get("state")
        )

        allowed_states = [
            normalize_text(state)
            for state in required_states
        ]

        if user_state not in allowed_states:

            eligible = False

            reasons.append(
                f"State requirement not satisfied. "
                f"Required: {', '.join(required_states)}."
            )

        else:

            reasons.append(
                "State requirement satisfied."
            )

    # --------------------------------
    # GENDER
    # --------------------------------

    required_genders = eligibility_rules.get(
        "gender", []
    )

    if required_genders:

        user_gender = normalize_text(
            user_profile.get("gender")
        )

        allowed_genders = [
            normalize_text(gender)
            for gender in required_genders
        ]

        if user_gender not in allowed_genders:

            eligible = False

            reasons.append(
                f"Gender requirement not satisfied. "
                f"Required: {', '.join(required_genders)}."
            )

        else:

            reasons.append(
                "Gender requirement satisfied."
            )

    # --------------------------------
    # EDUCATION
    # --------------------------------

    required_education = eligibility_rules.get(
        "education_level", []
    )

    if required_education:

        user_education = normalize_text(
            user_profile.get("education_level")
        )

        allowed_education = [
            normalize_text(level)
            for level in required_education
        ]

        if user_education not in allowed_education:

            eligible = False

            reasons.append(
                "Education requirement not satisfied."
            )

        else:

            reasons.append(
                "Education requirement satisfied."
            )

    # --------------------------------
    # GOVERNMENT SCHOOL
    # --------------------------------

    requires_government_school = (
        eligibility_rules.get(
            "studied_government_school"
        )
    )

    if requires_government_school is True:

        studied_government_school = (
            user_profile.get(
                "studied_government_school"
            )
        )

        if studied_government_school is not True:

            eligible = False

            reasons.append(
                "Government school education requirement "
                "not satisfied."
            )

        else:

            reasons.append(
                "Government school requirement satisfied."
            )

    # --------------------------------
    # CATEGORY
    # --------------------------------

    required_categories = eligibility_rules.get(
        "categories", []
    )

    if required_categories:

        user_category = normalize_text(
            user_profile.get("category")
        )

        allowed_categories = [
            normalize_text(category)
            for category in required_categories
        ]

        if user_category not in allowed_categories:

            eligible = False

            reasons.append(
                "Category requirement not satisfied."
            )

        else:

            reasons.append(
                "Category requirement satisfied."
            )

    # --------------------------------
    # FINAL RESULT
    # --------------------------------

    return {
        "scheme": scheme["name"],
        "eligible": eligible,
        "reasons": reasons
    }