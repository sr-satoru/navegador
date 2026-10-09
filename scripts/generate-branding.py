#!/usr/bin/env python3
"""
Gera todos os formatos e tamanhos de ícones do navegador a partir de additions/browser/branding/camoufox/default256.png.

Garante que compilações para Linux, Windows e macOS usem 100% o ícone personalizado
definido em default256.png em vez do ícone padrão do Firefox ou do Camoufox original.
"""

import os
import sys
from pathlib import Path
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent
BRANDING_DIR = REPO_ROOT / "additions" / "browser" / "branding" / "camoufox"
SOURCE_ICON = BRANDING_DIR / "default256.png"

def generate_branding():
    if not SOURCE_ICON.exists():
        print(f"❌ Ícone base não encontrado em {SOURCE_ICON}")
        sys.exit(1)

    print("=" * 70)
    print("🎨 Gerando ativos de branding completos a partir de default256.png...")
    print("=" * 70)

    with Image.open(SOURCE_ICON) as base:
        base = base.convert("RGBA")

        # 1. default*.png (Linux / Janelas / Abas)
        sizes = [16, 22, 24, 32, 48, 64, 128, 256]
        for s in sizes:
            resized = base.resize((s, s), Image.Resampling.LANCZOS)
            target = BRANDING_DIR / f"default{s}.png"
            resized.save(target, "PNG")
        print("✅ default*.png (16px a 256px) gerados.")

        # 2. logo.png (128x128)
        base.resize((128, 128), Image.Resampling.LANCZOS).save(BRANDING_DIR / "logo.png", "PNG")
        print("✅ logo.png (128x128) gerado.")

        # 3. VisualElements & PrivateBrowsing (Windows)
        base.resize((126, 126), Image.Resampling.LANCZOS).save(BRANDING_DIR / "VisualElements_70.png", "PNG")
        base.resize((270, 270), Image.Resampling.LANCZOS).save(BRANDING_DIR / "VisualElements_150.png", "PNG")
        base.resize((126, 126), Image.Resampling.LANCZOS).save(BRANDING_DIR / "PrivateBrowsing_70.png", "PNG")
        base.resize((270, 270), Image.Resampling.LANCZOS).save(BRANDING_DIR / "PrivateBrowsing_150.png", "PNG")
        print("✅ Ativos do menu Iniciar (VisualElements & PrivateBrowsing) gerados.")

        # 4. Ícones ICO Multi-resolução (Windows Executável e Barra de Tarefas)
        ico_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        base.save(BRANDING_DIR / "firefox.ico", format="ICO", sizes=ico_sizes)
        base.save(BRANDING_DIR / "firefox64.ico", format="ICO", sizes=ico_sizes)
        base.save(BRANDING_DIR / "pbmode.ico", format="ICO", sizes=ico_sizes)
        base.save(BRANDING_DIR / "newtab.ico", format="ICO", sizes=[(16, 16), (32, 32)])
        base.save(BRANDING_DIR / "newwindow.ico", format="ICO", sizes=[(16, 16), (32, 32)])
        print("✅ Arquivos .ico multi-resolução gerados.")

        # 5. Ícones ICNS (macOS)
        try:
            base.save(BRANDING_DIR / "firefox.icns", format="ICNS")
            base.save(BRANDING_DIR / "document.icns", format="ICNS")
            base.save(BRANDING_DIR / "disk.icns", format="ICNS")
            print("✅ Arquivos .icns para macOS gerados.")
        except Exception as e:
            print(f"⚠️  Falha ao gerar ICNS: {e}")

        # 6. Content (Modal 'Sobre o Navegador')
        content_dir = BRANDING_DIR / "content"
        if content_dir.exists():
            base.resize((192, 192), Image.Resampling.LANCZOS).save(content_dir / "about-logo.png", "PNG")
            base.resize((384, 384), Image.Resampling.LANCZOS).save(content_dir / "about-logo@2x.png", "PNG")
            base.resize((192, 192), Image.Resampling.LANCZOS).save(content_dir / "about-logo-private.png", "PNG")
            base.resize((384, 384), Image.Resampling.LANCZOS).save(content_dir / "about-logo-private@2x.png", "PNG")

            about_img = Image.new("RGBA", (300, 236), (0, 0, 0, 0))
            icon_about = base.resize((192, 192), Image.Resampling.LANCZOS)
            about_img.paste(icon_about, ((300 - 192) // 2, (236 - 192) // 2))
            about_img.save(content_dir / "about.png", "PNG")
            print("✅ Ativos da janela 'Sobre' gerados.")

        # 7. Assets.xcassets (macOS AppIcon Catalog)
        xcassets_dir = BRANDING_DIR / "Assets.xcassets" / "AppIcon.appiconset"
        if xcassets_dir.exists():
            xc_map = {
                "icon_16x16.png": 16,
                "icon_16x16@2x.png": 32,
                "icon_32x32.png": 32,
                "icon_32x32@2x.png": 64,
                "icon_128x128.png": 128,
                "icon_128x128@2x.png": 256,
                "icon_256x256.png": 256,
                "icon_256x256@2x.png": 512,
                "icon_512x512.png": 512,
                "icon_512x512@2x.png": 1024,
            }
            for name, sz in xc_map.items():
                base.resize((sz, sz), Image.Resampling.LANCZOS).save(xcassets_dir / name, "PNG")
            print("✅ Catálogo AppIcon.appiconset para macOS gerado.")

        # 8. MSIX Assets (Windows Store / AppX)
        msix_dir = BRANDING_DIR / "msix" / "Assets"
        if msix_dir.exists():
            msix_map = {
                "Document44x44.png": (44, 44),
                "Square44x44Logo.scale-200.png": (88, 88),
                "Square44x44Logo.targetsize-256.png": (256, 256),
                "Square44x44Logo.altform-unplated_targetsize-256.png": (256, 256),
                "Square44x44Logo.altform-lightunplated_targetsize-256.png": (256, 256),
                "SmallTile.scale-200.png": (142, 142),
                "StoreLogo.scale-200.png": (100, 100),
                "Square150x150Logo.scale-200.png": (300, 300),
                "LargeTile.scale-200.png": (620, 620),
            }
            for name, (w, h) in msix_map.items():
                base.resize((w, h), Image.Resampling.LANCZOS).save(msix_dir / name, "PNG")

            wide = Image.new("RGBA", (620, 300), (0, 0, 0, 0))
            icon_wide = base.resize((260, 260), Image.Resampling.LANCZOS)
            wide.paste(icon_wide, ((620 - 260) // 2, (300 - 260) // 2))
            wide.save(msix_dir / "Wide310x150Logo.scale-200.png", "PNG")
            print("✅ Pacotes MSIX para Windows atualizados.")

    print("\n🎉 Todos os ícones do sistema foram atualizados com o seu ícone personalizado!")

if __name__ == "__main__":
    generate_branding()
