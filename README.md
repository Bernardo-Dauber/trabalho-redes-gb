# Simulador de transmissão digital — Redes de Computadores (GB)

Simulador ponta a ponta de um enlace digital: mensagem ASCII → bits → codificação de linha → modulação → canal ruidoso → demodulação → decodificação → BER e eficiência espectral.

> 🚧 Em construção. Este README será completado ao longo do trabalho (arquitetura, parâmetros, resultados, vídeo).

## Instalação e execução

Requer [uv](https://docs.astral.sh/uv/).

```bash
uv sync            # instala Python 3.12 e as dependências fixadas em uv.lock
uv run pytest      # testes
```

## Arquitetura

| Etapa | Módulo |
|---|---|
| Texto ⇄ bits | `src/sim/source.py` |
| Codificação de linha (NRZ, Manchester, Manchester Diferencial) | `src/sim/line_codes.py` |
| Modulação (BPSK, QPSK, 16-QAM) | `src/sim/modulation.py` |
| Canal (AWGN, rajadas) | `src/sim/channel.py` |
| Enlace ponta a ponta | `src/sim/link.py` |
| Experimentos e gráficos | `experiments/` |

Contrato entre módulos: [`docs/interface.md`](docs/interface.md). Decisões de projeto e justificativas: [`docs/decisions.md`](docs/decisions.md). Glossário: [`CONTEXT.md`](CONTEXT.md).

## Mensagem transmitida

`data/source.txt`: trecho de *Dom Casmurro* (Machado de Assis, domínio público), transliterado para ASCII de 7 bits (12.533 caracteres = 100.264 bits). Regenerar com `uv run python scripts/make_source_txt.py`.

## Divisão de responsabilidades

| Integrante | Responsabilidade |
|---|---|
| _(nome)_ — Pessoa 1 | Enlace: fonte, codificação de linha, modulação, `link.py`, testes, demo |
| _(nome)_ — Pessoa 2 | Canal e experimentos: AWGN e rajadas, varredura, gráficos, tabela de compromisso |
