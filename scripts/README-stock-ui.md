# 🦊 Camoufox Stock UI & Branding Restorer

Script de automação para transformar o **Camoufox** na aparência, layout e ícones **100% nativos do Mozilla Firefox**, preservando **100% de todos os patches C++, spoofing de fingerprint e tecnologia anti-detecção**.

---

## 🎯 Objetivo

O Camoufox por padrão aplica customizações visuais invasivas:
- Barra de abas e botões alterados pelo tema Lepton/Proton (`userChrome.*`).
- Tema preto forçado com GIF animado de 2.7MB (`background.gif`) e botões roxos.
- Ícone e marca da máscara de raposa ("Camoufox").
- Regras CSS que desconfiguram o botão de fechar aba e nova aba.

O script `apply-stock-ui.py` automatiza a remoção de todas essas customizações visuais para que o navegador final tenha:
- **Design e layout 100% idênticos ao Firefox autêntico** (botão `x` de fechar abas, botão `+` de nova aba, espaçamentos e altura de barra nativos).
- **Temas nativos do Firefox** (Claro, Escuro e do Sistema).
- **Ícones oficiais da Mozilla** (raposa oficial com globo azul em alta resolução para Windows, Linux e macOS).
- **Nomes oficiais** ("Firefox" e "Mozilla Firefox" nas janelas e menus).

---

## 🚀 Como Executar

Dentro da pasta `camoufox`:

```bash
# Opção 1: Via Makefile
make stock-ui

# Opção 2: Diretamente via Python
python3 scripts/apply-stock-ui.py
```

> **Dica:** Sempre que você atualizar o Camoufox (`git pull`), basta rodar `make stock-ui` antes de compilar para reaplicar o visual padrão do Firefox!

---

## 📋 Arquivos e Modificações Realizadas

O script opera de forma cirúrgica exclusivamente nos arquivos de interface:

| Arquivo / Diretório | Ação Realizada | Motivo |
| :--- | :--- | :--- |
| `settings/chrome.css` | Resetado para arquivo limpo | Remove CSS customizado que deformava abas e ocultava botões nativos. |
| `settings/camoufox.cfg` | Desativa `toolkit.legacyUserProfileCustomizations.stylesheets` e comenta regras `userChrome.*` | Desliga o motor Lepton/Proton para restaurar o comportamento e geometria padrão do Firefox. |
| `additions/browser/themes/addons/dark/` | Pasta removida | Elimina o tema preto modificado e o `background.gif`, restaurando o tema escuro/claro oficial da Mozilla. |
| `additions/browser/branding/camoufox/default*.png` | Gerados a partir do ícone oficial 512px do Firefox | Gera ícones nítidos de 16, 22, 24, 32, 48, 64, 128 e 256px. |
| `additions/browser/branding/camoufox/firefox.ico` | Gerado com multi-resolução (16x16 até 256x256) | Ícone oficial do executável e barra de tarefas no Windows. |
| `additions/browser/branding/camoufox/locales/en-US/` | `brand.properties` e `brand.dtd` atualizados | Altera o nome de exibição de "Camoufox" para "Firefox" e "Mozilla Firefox". |
| `camoufox-*/` (pastas de build) | Sincronização automática | Caso já exista uma pasta de compilação em andamento, o script atualiza os arquivos diretamente nela. |

---

## 🔒 O Que Permanece 100% Intacto (Anti-Detect & Stealth)

**Nenhum código de anti-detecção foi alterado.** Todos os seguintes componentes continuam exatamente como no Camoufox original:

- **Patches C++** em `patches/`:
  - `webgl-spoofing.patch` (mascaramento de GPU, vendor e renderer).
  - `anti-font-fingerprinting.patch` e `font-hijacker.patch` (proteção de fontes).
  - `audio-fingerprint-manager.patch` (ruído no AudioContext).
  - `webrtc-ip-spoofing.patch` (proteção de vazamento de IP WebRTC).
  - `timezone-spoofing.patch` e `locale-spoofing.patch`.
  - `screen-spoofing.patch` e `navigator-spoofing.patch`.
- **Motor Juggler (Playwright / CDP)**:
  - Movimentos humanos do mouse gravados (`Cursory`).
  - Eventos de ponteiro autênticos (`MOZ_SOURCE_MOUSE`).
  - Proteção de `evaluate()` sem concessão prematura de `userActivation`.
- **Injeção de Impressões Digitais**:
  - Leitura e aplicação de configurações via variável de ambiente `CAMOU_CONFIG`.
