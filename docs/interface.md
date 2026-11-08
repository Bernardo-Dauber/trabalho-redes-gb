# Interface contract

What each module exposes. Person 1 (P1) = Link, Person 2 (P2) = Channel & experiments (D16). Change this file only by agreement — both sides code against it.

```python
# source.py  (P1)
load_source(path="data/source.txt") -> str
text_to_bits(text: str) -> np.ndarray          # uint8 0/1, 8 per char, MSB first
bits_to_text(bits: np.ndarray) -> str           # non-printable bytes → "?" (D17)

# line_codes.py  (P1)
LINE_CODES = {"nrz": ..., "manchester": ..., "diff_manchester": ...}
encode(bits) -> chips                           # uint8 0/1
decode(chips) -> tuple[bits, violations: int]   # NRZ always 0 violations
CHIPS_PER_BIT = {"nrz": 1, "manchester": 2, "diff_manchester": 2}

# modulation.py  (P1)
MODULATIONS = {"bpsk": ..., "qpsk": ..., "16qam": ...}
modulate(chips) -> np.ndarray[complex]          # Gray, unit average energy (D9)
demodulate(symbols) -> chips                    # hard decision, nearest point (D3)
CHIPS_PER_SYMBOL = {"bpsk": 1, "qpsk": 2, "16qam": 4}

# channel.py  (P2)
transmit(symbols, ebn0_db, bits_per_symbol, scenario, rng) -> np.ndarray[complex]
#   scenario: "awgn" | "burst"
#   bits_per_symbol = message bits per symbol = η (D10)
#   Es = 1 ⇒ Eb = 1/bits_per_symbol, N0 = Eb / 10^(ebn0_db/10); complex noise, N0/2 per dimension
#   burst constants: P_BAD = 0.01, MEAN_BURST = 20, BAD_EBN0_DB = 0 (D14)

# link.py  (P1, calls P2's channel)
run_link(text, line_code, modulation, scenario, ebn0_db, seed) -> LinkResult
#   LinkResult: ber, bit_errors, n_bits, violations, recovered_text, rx_symbols
```

## `results/raw.csv` — one row per run (D15)

`line_code, modulation, scenario, ebn0_db, seed, n_bits, bit_errors, ber, violations, spectral_efficiency`

- Grid: 3 line codes × 3 modulations × 2 scenarios × Eb/N0 ∈ {0, 2, …, 20} dB × seeds 0..4.
- `rng = np.random.default_rng(seed)`.
