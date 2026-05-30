---
name: anc-audio-prototyper
description: >
  Design and prototype audio signals optimized for penetrating Active Noise
  Cancelling headphones, based on the Skoda/Salford DuoBell research. Use when
  designing alert sounds, bike bells, or warning signals for any product that
  needs to reach users wearing ANC headphones. Covers frequency optimization,
  psychoacoustic design, hardware constraint matching, and Web Audio API
  prototyping.
---

# ANC Audio Prototyper

Design alert sounds that penetrate noise-cancelling headphones, grounded in
peer-reviewed acoustic research and constrained to specific hardware specs.

## When to Use

- Designing alert tones that must be heard through ANC headphones
- Prototyping bike bell or warning sounds for embedded speakers
- Evaluating audio hardware capabilities against ANC bypass requirements
- Generating WAV files for on-device testing
- Comparing sound designs using A/B methodology

## Research Foundation

All recommendations are based on the **University of Salford / Skoda DuoBell
research** (Report 07519, March 2026, Dr. Will Bailey et al.):

### Key Findings

1. **ANC Gap Frequency: 700-800 Hz**
   - ANC attenuation is weakest for tonal signals below 1000 Hz
   - 3 dB local dip in attenuation at the 800 Hz band for tone-in-tone signals
   - Tonal signals attenuated 4.9 dB less than mixed, 8.9 dB less than noise
   - No statistically significant effect from impulsivity or decay time

2. **Dual-Band Design: 700-800 Hz + 2000+ Hz**
   - Low band (700-800 Hz) penetrates ANC passive isolation
   - High band (2000+ Hz) provides psychoacoustic "bike bell" recognition
   - Both bands should have comparable sound power

3. **Detection Distance Improvement**
   - 750 Hz tuned bells detected 9.2m further away in quiet park
   - 2.3 dB improvement in detection threshold
   - ANC headphones reduced overall detection by 14.6m / 3.3 dB SPL

4. **Minimum SPL: 83 dBA @ 2m**
   - Overcomes ANC attenuation (8-26 dBA depending on headphone)
   - Below hearing damage threshold (85 dBA continuous / 137 dBA peak)

5. **Sharp Transient Attack**
   - Front-loaded acoustic energy defeats ANC processing latency
   - ANC algorithms need convergence time (FXLMS: tens-hundreds of ms)
   - Bursts shorter than convergence time partially leak through

6. **Headphone Attenuation Ranges (6 models tested)**
   - Apple AirPods Max: 26 dBA (worst case)
   - Sony WX1000: 20 dBA
   - Bose QuietComfort: 18 dBA
   - JBL Live Pro: 17 dBA
   - Apple AirPods Pro: 14 dBA
   - Samsung Galaxy Buds: 8 dBA

### Psychoacoustic Amplifiers (Edworthy et al.)

These techniques increase perceived urgency and detectability at lower SPL:

- **Auditory looming**: Rising intensity triggers evolutionary threat detection
- **Fletcher-Munson**: 2-4 kHz region perceived as loudest per unit SPL
- **Rapid pulse rate (4-8 Hz)**: Strongest driver of perceived urgency
- **AM modulation (8-12 Hz)**: Creates warbling that is harder for ANC to cancel
- **Inharmonic spectrum**: Non-integer harmonics increase urgency vs pure tones
- **Chirp sweep**: Non-stationary signals force ANC to continuously re-converge

## Hardware Requirements

To produce ANC-optimized bells, the speaker must be capable of:
- Reproducing 700-800 Hz at adequate SPL (rules out piezo-only drivers)
- Voice coil or balanced armature driver recommended
- Frequency response covering at least 300-5000 Hz
- SPL output of 40-85 dBA range
- Wet/weather operation with minimal housing attenuation
- WAV playback: mono, 16kHz, 16-bit signed PCM

## Prototyping Tool

The ANC Bell Prototyper lives at:

```
~/Projects/anc-bell-prototyper/ANC-Bell-Prototype-Beeper-vs-Speaker.html
```

Open with `open ~/Projects/anc-bell-prototyper/ANC-Bell-Prototype-Beeper-vs-Speaker.html`

### Features

- **Tone generator**: Fundamental frequency, waveform, attack/decay envelope
- **Dual-band mixing**: Independent high-frequency band with adjustable mix
- **Custom harmonics**: Add/remove arbitrary frequency components
- **Pulse patterns**: Count, rate, looming (rising intensity), chirp sweep
- **AM modulation**: Warbling effect with rate and depth control
- **8 research-based presets**: From pure DuoBell to max penetration
- **ANC penetration score**: 0-100 rating based on research parameters
- **Urgency rating**: Based on Edworthy psychoacoustic model
- **Detection distance estimate**: Extrapolated from Salford VR study data
- **Speaker response curve overlay**: See how the speaker shapes the sound
- **ANC attenuation overlay**: Visualize where ANC is weakest
- **A/B comparison**: Two slots to compare designs side-by-side
- **WAV export**: Mono 16kHz 16-bit PCM
- **Experiment log**: Name, rate, and annotate sounds with CSV export
- **Shareable URLs**: Encode presets in URL hash for team sharing
- **Keyboard shortcuts**: Space/S/L/E/1-8/A/B/N/O for rapid iteration

### Optimal Starting Point

Based on the research, the optimal ANC bell design:

```
Fundamental:     750 Hz (ANC gap center)
High band:       2800 Hz @ 55% mix (bell recognition + ear canal resonance)
Waveform:        Sine (least ANC attenuation per research)
Attack:          2 ms (defeats ANC convergence)
Decay:           50 ms
Burst duration:  55 ms
Pulse count:     4 @ 7 Hz
Looming:         40% (rising intensity)
Chirp:           35% (non-stationary for ANC)
AM:              8 Hz @ 60% depth (warble)
Harmonics:       1500 Hz @ 40%, 3200 Hz @ 25%
```

## Workflow

1. **Start with research presets** — Use presets 1-8 to hear the range
2. **Check scores** — ANC penetration > 70 and urgency > 50 are targets
3. **A/B compare** — Switch slots to compare designs
4. **Log experiments** — Press N to annotate what you hear
5. **Export WAV** — Use the 16kHz export for on-device testing
6. **Share with team** — Use Share URL to send exact parameters

## Reference

```
Skoda DuoBell Research PDF:
  https://d2p6e6u75xmxt8.cloudfront.net/2/2026/04/Skoda-DuoBell-Research-final.pdf

WAV format: ffmpeg -i <INPUT>.wav -ac 1 -ar 16000 -acodec pcm_s16le <OUTPUT>.wav
```
