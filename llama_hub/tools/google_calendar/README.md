# Google Calendar Tool

This tool connects to a Google account and allows an Agent to read and create new events on that users calendar.

As a prerequisite, you will need to register with Google and generate a `credentials.json` file in the directory where you run this loader. See [here](https://developers.google.com/workspace/guides/create-credentials) for instructions.

## Usage

This tool has more extensive example usage documented in a Jupyter notebook [here](https://github.com/emptycrown/llama-hub/tree/main/llama_hub/tools/notebooks/google_calendar.ipynb) and [here](https://github.com/emptycrown/llama-hub/tree/main/llama_hub/tools/notebooks/advanced_tools_usage.ipynb)


Here's an example usage of the GoogleCalendarToolSpec.

```python
from llama_hub.tools.google_calendar.base import GoogleCalendarToolSpec
from llama_index.agent import OpenAIAgent

tool_spec = GoogleCalendarToolSpec()

agent = OpenAIAgent.from_tools(tool_spec.to_tool_list())

agent.chat("Please create an event on june 15th, 2023 at 5pm for 1 hour and invite xyz@abc.com to discuss tax laws")
agent.chat('What is on my calendar for today?')
```

`load_data`: Load the upcoming events from your calendar
`create_event`: Creates a new Google Calendar event
`get_date`: Utility for the Agent to get todays date

This loader is designed to be used as a way to load data as a Tool in a Agent. See [here](https://github.com/emptycrown/llama-hub/tree/main) for examples.

