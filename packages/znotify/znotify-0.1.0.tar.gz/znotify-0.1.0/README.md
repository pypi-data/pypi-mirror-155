# notify-py-sdk

Send notifications to [Notify](https://github.com/znotify/Notify)

## Installation

```bash
pip install znotify
```

## Usage

```python
import znotify

client = znotify.Client.create("user_id")
client.send("Hello World")
```

## Development

### Run tests

```bash
python -m unittest discover
```

