#!/usr/bin/env python3
"""
Automated Stock Firefox UI & Branding Restorer for Camoufox.

Restaura 100% o layout, interface visual, temas e ÍCONES originais do Mozilla Firefox:
  1. Reseta settings/chrome.css para não sobrescrever nenhum elemento visual.
  2. Desativa userChrome e theming Lepton/Proton no settings/camoufox.cfg.
  3. Remove o tema escuro customizado (background.gif e cores pretas forçadas).
  4. Substitui todos os ícones da pasta de branding (default*.png, logo.png, firefox.ico)
     pelos ícones autênticos e oficiais do Mozilla Firefox em alta resolução.
  5. Atualiza brand.properties e brand.dtd para exibir "Firefox" e "Mozilla Firefox".
  6. Sincroniza qualquer diretório de build prévio existente.

TUDO ISSO SEM TOCAR EM NENHUM PATCH DE C++, FINGERPRINTING, WEBG/CANVAS/AUDIO OU JUGGLER.
"""

import os
import re
import shutil
import sys
from pathlib import Path
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent

# Caminho para o ícone oficial do Firefox em alta resolução no sistema
SYSTEM_FIREFOX_ICONS = [
    Path("/usr/share/icons/Mint-Y/apps/256@2x/firefox.png"),  # 512x512
    Path("/usr/share/icons/Mint-Y/apps/256/firefox.png"),     # 256x256
    Path("/usr/share/icons/hicolor/128x128/apps/firefox.png"),
]

def find_system_firefox_icon():
    for p in SYSTEM_FIREFOX_ICONS:
        if p.exists():
            return p
    return None

def restore_stock_ui():
    print("=" * 70)
    print("🦊 Camoufox: Restaurando Interface e Ícones 100% Originais do Firefox")
    print("=" * 70)

    # -------------------------------------------------------------
    # 1. Resetar settings/chrome.css
    # -------------------------------------------------------------
    chrome_css_path = REPO_ROOT / "settings" / "chrome.css"
    if chrome_css_path.exists():
        chrome_css_content = (
            "/* Interface Nativa Stock Firefox */\n"
            "/* Sem regras personalizadas de CSS para preservar abas e janelas originais */\n"
        )
        chrome_css_path.write_text(chrome_css_content, encoding="utf-8")
        print("✅ [1/6] settings/chrome.css resetado para padrão limpo.")

    # -------------------------------------------------------------
    # 2. Desativar userChrome e Theming no settings/camoufox.cfg
    # -------------------------------------------------------------
    cfg_path = REPO_ROOT / "settings" / "camoufox.cfg"
    if cfg_path.exists():
        content = cfg_path.read_text(encoding="utf-8")

        # Desativa toolkit.legacyUserProfileCustomizations.stylesheets
        content = re.sub(
            r'defaultPref\("toolkit\.legacyUserProfileCustomizations\.stylesheets",\s*true\);',
            'defaultPref("toolkit.legacyUserProfileCustomizations.stylesheets", false);',
            content,
        )

        # Comenta todas as preferências de customização de interface userChrome.*
        content = re.sub(
            r'(?m)^(\s*defaultPref\("userChrome\..*?\);)',
            r'// [STOCK-FIREFOX] \1',
            content,
        )

        cfg_path.write_text(content, encoding="utf-8")
        print("✅ [2/6] settings/camoufox.cfg: userChrome e temas Lepton/Proton desativados.")

    # -------------------------------------------------------------
    # 3. Remover o tema escuro customizado (background.gif e preto forçado)
    # -------------------------------------------------------------
    dark_theme_dir = REPO_ROOT / "additions" / "browser" / "themes" / "addons" / "dark"
    if dark_theme_dir.exists():
        shutil.rmtree(dark_theme_dir)
        print("✅ [3/6] additions/browser/themes/addons/dark removido (restaura temas nativos).")
    else:
        print("ℹ️  [3/6] additions/browser/themes/addons/dark já estava limpo.")

    # -------------------------------------------------------------
    # 4. Substituir Ícones de Branding pelos Ícones Oficiais do Firefox
    # -------------------------------------------------------------
    branding_dir = REPO_ROOT / "additions" / "browser" / "branding" / "camoufox"
    source_icon = find_system_firefox_icon()

    if source_icon and branding_dir.exists():
        try:
            with Image.open(source_icon) as base_img:
                base_img = base_img.convert("RGBA")

                # Gera os tamanhos padrão PNG para Linux, janelas e abas
                sizes = [16, 22, 24, 32, 48, 64, 128, 256]
                for s in sizes:
                    resized = base_img.resize((s, s), Image.Resampling.LANCZOS)
                    target_file = branding_dir / f"default{s}.png"
                    resized.save(target_file, "PNG")

                # Gera logo.png
                base_img.resize((128, 128), Image.Resampling.LANCZOS).save(branding_dir / "logo.png", "PNG")

                # Gera o firefox.ico multi-resolução para Windows
                ico_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
                ico_path = branding_dir / "firefox.ico"
                ico_path64 = branding_dir / "firefox64.ico"
                base_img.save(ico_path, format="ICO", sizes=ico_sizes)
                base_img.save(ico_path64, format="ICO", sizes=ico_sizes)

                print("✅ [4/6] Ícones oficiais do Firefox gerados e aplicados (default*.png, logo.png, firefox.ico).")
        except Exception as e:
            print(f"⚠️  [4/6] Falha ao gerar ícones com Pillow: {e}")
    else:
        print("ℹ️  [4/6] Ícone base não encontrado no sistema ou pasta de branding ausente.")

    # -------------------------------------------------------------
    # 5. Atualizar Textos de Marca (brand.properties e brand.dtd)
    # -------------------------------------------------------------
    brand_prop = branding_dir / "locales" / "en-US" / "brand.properties"
    if brand_prop.exists():
        prop_content = (
            "# Mozilla Public License, v. 2.0.\n"
            "brandShorterName=Firefox\n"
            "brandShortName=Firefox\n"
            "brandFullName=Mozilla Firefox\n"
            "brandProductName=Firefox\n"
            "vendorShortName=Mozilla\n"
            "syncBrandShortName=Firefox Sync\n"
        )
        brand_prop.write_text(prop_content, encoding="utf-8")

    brand_dtd = branding_dir / "locales" / "en-US" / "brand.dtd"
    if brand_dtd.exists():
        dtd_content = (
            "<!-- Mozilla Public License, v. 2.0. -->\n"
            '<!ENTITY  brandShorterName      "Firefox">\n'
            '<!ENTITY  brandShortName        "Firefox">\n'
            '<!ENTITY  brandFullName         "Mozilla Firefox">\n'
            '<!ENTITY  brandProductName      "Firefox">\n'
            '<!ENTITY  vendorShortName       "Mozilla">\n'
            '<!ENTITY  trademarkInfo.part1   " ">\n'
        )
        brand_dtd.write_text(dtd_content, encoding="utf-8")
    print("✅ [5/6] Textos de identificação atualizados para 'Firefox' e 'Mozilla Firefox'.")

    # -------------------------------------------------------------
    # 6. Sincronizar Diretórios de Build Prévios
    # -------------------------------------------------------------
    updated_build_dirs = 0
    for src_dir in REPO_ROOT.glob("camoufox-*"):
        if src_dir.is_dir():
            lw_cfg = src_dir / "lw" / "camoufox.cfg"
            if lw_cfg.exists() and cfg_path.exists():
                shutil.copy2(cfg_path, lw_cfg)

            lw_css = src_dir / "lw" / "chrome.css"
            if lw_css.exists() and chrome_css_path.exists():
                shutil.copy2(chrome_css_path, lw_css)

            copied_dark = src_dir / "browser" / "themes" / "addons" / "dark"
            if copied_dark.exists():
                shutil.rmtree(copied_dark)

            # Sincroniza ícones se o branding já tiver sido copiado
            copied_branding = src_dir / "browser" / "branding" / "camoufox"
            if copied_branding.exists() and branding_dir.exists():
                for icon_file in branding_dir.glob("default*.png"):
                    shutil.copy2(icon_file, copied_branding / icon_file.name)
                for ico in ["firefox.ico", "firefox64.ico", "logo.png"]:
                    if (branding_dir / ico).exists():
                        shutil.copy2(branding_dir / ico, copied_branding / ico)

            print(f"✅ [6/6] Diretório de compilação sincronizado: {src_dir.name}")
            updated_build_dirs += 1

    if updated_build_dirs == 0:
        print("ℹ️  [6/6] Nenhum diretório de build prévio para sincronizar (pronto para 'make dir' / 'make build').")

    print("\n" + "=" * 70)
    print("🎉 TUDO PRONTO! O navegador agora tem 100% a aparência e os ícones do Firefox.")
    print("🔒 Todos os patches anti-detect, C++, spoofing de GPU/Canvas/Áudio e Juggler intactos.")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    restore_stock_ui()
