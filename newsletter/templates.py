import html
from datetime import datetime
from typing import List, Dict, Optional

def _escape(s):
    return html.escape(str(s)) if s is not None else ""

def base_template(
    week_label: str,
    week_display: str,
    content: str,
    title: str = "Amorepacific Weekly",
    use_cid: bool = True,
    logo_cid: str = "amore_logo",
    logo_data_uri: Optional[str] = None,
    file_label: str = ""
) -> str:
    css = """
    :root{--page-bg:#eaf3fb;--panel-bg:#ffffff;--accent:#FF6B4A;--muted:#4b5563;--border:#d9e8f2}
    body{font-family:Inter, 'Helvetica Neue', Arial, sans-serif;background:var(--page-bg);margin:0;padding:28px;color:#0f1724}
    .container{max-width:980px;margin:0 auto}
    .panel{background:var(--panel-bg);border-radius:12px;overflow:hidden;box-shadow:0 14px 40px rgba(20,20,40,0.08)}
    .topbar{display:flex;justify-content:space-between;align-items:center;padding:18px 28px;border-bottom:1px solid var(--border);gap:12px;background:transparent}
    .title {font-size:28px;font-weight:800;color:#0b1220}
    .meta {text-align:right}
    .file-label{font-size:13px;color:#0b1220;font-weight:700}
    .generated {font-size:12px;color:var(--muted)}
    .logo-wrap{width:100%;padding:14px 28px;border-bottom:1px solid var(--border);background:transparent;display:flex;align-items:center;justify-content:center}
    .logo-wrap img{width:100%;max-height:140px;object-fit:contain;display:block}
    .hero{padding:22px 28px;background:transparent}
    .section{padding:18px;border-top:1px solid transparent;background:linear-gradient(0deg,#f5fbff, #f5fbff);margin:14px 28px;border-radius:10px}
    .section h2{font-size:18px;margin:0 0 12px;color:#0b1220}
    .lead{color:#0f1724;line-height:1.6;margin:6px 0 0}
    .intro{font-size:14px;color:#0b1220;margin-bottom:8px}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px;min-width:0}
    .grid.country-grid{grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:20px;max-width:100%}
    .card{background:var(--panel-bg);padding:14px;border-radius:10px;border:1px solid #cfeefc;box-shadow:0 6px 18px rgba(12,14,20,0.04);color:#0b1220}
    .product-card{display:flex;gap:12px;align-items:flex-start}
    .product-thumb{width:96px;height:96px;border-radius:8px;background:#fff;flex:0 0 96px;display:flex;align-items:center;justify-content:center;overflow:hidden;border:1px solid #ddd}
    .product-thumb img{max-width:100%;max-height:100%;object-fit:contain;display:block}
    .product-info{flex:1;color:#0b1220}
    .product-title{font-weight:700;margin-bottom:6px;color:#0b1220}
    .muted{color:var(--muted);font-size:13px}
    .hashtag-pill{display:inline-block;background:#ffffff;color:#0b1220;padding:6px 10px;border-radius:14px;font-size:13px;border:1px solid #d0eaf8}
    .rec-item{padding:12px;border-radius:8px;background:#ffffff;border:1px solid #cfeefc;box-shadow:0 2px 4px rgba(0,0,0,0.05)}
    .tokens{font-size:12px;color:#444;margin-top:8px}
    .section-footer{margin-top:10px;color:var(--muted);font-size:13px}

    /* ---- Country card styles (new) ---- */
    .country-hero{display:block;gap:16px;padding:20px;border-radius:12px;background:linear-gradient(180deg,#fff,#fbfdff);border:1px solid #e1f0fb;box-shadow:0 4px 12px rgba(0,0,0,0.05);overflow:hidden;min-width:0}
    .country-header{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;margin-bottom:16px;padding-bottom:16px;border-bottom:2px solid #e1f0fb;flex-wrap:wrap}
    .country-title{font-size:24px;font-weight:800;color:#0b1220;margin-bottom:4px}
    .country-summary{font-size:13px;color:var(--muted)}
    .country-body{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin-top:16px;min-width:0}
    .stat-list{list-style:none;padding:0;margin:0}
    .stat-list li{margin-bottom:8px;font-size:13px;color:#0b1220;padding:4px 0}
    .badge{display:inline-block;padding:6px 12px;border-radius:12px;background:#fff;border:1px solid #dceffd;font-weight:700;font-size:12px}
    .insight-box{background:#f1fcf9;border-left:4px solid #19a37a;padding:14px;border-radius:8px;margin-bottom:16px}
    .neg-token{display:inline-block;padding:6px 10px;border-radius:999px;background:#fff4f4;border:1px solid #ffd1d1;margin:4px 4px 4px 0;font-weight:700;font-size:12px;color:#b93a3a}
    .small-muted{font-size:12px;color:var(--muted)}
    
    /* Info cards with colors */
    .info-card{background:#fff;padding:16px;border-radius:10px;border:1px solid #e1f0fb;box-shadow:0 2px 8px rgba(0,0,0,0.04);margin-bottom:12px;min-width:0;overflow:hidden}
    .info-card-header{font-size:14px;font-weight:700;color:#0b1220;margin-bottom:12px;padding-bottom:8px;border-bottom:2px solid #f0f7ff}
    .info-card.ingredients .info-card-header{border-bottom-color:#e8f5e9;color:#2e7d32}
    .info-card.textures .info-card-header{border-bottom-color:#fff3e0;color:#e65100}
    .info-card.types .info-card-header{border-bottom-color:#e3f2fd;color:#1565c0}
    .info-card.features .info-card-header{border-bottom-color:#f3e5f5;color:#6a1b9a}
    .info-card.benefits .info-card-header{border-bottom-color:#e0f2f1;color:#00695c}
    .info-card.categories .info-card-header{border-bottom-color:#fce4ec;color:#c2185b}
    .info-card.brands .info-card-header{border-bottom-color:#fff8e1;color:#f57f17}
    .info-card.negative .info-card-header{border-bottom-color:#ffebee;color:#c62828}
    .info-card.insights .info-card-header{border-bottom-color:#e8f5e9;color:#2e7d32}
    
    .stat-item{display:flex;justify-content:space-between;align-items:center;padding:8px 12px;margin:4px 0;background:#f8fafc;border-radius:6px;border-left:3px solid #cbd5e1}
    .stat-item-value{font-weight:700;color:#0b1220}
    .stat-item.ingredient{border-left-color:#4caf50;background:#f1f8f4}
    .stat-item.texture{border-left-color:#ff9800;background:#fff8f0}
    .stat-item.type{border-left-color:#2196f3;background:#f0f7ff}
    .stat-item.feature{border-left-color:#9c27b0;background:#faf5fc}
    .stat-item.benefit{border-left-color:#009688;background:#f0f9f7}
    
    .total-products-card{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:#fff;padding:12px 16px;border-radius:10px;text-align:center;box-shadow:0 2px 8px rgba(102,126,234,0.2);display:inline-flex;align-items:center;gap:12px;flex-wrap:wrap;justify-content:center}
    .total-products-card .badge{background:rgba(255,255,255,0.2);border-color:rgba(255,255,255,0.3);color:#fff;font-size:11px;padding:4px 8px}
    .total-products-card strong{font-size:20px;display:inline-block;margin:0}
    
    @media (max-width:820px){.country-body{grid-template-columns:1fr}.country-header{flex-direction:column}}
    """
    logo_html = ""
    if use_cid:
        logo_html = f"<img src='cid:{_escape(logo_cid)}' alt='Amorepacific' />"
    else:
        if logo_data_uri:
            logo_html = f"<img src='{_escape(logo_data_uri)}' alt='Amorepacific' />"
        else:
            logo_html = ""

    html_doc = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{_escape(title)} — {_escape(week_label)}</title>
<style>{css}</style>
</head>
<body>
  <div class="container">
    <div class="panel">
      <div class="topbar">
        <div class="left">
          <div class="title">{_escape(title)}</div>
        </div>
        <div class="meta">
          <div class="file-label">{_escape(file_label)}</div>
          <div class="generated">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
        </div>
      </div>

      <div class="logo-wrap">
        {logo_html}
      </div>

      <div class="hero">
        {content}
      </div>
    </div>
  </div>
</body>
</html>"""
    return html_doc

def section(title: str, inner_html: str) -> str:
    return f"<div class='section'><h2>{_escape(title)}</h2>{inner_html}</div>"

def render_greeting(agent: Dict) -> str:
    week_range = agent.get('week_range') or agent.get('weekly_insights_all', {}).get('week_range') or ""
    role = agent.get('user_role') or '마케팅 팀'
    intro = (
        f"안녕하세요, Amorepacific {role} 여러분. "
        f"{_escape(week_range) + ' ' if week_range else ''}이번 주 SNS/올리브영 리테일 데이터에서 포착된 주요 신호와 인사이트를 기반으로 "
        "여러분의 업무에 활용하도록 권장 액션을 정리했습니다. \n아래 요약을 확인하시고 필요하면 세부 데이터로 들어가 보시면 됩니다."
    )
    return f"<div class='intro'>{_escape(intro)}</div>"

def render_summary(agent: Dict) -> str:
    summary = (
        agent.get('weekly_summary') or 
        agent.get('summary_top1') or 
        agent.get('summary') or
        (agent.get('weekly_insights_all') or {}).get('summary_top1') or
        (agent.get('weekly_insights_all') or {}).get('summary') or
        (agent.get('weekly_insights_all') or {}).get('weekly_summary') or
        (agent.get('aggregate') or {}).get('summary') or
        (agent.get('aggregate') or {}).get('final_two_line_suggestion') or
        ""
    )
    
    if not summary or summary.strip() == "" or summary == "요약 정보가 없습니다.":
        weekly_all = agent.get('weekly_insights_all') or {}
        comparison = weekly_all.get('comparison_with_llm_insights') or weekly_all.get('comparison') or {}
        llm_insight = comparison.get('llm_insight') or comparison.get('common') or comparison.get('summary') or ""
        
        if llm_insight:
            summary = llm_insight[:200] + "..." if len(llm_insight) > 200 else llm_insight
        else:
            agg = agent.get('aggregate') or {}
            final_two = agg.get('final_two_line_suggestion') or ""
            if final_two:
                summary = final_two[:200] + "..." if len(final_two) > 200 else final_two
            else:
                summary = "이번 주 데이터 분석이 진행 중입니다. 세부 섹션을 확인해주세요."
    
    return section("📌 이번 주 한 줄 요약", f"<p class='lead'>{_escape(summary)}</p>")

def render_opportunity(other: Dict) -> str:
    topk = other.get('topk_comparison') or other.get('topk') or other.get('new_tags_topk') or []
    if not topk:
        return section("🚀 이번 주 인스타그램 해시태그 동향", "<p class='lead'>데이터가 없습니다.</p>")
    blocks = ""
    for item in topk[:10]:
        tag = item.get('hashtag') or item.get('tag') or ''
        recent = item.get('count_recent') if item.get('count_recent') is not None else item.get('count','')
        old = item.get('count_old','')
        pct = item.get('pct_change')
        pct_html = ""
        if pct is not None:
            sign = "+" if pct > 0 else ""
            pct_html = f"<span style='margin-left:8px;color:{'#168a39' if pct>0 else '#b93a3a'};font-weight:700'>{sign}{round(pct,1)}%</span>"
        blocks += (
            f"<div class='rec-item'>"
            f"<span class='hashtag-pill'>{_escape(tag)}</span>"
            f"<div class='muted' style='margin-top:6px'>recent: {_escape(recent)} (old: {_escape(old)}) {pct_html}</div>"
            f"</div>"
        )
    return section("🚀 이번 주 인스타그램 해시태그 동향", f"<div class='grid'>{blocks}</div>")


def render_youtube_trends(other: Dict, agent: Dict = None) -> str:
    products = other.get('youtube_products') 
    if not products and agent:
        products = agent.get('instagram_trend', {}).get('youtube_products')
    
    if not products:
        return ""
    
    cards = ""
    for idx, p in enumerate(products[:4], 1):
        name = p.get('product') or 'Unknown'
        url = p.get('url') or '#'
        desc = p.get('features') or '상세 정보 분석 중'
        count = p.get('count') or '-'
        image = p.get('image') or ''
        
        quality = p.get('quality') or ''
        formulation = p.get('formulation') or ''
        ingredients = p.get('ingredients_snippet') or ''
        
        if image:
            thumb_html = f"<div class='product-thumb'><img src='{_escape(image)}' alt='thumb' /></div>"
        else:
            thumb_html = "<div class='product-thumb' style='background:#f0f0f0; color:#999; font-size:12px; text-align:center;'>이미지<br>준비중</div>"

        detail_items = []
        if quality:
            detail_items.append(f"<div style='margin-bottom:6px;'><strong style='color:#666; font-size:11px;'>품질:</strong> <span style='font-size:12px; color:#0b1220;'>{_escape(quality)}</span></div>")
        if formulation:
            detail_items.append(f"<div style='margin-bottom:6px;'><strong style='color:#666; font-size:11px;'>제형:</strong> <span style='font-size:12px; color:#0b1220;'>{_escape(formulation)}</span></div>")
        if ingredients:
            ingredients_short = ingredients[:100] + "..." if len(ingredients) > 100 else ingredients
            detail_items.append(f"<div style='margin-bottom:6px;'><strong style='color:#666; font-size:11px;'>성분:</strong> <span style='font-size:12px; color:#0b1220; line-height:1.4;'>{_escape(ingredients_short)}</span></div>")
        
        detail_html = "".join(detail_items) if detail_items else "<div style='font-size:12px; color:#999;'>상세 정보 수집 중</div>"

        cards += f"""
        <div class='card product-card'>
            {thumb_html}
            <div class='product-info'>
                <div style='margin-bottom:8px; display:flex; gap:8px; align-items:center; flex-wrap:wrap;'>
                    <span style='background:#FF0000; color:#fff; padding:3px 8px; border-radius:10px; font-size:11px; font-weight:700;'>YouTube Hot</span>
                    <span style='background:#f0f0f0; color:#666; padding:3px 8px; border-radius:10px; font-size:11px; font-weight:600;'>#{idx}</span>
                    <span style='color:#999; font-size:12px;'>언급 {_escape(count)}회</span>
                </div>
                
                <div class='product-title' style='font-size:15px; margin-bottom:10px;'>{_escape(name)}</div>
                
                <div style='margin-bottom:10px; padding:10px; background:#f8f9fa; border-radius:6px; border-left:3px solid #FF6B4A;'>
                    <div style='font-size:11px; color:#666; font-weight:600; margin-bottom:8px;'>📋 제품 정보</div>
                    {detail_html}
                </div>
                
                <a href='{_escape(url)}' target='_blank' style='display:inline-block; font-size:12px; color:#FF6B4A; font-weight:700; text-decoration:none; padding:6px 12px; background:#fff5f2; border-radius:6px; border:1px solid #ffd4c4;'>
                    제품 상세보기 →
                </a>
            </div>
        </div>
        """
    
    return section("🎥 유튜브 제품 트렌드", f"<div class='grid'>{cards}</div>")

def render_recent_products(other: Dict, products: Optional[List[Dict]] = None) -> str:
    if products is None:
        products = other.get('recent_products') or other.get('youtube_products') or other.get('products') or []
    if not products:
        return ""
    cards = ""
    for p in products[:2]:
        name = p.get('product') or p.get('name') or 'Unknown product'
        url = p.get('url') or p.get('link') or ''
        quality = p.get('quality') or ''
        ing = p.get('ingredients_snippet') or p.get('ingredients') or ''
        image = p.get('image') or p.get('image_url') or ''
        thumb_html = ""
        if image:
            thumb_html = f"<div class='product-thumb'><img src='{_escape(image)}' alt='thumb' /></div>"
        elif url and '//' in url:
            domain = url.split('/')[2]
            fav = f"https://www.google.com/s2/favicons?domain={_escape(domain)}"
            thumb_html = f"<div class='product-thumb'><img src='{_escape(fav)}' alt='fav' /></div>"
        else:
            thumb_html = "<div class='product-thumb'></div>"
        link_start = f"<a href='{_escape(url)}' target='_blank'>" if url else ""
        link_end = "</a>" if url else ""
        info_html = (
            f"<div class='product-info'>"
            f"{link_start}<div class='product-title'>{_escape(name)}</div>{link_end}"
            f"<div class='muted'>{_escape(quality)}</div>"
            f"<div class='tokens'>{_escape((ing or '')[:260])}</div>"
            f"</div>"
        )
        cards += f"<div class='card product-card'>{thumb_html}{info_html}</div>"
    return section("🔥 최근 화제의 제품 (Oliveyoung 링크 우선)", f"<div class='grid'>{cards}</div>")

def render_category_recs(agent: Dict) -> str:
    agg = agent.get('aggregate') or {}
    sample_recs = agg.get('category_sample_recs') or []
    if not sample_recs:
        return ""

    cards = ""
    for s in sample_recs[:8]:
        text = s if isinstance(s, str) else str(s)
        
        title = text.split(":")[0].strip()
        
        token_part = ""
        if "top_tokens=" in text:
            token_part = text.split("top_tokens=")[1].split(", auto_rec=")[0].strip()
        
        auto_rec_part = ""
        if 'auto_rec="' in text:
            auto_rec_part = text.split('auto_rec="')[1].rstrip(' "')
        elif "auto_rec='" in text:
            auto_rec_part = text.split("auto_rec='")[1].rstrip(" '")

        cards += f"""
        <div class='rec-item'>
            <div style='font-weight: bold; font-size: 1.1em; margin-bottom: 8px;'>{_escape(title)}</div>
            <div style='color: #666; font-size: 0.9em; margin-bottom: 4px;'><strong>Tokens:</strong> {_escape(token_part)}</div>
            <div style='margin-top: 8px; line-height: 1.4;'>{_escape(auto_rec_part)}</div>
        </div>
        """

    final_two = agg.get('final_two_line_suggestion') or ""
    footer = f"<div class='section-footer'><strong>요약 제안:</strong> {_escape(final_two)}</div>" if final_two else ""
    
    return section("⚠️ 리스크 & 이슈 신호", f"<div class='grid'>{cards}</div>{footer}")


def _render_country_card_from_summary(code: str, summary: Dict, weekly_ctx: Dict) -> str:
    if not summary:
        return ""
    country_name = summary.get('country_name') or code.upper()
    total_products = summary.get('total_products') or summary.get('total', '')
    categories = summary.get('categories') or {}
    brands = summary.get('brands') or {}
    top_ingredients = summary.get('top_ingredients') or []
    top_textures = summary.get('top_textures') or []
    top_product_types = summary.get('top_product_types') or []
    top_features = summary.get('top_features') or []
    top_benefits = summary.get('top_benefits') or []
    rag_ctx = (weekly_ctx or {}).get('rag_context') or {}
    llm_parsed = (weekly_ctx or {}).get('llm_parsed') or {}

    one_line = ""
    if isinstance(rag_ctx, dict):
        one_line = rag_ctx.get('weekly_one_line_summary') or ""
    if not one_line and isinstance(weekly_ctx, dict):
        one_line = weekly_ctx.get('summary_top1') or ""

    def _format_stat_items(items, item_type="", limit=5):
        if not items:
            return ""
        html = ""
        for it in items[:limit]:
            if isinstance(it, dict):
                if 'ingredient' in it:
                    k = it.get('ingredient')
                    v = it.get('count', '')
                    html += f"<div class='stat-item ingredient'><span>{_escape(k)}</span><span class='stat-item-value'>{_escape(v)}</span></div>"
                elif 'texture' in it:
                    k = it.get('texture')
                    v = it.get('count', '')
                    html += f"<div class='stat-item texture'><span>{_escape(k)}</span><span class='stat-item-value'>{_escape(v)}</span></div>"
                elif 'product_type' in it:
                    k = it.get('product_type')
                    v = it.get('count', '')
                    html += f"<div class='stat-item type'><span>{_escape(k)}</span><span class='stat-item-value'>{_escape(v)}</span></div>"
                elif 'feature' in it:
                    k = it.get('feature')
                    v = it.get('count', '')
                    html += f"<div class='stat-item feature'><span>{_escape(k)}</span><span class='stat-item-value'>{_escape(v)}</span></div>"
                elif 'benefit' in it:
                    k = it.get('benefit')
                    v = it.get('count', '')
                    html += f"<div class='stat-item benefit'><span>{_escape(k)}</span><span class='stat-item-value'>{_escape(v)}</span></div>"
                else:
                    ks = list(it.keys())
                    k = ks[0] if ks else str(it)
                    v = it.get(ks[0], '')
                    html += f"<div class='stat-item'><span>{_escape(k)}</span><span class='stat-item-value'>{_escape(v)}</span></div>"
            elif isinstance(it, (list, tuple)) and len(it) >= 2:
                html += f"<div class='stat-item'><span>{_escape(it[0])}</span><span class='stat-item-value'>{_escape(it[1])}</span></div>"
            else:
                html += f"<div class='stat-item'><span>{_escape(str(it))}</span></div>"
        return html

    cat_html = ""
    if categories:
        top_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]
        cat_items = "".join(f"<div class='stat-item'><span>{_escape(k)}</span><span class='stat-item-value'>{_escape(v)}</span></div>" for k,v in top_cats)
        cat_html = f"<div class='info-card categories'><div class='info-card-header'>카테고리 (Top5)</div>{cat_items}</div>"

    brand_html = ""
    if brands:
        top_brands = sorted(brands.items(), key=lambda x: x[1], reverse=True)[:5]
        brand_items = "".join(f"<div class='stat-item'><span>{_escape(k)}</span><span class='stat-item-value'>{_escape(v)}</span></div>" for k,v in top_brands)
        brand_html = f"<div class='info-card brands'><div class='info-card-header'>주요 브랜드 (Top5)</div>{brand_items}</div>"

    total_card = f"<div class='total-products-card'><span class='badge'>총 제품수</span><strong>{_escape(total_products)}</strong></div>"

    cards_html = ""
    
    if top_ingredients:
        items = _format_stat_items(top_ingredients, "ingredient", 5)
        cards_html += f"<div class='info-card ingredients'><div class='info-card-header'>주요 성분</div>{items}</div>"
    
    if top_textures:
        items = _format_stat_items(top_textures, "texture", 5)
        cards_html += f"<div class='info-card textures'><div class='info-card-header'>주요 텍스처</div>{items}</div>"
    
    if top_product_types:
        items = _format_stat_items(top_product_types, "type", 5)
        cards_html += f"<div class='info-card types'><div class='info-card-header'>제품 타입</div>{items}</div>"
    
    if top_features:
        items = _format_stat_items(top_features, "feature", 5)
        cards_html += f"<div class='info-card features'><div class='info-card-header'>주요 특징</div>{items}</div>"
    
    if top_benefits:
        items = _format_stat_items(top_benefits, "benefit", 5)
        cards_html += f"<div class='info-card benefits'><div class='info-card-header'>주요 효능</div>{items}</div>"

    neg_tokens = rag_ctx.get('negative_tokens') if isinstance(rag_ctx, dict) else []
    neg_html = ""
    if neg_tokens:
        badges = ""
        for t in neg_tokens[:6]:
            if isinstance(t, (list,tuple)) and len(t) >= 2:
                badges += f"<span class='neg-token'>{_escape(t[0])} ({_escape(t[1])})</span>"
        if badges:
            neg_html = f"<div class='info-card negative'><div class='info-card-header'>부정 신호 토큰</div><div style='margin-top:8px'>{badges}</div></div>"

    parsed_html = ""
    if isinstance(llm_parsed, dict):
        insights = llm_parsed.get('insights') or []
        if insights:
            parsed_html += "<div class='info-card insights'><div class='info-card-header'>주요 분석 결과</div>"
            for ins in insights[:3]:
                title = ins.get('title') or ''
                rec = ins.get('recommendation') or ''
                parsed_html += f"<div style='margin-top:12px;padding:12px;background:#f8fafc;border-radius:6px'><strong style='display:block;margin-bottom:6px;color:#0b1220'>{_escape(title)}</strong><div class='small-muted'>{_escape(rec)}</div></div>"
            parsed_html += "</div>"

    block = "<div class='country-hero card'>"
    block += "<div class='country-header'>"
    block += f"<div><div class='country-title'>{_escape(country_name)}</div><div class='country-summary small-muted' style='margin-top:6px'>Top categories & ingredients at a glance</div></div>"
    if one_line:
        block += f"<div style='flex:1;min-width:200px;max-width:100%'><div class='insight-box'><strong>주간 인사이트</strong><div class='small-muted' style='margin-top:6px'>{_escape(one_line)}</div></div></div>"
    else:
        block += "<div></div>"
    block += "</div>"

    block += "<div class='country-body'>"
    block += total_card
    if cat_html:
        block += cat_html
    if brand_html:
        block += brand_html
    block += cards_html
    if neg_html:
        block += neg_html
    if parsed_html:
        block += parsed_html
    block += "</div>"
    block += "</div>"

    return block

def render_country_cards(agent: Dict) -> str:
    parts = []
    product_summaries = agent.get('product_summaries') or agent.get('product_summary') or {}
    weekly_all = agent.get('weekly_insights_all') or agent.get('weekly_insights') or {}
    per_country_weekly = {}
    if isinstance(weekly_all, dict):
        per_country_weekly = weekly_all.get('per_country') or {}

    for code in ['usa', 'china', 'japan']:
        summary = product_summaries.get(code) or {}
        weekly_ctx = per_country_weekly.get(code) or {}
        if summary:
            parts.append(_render_country_card_from_summary(code, summary, weekly_ctx))

    if not parts:
        return ""
    inner = "<div class='grid country-grid'>" + "".join(parts) + "</div>"
    return section("🌐 국가별 상세 요약 (미국 / 중국 / 일본)", inner)

def render_agent_insights(agent: Dict) -> str:
    parts = []
    weekly_all = agent.get('weekly_insights_all') or agent.get('weekly_insights') or {}
    if isinstance(weekly_all, dict):
        comparison = weekly_all.get('comparison_with_llm_insights') or weekly_all.get('comparison') or agent.get('comparison_deterministic') or {}
        llm_insight = comparison.get('llm_insight') or comparison.get('common') or ""
        if llm_insight:
            parts.append(f"<div class='card'><strong>종합 인사이트(요약)</strong><p class='lead'>{_escape(llm_insight)}</p></div>")

    per_country = (weekly_all.get('per_country') if isinstance(weekly_all, dict) else {}) or {}
    for code, ctx in per_country.items():
        parsed_ctx = ctx.get('llm_parsed') or {}
        insights = parsed_ctx.get('insights') or []
        for ins in insights[:2]:
            title = ins.get('title') or ''
            rec = ins.get('recommendation') or ''
            tokens = ins.get('evidence', {}).get('tokens') if isinstance(ins.get('evidence'), dict) else None
            token_line = ""
            if tokens:
                top_tokens = ", ".join([f"{t[0]}({t[1]})" for t in tokens[:6]])
                token_line = f"<div class='tokens'>Top tokens: {_escape(top_tokens)}</div>"
            parts.append(f"<div class='card'><strong>{_escape(title)}</strong><p class='lead'>{_escape(str(rec))}</p>{token_line}</div>")

    if not parts and isinstance(agent.get('llm_parsed'), dict):
        insights = agent.get('llm_parsed', {}).get('insights') or []
        for ins in insights[:6]:
            title = ins.get('title') or "인사이트"
            rec = ins.get('recommendation') or ""
            tokens = ins.get('evidence', {}).get('tokens') if isinstance(ins.get('evidence'), dict) else None
            token_line = ""
            if tokens:
                top_tokens = ", ".join([f"{t[0]}({t[1]})" for t in tokens[:6]])
                token_line = f"<div class='tokens'>Top tokens: {_escape(top_tokens)}</div>"
            parts.append(f"<div class='card'><strong>{_escape(title)}</strong><p class='lead'>{_escape(str(rec))}</p>{token_line}</div>")

    if not parts:
        return ""
    return section("🔎 에이전트 인사이트 (주요)", f"<div class='grid'>{''.join(parts)}</div>")

def render_country_comparison(agent: Dict) -> str:
    weekly_all = agent.get('weekly_insights_all') or agent.get('weekly_insights') or {}
    comparison = weekly_all.get('comparison_with_llm_insights') or weekly_all.get('comparison') or {}
    llm_insight = comparison.get('llm_insight') or comparison.get('summary') or comparison.get('common') or ""
    if not llm_insight:
        return ""
    inner = f"<div class='card'><p class='lead'>{_escape(llm_insight)}</p></div>"
    return section("🌍 국가 간 종합 인사이트", inner)

def render_full(agent: Dict, other: Dict, products: Optional[List[Dict]] = None, use_cid: bool = True, logo_data_uri: Optional[str] = None) -> str:
    """
    Compose the full newsletter HTML content by assembling sections.
    Matches the expected signature used by builder.build_newsletter(...)
    """
    week_range = agent.get('week_range') or other.get('file_recent') or ""
    week_display = week_range or datetime.now().strftime("%Y.%m.%d")
    try:
        if "~" in str(week_range):
            parts = [p.strip() for p in week_range.split("~")]
            end = parts[-1]
            end_date = datetime.fromisoformat(end)
            iso = end_date.isocalendar()
            week_display = f"{iso[0]}년 {iso[1]}주차 ({week_range})"
    except Exception:
        pass

    parts = []
    parts.append(render_greeting(agent))
    parts.append(render_summary(agent))
    parts.append(render_opportunity(other))
    parts.append(render_youtube_trends(other))
    parts.append(render_country_cards(agent))
    parts.append(render_category_recs(agent))
    parts.append(render_country_comparison(agent))

    content = "\n".join([p for p in parts if p])
    file_label = other.get('file_recent') or ""
    return base_template(
        week_label=week_range or "",
        week_display=week_display,
        content=content,
        title="Amorepacific Weekly",
        use_cid=use_cid,
        logo_cid="amore_logo",
        logo_data_uri=logo_data_uri,
        file_label=file_label
    )