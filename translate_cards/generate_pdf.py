"""
Script para generar documentos PDF a partir de las cartas traducidas en la carpeta ES.
Soporta dos formatos:
  1. Print & Play (PnP): Cuadrícula 3x3 (9 cartas por hoja) en tamaño A4 o Carta (Letter)
     a 300 DPI, con guías y marcas de corte para impresión y recorte fácil.
  2. Individual: 1 carta por página (154 páginas a resolución completa).
"""

import os
import argparse
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ES_DIR = os.path.join(BASE_DIR, 'ES')

# Dimensiones a 300 DPI
PAPER_SIZES = {
    'A4': (2480, 3508),      # 210 x 297 mm
    'Letter': (2550, 3300),  # 215.9 x 279.4 mm (8.5 x 11 in)
}

# Tamaño estándar Poker a 300 DPI: 63.5 x 88.9 mm (2.5 x 3.5 in)
CARD_WIDTH_300DPI = 750
CARD_HEIGHT_300DPI = 1050


def get_sorted_card_files():
    if not os.path.exists(ES_DIR):
        raise FileNotFoundError(f"No se encontró la carpeta: {ES_DIR}")
    files = [f for f in sorted(os.listdir(ES_DIR)) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not files:
        raise ValueError(f"No se encontraron imágenes en: {ES_DIR}")
    return files


def generate_single_cards_pdf(output_path):
    print("\n-------------------------------------------------------------")
    print(f" Generando PDF de Cartas Individuales...")
    print("-------------------------------------------------------------")
    card_files = get_sorted_card_files()
    total = len(card_files)
    
    pages = []
    for i, f in enumerate(card_files):
        img_path = os.path.join(ES_DIR, f)
        im = Image.open(img_path).convert('RGB')
        pages.append(im)
        if (i + 1) % 25 == 0 or (i + 1) == total:
            print(f"  Procesando carta {i + 1}/{total}...")
            
    print(f"Guardando {output_path} ({total} páginas)...")
    pages[0].save(
        output_path,
        'PDF',
        save_all=True,
        append_images=pages[1:],
        resolution=300.0
    )
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"[OK] PDF Individual guardado: {output_path} ({size_mb:.2f} MB)")


def generate_pnp_pdf(output_path, paper_type='A4'):
    print("\n-------------------------------------------------------------")
    print(f" Generando PDF Print & Play (Cuadrícula 3x3 en {paper_type})...")
    print("-------------------------------------------------------------")
    card_files = get_sorted_card_files()
    total_cards = len(card_files)
    
    page_w, page_h = PAPER_SIZES.get(paper_type, PAPER_SIZES['A4'])
    card_w = CARD_WIDTH_300DPI
    card_h = CARD_HEIGHT_300DPI
    
    total_grid_w = card_w * 3
    total_grid_h = card_h * 3
    margin_x = (page_w - total_grid_w) // 2
    margin_y = (page_h - total_grid_h) // 2
    
    cards_per_page = 9
    total_pages = (total_cards + cards_per_page - 1) // cards_per_page
    print(f"Total de cartas: {total_cards} -> {total_pages} páginas de {cards_per_page} cartas.")
    
    tick_len = 35
    mark_color = (160, 160, 160)
    
    # Intentar cargar fuente Segoe UI para pie de página
    try:
        font_info = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 28)
    except Exception:
        font_info = ImageFont.load_default()
        
    pages = []
    
    for page_idx in range(total_pages):
        start_idx = page_idx * cards_per_page
        end_idx = min(start_idx + cards_per_page, total_cards)
        page_card_files = card_files[start_idx:end_idx]
        
        sheet = Image.new('RGB', (page_w, page_h), (255, 255, 255))
        draw = ImageDraw.Draw(sheet)
        
        for slot_idx, filename in enumerate(page_card_files):
            col = slot_idx % 3
            row = slot_idx // 3
            x = margin_x + col * card_w
            y = margin_y + row * card_h
            
            img_path = os.path.join(ES_DIR, filename)
            im = Image.open(img_path).convert('RGB')
            # Redimensionar a 750x1050 (300 DPI) con filtro de alta calidad
            im_resized = im.resize((card_w, card_h), Image.Resampling.LANCZOS)
            sheet.paste(im_resized, (x, y))
            
        # Dibujar marcas de corte exteriores (en los márgenes)
        # Líneas verticales
        for c in range(4):
            cx = margin_x + c * card_w
            draw.line([(cx, margin_y - tick_len), (cx, margin_y)], fill=mark_color, width=2)
            draw.line([(cx, margin_y + total_grid_h), (cx, margin_y + total_grid_h + tick_len)], fill=mark_color, width=2)
            
        # Líneas horizontales
        for r in range(4):
            ry = margin_y + r * card_h
            draw.line([(margin_x - tick_len, ry), (margin_x, ry)], fill=mark_color, width=2)
            draw.line([(margin_x + total_grid_w, ry), (margin_x + total_grid_w + tick_len, ry)], fill=mark_color, width=2)
            
        # Texto informativo en el pie de página
        footer_text = f"Not Enough Mana (Español) - Página {page_idx + 1} de {total_pages} - {paper_type} (300 DPI)"
        bbox = font_info.getbbox(footer_text)
        w_f = bbox[2] - bbox[0]
        draw.text(((page_w - w_f) / 2, page_h - margin_y // 2 - 10), footer_text, fill=(180, 180, 180), font=font_info)
        
        pages.append(sheet)
        print(f"  Hoja {page_idx + 1}/{total_pages} montada...")
        
    print(f"Guardando {output_path}...")
    pages[0].save(
        output_path,
        'PDF',
        save_all=True,
        append_images=pages[1:],
        resolution=300.0
    )
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"[OK] PDF Print & Play guardado: {output_path} ({size_mb:.2f} MB)")


def main():
    parser = argparse.ArgumentParser(description="Generador de PDF para cartas de Not Enough Mana (ES)")
    parser.add_argument('--format', choices=['both', 'pnp', 'single'], default='both',
                        help="Formato a generar: 'pnp' (cuadrícula 3x3), 'single' (1 carta por página), o 'both' (ambos)")
    parser.add_argument('--paper', choices=['A4', 'Letter'], default='A4',
                        help="Tamaño de papel para Print & Play (A4 o Letter, por defecto A4)")
    parser.add_argument('--output-pnp', default='Cartas_Espanol_Print_and_Play.pdf',
                        help="Nombre del archivo PDF para Print & Play")
    parser.add_argument('--output-single', default='Cartas_Espanol_Individuales.pdf',
                        help="Nombre del archivo PDF de cartas individuales")
                        
    args = parser.parse_args()
    
    print("=============================================================")
    print("  Generador de PDF - Not Enough Mana (Print & Play Español)  ")
    print("=============================================================")
    
    if args.format in ('both', 'single'):
        out_single = os.path.join(BASE_DIR, args.output_single)
        generate_single_cards_pdf(out_single)
        
    if args.format in ('both', 'pnp'):
        out_pnp = os.path.join(BASE_DIR, args.output_pnp)
        generate_pnp_pdf(out_pnp, paper_type=args.paper)
        
    print("\n=============================================================")
    print("  ¡Proceso de generación de PDFs completado exitosamente!     ")
    print("=============================================================")


if __name__ == '__main__':
    main()
