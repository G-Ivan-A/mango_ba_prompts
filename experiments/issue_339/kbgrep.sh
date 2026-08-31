#!/bin/bash
# Поиск по всем разделам БЗ: выводит doc/section и совпадение
grep -rniE "$1" kb/processed/*/sections/*.md kb/processed/*/*/sections/*.md 2>/dev/null | sed 's#kb/processed/##' | cut -c1-260
