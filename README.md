# YouTube News

## Usage

Run the following commands in sequence:

1. Load initial channel data:
```bash
python preload_channels.py
```

2. Load videos for each channel
```bash
python preload_videos.py
```

3. Start the FastAPI development server:

```bash
fastapi dev main.py 
```

The API will be available at `http://localhost:8001`
