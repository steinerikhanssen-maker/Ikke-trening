# GymNotFound – original Codex animation package in GitHub

This directory contains the **full 69-file animation production handoff** (original 7,864,379-byte ZIP from the GymNotFound ChatGPT conversation).

The binary was split into 14 numbered raw byte parts solely because a single large GitHub upload was rejected by the connector. **No files were removed or modified.**

## One-command reconstruction

From the repository root:

```bash
python3 marketing/animation/source-archive/rebuild_archive.py
```

This creates `GymNotFound_Codex_Profesjonell_Animasjon.zip` in this directory. The script verifies ZIP structure, exact size and SHA-256 before publishing the reconstructed file.

- Original ZIP size: **7,864,379 bytes**
- SHA-256: `cdf2332a59d40e7ade8d5db839dba1f1d544ae3685449dd9f0cb5b0873283a6e`
- Parts: 14 x `.partNN` binary files
- Files in reconstructed archive: 69

After reconstruction:

```bash
mkdir -p /tmp/gymnotfound-codex-assets
python3 -m zipfile -e marketing/animation/source-archive/GymNotFound_Codex_Profesjonell_Animasjon.zip /tmp/gymnotfound-codex-assets
```

Read `START_HER_CODEX.txt` inside the extracted `GymNotFound_Codex_Profesjonell_Animasjon` directory, then `verify_bundle.py`.

**Important:** The Blender script in the ZIP is a **starter, not a finished film**. It has not been proven to run in Blender. Codex must perform actual Blender tests, build missing Alex/tree rigs, direct acting and audio, and pass the qualitative release gates in [production instructions](../CODEX_PILOT_PROFF_ANIMASJON.md). Do not present a Ken Burns/slideshow output as a professional animation.

This source is isolated from the WordPress plugin. Do not merge app development or automatically publish a TikTok video.
