#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup


# ---------------- Core evaluators ----------------

def _eval_add_before_mul_no_parens(expr: str) -> int:
    """
    Evaluate an expression with only + and * (no parentheses),
    where ADDITION has higher precedence than MULTIPLICATION.
    Example flow: 1 + 2 * 3 + 4 * 5 + 6
      -> (1+2) * (3+4) * (5+6) in effect of precedence folding
    Implementation: first fold all additions left-to-right into numbers,
    then multiply the remaining numbers.
    """
    tokens = expr.split()
    if not tokens:
        raise ValueError("Empty expression")

    # First pass: collapse additions into single numbers
    # Keep a stack of tokens; when we see '+', fold stack[-1] + next number
    stack: list[str] = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok == '+':
            # fold previous number with next number
            if not stack:
                raise ValueError(f"Unexpected '+' at start in {expr!r}")
            a = int(stack.pop())
            if i + 1 >= len(tokens):
                raise ValueError(f"Trailing '+' in {expr!r}")
            b = int(tokens[i + 1])
            stack.append(str(a + b))
            i += 2
        else:
            stack.append(tok)
            i += 1

    # Second pass: multiply the remaining numbers (tokens are numbers and '*')
    result = 1
    for tok in stack:
        if tok == '*':
            continue
        result *= int(tok)
    return result


def calc_parens(expr: str) -> int:
    """
    Evaluate + and * with custom precedence:
      - ADDITION before MULTIPLICATION
      - Parentheses handled from innermost outward
    """
    expr = expr.strip()

    # Reduce innermost parentheses repeatedly
    while '(' in expr:
        left = expr.rfind('(')
        right = expr.find(')', left)
        if right == -1:
            raise ValueError(f"Unmatched '(' in {expr!r}")
        inside = expr[left + 1:right].strip()
        value = _eval_add_before_mul_no_parens(inside)
        expr = expr[:left] + str(value) + expr[right + 1:]

    # Final pass: no parentheses remain
    return _eval_add_before_mul_no_parens(expr)


# ---------------- Extraction ----------------

def extract_expressions(url: str) -> list[str]:
    """Fetch page text and extract arithmetic lines with +, *, and parentheses."""
    html = requests.get(url, timeout=15).text
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text("\n")

    lines = [ln.strip() for ln in text.splitlines()]
    exprs: list[str] = []
    for ln in lines:
        # keep lines that are only digits/space/+/*/parens and contain at least one operator
        if re.match(r'^[\d\s+*()]+$', ln) and any(op in ln for op in ['+', '*']):
            exprs.append(" ".join(ln.split()))  # normalize spaces
    return exprs


# ---------------- Demo / main ----------------

if __name__ == "__main__":
    # Quick sanity check with your example:
    example = "1 + 2 * 3 + 4 * 5 + 6"
    print(example, "=>", calc_parens(example))  # should print 231 per your steps

    url = "https://www.samsclass.info/COMSC132/proj/VP29"
    expressions = extract_expressions(url)

    total = 0
    for e in expressions:
        val = calc_parens(e)
        print(f"{e} => {val}")
        total += val

    print("-" * 40)
    print(f"Grand total = {total}")
