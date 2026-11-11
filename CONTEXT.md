# Simulador de transmissão digital

Um simulador de um enlace de comunicação digital — da mensagem ASCII até a mensagem recuperada — usado para medir como a codificação de linha, a modulação e o ruído do canal afetam a taxa de erro de bits e a eficiência espectral.

Cada termo traz entre parênteses o nome em inglês usado no código.

## Linguagem

**Bit da mensagem** (*message bit*):
Um bit da mensagem ASCII original, antes de qualquer codificação de linha. A BER é sempre medida sobre os bits da mensagem.
_Evitar_: bit de dados, bit de informação (quando ambíguo)

**Codificação de linha** (*line code*):
Uma regra que transforma bits da mensagem em chips para moldar o sinal (transições, polaridade), não para corrigir erros. Nossas codificações de linha são NRZ, Manchester e Manchester Diferencial.
_Evitar_: codificação de canal, "codificação" sozinha (ambígua com codificação de correção de erros)

**Chip** (*chip*):
Uma saída binária da codificação de linha; a unidade que alimenta o modulador. Com NRZ, um bit da mensagem é um chip; com Manchester e Manchester Diferencial, um bit da mensagem são dois chips.
_Evitar_: bit codificado, sub-bit

**Modulação** (*modulation*):
O mapeamento de grupos de chips em símbolos complexos (BPSK, QPSK, 16-QAM).
_Evitar_: codificação de linha

**Símbolo** (*symbol*):
Um ponto da constelação de uma modulação; carrega 1 (BPSK), 2 (QPSK) ou 4 (16-QAM) chips.

**Eb/N0** (*Eb/N0*):
Energia por bit da mensagem sobre a densidade espectral de potência do ruído, em dB; o único eixo x de toda curva de BER. Quando o enunciado diz "SNR", queremos dizer isto.
_Evitar_: SNR (sem qualificação), Es/N0, SNR por chip

**Violação** (*violation*):
Um par de chips recebido que nenhum bit da mensagem pode produzir em Manchester ou Manchester Diferencial (`00` ou `11`); um erro detectado. Ainda assim ele é decodificado para um bit por uma regra fixa.
_Evitar_: símbolo inválido, erro de decodificação

## Canal

**Cenário de canal** (*channel scenario*):
Um dos dois modelos de ruído pelos quais uma transmissão passa: o canal AWGN ou o canal com rajadas.
_Evitar_: tipo de canal, modo de ruído

**Canal AWGN** (*AWGN channel*):
O cenário de canal de referência: ruído gaussiano independente em cada símbolo, definido por Eb/N0.

**Canal com rajadas** (*burst channel*):
O segundo cenário de canal: o canal AWGN mais um processo de rajadas que, enquanto está no estado ruim, adiciona ruído muito mais forte.
_Evitar_: canal com desvanecimento, canal degradado

**Estado ruim** (*bad state*):
A condição do canal com rajadas em que ruído extra, em um nível fixo independente de Eb/N0, é somado ao ruído de fundo. O oposto é o estado bom (*good state*: só ruído de fundo).
_Evitar_: estado de erro, modo ruidoso

**Rajada** (*burst*):
Uma sequência contígua de símbolos durante a qual o canal com rajadas está no estado ruim.

## Fonte

**Texto-fonte** (*source text*):
O único texto longo em português, de domínio público, transliterado para ASCII de 7 bits, que toda transmissão envia; a origem de todos os bits da mensagem (8 por caractere).
_Evitar_: payload, dados de entrada, bits aleatórios

## Modulação

**Constelação** (*constellation*):
O conjunto de pontos complexos que uma modulação pode enviar, rotulados em código Gray e escalados para energia média unitária.
_Evitar_: mapa de símbolos, alfabeto

## Métricas

**BER** (*BER*):
Fração dos bits da mensagem recuperados errados, após a decodificação de linha.
_Evitar_: taxa de erro de chip, taxa de erro de símbolo (são grandezas diferentes)

**Eficiência espectral** (*spectral efficiency*):
Os bits da mensagem por segundo por hertz nominais que uma combinação codificação de linha × modulação entrega, assumindo pulsos de Nyquist ideais.
_Evitar_: vazão (throughput), eficiência de banda, taxa de dados
