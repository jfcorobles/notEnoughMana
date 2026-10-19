"""
Programa para traducir las cartas de Not Enough Mana (EN -> ES).
Lee las cartas originales en la carpeta EN, limpia el área de texto preservando
el diseño, marco, fondo y resolución original, aplica la tipografía exacta
(MedievalSharp, Cambria y Segoe UI con iconos de vida y maná) y guarda
las 154 cartas traducidas en la carpeta ES.
"""

import os
import re
import io
import json
import base64
import hashlib
import urllib.request
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EN_DIR = os.path.join(BASE_DIR, 'EN')
ES_DIR = os.path.join(BASE_DIR, 'ES')
CARDS_DB_PATH = os.path.join(BASE_DIR, 'cards_database.json')

FONT_TITLE_PATH = os.path.join(BASE_DIR, 'MedievalSharp.ttf')
FONT_SUB_IT = r'C:\Windows\Fonts\cambriai.ttf'
FONT_SUB_REG = r'C:\Windows\Fonts\cambria.ttc'
FONT_BODY_REG = r'C:\Windows\Fonts\segoeui.ttf'
FONT_BODY_BLD = r'C:\Windows\Fonts\segoeuib.ttf'
FONT_BODY_IT = r'C:\Windows\Fonts\segoeuii.ttf'
FONT_BODY_BI = r'C:\Windows\Fonts\segoeuiz.ttf'

# Iconos incrustados directamente en base64 para no depender de archivos externos
HEART_B64 = b'iVBORw0KGgoAAAANSUhEUgAAABUAAAATCAYAAAB/TkaLAAABoklEQVR4nK2UO08CURCFz15w1UVFCGujbgTfwRCjJIs0vhKuhaGwITY2FtpYWJFQWpj4EyysbSypaE002FMZbUBAgpJoZBMfjI0gsktA3VPdZM58c6aYCzTo8XA9VNxR6fFwPdRYa/Q97LX2oRDxU9ouU8aqUEaR6T48a9hUiPjpbnKKMlaF0naZChtzVF8Xqo9c0EsfV8/6SQ4N0r7KnbF4AgAyikzIdutslmAvOtfc3BmLJwQAyC/P0Pv5U/MVZA3iwjDeUmXQTbm57yuAUNxWSTu7hfCin/4XiWEX2OtlyTQgALylymCVUsk0IABU8g9gFveAqVDLoAOsY7rHXOiYBOY6SQrWpT7ToB2BIc4AQFwZ4cKo9G+gdbUfzlg8wQDAGYsnxID9X0DmlSAuKhyouyig+bW0Etk02KLfV8fqi9KuyuHQfg2UtjyoAnVJAaAUDdLL6TXaSixr6Ap74DpO/uCwRp/j6EKwbY6DbK0TGwENoTVwVOVsvtcQJoxKkA583AjYlvLcV/tj03aZckEvte5qQ8VtlbIzE1SI+NsCfgKHZpMhe+mRIwAAAABJRU5ErkJggg=='
DROP_B64 = b'iVBORw0KGgoAAAANSUhEUgAAAAwAAAAQCAYAAAAiYZ4HAAABUklEQVR4nI2RwUsCQRjF3+6ok47KhJDRii0KQpcgEARBBYM95V/TvT+mjt3y5qGD1251EwyFrAzESdtq0dntoCu7a5bvNPPN93vz5hsFHp00Lm6kZQpCGbdJmDqfYggAhDIeCUeiZ0diqHoBaZkCAGQh34iflg0lxtNu/etj/HJ959g+AADUZErjRhWkkIOTzxrB89CxcX7pLbBaqe6uuVGF8vyqj0dvvZWht3k3taeTQs7nOC8XK2oypa0BSoyn5+ViJRiBFHJgtVKdUMZ9gJPPGkF3L+TQHbYCCGU8oWd+bXZlH2p1AAgBQDLOuLPB3XcTZVwFgPHB/lr2oBJ6BjYJU3WbOMDiHTwaia593F96n8nZ1oDsPEKxvk1VWqaY9p7+Baa9J0jLFIuxdrpN0WpvbBatNkin2wSWY5WWKfBwfzXpDzR33q7U/uAWk9FALvc/PJtqyI7O/vQAAAAASUVORK5CYII='

def get_font_title():
    if not os.path.exists(FONT_TITLE_PATH):
        url = 'https://raw.githubusercontent.com/google/fonts/main/ofl/medievalsharp/MedievalSharp.ttf'
        try:
            print(f"Descargando fuente {FONT_TITLE_PATH}...")
            urllib.request.urlretrieve(url, FONT_TITLE_PATH)
        except Exception as e:
            print(f"Error descargando fuente: {e}")
    return FONT_TITLE_PATH


def load_card_database():
    if not os.path.exists(CARDS_DB_PATH):
        raise FileNotFoundError(f"No se encontró el archivo de base de datos de cartas: {CARDS_DB_PATH}")
    with open(CARDS_DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)



def inpaint_card(img_path, is_event=False):
    bgr = cv2.imread(img_path)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    mask = np.zeros(gray.shape, dtype=np.uint8)
    
    sub = gray[390:680, 20:477]
    if not is_event:
        mask_roi = ((sub < 165) | (bgr[390:680, 20:477, 2] > 160) | (bgr[390:680, 20:477, 0] > 160)).astype(np.uint8) * 255
    else:
        mask_roi = ((sub > 80) | (bgr[390:680, 20:477, 0] > 110) | (bgr[390:680, 20:477, 2] > 110)).astype(np.uint8) * 255
        
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask_roi = cv2.dilate(mask_roi, kernel, iterations=2)
    mask[390:680, 20:477] = mask_roi
    
    inpainted = cv2.inpaint(bgr, mask, 5, cv2.INPAINT_TELEA)
    return Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB))


def parse_tokens(text):
    # Splits text into individual words, spaces, icons and bold text
    pattern = r'(\*\*.*?\*\*|\{heart\}|\{drop\}|\s+|[^\s*{}]+)'
    raw_tokens = re.findall(pattern, text)
    tokens = []
    for t in raw_tokens:
        if not t:
            continue
        if t == '{heart}':
            tokens.append(('icon', 'heart'))
        elif t == '{drop}':
            tokens.append(('icon', 'drop'))
        elif t.startswith('**') and t.endswith('**') and len(t) >= 4:
            tokens.append(('bold', t[2:-2]))
        else:
            tokens.append(('text', t))
            
    # Group words with following icons or punctuation into unbreakable clusters
    # so an icon or period NEVER wraps to a line by itself!
    clusters = []
    i = 0
    while i < len(tokens):
        item = tokens[i]
        # If item is space, keep as standalone space
        if item[0] == 'text' and item[1].isspace():
            clusters.append([item])
            i += 1
            continue
            
        # Start a word cluster
        cluster = [item]
        i += 1
        # If followed immediately by an icon or punctuation without space, bond them
        while i < len(tokens) and not (tokens[i][0] == 'text' and tokens[i][1].isspace()):
            cluster.append(tokens[i])
            i += 1
        clusters.append(cluster)
        
    return clusters


def render_clusters_to_lines(clusters, font_reg, font_bld, heart_img, drop_img, max_w):
    lines = []
    cur_line = []
    cur_w = 0
    
    for cluster in clusters:
        # Calculate total width of this cluster
        cluster_w = 0
        items_with_w = []
        for kind, val in cluster:
            if kind == 'icon':
                w = (heart_img.size[0] if val == 'heart' else drop_img.size[0]) + 1
            elif kind == 'bold':
                bbox = font_bld.getbbox(val)
                w = bbox[2] - bbox[0]
            else:
                bbox = font_reg.getbbox(val)
                w = bbox[2] - bbox[0]
            items_with_w.append((kind, val, w))
            cluster_w += w
            
        # Is it just whitespace?
        is_space = len(cluster) == 1 and cluster[0][0] == 'text' and cluster[0][1].isspace()
        
        if cur_w + cluster_w > max_w and cur_line:
            if is_space:
                continue # ignore space at start of line
            lines.append(cur_line)
            cur_line = []
            cur_w = 0
            
        for item in items_with_w:
            cur_line.append(item)
        cur_w += cluster_w
        
    if cur_line:
        lines.append(cur_line)
    return lines


def render_card_image(card_def, heart_img, drop_img):
    img_path = os.path.join(EN_DIR, card_def['source_file'])
    is_event = card_def.get('type') == 'event'
    card = inpaint_card(img_path, is_event=is_event)
    draw = ImageDraw.Draw(card)
    
    text_color = (245, 240, 235) if is_event else (28, 24, 24)
    sub_color = (235, 230, 220) if is_event else (35, 30, 30)
    
    # 1. Title
    title = card_def['title_es'].upper()
    title_size = 27
    font_file = get_font_title()
    font_title = ImageFont.truetype(font_file, title_size)
    bbox = font_title.getbbox(title)
    w_t = bbox[2] - bbox[0]
    while w_t > 385 and title_size > 17:
        title_size -= 1
        font_title = ImageFont.truetype(font_file, title_size)
        bbox = font_title.getbbox(title)
        w_t = bbox[2] - bbox[0]
        
    title_y = 408
    draw.text(((497 - w_t) / 2, title_y), title, fill=text_color, font=font_title)
    
    # 2. Subtitle
    subtitle = card_def.get('subtitle_es')
    if subtitle:
        sub_font_file = FONT_SUB_REG if card_def.get('subtitle_is_regular') else FONT_SUB_IT
        font_sub = ImageFont.truetype(sub_font_file, 18)
        bbox_s = font_sub.getbbox(subtitle)
        w_s = bbox_s[2] - bbox_s[0]
        sub_y = 446
        draw.text(((497 - w_s) / 2, sub_y), subtitle, fill=sub_color, font=font_sub)
        
    # 3. Body Text
    body_paragraphs = card_def.get('body_es', [])
    body_y = card_def.get('body_y', 492)
    max_w = 394
    start_x = 55
    
    body_font_size = 15.5
    line_h = 23
    if len(body_paragraphs) >= 4:
        body_font_size = 14.5
        line_h = 21
        body_y = 486

    font_reg = ImageFont.truetype(FONT_BODY_REG, int(body_font_size))
    font_bld = ImageFont.truetype(FONT_BODY_BLD, int(body_font_size))
    
    for p in body_paragraphs:
        clusters = parse_tokens(p)
        lines = render_clusters_to_lines(clusters, font_reg, font_bld, heart_img, drop_img, max_w)
        for line in lines:
            cur_x = start_x
            for kind, val, w in line:
                if kind == 'icon':
                    ic = heart_img if val == 'heart' else drop_img
                    card.paste(ic, (int(cur_x), int(body_y + 3)), ic)
                elif kind == 'bold':
                    draw.text((cur_x, body_y), val, fill=text_color, font=font_bld)
                else:
                    draw.text((cur_x, body_y), val, fill=text_color, font=font_reg)
                cur_x += w
            body_y += line_h
        body_y += 6
        
    # 4. Footer Reminder Text
    footer = card_def.get('footer_es')
    if footer:
        footer_font_size = 13.5
        font_it = ImageFont.truetype(FONT_BODY_IT, int(footer_font_size))
        font_bi = ImageFont.truetype(FONT_BODY_BI, int(footer_font_size))
        footer_y = card_def.get('footer_y', 625)
        
        # Split footer into tokens
        tokens = []
        for t in re.findall(r'(\*\*.*?\*\*|\s+|[^\s*]+)', footer):
            if t.startswith('**') and t.endswith('**') and len(t) >= 4:
                tokens.append(('bi', t[2:-2]))
            else:
                tokens.append(('it', t))
                
        lines = []
        cur_line = []
        cur_w = 0
        for kind, val in tokens:
            f = font_bi if kind == 'bi' else font_it
            bbox = f.getbbox(val)
            item_w = bbox[2] - bbox[0]
            if cur_w + item_w > (max_w + 5) and cur_line and val.strip():
                lines.append(cur_line)
                cur_line = []
                cur_w = 0
                if val.isspace():
                    continue
            cur_line.append((kind, val, item_w))
            cur_w += item_w
        if cur_line:
            lines.append(cur_line)
            
        for line in lines:
            cur_x = start_x
            for kind, val, w in line:
                f = font_bi if kind == 'bi' else font_it
                draw.text((cur_x, footer_y), val, fill=text_color, font=f)
                cur_x += w
            footer_y += 18
            
    return card


def main():
    print("==================================================================")
    print("      Traductor de Cartas 'Not Enough Mana' (EN -> ES)            ")
    print("==================================================================")
    os.makedirs(ES_DIR, exist_ok=True)
    
    # Cargar iconos directamente desde memoria (base64)
    heart_img = Image.open(io.BytesIO(base64.b64decode(HEART_B64))).convert('RGBA')
    drop_img = Image.open(io.BytesIO(base64.b64decode(DROP_B64))).convert('RGBA')
    
    card_database = load_card_database()
    print(f"Base de datos cargada con {len(card_database)} definiciones de cartas.")
    
    en_files = sorted(os.listdir(EN_DIR))
    print(f"Total de cartas en carpeta EN: {len(en_files)}")
    
    file_hashes = {}
    for f in en_files:
        path = os.path.join(EN_DIR, f)
        h = hashlib.md5(open(path, 'rb').read()).hexdigest()
        file_hashes.setdefault(h, []).append(f)
        
    print(f"Cartas únicas detectadas: {len(file_hashes)}")
    
    processed_count = 0
    saved_files_count = 0
    
    for h, flist in sorted(file_hashes.items(), key=lambda x: x[1][0]):
        primary_file = flist[0]
        if primary_file not in card_database:
            print(f"[ADVERTENCIA] No hay definición para {primary_file}")
            continue
            
        cdef = card_database[primary_file]
        cdef['source_file'] = primary_file
        
        print(f"[{processed_count + 1:2d}/{len(file_hashes)}] Traduciendo: {primary_file} -> '{cdef['title_es']}' ({len(flist)} copias)")
        rendered_card = render_card_image(cdef, heart_img, drop_img)
        
        for target_filename in flist:
            dest_path = os.path.join(ES_DIR, target_filename)
            rendered_card.save(dest_path)
            saved_files_count += 1
            
        processed_count += 1
        
    print("==================================================================")
    print(f"Proceso completado con éxito!")
    print(f"Se tradujeron {processed_count} cartas únicas.")
    print(f"Se generaron {saved_files_count} archivos de cartas en español en: {ES_DIR}")
    print("==================================================================")


if __name__ == '__main__':
    main()
