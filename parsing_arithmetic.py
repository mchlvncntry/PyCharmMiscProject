# without parentheses
import re, requests
from bs4 import BeautifulSoup

def calculate(expression):
    if len(expression) == 1:
        return expression
    else:
        answer = 0
        if expression[1] == "+":
            answer = int(expression[0]) + int(expression[2])
        elif expression[1] == "*":
            answer = int(expression[0]) * int(expression[2])
        print("expression", expression)
        print("answer", answer)

        new_expression  = [str(answer)]
        for e in expression[3:]:
            new_expression.append(e)
    return calculate(new_expression)

def calc_parens(expr):
    """Evaluate + and * with equal precedence, left-to-right, supporting parentheses."""
    expr = expr.strip()

    # Base case: no parentheses left
    if '(' not in expr:
        tokens = expr.split()
        result = int(tokens[0])
        i = 1
        while i < len(tokens):
            op, val = tokens[i], int(tokens[i + 1])
            if op == '+':
                result += val
            elif op == '*':
                result *= val
            i += 2
        return result

    # Recursive case: find innermost parentheses
    left = expr.rfind('(')
    right = expr.find(')', left)
    inside = expr[left + 1:right]

    # Evaluate what’s inside
    inner_value = calc_parens(inside)

    # Replace "( ... )" with its result and recurse again
    new_expr = expr[:left] + str(inner_value) + expr[right + 1:]
    return calc_parens(new_expr)

def extract_expressions(url: str) -> list[str]:
    """Fetch page text and extract arithmetic lines with +, *, and parentheses."""
    html = requests.get(url, timeout=15).text
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text("\n")

    lines = [ln.strip() for ln in text.splitlines()]
    exprs = []
    for ln in lines:
        if re.match(r'^[\d\s+*()]+$', ln) and any(op in ln for op in ['+', '*']):
            exprs.append(" ".join(ln.split()))  # normalize spaces
    return exprs


if __name__ == "__main__":
    url = "https://www.samsclass.info/COMSC132/proj/VP29"
    expressions = extract_expressions(url)

    total = 0
    for e in expressions:
        val = calc_parens(e)
        print(f"{e} => {val}")
        total += val

    print("-" * 40)
    print(f"Grand total = {total}")
