from __future__ import annotations
import argparse
import sys

def add(a: float, b: float) -> float:
    return a + b

def subtract(a: float, b: float) -> float:
    return a - b

def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Simple add/subtract CLI")
    sub = p.add_subparsers(dest="cmd", required=False)

    pa = sub.add_parser("add", help="Add two numbers")
    pa.add_argument("a", type=float)
    pa.add_argument("b", type=float)

    ps = sub.add_parser("sub", help="Subtract two numbers (a - b)")
    ps.add_argument("a", type=float)
    ps.add_argument("b", type=float)

    p.add_argument("--expr", help="Simple expression like '2 + 3' or '5 - 1'")

    args = p.parse_args(argv[1:])

    if args.expr:
        try:
            parts = args.expr.split()
            if len(parts) == 3:
                a = float(parts[0])
                op = parts[1]
                b = float(parts[2])
                if op == "+":
                    print(add(a, b))
                    return 0
                if op == "-":
                    print(subtract(a, b))
                    return 0
            print("Invalid expression. Use format: <num> <+|-> <num>")
            return 2
        except Exception as e:
            print(f"Error parsing expression: {e}")
            return 3

    if args.cmd == "add":
        print(add(args.a, args.b))
        return 0
    if args.cmd == "sub":
        print(subtract(args.a, args.b))
        return 0

    # If no args provided, show brief interactive prompt
    try:
        s = input("Enter operation (e.g. 2 + 3) or blank to exit: ").strip()
        if not s:
            return 0
        parts = s.split()
        a = float(parts[0]); op = parts[1]; b = float(parts[2])
        if op == "+":
            print(add(a, b))
        elif op == "-":
            print(subtract(a, b))
        else:
            print("Unsupported operator. Use + or -.")
            return 2
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 3

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))