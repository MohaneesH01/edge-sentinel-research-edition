# GitHub Publish Guide

Use this guide to publish Edge Sentinel Research Edition to GitHub.

## Recommended Repository Settings

Repository name:

```text
edge-sentinel-research-edition
```

Visibility:

```text
Public
```

Do not initialize the GitHub repo with:

- README
- `.gitignore`
- license

Those files already exist locally.

## Option 1: Push With HTTPS

After creating the empty GitHub repository, run:

```bash
git remote add origin https://github.com/MohaneesH01/edge-sentinel-research-edition.git
git push -u origin main
```

If GitHub asks for a password, use a GitHub personal access token instead of your account password.

## Option 2: Push With SSH

First make sure your SSH key is added to GitHub.

Then run:

```bash
git remote add origin git@github.com:MohaneesH01/edge-sentinel-research-edition.git
git push -u origin main
```

## Professional Repository Description

Use this GitHub description:

```text
Low-cost ESP32-based renewable-energy monitoring and TinyML fault-detection research prototype.
```

## Suggested Topics

Add these topics on GitHub:

```text
esp32
tinyml
renewable-energy
solar-monitoring
fault-detection
iot
mqtt
edge-ai
embedded-systems
machine-learning
```

## Suggested Pinned Repository Summary

Use this when pinning the repository on your profile:

```text
Edge Sentinel Research Edition is an ESP32-based solar monitoring and fault-detection platform using INA219/DHT22 sensing, MQTT telemetry, local analytics, and TinyML-ready edge inference.
```

## After Pushing

1. Pin the repository on your GitHub profile.
2. Add the SLD image from `docs/assets/edge_sentinel_sld.svg` to the repository README later if you want a visual first impression.
3. Keep committing hardware progress:
   - `docs: add first hardware wiring photo notes`
   - `data: document normal operation collection session`
   - `feat: log live MQTT telemetry from ESP32`
   - `docs: update experimental results with hardware data`
