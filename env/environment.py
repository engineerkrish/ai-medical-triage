import random
import os
import yaml

from env.cases import CASES
from env.models import Observation, Action   # ✅ FIXED IMPORT


class MedTriageEnv:
    def __init__(self, difficulty: str = "easy"):
        self.difficulty = difficulty
        self.max_steps = 8
        self.steps = 0
        self.history = []
        self.asked = set()
        self.done = False

        config_path = os.path.join(os.path.dirname(__file__), "..", "openenv.yaml")
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.case = self._choose_case()

    def _choose_case(self):
        cases = CASES.get(self.difficulty, CASES["easy"])
        return random.choice(cases)

    def reset(self):
        self.case = self._choose_case()
        self.history = []
        self.asked = set()
        self.done = False
        self.steps = 0

        return Observation(
            patient_message=self.case["initial"],
            patient_reply="Hello doctor, please help me.",
            asked=[]
        )

    def step(self, action: Action):
        self.steps += 1
        raw_reward = 0.0

        action_type = action.action_type
        content = action.content.lower().strip()

        # Anti-loop
        if len(self.history) >= 1 and action == self.history[-1]:
            raw_reward -= 3

        self.history.append(action)

        reply = "Could you clarify your question?"

        # =========================
        # ASK SYMPTOM
        # =========================
        if action_type == "check_symptom":
            symptom = content   # ✅ FIXED

            if symptom in self.asked:
                raw_reward -= 5
                reply = "You already asked that."
            else:
                self.asked.add(symptom)

                if symptom in self.case.get("hidden_info", {}):
                    raw_reward += 2
                    reply = self.case["hidden_info"][symptom]
                else:
                    raw_reward -= 1
                    reply = "I don't have that issue."

        # =========================
        # FINAL DECISION
        # =========================
        elif action_type == "final":

            if "non-emergency" in content:
                pred = "non-emergency"
            elif "emergency" in content:
                pred = "emergency"
            else:
                pred = "unknown"

            correct = self.case["expected"]["triage"]

            if pred == correct:
                raw_reward += 20
                reply = "Correct triage decision."
            else:
                raw_reward -= 15
                reply = "Incorrect triage decision."

            # Critical symptom reward
            critical = self.case.get("critical_symptoms", [])
            checked = sum(1 for c in critical if c in self.asked)
            raw_reward += checked * 2

            self.done = True

        # =========================
        # INVALID ACTION
        # =========================
        else:
            raw_reward -= 2
            reply = "Invalid action."

        # =========================
        # STEP PENALTY
        # =========================
        if self.steps >= 6 and action_type != "final":
            raw_reward -= 2

        if self.steps >= self.max_steps:
            self.done = True
            raw_reward -= 10
            reply = "Too many steps."

        # =========================
        # EFFICIENCY BONUS
        # =========================
        if self.done:
            bonus = max(0, (self.max_steps - self.steps) * 0.5)
            raw_reward += bonus

        # =========================
        # NORMALIZE
        # =========================
        reward = max(min(raw_reward / 25.0, 1.0), 0.0)

        obs = Observation(
            patient_message=self.case["initial"],
            patient_reply=reply,
            asked=list(self.asked)
        )

        return obs, reward, self.done, {}

    def state(self):
        return {
            "case_id": self.case["id"],
            "difficulty": self.case.get("difficulty", "easy"),
            "steps": self.steps,
            "asked": list(self.asked),
            "history": [str(a) for a in self.history]  # nice logging
        }