class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register_tool(self, tool_name, tool):
        self.tools[tool_name] = tool

    def get_tool(self, tool_name):
        return self.tools.get(tool_name)