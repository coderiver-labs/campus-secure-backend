
from permission.core.types import PolicyType
class PolicyEngine:

    def __init__(self, policy: dict):
        self.policy: PolicyType = policy

    def evaluate(self, permission_key: str, role: str, action: str, user=None):
        key_policy = self.policy.get(permission_key)
        if not key_policy:
            return False

        role_policy = key_policy.get(role)
        if not role_policy:
            return False

        # admin shortcut
        if role_policy.get("*"):
            return True

        action_rule = role_policy.get(action)

        if action_rule is None:
            return False

        if action_rule is True:
            return True

        if isinstance(action_rule, set):
            if role != "staff":
                return False

            staff_profile = getattr(user, "staff_profile", None)
            if not staff_profile or not staff_profile.position:
                return False

            return staff_profile.position.name in action_rule

        return False