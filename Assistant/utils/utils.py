## Utilities required for the Assistant

# Inspect the tool call for the TrustCall
class Spy:
    def __init__(self):
        self.called_tools = []

    def __call__(self , run):
        q = [run]
        while q:
            r = q.pop()
            if r.child_runs:
                q.extend(r.child_runs)
            if r.run_type == "chat_model":
                self.called_tools.append(
                    r.outputs["generations"][0][0]["message"]["kwargs"]["tool_calls"]
                )

