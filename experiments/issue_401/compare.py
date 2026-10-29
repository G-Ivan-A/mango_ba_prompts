"""Reproducible normalized token comparison; no semantic equivalence claims."""
from difflib import SequenceMatcher
import re
import unicodedata


def tokens(text):
    text = re.sub(r'(?<=\w)-\s*\n\s*(?=\w)', '', text)
    text = unicodedata.normalize('NFKC', text).replace('\u00ad', '').lower().replace('ё', 'е')
    return re.findall(r'[^\W_]+', text, re.UNICODE)


def text_difference(pdf_text, web_text):
    a, b = tokens(pdf_text), tokens(web_text)
    if not a or not b:
        return {'pdf_tokens': len(a), 'web_tokens': len(b), 'matched_tokens': 0,
                'difference_pct': None if not a else 100.0, 'changes': []}
    matcher = SequenceMatcher(None, a, b, autojunk=False)
    changes = [{'kind': op, 'pdf_start': i, 'pdf_end': j, 'web_start': k, 'web_end': l,
                'pdf_tokens': j-i, 'web_tokens': l-k}
               for op, i, j, k, l in matcher.get_opcodes() if op != 'equal']
    matched = sum(m.size for m in matcher.get_matching_blocks())
    return {'pdf_tokens': len(a), 'web_tokens': len(b), 'matched_tokens': matched,
            'difference_pct': 100 * (1 - 2 * matched / (len(a) + len(b))), 'changes': changes}


def ssot_decision(differences):
    if any(v is None for v in differences):
        return 'combined-required-unverified'
    return 'combined-required' if any(v > 5 for v in differences) else 'web-eligible-for-reference-product'
