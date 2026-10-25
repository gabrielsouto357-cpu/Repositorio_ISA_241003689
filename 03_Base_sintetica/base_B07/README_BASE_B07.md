# Base SINTÉTICA de Ativos da concessão – ISA Energia Brasil 2025 (Bloco 07)

> **Aviso.** Esta é uma base **sintética, criada para fins didáticos** [SD]. **Não** são registros internos da ISA Energia Brasil e não foram obtidos da companhia. Os totais por grupo reproduzem as demonstrações publicadas (F0003 p.23, p.45 e p.47); contratos, entidades, RAP e módulos ANEEL são dados públicos reais (F0003 p.36; F0242). Tudo abaixo desse nível é simulado: a divisão por contrato, mês, documento, usuário e fornecedor. Nenhuma conclusão sobre os registros reais da companhia pode ser tirada desta base.

Projeto validado: D-019, D-020 e D-021 (20/10/2026, 22h54). Preparado por: matrícula 241003689 (execução assistida por IA). Revisão humana: ____________ (em branco).

## Pastas
| Pasta | Conteúdo | Natureza |
|---|---|---|
| `dados_reais_derivados/` | Extratos de fontes públicas: 28 contratos (F0003 p.36) e catálogo de 4.471 módulos ANEEL (F0242) | **Real** (público) |
| `dados_sinteticos/` | Lançamentos 2025 e jan–fev/2026 (REFERENCIA e TESTE), saldos, cadastros e parâmetros | **Sintético** |
| `gabarito_LACRADO/` | Registro dos erros inseridos, linhas alteradas, mapa de IDs e ponte de efeito | **Lacrado**: não usar em testes; abrir só no PT 450 |
| `config/` | `config_B07.json`: semente 20251231, premissas e metas (R$ mil) com fonte | — |
| `codigo/` | Scripts e `requirements.txt` | — |
| `controle/` | Conciliação, relatório de verificações, log de execução, hashes e teste de reprodução | — |

## Instrução vigente de reprodução
Use o README.md da raiz de07_Entrega e o programa reproduzir_entrega.py, que executa em cópia nova sem sobrescrever esta base. O ambiente Windows foi novamente testado em 23/10/2026 com Python3.12.14 e as versões fixadas. Compare conteúdo dos dados, valores/fórmulas e resultados; CSV/gzip pode mudar em bytes por terminador de linha/cabeçalho e XLSX por metadados/caches.

## Procedimento histórico de geração do Bloco07
1. Instale Python 3.13 (testado em 3.13.16) e as dependências: `pip install -r codigo/requirements.txt`.
2. Na pasta `base_B07`, rode `python codigo/run_all.py`. Leva cerca de 1,5 minuto, sem acesso à rede e sem senhas. A ordem é: `gerar_referencia.py` → `inserir_erros.py` → `conciliar.py` → `verificar.py` → `gerar_dicionario.py`.
3. Confira os hashes em `controle/HASHES_SHA256.txt`. CSV e CSV.gz são determinísticos no ambiente de origem; entre sistemas, compare os dados e observe a ressalva da instrução vigente acima. Nos arquivos .xlsx, compare os valores das células, porque os metadados guardam a data de gravação.
4. (Opcional) Abra as planilhas no Excel, que recalcula as fórmulas ao abrir. Nesta entrega elas também foram recalculadas no LibreOffice.

## Leitura dos arquivos
- CSV em UTF-8, separador `;`, **ponto decimal**.
- No pandas: `pd.read_csv(arquivo, sep=';', dtype=str, keep_default_na=False)`. Converta o valor para centavos inteiros antes de somar.
- No Excel: Dados → De Texto/CSV → delimitador ponto e vírgula; em configurações regionais, use "." como decimal.
- O campo `base_calculo_brl` é **estoque** informativo e não deve ser somado. Os saldos só se somam dentro da mesma `data_base`.

## Resultado da execução (20/10/2026)
- Referência: 600.650 linhas em 2025 (excluído o cabeçalho), 26.144 em 2026 e 110 saldos.
  - Σ = R$ 36.431.298.000,00 = R$ 36.431.298 mil publicados (diferença 0).
  - C1–C7 conciliados.
  - 0 falhas de geração.
- Teste: 600.474 linhas em 2025 e 26.417 em 2026.
  - A diferença agregada a investigar contra o publicado é de R$ 31.725,8 mil (sem compensação).
  - A causa não está identificada fora do gabarito lacrado.
