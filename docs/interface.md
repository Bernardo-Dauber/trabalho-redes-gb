# Contrato de interface

O que cada módulo expõe. Pessoa 1 (P1) = Enlace, Pessoa 2 (P2) = Canal e experimentos (D16). Altere este arquivo só por acordo — os dois lados programam contra ele.

Os esquemas são escolhidos por **string de nome** (D20); os nomes são exatamente os valores gravados no CSV. Um nome desconhecido gera `KeyError`.

```python
# source.py  (P1)
load_source(path="data/source.txt") -> str
text_to_bits(text: str) -> np.ndarray          # uint8 0/1, 8 por caractere, MSB primeiro
bits_to_text(bits: np.ndarray) -> str           # bytes não imprimíveis → "?" (D17)

# line_codes.py  (P1)
NAMES = ("nrz", "manchester", "diff_manchester")
encode(bits, code: str) -> chips               # uint8 0/1
decode(chips, code: str) -> tuple[bits, violations: int]   # NRZ sempre 0 violações
chips_per_bit(code: str) -> int                # nrz 1, manchester 2, diff_manchester 2

# modulation.py  (P1)
NAMES = ("bpsk", "qpsk", "16qam")
modulate(chips, mod: str) -> np.ndarray[complex]   # Gray, energia média unitária (D9)
demodulate(symbols, mod: str) -> chips             # decisão abrupta, ponto mais próximo (D3)
chips_per_symbol(mod: str) -> int              # bpsk 1, qpsk 2, 16qam 4
constellation(mod: str) -> np.ndarray[complex] # pontos ideais; índice i = rótulo i lido em binário (D21)

# channel.py  (P2)
transmit(symbols, ebn0_db, bits_per_symbol, scenario, rng) -> np.ndarray[complex]
#   scenario: "awgn" | "burst"
#   bits_per_symbol = bits da mensagem por símbolo = η (D10)
#   Es = 1 ⇒ Eb = 1/bits_per_symbol, N0 = Eb / 10^(ebn0_db/10); ruído complexo, N0/2 por dimensão
#   constantes das rajadas: P_BAD = 0.01, MEAN_BURST = 20, BAD_EBN0_DB = 0 (D14)
#   ebn0_db = math.inf ⇒ N0 = 0: o canal AWGN não adiciona ruído (teste sem ruído, D24)

# link.py  (P1, chama o canal da P2)
run_link(text, line_code, modulation, scenario, ebn0_db, seed) -> LinkResult
#   LinkResult: ber, bit_errors, n_bits, violations, recovered_text, rx_symbols
```

## `results/raw.csv` — uma linha por execução (D15)

`line_code, modulation, scenario, ebn0_db, seed, n_bits, bit_errors, ber, violations, spectral_efficiency`

- Grade: 3 codificações de linha × 3 modulações × 2 cenários × Eb/N0 ∈ {0, 2, …, 20} dB × sementes 0..4.
- `rng = np.random.default_rng(seed)`.

## `results/run_info.json` — gravado por toda varredura ao lado do `raw.csv` (D22)

Grade de Eb/N0, sementes, constantes das rajadas (lidas de `channel.py`, nunca copiadas à mão), bits da mensagem por execução, hash do commit git + indicador de alterações não commitadas (dirty), data e hora. Os dois arquivos são commitados no git.
