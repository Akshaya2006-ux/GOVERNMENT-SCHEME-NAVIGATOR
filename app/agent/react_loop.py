import json

from app.agent.state import AgentState
from app.agent.reasoning import ask_gemini

from app.tools.scheme_search import search_schemes
from app.tools.eligibility import check_eligibility
from app.tools.scheme_details import get_scheme_details


class ReActAgent:

    def __init__(self):
        self.state = None

    def run(self, user_query, user_profile=None):

        self.state = AgentState(user_query)

        if user_profile is None:
            user_profile = {}

        self.state.user_profile.update(user_profile)

        print("\n🧠 GEMINI: Understanding your request...")

        # -----------------------------------------
        # STEP 1: Extract information from user
        # -----------------------------------------

        extraction_prompt = f"""
You are an AI assistant for a Government Scheme Tracker.

Extract structured information from the user's message.

User message:
{user_query}

Return ONLY valid JSON.

Use exactly these fields:

{{
    "goal": "",
    "age": null,
    "gender": null,
    "state": null,
    "occupation": null,
    "income": null,
    "category": null,
    "education_level": null,
    "studied_government_school": null
}}

If information is not provided, use null.

User message:
{user_query}
"""

        extracted = ask_gemini(extraction_prompt)

        print("\n📋 Gemini extracted:")
        print(extracted)

        # Try to convert Gemini response to JSON
        try:

            extracted = extracted.strip()

            if extracted.startswith("```"):
                extracted = extracted.replace("```json", "")
                extracted = extracted.replace("```", "")

            profile = json.loads(extracted)

        except Exception:

            print(
                "\n⚠️ Could not parse Gemini profile."
            )

            profile = {}

        # -----------------------------------------
        # STEP 2: Update agent state
        # -----------------------------------------

        for key, value in profile.items():

            if value is not None:

                if key == "goal":
                    self.state.goal = value

                else:
                    self.state.update_profile(
                        key,
                        value
                    )

        # -----------------------------------------
        # STEP 3: Gemini decides what to do
        # -----------------------------------------

        planning_prompt = f"""
You are the reasoning engine of a Government Scheme Tracker.

User query:
{user_query}

Extracted user information:
{json.dumps(self.state.user_profile, indent=2)}

Available tools:

1. search_schemes
   Searches the government scheme dataset.

2. check_eligibility
   Checks whether a user satisfies scheme requirements.

3. get_scheme_details
   Gets benefit, documents and application information.

Decide the next action.

Return ONLY JSON in this format:

{{
    "action": "search_schemes"
}}

Possible actions:

search_schemes
check_eligibility
get_scheme_details
final_answer

Do not explain your reasoning.
"""

        decision = ask_gemini(planning_prompt)

        print("\n🧠 GEMINI ACTION:")
        print(decision)

        try:

            if decision.startswith("```"):
                decision = decision.replace("```json", "")
                decision = decision.replace("```", "")

            decision = json.loads(decision)

        except Exception:

            decision = {
                "action": "search_schemes"
            }

        action = decision.get(
            "action",
            "search_schemes"
        )

        # -----------------------------------------
        # STEP 4: Execute search
        # -----------------------------------------

        if action == "search_schemes":

            print(
                "\n🔎 ACTION: Searching government schemes..."
            )

            self.state.add_action(
                "search_schemes"
            )

            schemes = search_schemes(
                query=self.state.goal,
                state=self.state.user_profile.get(
                    "state"
                ),
                occupation=self.state.user_profile.get(
                    "occupation"
                )
            )

            self.state.candidate_schemes = schemes

            observation = (
                f"Found {len(schemes)} candidate schemes."
            )

            print(
                "📋 OBSERVATION:",
                observation
            )

            self.state.add_observation(
                observation
            )

            # -----------------------------------------
            # STEP 5: Ask Gemini for final response
            # -----------------------------------------

            final_prompt = f"""
You are a Government Scheme Assistant.

User asked:
{user_query}

User information:
{json.dumps(self.state.user_profile, indent=2)}

Candidate schemes found:
{json.dumps(schemes, indent=2, ensure_ascii=False)}

Give a helpful answer.

Important:
- Do not invent eligibility requirements.
- Clearly say when eligibility cannot yet be confirmed.
- If important information is missing, ask the user for it.
- Mention the scheme benefit.
- Mention important documents.
- Keep the answer easy to understand.
"""

            final_answer = ask_gemini(
                final_prompt
            )

            self.state.final_answer = final_answer

            return final_answer

        # -----------------------------------------
        # FALLBACK
        # -----------------------------------------

        return (
            "I found your request, but I need "
            "more information to continue."
        )