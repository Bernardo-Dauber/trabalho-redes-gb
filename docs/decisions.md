# Registro de decisões

Toda decisão de projeto que tomamos, com o motivo, para podermos explicar "por que escolhemos implementar assim" na apresentação. As mais recentes ficam no fim.

Formato: **Decisão** — o que escolhemos. **Por quê** — o motivo. **Rejeitado** — o que mais consideramos e por que não.

---

## D1 — A codificação de linha fica dentro de uma única cadeia, antes da modulação

**Decisão:** Um único pipeline ponta a ponta: bits da mensagem → codificação de linha → chips → modulação → canal → demodulação → decodificação de linha → bits. As codificações de linha se restringem às que produzem chips *binários*: **NRZ** (referência, sem codificação de linha), **Manchester**, **Manchester Diferencial (bifase)**.

**Por quê:**
- É literalmente o pipeline que o enunciado descreve (geração → codificação de linha → modulação → canal → demodulação → decodificação → métricas).
- Chips binários podem alimentar qualquer modulação, então toda combinação codificação de linha × modulação funciona (grade de resultados 3 × 3).
- Dá material concreto para a explicação exigida de "codificação de linha vs. codificação de correção de erros":
  - Manchester dobra os chips (reduz a eficiência espectral pela metade), mas pares de chips inválidos (`00`/`11`) revelam erros — *detecção*, não correção.
  - Manchester Diferencial propaga erros (1 erro de chip → 2 erros de bit), mas é imune a uma inversão de fase de 180°.

**Rejeitado:**
- *Dois ramos separados* (codificação de linha sobre seu próprio canal em banda base, modulação em outro) — mais limpo, mas as partes nunca interagem e fica menos parecido com um sistema ponta a ponta.
- *AMI na cadeia* — AMI é ternário (−1, 0, +1) e não se mapeia naturalmente em símbolos QPSK/16-QAM. AMI é só um exemplo no enunciado, então deixá-lo de fora é permitido.

## D2 — O eixo x é Eb/N0 por bit da mensagem

**Decisão:** Toda curva de BER usa **Eb/N0 (dB), onde Eb é a energia por bit da mensagem** (o bit ASCII original, antes da codificação de linha). O ruído de cada execução é derivado dele: energia por chip = Eb × (bits da mensagem / chips), energia por símbolo = energia por chip × chips por símbolo.

**Por quê:**
- O enunciado exige "parâmetros equivalentes nas comparações". Dar a toda combinação codificação de linha × modulação a mesma energia por bit da *mensagem* é a única base justa: o custo de cada esquema aparece na curva em vez de ficar escondido.
- Manchester envia 2 chips por bit, então cada chip recebe metade da energia — seu custo de redundância fica visível, que é exatamente o que queremos discutir.
- É o eixo padrão das curvas teóricas de BER, então podemos sobrepor a teoria (item opcional de aprofundamento).
- Na apresentação mostramos a conversão de uma linha para SNR por símbolo (Es/N0 = Eb/N0 × bits por símbolo), para que a palavra "SNR" do enunciado fique explicitamente coberta.

**Rejeitado:**
- *Es/N0 por símbolo* — penaliza o 16-QAM (4 chips por símbolo) e esconde o custo por bit.
- *SNR por chip* — esconde totalmente o custo do Manchester (cada chip receberia a energia inteira).

## D3 — Demodulação por decisão abrupta (hard decision); o decodificador de linha só vê chips

**Decisão:** O demodulador decide cada símbolo e entrega **chips (0/1)**. O decodificador de linha trabalha só com chips. Para Manchester: `01`→0, `10`→1; `00`/`11` é uma **violação** (erro detectado), resolvida por uma regra fixa — pegar o primeiro chip. As violações são contadas como uma métrica extra.

**Por quê:**
- Uma interface uniforme (chips entram, chips saem) permite encaixar qualquer modulação em qualquer codificação de linha sem casos especiais.
- Produz um resultado concreto e explicável: com decisão abrupta e Eb/N0 por bit da mensagem (D2), Manchester deve sair ~3 dB pior que NRZ, já que cada chip recebe metade da energia e é decidido sozinho. Frase para a apresentação: "este é o preço da decisão abrupta; um receptor com decisão suave (soft decision) recuperaria isso."
- Contar violações mostra a capacidade de *detecção* do Manchester (erros detectados vs. erros que de fato aconteceram) — alimenta a discussão codificação de linha vs. correção de erros.

**Rejeitado:**
- *Decisão suave* (passar valores reais; Manchester decodifica como r1 − r2, recuperando a energia completa do bit) — simples para BPSK, mas complicado para QPSK/16-QAM, em que os dois chips de um bit podem cair em símbolos diferentes com confiabilidades diferentes. Mais código e uma fronteira de módulo menos clara, por um ganho que podemos explicar verbalmente.

## D4 — Python + NumPy + Matplotlib, scripts simples, gerenciados com uv

**Decisão:** Python, vetorizado com NumPy, gráficos com Matplotlib. Os experimentos são scripts simples — um comando por experimento grava os resultados brutos (CSV) e os gráficos (PNG). Dependências fixadas e gerenciadas com `uv` (`uv sync`, depois `uv run ...`).

**Por quê:**
- O tamanho do experimento é ~18 combinações × 8+ pontos de Eb/N0 × 5 sementes × 100 mil+ bits ≈ 72 milhões+ de bits; NumPy vetorizado roda isso em segundos a minutos.
- Scripts simples tornam trivial "reproduzir todos os gráficos com um comando" — a rubrica avalia reprodutibilidade.
- `uv` dá uma instalação de dois comandos no README e versões fixadas para resultados reprodutíveis.

**Rejeitado:**
- *Jupyter como fonte da verdade* — estado oculto e ordem das células tornam a reprodução frágil; notebooks geram diffs ruins com duas pessoas editando. (Um notebook ainda pode ser adicionado depois para o vídeo/demonstração de constelação, lendo os CSVs.)
- *MATLAB/Octave* — custo de licença / configuração mais lenta e desajeitada.
- *C++/Rust/JS* — mais rápidos, mas teríamos que escrever nós mesmos a parte numérica e de gráficos, sem benefício na nota.

## D5 — Segundo cenário de canal: ruído em rajadas (Gilbert–Elliott)

**Decisão:** Além do AWGN puro, um **canal com rajadas** modelado como um processo de Gilbert–Elliott de dois estados: um *estado bom* (só AWGN de fundo) e um *estado ruim* (AWGN de fundo + ruído extra muito mais forte), com comprimento médio de rajada fixo. O eixo x continua sendo o Eb/N0 de fundo (D2); a rajada adiciona ruído por cima. Os parâmetros da rajada (fração do tempo no estado ruim, comprimento médio da rajada, nível de ruído do estado ruim) são fixos e registrados junto com os resultados. *(Alterada pela D14: o ruído do estado ruim é um nível absoluto fixo, não um multiplicador do ruído de fundo.)*

**Por quê:**
- É o primeiro exemplo do próprio enunciado ("ruído em rajadas").
- Não precisa de nenhum mecanismo novo no receptor — a demodulação por decisão abrupta (D3) funciona sem mudanças.
- Dá o contraste mais rico com o AWGN:
  - os erros se agrupam → o texto recuperado mostra trechos visíveis de lixo (bom para o vídeo);
  - uma rajada atinge os dois chips de um par Manchester → as violações se comportam diferente do AWGN;
  - a propagação de erros do Manchester Diferencial se acumula dentro de uma rajada;
  - a BER atinge um piso em Eb/N0 alto — mais potência não resolve rajadas.

**Rejeitado:**
- *Desvanecimento plano Rayleigh* — realista, mas a fase aleatória quebra QPSK/16-QAM sem estimação de canal/equalização; ou um atalho injustificado de "CSI perfeita" ou muito mais código.
- *Ruído impulsivo* — mais simples, porém menos interessante: picos isolados, sem agrupamento, parece "AWGN com outliers".

## D6 — Um único texto ASCII longo é a única fonte

**Decisão:** Toda transmissão — incluindo as varreduras de BER — envia o mesmo texto ASCII longo de domínio público (≥ 12.500 caracteres ⇒ ≥ 100.000 bits de mensagem; por exemplo, um trecho de Machado de Assis). As 5 repetições variam só a semente do ruído. Não existe fonte de bits aleatórios.

**Por quê:**
- A rubrica enfatiza a implementação ponta a ponta (item 2) e a recuperação da mensagem. "Todo ponto dos nossos gráficos vem da transmissão de texto real" é uma frase forte para a apresentação, e qualquer execução pode ser mostrada como texto recuperado.
- Uma fonte significa um pipeline — sem "modo estatística" separado de "modo demonstração".

**Efeito conhecido (ponto de discussão, não falha):** ASCII não é aleatório — o bit mais significativo de todo byte é 0. Com 16-QAM isso desequilibra quais pontos da constelação são usados, então a BER medida pode se afastar um pouco da teoria. Manchester cancela esse desequilíbrio (todo bit vira `01` ou `10`).

**Rejeitado:**
- *Bits aleatórios nas varreduras, ASCII só nas demonstrações* — estatisticamente mais limpo, mas as varreduras avaliadas não seriam o sistema ASCII → … → mensagem.
- *Mensagem curta repetida até 100 mil bits* — continua desequilibrada, e repetitiva.

## D7 — Uma grade de Eb/N0 compartilhada: 0 a 20 dB, passo de 2 dB (11 pontos)

**Decisão:** Todas as 18 combinações (3 codificações de linha × 3 modulações × 2 cenários de canal) usam a mesma grade: Eb/N0 = 0, 2, 4, …, 20 dB. Pontos onde nenhum erro é observado não são plotados como 0 (impossível em eixo log), mas como um limite superior (regra de três: BER < 3/N com 95% de confiança, N = bits de mensagem enviados).

**Por quê:**
- Mais que os 8 pontos exigidos, e larga o bastante para a combinação mais lenta: 16-QAM precisa de ~12 dB para BER ≈ 10⁻⁵, mais ~3 dB para Manchester com decisão abrupta (D3) ⇒ ~15 dB.
- Toda combinação chega à sua região sem erros, de que o teste de consistência em SNR alta precisa.
- Uma grade compartilhada mantém as comparações diretas ("parâmetros equivalentes") e permite que a tabela BER × eficiência espectral leia valores no mesmo Eb/N0.
- Custo: 11 × 18 × 5 ≈ 1.000 execuções de 100 mil bits — minutos em NumPy (D4).

**Rejeitado:**
- *0–14 dB (exatamente 8 pontos)* — corta a curva Manchester + 16-QAM antes de ela cair.
- *Grades por modulação* — curvas mais bonitas, mas sem valores de x em comum para as comparações e a tabela de compromisso.

## D8 — Variabilidade: BER média com intervalos de confiança de 95% (t de Student, n = 5)

**Decisão:** Cada ponto de uma curva BER × Eb/N0 é a média das 5 BERs por semente, com barras de erro = intervalo de confiança de 95%: média ± t · s/√5, t ≈ 2,776 (4 graus de liberdade). O limite inferior é cortado onde ficaria ≤ 0 no eixo log — isso é dito no slide. O CSV bruto guarda a BER de cada semente para que qualquer um possa recalcular.

**Por quê:**
- O item 7 da rubrica avalia "análise de variabilidade"; um intervalo de confiança é uma estatística com a qual podemos *raciocinar*: "as curvas são distinguíveis onde seus intervalos não se sobrepõem".
- Explicar por que os intervalos se alargam em BER baixa (poucos erros ⇒ grande incerteza relativa) mostra entendimento estatístico — o que o avaliador valoriza ("capacidade de interpretar os resultados").

**Rejeitado:**
- *Barras mínimo–máximo* — honestas, mas só descritivas; menos para analisar.
- *Média ± 1 desvio padrão* — nem intervalo de confiança nem a faixa real; fácil de interpretar errado.

## D9 — Mapeamento Gray, constelações normalizadas para energia média unitária

**Decisão:** QPSK e 16-QAM usam constelações **com código Gray** (pontos adjacentes diferem em exatamente um chip). Toda constelação (incluindo BPSK) é escalada para energia média de símbolo 1.

**Por quê:**
- Com decisão abrupta (D3), a maioria dos erros de símbolo cai num ponto vizinho; o mapeamento Gray faz esse erro custar ~1 chip em vez de até 4. Frase para a apresentação: "o mapeamento Gray faz um erro de símbolo custar cerca de um bit."
- As curvas teóricas de BER dos livros assumem mapeamento Gray, então a sobreposição teórica opcional se alinha.
- Energia média unitária mantém idêntica a derivação do ruído da D2 para todas as modulações (basta multiplicar pelos chips por símbolo).
- Custo: ~10 linhas de tabelas de consulta.

**Rejeitado:**
- *Rotulação binária natural* — vizinhos podem diferir em 2+ chips, inflando a BER por motivos que não têm a ver com a modulação em si — um fator de confusão que teríamos que justificar.

## D10 — Eficiência espectral nominal = bits de mensagem por chip × chips por símbolo (Nyquist ideal)

**Decisão:** η (bits/s/Hz) = (bits de mensagem por chip) × (chips por símbolo), assumindo pulsos de Nyquist ideais (largura de banda = taxa de símbolos).

| | BPSK | QPSK | 16-QAM |
|---|---|---|---|
| NRZ | 1 | 2 | 4 |
| Manchester / Manchester Diferencial | 0,5 | 1 | 2 |

**Por quê:**
- O enunciado pede eficiência *nominal* — um valor calculado, não medido.
- Simples, exato, e torna visível o custo da codificação de linha: Manchester reduz η pela metade. Junto com sua perda de ~3 dB (D3), Manchester paga tanto em banda quanto em potência, comprando detecção de violações e transições para o relógio — a ideia central da tabela de compromisso.
- Nota para o slide: sistemas reais usam roll-off α, dividindo todas as entradas por (1 + α) sem mudar a ordem.

**Rejeitado:**
- *Roll-off de cosseno levantado na fórmula* — mais realista, mas um parâmetro extra que escala todas as entradas igualmente e não muda nenhuma comparação.
- *η medido pela FFT do sinal* — não é "nominal", exige formatação de pulso e sobreamostragem que não simulamos, muito mais código.

## D11 — Tabela de compromisso: uma linha por codificação de linha × modulação, custo de potência em BER = 10⁻³

**Decisão:** 9 linhas (3 codificações de linha × 3 modulações). Colunas:

| Coluna | Significado |
|---|---|
| η (bits/s/Hz) | da D10 |
| Eb/N0 necessário para BER = 10⁻³ — AWGN | lido da curva, interpolado entre pontos da grade — o custo de potência |
| Eb/N0 necessário para BER = 10⁻³ — rajadas | o mesmo com rajadas; "não atingido" se a curva tiver piso (isso já é um resultado) |
| BER em um Eb/N0 fixo (por exemplo, 10 dB), nos dois canais | retrato direto |
| Melhor quando… | veredito de uma linha, por exemplo "16-QAM/NRZ: SNR de sobra, banda escassa" |

**Por quê:**
- O enunciado pede uma "tabela de compromisso" e *quando* cada modulação é mais adequada; Eb/N0 necessário vs η é exatamente o compromisso potência vs. banda.
- Alvo de 10⁻³ porque, com 100 mil bits, isso significa ~100 erros por semente — estatisticamente sólido, intervalos estreitos (D8). Em 10⁻⁵ seria ~1 erro — ruído.

**Rejeitado:**
- *Alvo de 10⁻⁴* — mais próximo de enlaces reais, mas ~10 erros por semente; precisaria de mais bits (e justificativa) para números sólidos.
- *Só η e BER em um Eb/N0* — perde a coluna de potência necessária, o coração do compromisso.

## D12 — Teste de consistência em duas camadas: pytest sem ruído + demonstração a 20 dB

**Decisão:**
1. **Teste automatizado (pytest), canal sem ruído:** todas as 9 combinações codificação de linha × modulação devem recuperar o texto-fonte *exatamente* (zero erros de bit, string idêntica).
2. **Demonstração a 20 dB** (topo da grade), todas as 18 combinações: imprime a BER e um trecho do texto recuperado. Esperado: AWGN ⇒ texto perfeito; rajadas ⇒ erros residuais mesmo a 20 dB (o piso da D5) — a divergência que explicamos.

Premissa de protocolo: codificador e decodificador Manchester Diferencial compartilham um nível de referência inicial fixo (**baixo**).

Fato verificado: nunca é preciso preenchimento (padding) — 8 bits por caractere sempre se dividem em 1, 2 ou 4 chips por símbolo.

**Por quê:**
- O teste sem ruído é a "validação funcional" da rubrica (item 2), roda em segundos e protege contra regressões enquanto duas pessoas escrevem código.
- A demonstração a 20 dB cobre a parte "explicar eventuais divergências" com uma divergência real e explicável (piso das rajadas) — bom material para o vídeo.

**Rejeitado:**
- *Só a demonstração a 20 dB* — sem garantia automatizada; uma realização de ruído com sorte pode esconder um bug.
- *Só o teste sem ruído* — prova o encanamento, mas não cobre a exigência de "explicar divergências".

## D13 — Aprofundamento opcional: os dois, mantidos enxutos

**Decisão:**
- **Sobreposição teórica:** curvas teóricas de BER tracejadas no gráfico AWGN para as linhas NRZ — BPSK/QPSK: Q(√(2·Eb/N0)); 16-QAM: aproximação Gray padrão. As variantes Manchester recebem as mesmas curvas deslocadas em +3 dB, verificando visualmente a previsão da D3.
- **Diagramas de dispersão da constelação:** 16-QAM, símbolos recebidos em ~3 valores de Eb/N0 (baixo, médio, alto), para os dois cenários de canal.

**Por quê:**
- Se as curvas simuladas ficarem sobre as linhas teóricas, o simulador é validado por um argumento *independente* — mais forte que qualquer teste unitário. Alimenta os itens 7–8 da rubrica ("análise", "conclusões técnicas").
- Os diagramas de dispersão são o material mais visual para o vídeo de 5 minutos: com rajadas, uma nuvem compacta mais pontos espalhados.
- Custo: cerca de uma hora no total (~10 linhas de fórmulas teóricas, ~20 linhas de gráficos).

**Rejeitado:**
- *Só a teoria* — mantém a evidência mais forte, mas perde o visual.
- *Nenhum* — economiza uma hora, perde a validação mais barata e o melhor visual para o vídeo.

## D14 — O ruído do estado ruim é um nível absoluto fixo (altera a D5)

**Decisão:** No canal com rajadas, o estado ruim adiciona ruído em um **nível fixo, independente da varredura de Eb/N0**: Eb/N0 do estado ruim = **0 dB** (nas mesmas unidades por bit de mensagem da D2, para que toda combinação sofra uma rajada equivalente). Valores iniciais (ajustáveis após uma primeira execução, depois congelados e registrados):
- fração do tempo no estado ruim: **1%**
- comprimento médio da rajada: **20 símbolos**
- o processo de rajadas avança por **símbolo** (taxa de símbolos fixa, coerente com a premissa de banda da D10)

**Por quê:**
- Um *multiplicador* de ruído (a redação original da D5) encolhe junto com o ruído de fundo conforme Eb/N0 sobe — as rajadas sumiriam em SNR alta e não haveria piso. Um nível fixo produz um piso real: BER_piso ≈ (fração no estado ruim) × BER(0 dB). Previsível no papel ⇒ mais uma verificação independente contra o gráfico.
- Pisos previstos ≈ 8·10⁻⁴ (NRZ-BPSK) a 1–2·10⁻³ (16-QAM): algumas combinações atingem o alvo de 10⁻³ da D11 com rajadas e outras não — uma tabela que discrimina.
- Rajadas por símbolo: uma rajada de 20 símbolos corrompe 4× mais chips no 16-QAM que no BPSK — realista, e mais um efeito para explicar.

**Rejeitado:**
- *Ruído do estado ruim como multiplicador do ruído de fundo* — sem piso; perde o argumento "mais potência não resolve rajadas" e a demonstração de erros residuais a 20 dB (D12).

## D15 — Um módulo por etapa do pipeline; um CSV de resultados brutos é o contrato execução ↔ gráfico

**Decisão:**
```
src/sim/
  source.py        texto ⇄ bits da mensagem
  line_codes.py    NRZ, Manchester, Manchester Diferencial: bits ⇄ chips (+ contagem de violações)
  modulation.py    BPSK, QPSK, 16-QAM: chips ⇄ símbolos (Gray, energia unitária)
  channel.py       AWGN e rajadas: símbolos + Eb/N0 + semente → símbolos com ruído
  link.py          uma transmissão ponta a ponta → BER, violações, texto recuperado
experiments/
  run_sweep.py     grade completa → results/raw.csv (uma linha por combinação × Eb/N0 × semente)
  make_plots.py    raw.csv → curvas de BER, tabela de compromisso, constelações
  demo.py          demonstração de consistência a 20 dB (D12)
tests/             pytest sem ruído (D12) + pequenos testes por etapa
```
Cada etapa é um par de funções puras (encode/decode, modulate/demodulate) sobre arrays NumPy. Os gráficos nunca rodam a simulação de novo — só leem o CSV.

**Por quê:**
- As fronteiras entre módulos são onde a dupla divide o trabalho; as assinaturas das funções são o que combinamos antes de programar.
- Cada etapa é testável isoladamente.
- O contrato do CSV atende "resultados brutos e scripts para reproduzir todos os gráficos" — exigido explicitamente — e permite começar os gráficos no primeiro dia a partir de um CSV falso.

**Rejeitado:**
- *Um único simulator.py* — conflitos de merge constantes com duas pessoas, sem divisão natural.
- *Hierarquia de classes (classes base Modulator/Channel)* — cerimônia para 3 codificações de linha e 3 modulações; funções simples mais um dicionário de consulta fazem o mesmo trabalho.

## D16 — Divisão do trabalho na fronteira da D15: enlace vs. canal e experimentos

**Decisão:**

| | **Pessoa 1 — Enlace** | **Pessoa 2 — Canal e experimentos** |
|---|---|---|
| Código | `source.py`, `line_codes.py`, `modulation.py`, `link.py`, pytest sem ruído, `demo.py` | `channel.py` (AWGN + rajadas), `run_sweep.py`, `make_plots.py` (curvas + IC, sobreposição teórica, constelações, tabela de compromisso) |
| Apresenta | pipeline, codificação de linha vs. codificação de correção de erros, violações do Manchester, mapeamento Gray, teste de consistência | modelos de canal, justiça do Eb/N0, curvas de BER e variabilidade, tabela de compromisso e conclusões |

Compartilhado: vídeo e README (cada um escreve a sua seção).

**Papéis:** Pessoa 1 (Enlace) = autor do plano (quem tomou as decisões D1–D16 — o lado do enlace é o que mais depende desse raciocínio). Pessoa 2 (Canal e experimentos) = o colega — esse lado é especificado principalmente por fórmulas e parâmetros (D2, D5, D7, D8, D10, D11, D13, D14) e é o mais fácil de assumir sem contexto prévio.

**Por quê:**
- Os dois podem começar no primeiro dia: a Pessoa 2 constrói o canal e os gráficos sobre um CSV falso enquanto a Pessoa 1 constrói a cadeia; eles se encontram em `link.py` e `raw.csv`.
- Carga mais ou menos igual: a cadeia tem mais módulos, o lado dos experimentos carrega a estatística e a análise.
- Cada pessoa apresenta o que construiu — item 1 da rubrica (participação equilibrada) e a "divisão de responsabilidades" do README.

**Rejeitado:**
- *Dividir por modulação/codificação de linha* — os dois mexem em todos os módulos ⇒ conflitos, estilo inconsistente.
- *Um programa, o outro analisa/apresenta* — desequilibrado; quem não programou tem dificuldade com perguntas sobre o código.

## D17 — O texto-fonte é em português, transliterado para ASCII de 7 bits; bytes ilegíveis decodificam como `?`

**Decisão:**
- `data/source.txt` é um texto em português de domínio público (por exemplo, Machado de Assis), ≥ 12.500 caracteres, **transliterado uma vez para ASCII de 7 bits** (Python `unicodedata` NFKD → ASCII, descartando os acentos combinantes: "ação" → "acao"). O trecho de conversão usado uma vez é mantido para que o arquivo seja reprodutível.
- Ao decodificar os bits recebidos, qualquer byte que não seja ASCII imprimível é mostrado como `?` — a decodificação nunca falha, então texto corrompido ainda é impresso na demonstração.

**Por quê:**
- O enunciado diz literalmente "mensagem em ASCII". Acentos em UTF-8 transformariam um caractere em 2 bytes, quebrando "1 caractere = 8 bits" e o fato de não haver padding (D12).
- O português mantém a saída corrompida legível para um público brasileiro no vídeo.
- A regra do `?` torna a saída corrompida visível em vez de travar.

**Rejeitado:**
- *Texto em inglês* — nativamente ASCII e igualmente válido, só menos natural para o público.
- *UTF-8 com acentos* — não é ASCII; viola a exigência.

## D18 — Contrato de interface congelado em `docs/interface.md`

**Decisão:** As assinaturas dos módulos e as colunas do `raw.csv` em `docs/interface.md` são o contrato da dupla; só mudam por acordo. Detalhes resolvidos durante a redação:
- **Manchester Diferencial também reporta violações** — ele tem uma transição no meio de todo bit, então `00`/`11` também é inválido ali. As duas codificações de linha ganham a métrica de detecção.
- **O canal só precisa de η (bits de mensagem por símbolo)** para escalar o ruído de forma justa (D2) — ele nunca precisa saber qual codificação de linha ou modulação produziu os símbolos.
- **Números aleatórios comuns:** sementes 0..4 via `np.random.default_rng(seed)`; toda combinação vê o mesmo ruído para a mesma semente, o que reduz a variância nas *comparações* entre combinações.

**Por quê:** Um contrato escrito permite que os dois trabalhem em paralelo desde o primeiro dia sem bloquear um ao outro (D16).

## D19 — Cronograma, repositório e idioma das entregas

**Decisão — marcos (hoje 8/11; prazo 19/11, link no Moodle até 19h):**

| Data | Marco | Quem |
|---|---|---|
| 8–9/11 | Criar o repositório no GitHub, subir este plano (`CONTEXT.md`, `docs/`), commitar `data/source.txt`, estruturar `uv` + pytest | P1 |
| 9/11 | Colega lê o plano; objeções agora, não depois | P2 |
| 12/11 | **Integração:** pytest sem ruído passando para as 9 combinações (P1); `transmit()` + gráficos a partir de um CSV falso (P2) | ambos |
| 14/11 | Primeira varredura completa → `raw.csv` real; conferir as previsões (Manchester ≈ +3 dB, piso das rajadas ≈ 10⁻³, curvas sobre a teoria); ajustar e congelar os valores das rajadas (D14) | P2 |
| 16/11 | Resultados congelados; rascunho dos slides e do README | ambos |
| 17/11 | Gravar o vídeo (≤ 5 min), commitar no repositório | ambos |
| 18/11 | Folga: ensaiar a apresentação de 10 min, revisão final do README | ambos |
| 19/11 | Link no Moodle antes das 19h; apresentar | ambos |

**Decisão — regras do repositório:**
- Repositório **público** no GitHub — o professor não precisa de convite.
- **Vídeo commitado no repositório** (MP4 < ~50 MB, ou anexado a uma Release do GitHub se for maior). O item 10 da rubrica diz "vídeo disponibilizado no GitHub"; só um link do YouTube é arriscado frente a essa redação.
- **Idioma:** README, slides e vídeo em **português** (idioma da disciplina); código e identificadores em inglês; documentos de planejamento (`docs/`, `CONTEXT.md`) podem ficar em inglês.

**Por quê:** Um ponto de integração cedo (12/11) revela incompatibilidades de interface com uma semana de folga; congelar os resultados em 16/11 deixa três dias para a parte que mais pesa na nota — interpretação e apresentação.

## D20 — Os esquemas são escolhidos pelo nome; a tabela de esquemas é privada de cada módulo

**Decisão:** `line_codes` e `modulation` expõem funções que recebem o nome do esquema como parâmetro — `encode(bits, "manchester")`, `decode(chips, "manchester")`, `chips_per_bit("manchester")`, `modulate(chips, "16qam")`, `demodulate(symbols, "16qam")`, `chips_per_symbol("16qam")` — mais uma tupla `NAMES` para iterar. A tabela nome → implementação fica dentro de cada módulo. Nome desconhecido ⇒ `KeyError`. (Substitui os dicionários `LINE_CODES`/`CHIPS_PER_BIT` esboçados na D18; `docs/interface.md` atualizado.)

**Por quê:**
- O rascunho da D18 tinha dois dicionários descrevendo os mesmos esquemas (`LINE_CODES` e `CHIPS_PER_BIT`) — adiciona-se um esquema em um, esquece-se do outro, e eles divergem silenciosamente. Uma tabela privada não tem como divergir.
- Menor superfície para todo chamador: `link.py` se lê como o pipeline (encode → modulate → transmit → demodulate → decode), a varredura só itera sobre `NAMES`, e as strings dos nomes são exatamente os valores do CSV — sem etapa de tradução.

**Rejeitado:**
- *Um registro por esquema* (`LineCode(name, chips_per_bit, encode, decode)`) — também sem divergência, mas todo chamador precisa aprender o formato do registro e desempacotá-lo.
- *Dicionários separados como esboçado na D18* — risco de divergência.

## D21 — Um modulador genérico sobre três tabelas de constelação

**Decisão:** `modulation.py` tem uma única implementação guiada por uma tabela privada de constelações (`bpsk`: 2 pontos, `qpsk`: 4, `16qam`: 16). O índice *i* de uma tabela é o ponto cujo rótulo de chips é *i* lido em binário, com a ordem Gray embutida na tabela e a escala para energia média unitária aplicada quando a tabela é construída.
- modulate: chips → grupos de `chips_per_symbol` → índice → table[índice]
- demodulate: ponto mais próximo (argmin |símbolo − ponto| sobre a tabela) → índice → chips

Uma função pública `constellation(mod)` devolve os pontos ideais, para que os diagramas de dispersão da constelação (D13) os marquem a partir da mesma tabela.

**Por quê:**
- As três modulações diferem *só* na tabela; uma implementação (~25 linhas) significa um lugar para bugs. Uma nova modulação (8-PSK, 64-QAM) seria só uma nova tabela.
- Mapeamento Gray e energia unitária (D9) são verificados por um teste que percorre todas as tabelas (vizinhos diferem em 1 chip; média de |ponto|² = 1).
- Custo da busca exaustiva pelo ponto mais próximo: ≤ 100 mil × 16 distâncias — milissegundos em NumPy.

**Rejeitado:**
- *Três pares escritos à mão* (sinal da parte real; sinais das partes real/imaginária; limiares por eixo para o 16-QAM) — de livro-texto e um pouco mais rápidos, mas três implementações, cada uma com sua lógica de Gray/energia e seus testes, sem ganho mensurável.

## D22 — Os parâmetros são constantes onde são usados; toda varredura grava um retrato da execução

**Decisão:**
- As constantes das rajadas ficam em `channel.py` (D14); a grade de Eb/N0 e as sementes são constantes no topo de `run_sweep.py`.
- `run_sweep.py` grava `results/raw.csv` **e** `results/run_info.json`: grade, sementes, constantes das rajadas (lidas de `channel.py`, nunca copiadas à mão), bits de mensagem por execução, **hash do commit git + indicador de alterações não commitadas (dirty)**, data e hora. As versões das bibliotecas são fixadas pelo `uv.lock`.
- Os dois arquivos são commitados no git.

**Por quê:**
- Cobre "registrar configurações, variações, número de bits, resultados brutos" e o item 6 da rubrica (reprodutibilidade).
- O hash do commit amarra cada gráfico ao código exato que o produziu; o indicador dirty expõe gráficos feitos a partir de código não commitado antes de os resultados serem congelados (16/11, D19).

**Rejeitado:**
- *Arquivo de configuração (TOML/YAML) + flags de linha de comando* — um parser e uma segunda fonte da verdade para um experimento que tem exatamente uma configuração.
- *Só o CSV* — perde as constantes das rajadas e a versão do código, exatamente o necessário para reproduzir as curvas com rajadas.

## D23 — Varredura sequencial; `run_link` cria o gerador a partir da semente

**Decisão:** `run_sweep.py` é um laço aninhado simples (cenário × codificação de linha × modulação × Eb/N0 × semente) chamando `run_link(..., seed)`, imprimindo uma linha de progresso por combinação. Dentro dele, `rng = np.random.default_rng(seed)` é criado e passado para `transmit()` (D18). Sem paralelismo, a menos que uma execução real se mostre lenta.

**Por quê:**
- 990 execuções × dezenas de ms cada ≈ menos de um minuto — paralelismo não ganha nada.
- Mantém os números aleatórios comuns (D18): a mesma semente dá a mesma fonte de ruído a toda combinação ⇒ menor variância nas comparações. Efeito colateral a mencionar no slide: para uma dada semente, as posições das rajadas são idênticas em todos os valores de Eb/N0, então pontos vizinhos de Eb/N0 são correlacionados (curvas mais suaves); as 5 sementes continuam diferentes entre si.

**Rejeitado:**
- *multiprocessing* — 4–8× mais rápido em algo que já leva menos de um minuto, mais as peculiaridades de inicialização de processos no Windows.
- *Fluxos independentes por combinação (`SeedSequence.spawn`)* — estatisticamente mais puro, mas descarta a redução de variância: comparações mais ruidosas para o mesmo número de bits.

## D24 — Os testes passam só pelo contrato; cada dono testa seus módulos

**Decisão:** Os testes chamam só as funções de `docs/interface.md`, nunca detalhes internos.

| Módulo | Testes (dono) |
|---|---|
| `source` | ida e volta texto → bits → texto; `"A"` → `01000001`; byte não imprimível → `?` (P1) |
| `line_codes` | ida e volta para todo nome em `NAMES`; vetores conhecidos (Manchester `0`→`01`); `00`/`11` injetados contados como violações; **inverter todos os chips ainda decodifica corretamente no Manchester Diferencial** (P1) |
| `modulation` | ida e volta para todo nome; Gray (vizinhos mais próximos diferem em 1 chip); energia média unitária (P1) |
| `channel` | variância do ruído medida ≈ N0; fração do tempo no estado ruim ≈ 1%; comprimento médio da rajada ≈ 20; mesma semente ⇒ mesma saída (P2) |
| `link` | sem ruído, as 9 combinações recuperam o texto exatamente (D12) |
| teoria | a BER de NRZ-BPSK em alguns valores de Eb/N0 concorda com Q(√(2·Eb/N0)) dentro do intervalo de confiança (P2) |

"Sem ruído" não precisa de modo especial: `ebn0_db = math.inf` ⇒ N0 = 0, e o canal AWGN não adiciona nada (adicionado ao contrato).

**Por quê:**
- Testar pelo contrato permite que as implementações mudem sem quebrar os testes.
- Testes por módulo localizam falhas — essencial quando duas pessoas integram em 12/11 (D19).
- O teste de inversão do Manchester Diferencial transforma uma afirmação de slide (D1: imune à inversão de 180°) em evidência; o teste teórico automatiza a verificação independente da D13.

**Rejeitado:**
- *Só o teste ponta a ponta sem ruído* — quando falha, ninguém sabe qual dos 5 módulos quebrou.
- *CI no GitHub Actions a cada push* — barato (~15 linhas de YAML) e ajudaria na qualidade do repositório, mas não escolhido por enquanto; fácil de adicionar depois se a integração der trabalho.
