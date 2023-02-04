# Discord Loader

This loader loads conversations from Discord. The user specifies `channel_ids` and we fetch conversations from
those `channel_ids`.

## Usage

Here's an example usage of the DiscoredReader.

```python
from gpt_index import download_loader
import os

DiscordReader = download_loader('DiscordReader')

discord_token = os.getenv("DISCORD_TOKEN")
channel_ids = [1057178784895348746]  # Replace with your channel_id
reader = DiscordReader(discord_token=discord_token)
documents = reader.load_data(channel_ids=channel_ids)
```
