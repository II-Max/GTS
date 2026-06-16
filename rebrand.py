import os
import glob
import re

def rebrand():
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    html_files = glob.glob(os.path.join(frontend_dir, '*.html'))
    
    replacements = [
        # Title patterns
        (r'<title>NEO Online Judge —', r'<title>GTS (Go to Success) —'),
        (r'content="NEO Online Judge - Hệ thống', r'content="GTS (Go to Success) - Hệ thống'),
        (r'content=".*? NEO Online Judge.*?"', lambda m: m.group(0).replace('NEO Online Judge', 'GTS (Go to Success)')),
        
        # Navigation brand and logos
        (r'<span class="brand-dot"></span>NEO<span style="color:var\(--text-secondary\)">OJ</span>', r'<span class="brand-dot"></span>GTS'),
        (r'<div class="auth-brand">NEO<span>OJ</span></div>', r'<div class="auth-brand">GTS<span>.</span></div>'),
        (r'<div class="gateway-logo">\s*NEO<span>OJ</span>\s*</div>', r'<div class="gateway-logo">GTS<span>.</span></div>'),
        
        # Introduction text
        (r'NEO Online Judge là nền tảng', r'GTS (Go to Success) là nền tảng'),
        (r'NEO Online Judge', r'GTS (Go to Success)'),
        (r'NEOOJ', r'GTS'),
        (r'NEO Judge', r'GTS'),
        (r'NEO OJ', r'GTS'),
    ]
    
    for filepath in html_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = content
        for pattern, replacement in replacements:
            if callable(replacement):
                new_content = re.sub(pattern, replacement, new_content)
            else:
                new_content = re.sub(pattern, replacement, new_content)
                
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {os.path.basename(filepath)}")

    # Update README and Docs
    md_files = glob.glob(os.path.join(os.path.dirname(__file__), '*.md'))
    for filepath in md_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = content
        new_content = new_content.replace('NEO ONLINE JUDGE', 'GTS (GO TO SUCCESS)')
        new_content = new_content.replace('NEO Online Judge', 'GTS (Go to Success)')
        new_content = new_content.replace('NEO OJ', 'GTS')
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {os.path.basename(filepath)}")

if __name__ == '__main__':
    rebrand()
