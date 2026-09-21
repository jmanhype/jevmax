# Resume the live Comedy Test Sprint

The Codex shell sandbox currently has no DNS configuration and blocks direct
DNS sockets, including the host's Tailscale MagicDNS resolver at
`100.100.100.100`. Run the following from a normal macOS Terminal, where the
host resolver is available:

```bash
cd /Users/batmanosama/jevmax
sh studio/comedy/resume-live-selection.sh
```

The script:

1. preserves the already generated 120-premise corpus when present
2. runs live Jev round one to 24 survivors
3. mutates all survivors
4. runs live Jev round two to eight finalists
5. creates eight board prompts
6. creates the PixVerse board queue command file
7. validates the selection artifacts

It does **not** submit PixVerse image or video generation.

After the script finishes, return to Codex and say:

```text
Live selection completed. Continue from the comedy artifacts.
```
