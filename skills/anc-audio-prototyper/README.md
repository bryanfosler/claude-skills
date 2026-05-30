# ANC Audio Prototyper

Design alert sounds that penetrate Active Noise Cancelling headphones, grounded in the University of Salford / Skoda DuoBell research. Built for bike computers but applicable to any product that needs to reach ANC headphone users.

## When to Use

- Designing a bike bell or alert tone for an embedded speaker
- Prototyping sounds that must be heard through ANC headphones
- Evaluating speaker hardware against ANC bypass requirements
- Generating WAV files for on-device testing
- A/B comparing sound designs with research-backed scoring

## What It Produces

- Sound design recommendations with research citations
- ANC penetration scores (0-100) based on DuoBell parameters
- Urgency ratings based on Edworthy psychoacoustic model
- Detection distance estimates from Salford VR study data
- WAV exports (mono, 16kHz, 16-bit signed PCM)

## Prerequisites

- The prototyper tool at `~/Projects/anc-bell-prototyper/`
- A browser (the tool is a standalone HTML/Web Audio API app)
- No API keys or build steps required

## Key Research Parameters

| Parameter | Optimal Value | Why |
|-----------|--------------|-----|
| Fundamental | 750 Hz | ANC attenuation weakest at 700-800 Hz |
| High band | 2800 Hz | Psychoacoustic "bell" recognition + ear canal resonance |
| Attack | 2 ms | Defeats ANC algorithm convergence time |
| Min SPL | 83 dBA @ 2m | Overcomes worst-case ANC attenuation (26 dBA) |
| Pulse rate | 4-8 Hz | Strongest driver of perceived urgency |

## Hardware Requirements

The speaker must support voice coil or balanced armature drivers covering 300-5000 Hz. Piezo-only elements cannot produce the critical 700-800 Hz ANC gap frequency.

## Research Source

University of Salford / Skoda DuoBell Research (Report 07519, March 2026, Dr. Will Bailey et al.)
