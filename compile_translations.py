#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Compile .po files to .mo files using polib
"""
import polib
import os

def compile_po_to_mo(po_file, mo_file):
    """Compile .po file to .mo file using polib"""
    try:
        po = polib.pofile(po_file, encoding='utf-8')
        po.save_as_mofile(mo_file)
        print(f'✓ Compiled {po_file} -> {mo_file}')
        print(f'  Total entries: {len(po)}')
        print(f'  Translated: {len(po.translated_entries())}')
        print(f'  Untranslated: {len(po.untranslated_entries())}')
        return True
    except Exception as e:
        print(f'✗ Error compiling {po_file}: {e}')
        return False

if __name__ == '__main__':
    success_count = 0
    fail_count = 0
    
    # Compile Hindi
    po_file_hi = 'locale/hi/LC_MESSAGES/django.po'
    mo_file_hi = 'locale/hi/LC_MESSAGES/django.mo'
    
    if os.path.exists(po_file_hi):
        if compile_po_to_mo(po_file_hi, mo_file_hi):
            success_count += 1
        else:
            fail_count += 1
            print()
    else:
        print(f'✗ Error: {po_file_hi} not found\n')
    
    # Compile Marathi
    po_file_mr = 'locale/mr/LC_MESSAGES/django.po'
    mo_file_mr = 'locale/mr/LC_MESSAGES/django.mo'
    
    if os.path.exists(po_file_mr):
        if compile_po_to_mo(po_file_mr, mo_file_mr):
            success_count += 1
        else:
            fail_count += 1
            print()
    else:
        print(f'✗ Error: {po_file_mr} not found\n')
    
    if success_count > 0:
        print(f'\n✓ Translation compilation successful! ({success_count} language(s))')
    if fail_count > 0:
        print(f'✗ {fail_count} language(s) failed!')
