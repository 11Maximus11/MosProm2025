class ExecutorAgent:
    def execute_plan(self, plan: list) -> dict:
        if not plan:
            return {"status": "no_actions_required", "results": []}
        return {"status": "plan_executed_mock", "results": []}