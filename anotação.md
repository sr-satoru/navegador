# 🦊 Guia Técnico do Camoufox: Parâmetros e Recursos Reais

> **Finalidade:** Documento de referência técnica para o desenvolvimento da interface (Frontend/Dashboard) do seu próprio navegador anti-detect.
> Aqui estão listadas todas as propriedades que o **Camoufox** realmente suporta no nível de código C++ e na API Python/Playwright.

---

## 📌 1. Identificação Geral do Sistema e Navegador

| Parâmetro no Frontend | Chave de Configuração Camoufox | Valores Válidos / Exemplos | Descrição Técnica |
| :--- | :--- | :--- | :--- |
| **Sistema Operacional (OS)** | `os` | `"windows"`, `"macos"`, `"linux"` | Define o universo de fontes, WebGL e comportamento do sistema. |
| **User-Agent** | `navigator.userAgent` | Ex: `Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0` | String enviada nos cabeçalhos HTTP e reportada pelo navegador. |
| **Plataforma** | `navigator.platform` | `"Win32"`, `"MacIntel"`, `"Linux x86_64"` | Deve bater com o sistema operacional escolhido. |
| **CPU do Sistema** | `navigator.oscpu` | Ex: `"Windows NT 10.0; Win64; x64"`, `"Intel Mac OS X 10.15"` | String interna do Gecko para identificação da CPU. |
| **Versão da Aplicação** | `navigator.appVersion` | Gerado automaticamente compatível com o User-Agent | Mantém consistência interna. |
| **Do Not Track** | `navigator.doNotTrack` | `null`, `"1"`, `"0"` | Preferência de rastreamento do usuário. |
| **Global Privacy Control** | `navigator.globalPrivacyControl` | `true`, `false` | Header e API de privacidade GPC. |

---

## 💻 2. Hardware e Processamento

| Parâmetro no Frontend | Chave de Configuração Camoufox | Valores Válidos / Exemplos | Descrição Técnica |
| :--- | :--- | :--- | :--- |
| **Núcleos de CPU** | `navigator.hardwareConcurrency` | `2`, `4`, `8`, `12`, `16`, `32` | Quantidade de threads/núcleos lógicos reportados para o JavaScript. |
| **Pontos de Toque (Touch)** | `navigator.maxTouchPoints` | `0` (Desktop normal), `5` ou `10` (Touchscreen/Notebook touch) | Emula suporte a tela sensível ao toque. |
| **Tipo de Ponteiro** | `force-default-pointer` | `mouse`, `touch` | Garante que os eventos de mouse/toque fiquem consistentes. |

---

## 🖥️ 3. Tela, Janela e Resolução (Screen & Window)

| Parâmetro no Frontend | Chave de Configuração Camoufox | Valores Válidos / Exemplos | Descrição Técnica |
| :--- | :--- | :--- | :--- |
| **Resolução da Tela (Largura x Altura)** | `screen.width`, `screen.height` | `1920x1080`, `2560x1440`, `1366x768`, `1440x900` | Dimensão física total do monitor. |
| **Área Disponível (sem barra de tarefas)** | `screen.availWidth`, `screen.availHeight` | Ex: `1920` x `1040` (descontando os 40px da barra de tarefas do Windows) | Onde muitos anti-detects amadores erram; o Camoufox calcula o desconto da barra. |
| **Tamanho da Janela Externa** | `window.outerWidth`, `window.outerHeight` | Ex: `1920x1040` (maximizada) ou menor se estiver em janela | Tamanho da moldura do navegador. |
| **Tamanho da Janela Interna (Viewport)** | `window.innerWidth`, `window.innerHeight` | Tamanho útil da página web renderizada | O que o site realmente visualiza e ajusta via CSS. |
| **Posição da Janela** | `window.screenX`, `window.screenY` | `0, 0` (maximizada) ou coordenadas randômicas | Posição onde a janela abre na tela. |
| **Profundidade de Cores** | `screen.colorDepth`, `screen.pixelDepth` | `24` (Padrão mundial), `30` (Monitores HDR) | Profundidade de bits por pixel. |

---

## 🎨 4. Gráficos, WebGL e Canvas (GPU)

| Parâmetro no Frontend | Chave de Configuração Camoufox | Valores Válidos / Exemplos | Descrição Técnica |
| :--- | :--- | :--- | :--- |
| **Fabricante WebGL (Vendor)** | `webgl:vendor` | Ex: `Google Inc. (NVIDIA)`, `Google Inc. (Intel)`, `Apple` | Forja a fabricante da placa de vídeo. |
| **Renderizador WebGL (Renderer)** | `webgl:renderer` | Ex: `ANGLE (NVIDIA GeForce RTX 4060 Direct3D11...)`, `Apple M2` | Forja o modelo exato da placa de vídeo. |
| **Banco de Metadados WebGL** | `webgl_data.db` (Nativo) | Pareamentos reais por OS extraídos de máquinas autênticas | Injeta shaders, limites de textura e extensões que batem com a GPU real. |
| **Ruído no Canvas** | Motor Skia modificado (C++) | Determinístico por perfil | Altera levemente a rasterização de pixels para que o hash de Canvas seja único e persistente sem quebrar imagens. |

---

## 🔊 5. Áudio (AudioContext)

| Parâmetro no Frontend | Chave de Configuração Camoufox | Valores Válidos / Exemplos | Descrição Técnica |
| :--- | :--- | :--- | :--- |
| **Frequência de Amostragem (Sample Rate)** | `audioContext.sampleRate` | `44100` Hz ou `48000` Hz | Frequência de saída do hardware de áudio. |
| **Canais de Áudio** | `audioContext.maxChannelCount`| `2` (Estéreo) | Número de canais de áudio suportados. |
| **Latência de Áudio** | `audioContext.outputLatency` | Valor decimal de latência em segundos | Latência de buffer da placa de som. |
| **Ruído de Fingerprint de Áudio** | `audio-fingerprint-manager.patch` | Ruído determinístico | Altera o resultado do cálculo do DynamicsCompressor. |

---

## 🌐 6. Rede, Proxy e WebRTC

| Parâmetro no Frontend | Configuração no Camoufox | Descrição Técnica |
| :--- | :--- | :--- |
| **Protocolos de Proxy Suportados** | `HTTP`, `HTTPS`, `SOCKS5` | Suporta proxies com ou sem autenticação de usuário e senha. |
| **Proteção de DNS (DNS Leak)** | `network.proxy.socks_remote_dns = true` | Força toda resolução DNS a passar por dentro do proxy SOCKS5, impedindo vazamento do IP real da sua operadora. |
| **WebRTC: Desativar** | `media.peerconnection.enabled = false` | Desliga completamente o WebRTC. |
| **WebRTC: Spoofing de IP (Avançado)** | `webrtc-ip-spoofing.patch` | O Camoufox reescreve os pacotes SDP no nível do protocolo UDP: ele substitui o IP local pelo IP do Proxy e usa nomes mDNS `<uuid>.local` para não vazar o IP real em sites de conferência/WebRTC. |

---

## 📍 7. Fuso Horário, Geolocalização e Idioma

| Parâmetro no Frontend | Opções no Camoufox | Descrição Técnica |
| :--- | :--- | :--- |
| **Fuso Horário (Timezone)** | `timezone`: `"Automatic"` (baseado no IP) ou manual (ex: `"America/Sao_Paulo"`, `"Europe/London"`) | Modifica o relógio interno do navegador, a função `Intl.DateTimeFormat` e o método `Date().getTimezoneOffset()`. |
| **Geolocalização (GPS)** | `geolocation`: `{ latitude: -23.55, longitude: -46.63, accuracy: 15 }` | Injeta coordenadas exatas de GPS quando a página pedir permissão de localização. |
| **Idioma Principal** | `locale`: `"pt-BR"`, `"en-US"`, `"es-ES"` | Modifica `navigator.language` e o cabeçalho HTTP `Accept-Language`. |
| **Lista de Idiomas Suportados** | `languages`: `["pt-BR", "pt", "en-US", "en"]` | Modifica `navigator.languages`. |

---

## 🔤 8. Fontes do Sistema (Anti-Font Fingerprinting)

| Recurso | Como o Camoufox funciona |
| :--- | :--- |
| **Fontes Embutidas por OS** | O Camoufox já vem com os arquivos de fontes oficiais do **Windows, Mac e Linux** embutidos internamente. |
| **Subconjunto Estatístico** | Ele seleciona uma lista de fontes realista (30% a 80% das fontes comuns daquele sistema) para não parecer um navegador genérico. |
| **Micro-ruído de Métrica de Fontes** | Ele adiciona um micro-espaçamento randômico invisível entre as letras, impedindo que testes de Javascript meçam a largura exata de um texto para identificar sua máquina. |

---

## 🔋 9. Outros Sensores e APIs Extras

* **Bateria (Battery API):** Modifica `battery.charging` (carregando ou na bateria) e o nível de carga (`battery.level`).
* **Vozes do Sistema (SpeechSynthesis):** Injeta a lista correta de vozes do sistema operacional selecionado (`speechSynthesis.getVoices()`).
* **Dispositivos de Mídia (MediaDevices):** Permite simular a quantidade de microfones, webcams e caixas de som disponíveis (`navigator.mediaDevices.enumerateDevices()`).
* **Automação Invisível (Anti-Bot):** Remove 100% da propriedade `navigator.webdriver` e isola os scripts de controle para sites como Cloudflare não detectarem Playwright/automação.

---

## 🛠️ Estrutura do JSON do Perfil (Ideal para o seu Frontend salvar)

Quando o usuário clicar em **"Salvar Perfil"** no seu painel, este é o formato de dados completo e perfeito para armazenar:

```json
{
  "id": "perfil-001",
  "name": "Conta Instagram - Operação 01",
  "created_at": "2026-09-18T12:00:00Z",
  "os": "windows",
  "browser": {
    "engine": "camoufox",
    "version": "135.0"
  },
  "proxy": {
    "enabled": true,
    "type": "socks5",
    "host": "189.40.12.34",
    "port": 1080,
    "username": "user",
    "password": "password"
  },
  "fingerprint": {
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
    "screen": {
      "width": 1920,
      "height": 1080,
      "avail_width": 1920,
      "avail_height": 1040,
      "color_depth": 24
    },
    "hardware": {
      "cpu_cores": 16,
      "touch_points": 0
    },
    "gpu": {
      "vendor": "Google Inc. (NVIDIA)",
      "renderer": "ANGLE (NVIDIA GeForce RTX 4060 Direct3D11 vs_5_0 ps_5_0)"
    },
    "audio": {
      "sample_rate": 48000,
      "noise": true
    },
    "locale": {
      "timezone": "America/Sao_Paulo",
      "language": "pt-BR",
      "languages": ["pt-BR", "pt", "en-US"]
    },
    "webrtc": {
      "mode": "spoof_ip"
    },
    "canvas": {
      "noise": true
    },
    "fonts": {
      "use_os_pack": true,
      "mask_metrics": true
    }
  }
}
```
