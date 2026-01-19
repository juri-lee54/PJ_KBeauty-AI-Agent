import json
import os
import csv
import base64
import mimetypes
from datetime import datetime
from typing import List, Dict, Optional, Tuple

from . import templates

PROJECT_ROOT = os.getcwd()
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DIST_DIR = os.path.join(PROJECT_ROOT, "dist")

def load_json(path: str) -> Dict:
    if not path or not os.path.exists(path):
        return {}
    with open(path, encoding='utf-8') as f:
        try:
            return json.load(f)
        except Exception:
            return {}


def load_products_csv(path: str) -> List[Dict]:
    rows = []
    if not path or not os.path.exists(path):
        return rows
    with open(path, encoding='utf-8-sig', errors='ignore') as f:  # BOM 제거
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({
                'product': (r.get('product') or r.get('name') or '').strip(),
                'count': int((r.get('count') or '0').strip()) if (r.get('count') or '').strip().isdigit() else (r.get('count') or 0),
                'url': (r.get('url') or r.get('link') or '').strip(),
                'quality': (r.get('quality') or '').strip(),
                'ingredients_snippet': (r.get('ingredients_snippet') or r.get('ingredients') or '').strip(),
                'formulation': (r.get('formulation') or '').strip(),
                'image': (r.get('image') or r.get('image_url') or '').strip()
            })
    return rows

def _encode_image_to_data_uri(path: str) -> Optional[str]:
    if not path or not os.path.exists(path):
        return None
    mime, _ = mimetypes.guess_type(path)
    mime = mime or "image/png"
    with open(path, "rb") as f:
        b = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{b}"

def parse_youtube_csv_data(file_path: str) -> List[Dict]:
        
    img_dir = os.path.join(DATA_DIR, "img")
    
    products_dict = {}
    
    with open(file_path, encoding='utf-8-sig', errors='ignore') as f:
        reader = csv.DictReader(f)
                
        for row in reader:
            
            product_name = (row.get('product') or '').strip()
            
            if not product_name:
                continue
            count = row.get('count', '0')
            url = (row.get('url') or '').strip()
            quality = (row.get('quality') or '').strip()
            ingredients_snippet = (row.get('ingredients_snippet') or '').strip()
            formulation = (row.get('formulation') or '').strip()
            
            if product_name not in products_dict:
                products_dict[product_name] = {
                    'product': product_name,
                    'count': count,
                    'urls': [],
                    'quality': quality,
                    'ingredients_snippet': ingredients_snippet,
                    'formulation': formulation
                }
            
            if url and url not in products_dict[product_name]['urls']:
                products_dict[product_name]['urls'].append(url)
            
            if quality and quality != 'no_data' and (not products_dict[product_name]['quality'] or products_dict[product_name]['quality'] == 'no_data'):
                products_dict[product_name]['quality'] = quality
            
            if ingredients_snippet and (not products_dict[product_name]['ingredients_snippet'] or products_dict[product_name]['ingredients_snippet'] == 'no_data'):
                products_dict[product_name]['ingredients_snippet'] = ingredients_snippet
            
            if formulation and (not products_dict[product_name]['formulation'] or products_dict[product_name]['formulation'] == 'no_data'):
                products_dict[product_name]['formulation'] = formulation
        
    parsed_products = []
    for product_name, data in products_dict.items():
        display_image_path = None
        for ext in ['.png', '.jpg', '.jpeg', '.webp']:
            potential_path = os.path.join(img_dir, f"{product_name}{ext}")
            if os.path.exists(potential_path):
                display_image_path = potential_path
                break
        
        url = ''
        for u in data['urls']:
            if 'oliveyoung' in u.lower():
                url = u
                break
        if not url and data['urls']:
            url = data['urls'][0]
        
        ingredients_snippet = data['ingredients_snippet'].replace("ation during transmission", "").strip()
        quality = data['quality'] if data['quality'] != 'no_data' else ''
        formulation = data['formulation'] if data['formulation'] != 'no_data' else ''
        
                
        parsed_products.append({
            'product': product_name,
            'count': data['count'],
            'url': url,
            'ingredients_snippet': ingredients_snippet,
            'quality': quality,
            'formulation': formulation,
            'image_path': display_image_path
        })
    
    return parsed_products


def _aggregate_products(products: List[Dict]) -> List[Dict]:
    agg = {}
    for p in products:
        name = (p.get('product') or '').strip()
        if not name:
            continue
        key = name
        cnt = p.get('count') or 0
        try:
            cnt = int(cnt)
        except Exception:
            cnt = 0
        if key not in agg:
            agg[key] = {
                'product': key,
                'count': 0,
                'urls': [],
                'quality': '',
                'ingredients_snippet': '',
                'image': None
            }
        agg[key]['count'] += cnt
        url = p.get('url') or ''
        if url and url not in agg[key]['urls']:
            agg[key]['urls'].append(url)
        if p.get('quality') and not agg[key]['quality']:
            agg[key]['quality'] = p.get('quality')
        if p.get('ingredients_snippet') and not agg[key]['ingredients_snippet']:
            agg[key]['ingredients_snippet'] = p.get('ingredients_snippet')
        if p.get('image') and not agg[key]['image']:
            agg[key]['image'] = p.get('image')

    items = list(agg.values())
    items.sort(key=lambda x: x.get('count', 0), reverse=True)
    return items


def _choose_oliveyoung_url(urls: List[str]) -> Optional[str]:
    if not urls:
        return None
    for u in urls:
        if u and 'oliveyoung' in u.lower():
            return u
    for u in urls:
        if u:
            return u
    return None


def _pick_top_products_with_oliveyoung(products_raw: List[Dict], topn: int = 2) -> List[Dict]:
    agg = _aggregate_products(products_raw)
    out = []
    for it in agg[:topn]:
        chosen_url = _choose_oliveyoung_url(it.get('urls', []))
        out.append({
            'product': it['product'],
            'count': it.get('count', 0),
            'url': chosen_url or '',
            'quality': it.get('quality', ''),
            'ingredients_snippet': it.get('ingredients_snippet', '')[:400],
            'image': it.get('image', None)
        })
    return out

def build_newsletter(
    agent_path: Optional[str] = None,
    other_path: Optional[str]= None,
    youtube_csv: Optional[str] = None,
    out_path: Optional[str] =  None,
    logo_path: Optional[str] = None,
    weekly_path: Optional[str] = None,
    usa_summary_path: Optional[str] = None,
    japan_summary_path: Optional[str] = None,
    china_summary_path: Optional[str] = None
) -> Tuple[str, str, Optional[str]]:

    if agent_path is None:
        agent_path = os.path.join(DATA_DIR, "agent_results.json")
    if other_path is None:
        other_path = os.path.join(DATA_DIR, "instagram_trend.json")
    if youtube_csv is None:
        youtube_csv = os.path.join(DATA_DIR, "youtube_trend.csv")
    if weekly_path is None:
        weekly_path = os.path.join(DATA_DIR, "weekly_insights_all.json")
    if usa_summary_path is None:
        usa_summary_path = os.path.join(DATA_DIR, "amorepacific_product_summary_usa.json")
    if japan_summary_path is None:
        japan_summary_path = os.path.join(DATA_DIR, "amorepacific_product_summary_japan.json")
    if china_summary_path is None:
        china_summary_path = os.path.join(DATA_DIR, "amorepacific_product_summary_china.json")

    agent = load_json(agent_path)
    other = load_json(other_path)
    weekly_all = load_json(weekly_path)
    usa_summary = load_json(usa_summary_path)
    japan_summary = load_json(japan_summary_path)
    china_summary = load_json(china_summary_path)
    
    youtube_trends = parse_youtube_csv_data(youtube_csv)
    
    for p in youtube_trends:
        if p.get('image_path'):
            encoded = _encode_image_to_data_uri(p['image_path'])
            p['image'] = encoded if encoded else ""
        else:
            p['image'] = ""

    if not isinstance(other, dict): 
        other = {}
    
    other['youtube_products'] = youtube_trends

    products = []
    if os.path.exists(youtube_csv):
        with open(youtube_csv, encoding='utf-8-sig', errors='ignore') as f:  # BOM 제거
            raw_rows = list(csv.DictReader(f))
        products = _pick_top_products_with_oliveyoung(raw_rows, topn=2)
    
    agent_combined = dict(agent) if isinstance(agent, dict) else {}
    agent_combined.setdefault('weekly_insights_all', weekly_all or {})
    agent_combined.setdefault('instagram_trend', other or {})
    agent_combined.setdefault('product_summaries', {
        'usa': usa_summary or {},
        'japan': japan_summary or {},
        'china': china_summary or {}
    })
    user_role = os.getenv('USER_ROLE', '마케팅 팀')
    agent_combined['role'] = user_role
    if isinstance(weekly_all, dict) and weekly_all.get('aggregate'):
        agent_combined.setdefault('aggregate', weekly_all.get('aggregate'))

    logo_file = logo_path or os.path.join(DATA_DIR, "assets", "amore_logo.png")
    if not os.path.exists(logo_file):
        logo_file = None

    email_html = templates.render_full(agent_combined, other, products, use_cid=True, logo_data_uri=None)
    logo_data_uri = _encode_image_to_data_uri(logo_file) if logo_file else None
    preview_html = templates.render_full(agent_combined, other, products, use_cid=False, logo_data_uri=logo_data_uri)

    os.makedirs(DIST_DIR, exist_ok=True)
    week_label = agent_combined.get('week_range') or weekly_all.get('file_recent') or other.get('file_recent') or datetime.now().strftime('%Y.%m.%d')
    safe_label = str(week_label).replace('/', '_').replace('~', '_').replace(' ', '_')
    preview_path = out_path or os.path.join(DIST_DIR, f"newsletter_preview_{safe_label}.html")
    with open(preview_path, 'w', encoding='utf-8') as f:
        f.write(preview_html)

    return email_html, preview_path, logo_file


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build newsletter; returns email HTML (cid-based) and preview HTML")
    parser.add_argument("--agent", help="agent_results.json path", default=None)
    parser.add_argument("--other", help="instagram_trend.json path", default=None)
    parser.add_argument("--youtube", help="youtube_trend.csv path", default=None)
    parser.add_argument("--weekly", help="weekly_insights_all.json path", default=None)
    parser.add_argument("--usa", help="amorepacific_product_summary_usa.json path", default=None)
    parser.add_argument("--japan", help="amorepacific_product_summary_japan.json path", default=None)
    parser.add_argument("--china", help="amorepacific_product_summary_china.json path", default=None)
    parser.add_argument("--out", help="output preview html file", default=None)
    parser.add_argument("--logo", help="logo file path (data/assets/amore_logo.png recommended)", default=None)
    args = parser.parse_args()
    build_newsletter(args.agent, args.other, args.youtube, args.out, logo_path=args.logo,
                     weekly_path=args.weekly, usa_summary_path=args.usa,
                     japan_summary_path=args.japan, china_summary_path=args.china)