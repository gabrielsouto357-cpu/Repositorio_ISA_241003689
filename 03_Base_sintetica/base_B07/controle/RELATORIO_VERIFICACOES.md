# Relatório de verificações da base sintética (Bloco 07)

Gerado por `codigo/verificar.py` (não lê o gabarito lacrado). Base **SINTÉTICA** didática [SD]; não são dados internos da ISA Energia Brasil.

**Critério de classificação:**
- **G – integridade de geração:** tem de passar nos dois cenários. Uma ocorrência é **falha de geração** e bloqueia a entrega.
- **N – regras de negócio e econômicas:** têm de passar na referência (ocorrência = falha de geração). No cenário de TESTE, ocorrências são **exceções a investigar**: o cenário contém erros inseridos de propósito, mas o relatório não diz quais. Também não se presume que toda exceção seja erro, porque há situações incomuns legítimas.
- **I – informativo:** só contagem. Não é critério de aprovação.

**Resultado:** 0 falha(s) de geração. Entrega liberada.

## Cenário REFERENCIA

Linhas lidas: 2025 = 600.650; 2026 (jan–fev) = 26.144; saldos = 110. Σ 2025 = R$ 36.431.298.000,00.

| Código | Verificação | Ocorrências | Status |
|---|---|---|---|
| G01 | Esquema: 31 colunas na ordem do dicionário (2025 e 2026) | 0 | OK |
| G02 | Contagem 2025 ≥ 500.000 linhas de dados (lidas: 600.650) | 0 | OK |
| G03 | Chave primária id_lancamento única e não vazia (2025 + 2026) | 0 | OK |
| G04 | Formato do id_lancamento (L25/L26 + 8 dígitos) | 0 | OK |
| G05 | natureza_dado = SINTETICO_DIDATICO em todas as linhas | 0 | OK |
| G06 | valor_movimento_brl numérico com exatamente 2 casas (sem notação científica) | 0 | OK |
| G07 | Campos obrigatórios gerais preenchidos (12 campos) | 0 | OK |
| G08 | data_lancamento válida e dentro de 2025 (arquivo 2025) | 0 | OK |
| G09 | data_lancamento do arquivo 2026 entre 01/01 e 28/02/2026 | 0 | OK |
| G10 | Domínios: componente. grupo. origem | 0 | OK |
| G11 | Domínio tipo_movimento (13 tipos do dicionário) | 0 | OK |
| G12 | FK contrato ∈ 28 contratos reais (F0003 p.36) | 0 | OK |
| G13 | Tabela de saldos: circulante + não circulante = saldo (por linha) | 0 | OK |
| G14 | Tabela de saldos: chave (data_base. contrato. componente) única | 0 | OK |
| N01 | Entidade e grupo coerentes com o contrato (F0003 p.36) | 0 | OK |
| N02 | Chave natural (id_documento. seq_linha_documento) única | 0 | OK |
| N03 | Linhas idênticas (todas as colunas exceto id_lancamento) | 0 | OK |
| N04 | Duplicidade indevida em RECEITA_INFRA: mesmos contrato. fornecedor. módulo. tipo de custo. valor e custo. com mesmo documento ou lançados com até 10 dias de distância | 0 | OK |
| I02 | Duplicidade aparente justificada: mesmo contrato. fornecedor e valor. mas documentos distintos e sem o padrão do N04 (coincidência de valores em itens pequenos de fornecedor frequente) | 74 | INFORMATIVO (justificada) |
| N05 | Lançamento sem documento-suporte (id_documento ou data_documento vazio) | 0 | OK |
| N06 | Sinal coerente com o tipo (receitas > 0; recebimentos. estornos e perdas < 0) | 0 | OK |
| N07 | RECEITA_INFRA com módulo ANEEL válido (FK ao catálogo real F0242) | 0 | OK |
| N08 | Módulo ANEEL pertence ao contrato do lançamento | 0 | OK |
| N09 | RECEITA_INFRA com fornecedor cadastrado e tipo de custo do domínio de obra | 0 | OK |
| N10 | Recálculo: valor = custo do documento × (1 + margem). tolerância de arredondamento ≤ R$ 0.02 | 0 | OK |
| N11 | Faturas e recebimentos com usuário pagador cadastrado | 0 | OK |
| N12 | Corte: documento de 2024 lançado como movimento de 2025 | 0 | OK |
| N13 | Data do documento posterior ao lançamento (exceto remuneração. calculada no fim do mês e lançada no último dia útil) | 0 | OK |
| N14 | Competência = mês do lançamento (recebimentos usam o mês da fatura; aberturas 2024-12) | 0 | OK |
| N15 | Lançamento manual fora do horário 07h–20h ou sem hora | 0 | OK |
| N16 | Segregação: lançamento manual aprovado pelo próprio usuário | 0 | OK |
| I01 | Informativo: lançamentos manuais (exceto reclassificações) com valor redondo ≥ R$ 1 milhão (há marcos contratuais legítimos) | 12 | INFORMATIVO |
| N17 | Reclassificações: cada documento soma zero | 0 | OK |
| N18 | Taxa implícita da remuneração dentro da faixa divulgada 4.2%–9.9% a.a. (F0003 p.44) | 0 | OK |
| N19 | Recebimentos: linha 1 de cada documento quita O&M e todo documento tem linha 1 | 0 | OK |
| N25 | Recebimentos: todas as linhas de um documento no mesmo contrato | 0 | OK |
| N20 | Saldo 31/12/2025 (tabela) = abertura + Σ fluxos. por contrato e componente; abertura = saldo 31/12/2024 | 0 | OK |
| N21 | Parcelas circulante e não circulante não negativas | 0 | OK |
| N22 | O&M (prazo < 30 dias) integralmente circulante | 0 | OK |
| N23 | Σ base 2025 = saldo publicado 36.431.298 mil (diferença em R$ mil: 0.000) | 0 | OK |
| N24 | Σ circulante 31/12/2025 = 4.106.084 mil (diferença em R$ mil: 0.000) | 0 | OK |

## Cenário TESTE

Linhas lidas: 2025 = 600.474; 2026 (jan–fev) = 26.417; saldos = 110. Σ 2025 = R$ 36.463.023.784,44.

| Código | Verificação | Ocorrências | Status |
|---|---|---|---|
| G01 | Esquema: 31 colunas na ordem do dicionário (2025 e 2026) | 0 | OK |
| G02 | Contagem 2025 ≥ 500.000 linhas de dados (lidas: 600.474) | 0 | OK |
| G03 | Chave primária id_lancamento única e não vazia (2025 + 2026) | 0 | OK |
| G04 | Formato do id_lancamento (L25/L26 + 8 dígitos) | 0 | OK |
| G05 | natureza_dado = SINTETICO_DIDATICO em todas as linhas | 0 | OK |
| G06 | valor_movimento_brl numérico com exatamente 2 casas (sem notação científica) | 0 | OK |
| G07 | Campos obrigatórios gerais preenchidos (12 campos) | 0 | OK |
| G08 | data_lancamento válida e dentro de 2025 (arquivo 2025) | 0 | OK |
| G09 | data_lancamento do arquivo 2026 entre 01/01 e 28/02/2026 | 0 | OK |
| G10 | Domínios: componente. grupo. origem | 0 | OK |
| G11 | Domínio tipo_movimento (13 tipos do dicionário) | 0 | OK |
| G12 | FK contrato ∈ 28 contratos reais (F0003 p.36) | 0 | OK |
| G13 | Tabela de saldos: circulante + não circulante = saldo (por linha) | 0 | OK |
| G14 | Tabela de saldos: chave (data_base. contrato. componente) única | 0 | OK |
| N01 | Entidade e grupo coerentes com o contrato (F0003 p.36) | 0 | OK |
| N02 | Chave natural (id_documento. seq_linha_documento) única | 70 | EXCEÇÃO A INVESTIGAR |
| N03 | Linhas idênticas (todas as colunas exceto id_lancamento) | 0 | OK |
| N04 | Duplicidade indevida em RECEITA_INFRA: mesmos contrato. fornecedor. módulo. tipo de custo. valor e custo. com mesmo documento ou lançados com até 10 dias de distância | 70 | EXCEÇÃO A INVESTIGAR |
| I02 | Duplicidade aparente justificada: mesmo contrato. fornecedor e valor. mas documentos distintos e sem o padrão do N04 (coincidência de valores em itens pequenos de fornecedor frequente) | 72 | INFORMATIVO (justificada) |
| N05 | Lançamento sem documento-suporte (id_documento ou data_documento vazio) | 2 | EXCEÇÃO A INVESTIGAR |
| N06 | Sinal coerente com o tipo (receitas > 0; recebimentos. estornos e perdas < 0) | 0 | OK |
| N07 | RECEITA_INFRA com módulo ANEEL válido (FK ao catálogo real F0242) | 60 | EXCEÇÃO A INVESTIGAR |
| N08 | Módulo ANEEL pertence ao contrato do lançamento | 0 | OK |
| N09 | RECEITA_INFRA com fornecedor cadastrado e tipo de custo do domínio de obra | 60 | EXCEÇÃO A INVESTIGAR |
| N10 | Recálculo: valor = custo do documento × (1 + margem). tolerância de arredondamento ≤ R$ 0.02 | 20 | EXCEÇÃO A INVESTIGAR |
| N11 | Faturas e recebimentos com usuário pagador cadastrado | 0 | OK |
| N12 | Corte: documento de 2024 lançado como movimento de 2025 | 150 | EXCEÇÃO A INVESTIGAR |
| N13 | Data do documento posterior ao lançamento (exceto remuneração. calculada no fim do mês e lançada no último dia útil) | 0 | OK |
| N14 | Competência = mês do lançamento (recebimentos usam o mês da fatura; aberturas 2024-12) | 0 | OK |
| N15 | Lançamento manual fora do horário 07h–20h ou sem hora | 2 | EXCEÇÃO A INVESTIGAR |
| N16 | Segregação: lançamento manual aprovado pelo próprio usuário | 2 | EXCEÇÃO A INVESTIGAR |
| I01 | Informativo: lançamentos manuais (exceto reclassificações) com valor redondo ≥ R$ 1 milhão (há marcos contratuais legítimos) | 14 | INFORMATIVO |
| N17 | Reclassificações: cada documento soma zero | 0 | OK |
| N18 | Taxa implícita da remuneração dentro da faixa divulgada 4.2%–9.9% a.a. (F0003 p.44) | 0 | OK |
| N19 | Recebimentos: linha 1 de cada documento quita O&M e todo documento tem linha 1 | 0 | OK |
| N25 | Recebimentos: todas as linhas de um documento no mesmo contrato | 8 | EXCEÇÃO A INVESTIGAR |
| N20 | Saldo 31/12/2025 (tabela) = abertura + Σ fluxos. por contrato e componente; abertura = saldo 31/12/2024 | 0 | OK |
| N21 | Parcelas circulante e não circulante não negativas | 0 | OK |
| N22 | O&M (prazo < 30 dias) integralmente circulante | 0 | OK |
| N23 | Σ base 2025 = saldo publicado 36.431.298 mil (diferença em R$ mil: 31.725.784) | 1 | EXCEÇÃO A INVESTIGAR |
| N24 | Σ circulante 31/12/2025 = 4.106.084 mil (diferença em R$ mil: 61.200.000) | 1 | EXCEÇÃO A INVESTIGAR |

IDs de exemplo de cada ocorrência: `controle/VERIFICACOES_RESULTADO.csv` (coluna exemplo_ids).