# Vision Analysis: Z.ai MCP Wrapper vs Built-in Tools

## Critical Issue

**The built-in `vision_analyze` tool HALLUCINATES descriptions.** It will confidently describe images that don't exist, see content that isn't there, and provide detailed but completely fabricated analysis.

**The Z.ai Vision MCP wrapper is reliable** and sees actual pixels.

## When This Matters

- Verifying generated images match prompts
- Comparing reference images to generated outputs
- Analyzing video frames for QC
- Any workflow where accurate visual description is required

## Z.ai Vision MCP Wrapper Usage

```bash
# Initialize the MCP server
echo '{"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"hermes","version":"1.0"}}}' | /Users/speed/.hermes/bin/zai-vision-mcp-wrapper

# Send initialized notification
echo '{"jsonrpc":"2.0","method":"notifications/initialized"}' | /Users/speed/.hermes/bin/zai-vision-mcp-wrapper

# Analyze image
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"analyze_image","arguments":{"image_source":"/path/to/image.jpg","prompt":"Describe this image"}}}' | /Users/speed/.hermes/bin/zai-vision-mcp-wrapper
```

## Programmatic Usage (Python)

```python
import subprocess, json, time, select

def read_line(proc, timeout=60):
    start = time.time()
    buf = b""
    while time.time() - start < timeout:
        if select.select([proc.stdout], [], [], 0.1)[0]:
            byte = proc.stdout.read(1)
            if byte == b"\n":
                return buf.decode("utf-8", errors="replace")
            buf += byte
    return buf.decode("utf-8", errors="replace")

proc = subprocess.Popen(
    ["/Users/speed/.hermes/bin/zai-vision-mcp-wrapper"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    bufsize=0
)

# Initialize
init_msg = json.dumps({"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"hermes","version":"1.0"}}})
proc.stdin.write((init_msg + "\n").encode())
proc.stdin.flush()

resp1 = read_line(proc, timeout=10)

# Initialized notification
proc.stdin.write((json.dumps({"jsonrpc":"2.0","method":"notifications/initialized"}) + "\n").encode())
proc.stdin.flush()
time.sleep(0.5)

# Tool call
tool_msg = json.dumps({"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"analyze_image","arguments":{"image_source":"/path/to/image.jpg","prompt":"Describe EXACTLY what is in this image"}}})
proc.stdin.write((tool_msg + "\n").encode())
proc.stdin.flush()

resp2 = read_line(proc, timeout=60)

proc.stdin.close()
proc.wait(timeout=5)

# Parse response
data = json.loads(resp2)
if "result" in data and "content" in data["result"]:
    for item in data["result"]["content"]:
        if item.get("type") == "text":
            print(item["text"])
```

## Example: What Went Wrong

**Task:** Compare three scontent images to Mario Kart generated images

**Built-in vision_analyze said:**
- Image 1: "Cream/off-white chunky cable-knit sweater, hands cradling glass mug with latte"
- Image 2: "Dusty rose/mauve chunky cable-knit sweater, hands resting on lap"
- Image 3: "Dark charcoal/black ribbed-knit sweater, hands holding small dark rectangular device"

**Reality (from Z.ai wrapper):**
- All three images were go-kart racing footage from 1995 VHS tapes
- Mario in costume driving karts on muddy tracks
- Giant mushroom props and banana peels on track
- Spectators and crowds

The built-in tool completely fabricated cozy lifestyle photography descriptions for go-kart racing footage.

## Rule

**NEVER use `vision_analyze` for image verification or comparison.** Always use the Z.ai Vision MCP wrapper when accuracy matters.