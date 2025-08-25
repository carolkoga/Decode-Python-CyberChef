# Decodificação e triagem com CyberChef

## Decodificação e Triagem com CyberChef (Base64 + XOR simples)

Projeto educativo que mostra, na prática, como decodificar um payload ofuscado com Base64 + XOR simples usando o CyberChef, calcular hashes, identificar IoCs (Indicators of Compromise) e documentar todo o fluxo de análise.

> Aviso: uso estritamente didático. Não execute técnicas de análise em dados/sistemas sem autorização.

---

## O que você vai conseguir com este projeto

- Entender e reproduzir uma cadeia de ofuscação comum: Base64 seguido de XOR de 1 byte.
- Gerar uma amostra de payload ofuscado e seu correspondente “limpo” para testes.
- Decodificar no CyberChef (ou via Python) e validar o resultado.
- Calcular hashes (MD5/SHA‑1/SHA‑256) para integridade e referência.
- Extrair IoCs básicos (URLs, domínios, IPs, e-mails) do conteúdo decodificado.
- Documentar a análise: recipe exportado, arquivos de saída e conclusões.

---

## Requisitos rápidos

- Python 3.11+ (funciona em 3.8+, mas recomendado recente)
- Acesso ao CyberChef no navegador: https://gchq.github.io/CyberChef/ {target="_blank"}
- PowerShell (Windows) ou terminal bash (Linux/macOS) para comandos de hash

---

## Passo a passo (rápido)

1) Clonar e entrar no projeto
- Baixe/clone o repositório e acesse a pasta do projeto no terminal.

2) Gerar os arquivos de teste
- Execute o script que gera a amostra ofuscada e a “limpa”:
  - Windows (PowerShell):
    ```
    python .\generate_payload.py
    ```
  - Linux/macOS:
    ```
    python3 ./generate_payload.py
    ```
- Saída esperada:
  - Pasta payload/ criada automaticamente
  - Arquivos:
    - payload/payload_plain.txt
    - payload/payload_obfuscated.txt
  - Console exibindo a chave XOR (ex.: “Chave XOR (hex): 0x37”)

3) Decodificar no CyberChef
- Abra o CyberChef no navegador.
- Cole o conteúdo de payload_obfuscated.txt no pane de entrada.
- Adicione os “ops” (lado esquerdo):
  - From Base64
  - XOR
    - Key: use a chave impressa pelo script (ex.: 0x37). Marque como “Single byte key”.
- Verifique o texto decodificado no pane de saída (deverá bater com payload_plain.txt).
- Exporte o recipe: Save recipe → salve como recipe_cyberchef.txt.

4) Salvar saídas e calcular hashes
- Salve o conteúdo decodificado como payload_decoded.txt (opcional, se quiser guardar a saída do CyberChef).
- Calcule hashes:
  - Windows (PowerShell):
    ```
    Get-FileHash .\payload\payload_obfuscated.txt -Algorithm SHA256
    Get-FileHash .\payload\payload_plain.txt -Algorithm SHA256
    ```
  - Linux/macOS:
    ```
    sha256sum ./payload/payload_obfuscated.txt
    sha256sum ./payload/payload_plain.txt
    ```

5) Triagem de IoCs (básico)
- Procure por:
  - URLs/domínios (http[s]://, .com, .net, etc.)
  - IPs (padrão IPv4)
  - E-mails
- Registre os achados em iocs.txt.

---

## Como funciona (resumo técnico)

- O script generate_payload.py cria um conteúdo de exemplo “limpo” (payload_plain.txt).
- Em seguida aplica XOR de 1 byte e depois Base64, gerando payload_obfuscated.txt.
- No CyberChef, a ordem inversa recupera o original:
  - From Base64 → XOR (mesma chave do script).
- Você valida a integridade comparando o decodificado com o original e calcula hashes para referência.
- A partir do texto decodificado, você extrai IoCs simples para triagem.

---

## Saídas esperadas

- recipe_cyberchef.txt — receita exportada do CyberChef.
- Hashes (MD5/SHA‑1/SHA‑256) do conteúdo ofuscado e do conteúdo limpo.
- iocs.txt — lista opcional de IoCs extraídos.
- screenshots — opcional, mostrando:
  - Pane de entrada/saída no CyberChef
  - Config do operador XOR (chave)
  - Export da recipe

---

## Notas e solução de problemas

- Erro de caminho/pastas: certifique-se de que a pasta payload/ exista. O script fornecido já cria, mas se adaptou o código, não esqueça de criar:
  ```
  mkdir payload
  ```
- Chave XOR: use exatamente a chave impressa no console pelo script (ex.: 0x37). No CyberChef, defina como “Single byte key”.
- Encoding: se o decodificado aparecer com caracteres estranhos, é provável que seja texto binário; valide com hashes.

---

## Licença e ética

- Projeto para fins educacionais e de portfólio.
- Não utilizar para analisar, armazenar ou disseminar conteúdo malicioso real sem autorização e sem ambiente controlado.