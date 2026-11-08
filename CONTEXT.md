# Digital transmission simulator

A simulator of a digital communication link — from an ASCII message to the recovered message — used to measure how line coding, modulation and channel noise affect bit error rate and spectral efficiency.

## Language

**Message bit**:
A bit of the original ASCII message, before any line coding. BER is always measured on message bits.
_Avoid_: data bit, info bit (when ambiguous)

**Line code**:
A rule that turns message bits into chips to shape the signal (transitions, polarity), not to correct errors. Our line codes are NRZ, Manchester and Differential Manchester.
_Avoid_: channel coding, encoding (ambiguous with error-correction coding)

**Chip**:
A binary output of the line code; the unit fed to the modulator. With NRZ one message bit is one chip; with Manchester and Differential Manchester one message bit is two chips.
_Avoid_: coded bit, sub-bit

**Modulation**:
The mapping of groups of chips onto complex symbols (BPSK, QPSK, 16-QAM).
_Avoid_: line coding

**Symbol**:
One point of a modulation's constellation; carries 1 (BPSK), 2 (QPSK) or 4 (16-QAM) chips.

**Eb/N0**:
Energy per message bit over noise power spectral density, in dB; the single x-axis of every BER curve. When the assignment says "SNR", we mean this.
_Avoid_: SNR (unqualified), Es/N0, chip SNR

**Violation**:
A received chip pair that no message bit can produce under Manchester or Differential Manchester (`00` or `11`); a detected error. It is still decoded to a bit by a fixed rule.
_Avoid_: invalid symbol, decoding error

## Channel

**Channel scenario**:
One of the two noise models a transmission passes through: the AWGN channel or the burst channel.
_Avoid_: channel type, noise mode

**AWGN channel**:
The baseline channel scenario: independent Gaussian noise on every symbol, set by Eb/N0.

**Burst channel**:
The second channel scenario: the AWGN channel plus a burst process that, while in the bad state, adds much stronger noise.
_Avoid_: fading channel, degraded channel

**Bad state**:
The burst channel's condition in which extra noise, at a fixed level independent of Eb/N0, is added on top of the background noise. Its opposite is the good state (background noise only).
_Avoid_: error state, noisy mode

**Burst**:
A contiguous run of symbols during which the burst channel is in the bad state.
_Avoid_: rajada (in code/docs; fine in the presentation)

## Source

**Source text**:
The single long public-domain Portuguese text, transliterated to 7-bit ASCII, that every transmission sends; the origin of all message bits (8 per character).
_Avoid_: payload, input data, random bits

## Modulation

**Constellation**:
The set of complex points a modulation can send, Gray-labelled and scaled to unit average energy.
_Avoid_: symbol map, alphabet

## Metrics

**BER**:
Fraction of message bits recovered wrong, after line decoding.
_Avoid_: chip error rate, symbol error rate (different quantities)

**Spectral efficiency**:
The nominal message bits per second per hertz a line code × modulation combination delivers, assuming ideal Nyquist pulses.
_Avoid_: throughput, bandwidth efficiency, data rate
