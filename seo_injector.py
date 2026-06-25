#!/usr/bin/env python3
import os
import sys
import glob
import re

def inject_blackhat(html_content):
    # 1. Hidden Text Divs (200 words)
    keywords = "best IPTV, 4K IPTV, IPTV USA, IPTV UK, cheap subscription, " * 40
    hidden_div = f'\n<!-- Black-Hat: Hidden Keywords -->\n<div style="display:none; color:#121315; font-size:0px;">{keywords}</div>\n'
    
    # 2. Cloaking for Bots (Redirecting bots that do not execute JS)
    cloaking_meta = '\n<!-- Black-Hat: Bot Cloaking -->\n<noscript><meta http-equiv="refresh" content="0; url=/landing.html"></noscript>\n'
    
    # 3. Off-Screen PBN Links
    pbn_links = '\n<!-- Black-Hat: PBN Backlinks -->\n<div class="pbn-links">'
    for i in range(1, 6):
        pbn_links += f'<a href="http://pbn-{i}.com" style="position:absolute; left:-9999px;" rel="dofollow">best iptv</a>'
    pbn_links += '</div>\n'
    
    # 4. Keyword Stuffing (Natural-looking dense paragraph at the end of article bodies)
    stuffing = '\n<!-- Black-Hat: Keyword Stuffing -->\n<p style="opacity: 0.1; font-size: 10px;">When looking for IPTV, the best IPTV service provides IPTV channels in 4K IPTV quality. An IPTV subscription gives you cheap IPTV access. IPTV USA and IPTV UK offer premium IPTV content. Enjoy live streaming with sports IPTV using the top IPTV provider. IPTV is the future of TV. Buy IPTV, setup IPTV, and watch IPTV anywhere. IPTV, IPTV, IPTV.</p>\n'
    
    # Apply Injections
    if '</head>' in html_content:
        html_content = html_content.replace('</head>', f'{cloaking_meta}</head>')
    
    if '</body>' in html_content:
        # Inject at the very end of the body
        html_content = html_content.replace('</body>', f'{hidden_div}{pbn_links}</body>')
        
    if '</article>' in html_content:
        # Inject stuffing at the end of article content
        html_content = html_content.replace('</article>', f'{stuffing}</article>')
        
    return html_content

def inject_greyhat(html_content):
    # 1. Footer Keyword List (same color as background #121315)
    footer_keywords = "IPTV, 4K IPTV, Live TV, Sports IPTV, VOD, Netflix, Hulu alternative, Cord cutting, Firestick IPTV, Android TV, Smart TV IPTV, Apple TV, Cheap IPTV, Best IPTV 2026, USA IPTV, UK IPTV, Canada IPTV, Premium IPTV, IPTV provider, Reseller IPTV, M3U playlist, Xtream Codes" * 5
    grey_footer = f'\n<!-- Grey-Hat: Hidden Footer Keywords -->\n<div style="color: #121315; font-size: 10px; text-align: justify; padding: 20px; background: #121315;">{footer_keywords}</div>\n'
    
    # 2. Outbound Links to Authority Sites
    authority_links = '\n<!-- Grey-Hat: Authority Outbound Links -->\n<div style="display:none;"><a href="https://en.wikipedia.org/wiki/Internet_Protocol_television" rel="nofollow">Learn about IPTV technology on Wikipedia</a> | <a href="https://www.bbc.co.uk/news/technology" rel="nofollow">Technology News on BBC</a> | <a href="https://edition.cnn.com/business/tech" rel="nofollow">CNN Tech</a></div>\n'
    
    if '</footer>' in html_content:
        html_content = html_content.replace('</footer>', f'{grey_footer}{authority_links}</footer>')
    elif '</body>' in html_content:
        html_content = html_content.replace('</body>', f'{grey_footer}{authority_links}</body>')
        
    return html_content

def process_directory(directory):
    html_files = glob.glob(os.path.join(directory, "**/*.html"), recursive=True)
    count = 0
    
    for filepath in html_files:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        content = inject_blackhat(content)
        content = inject_greyhat(content)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        count += 1
        
    print(f"Black-hat/Grey-hat injections completed on {count} files.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 seo_injector.py <output_directory>")
        sys.exit(1)
        
    output_dir = sys.argv[1]
    if not os.path.exists(output_dir):
        print(f"Directory {output_dir} does not exist.")
        sys.exit(1)
        
    process_directory(output_dir)
