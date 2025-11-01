"""
Verify 4-Combo Strategy
Verifies the 4-number combination tracking matches actual results

This script:
1. Loads all historical draws
2. Extracts all 4-number combinations from draws
3. Calculates which 4-combos remain undrawn
4. Shows statistics to verify HTML app calculations

Usage:
python verify_4combo_strategy.py a_649.txt
"""

import sys
import itertools
from datetime import datetime

MAX = 49
MAX_PLAY = 6
TOTAL_4_COMBOS = 211876  # C(49,4)

def get_4combos_from_6(numbers):
    """Get all 4-number combinations from a 6-number draw"""
    combos = []
    for combo in itertools.combinations(numbers, 4):
        combos.append(tuple(sorted(combo)))
    return combos

def load_draws(filename):
    """Load draws from a_649.txt format"""
    draws = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Parse: YYMMDD:  n1, n2, n3, n4, n5, n6 / bonus
                if ':' in line:
                    parts = line.split(':')[1].split('/')
                    nums_part = parts[0].strip()
                    
                    numbers = []
                    for num_str in nums_part.split(','):
                        num_str = num_str.strip()
                        if num_str.isdigit():
                            num = int(num_str)
                            if 1 <= num <= MAX:
                                numbers.append(num)
                    
                    if len(numbers) == MAX_PLAY:
                        draws.append(tuple(sorted(numbers)))
        
        return draws
        
    except FileNotFoundError:
        print(f"Error: File {filename} not found")
        return []
    except Exception as e:
        print(f"Error loading draws: {e}")
        return []

def analyze_4combos(draws):
    """Analyze 4-number combination coverage"""
    drawn_4combos = set()
    
    print(f"Analyzing {len(draws)} draws...")
    print(f"Each draw contains C(6,4) = 15 four-number combinations\n")
    
    for i, draw in enumerate(draws, 1):
        combos = get_4combos_from_6(draw)
        drawn_4combos.update(combos)
        
        if i % 500 == 0 or i == len(draws):
            print(f"Processed {i:5d} draws | "
                  f"Drawn 4-combos: {len(drawn_4combos):6d} | "
                  f"Remaining: {TOTAL_4_COMBOS - len(drawn_4combos):6d}")
    
    return drawn_4combos

def verify_totals(drawn_4combos, total_draws):
    """Verify and display statistics"""
    drawn_count = len(drawn_4combos)
    remaining_count = TOTAL_4_COMBOS - drawn_count
    coverage_percent = (drawn_count / TOTAL_4_COMBOS) * 100
    
    print(f"\n{'='*60}")
    print("4-NUMBER COMBINATION ANALYSIS")
    print(f"{'='*60}")
    print(f"Total possible 4-combos:  {TOTAL_4_COMBOS:,}")
    print(f"Total draws analyzed:     {total_draws:,}")
    print(f"Total 4-combos drawn:     {drawn_count:,}")
    print(f"Remaining 4-combos:       {remaining_count:,}")
    print(f"Coverage:                 {coverage_percent:.2f}%")
    print(f"{'='*60}")
    
    # Calculate theoretical maximum
    max_possible = total_draws * 15  # Each draw has 15 four-combos
    overlap = max_possible - drawn_count
    overlap_percent = (overlap / max_possible) * 100
    
    print(f"\nOverlap Analysis:")
    print(f"Max possible (if no overlap): {max_possible:,}")
    print(f"Actual drawn:                 {drawn_count:,}")
    print(f"Overlap (reused 4-combos):    {overlap:,} ({overlap_percent:.1f}%)")
    print(f"{'='*60}\n")
    
    return remaining_count

def sample_remaining_4combos(drawn_4combos, count=10):
    """Show sample of remaining 4-combos"""
    print(f"Sample of remaining 4-number combinations (first {count}):")
    print("-" * 60)
    
    found = 0
    for combo in itertools.combinations(range(1, MAX + 1), 4):
        if combo not in drawn_4combos:
            print(f"{combo[0]:2d}, {combo[1]:2d}, {combo[2]:2d}, {combo[3]:2d}")
            found += 1
            if found >= count:
                break
    
    print("-" * 60)

def check_6combo_contains_undrawn_4combos(six_combo, drawn_4combos):
    """Check how many undrawn 4-combos a 6-number combo contains"""
    four_combos = get_4combos_from_6(six_combo)
    undrawn_count = sum(1 for c in four_combos if c not in drawn_4combos)
    return undrawn_count, len(four_combos)

def sample_good_6combos(drawn_4combos, count=5):
    """Show sample 6-number combos with many undrawn 4-combos"""
    print(f"\nSample 6-number combinations with undrawn 4-combos (first {count}):")
    print("-" * 60)
    
    found = 0
    for combo in itertools.combinations(range(1, MAX + 1), 6):
        undrawn, total = check_6combo_contains_undrawn_4combos(combo, drawn_4combos)
        
        if undrawn >= 10:  # Look for combos with at least 10 undrawn 4-combos
            nums_str = ', '.join(f'{n:2d}' for n in combo)
            print(f"{nums_str} | Undrawn 4-combos: {undrawn}/{total}")
            found += 1
            if found >= count:
                break
    
    print("-" * 60)

def main():
    print("="*60)
    print("4-Combo Strategy Verification")
    print("="*60)
    print()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python verify_4combo_strategy.py <draws_file>")
        print()
        print("Example:")
        print("  python verify_4combo_strategy.py a_649.txt")
        print("="*60)
        sys.exit(0)
    
    filename = sys.argv[1]
    
    # Load draws
    draws = load_draws(filename)
    if not draws:
        print("No draws loaded. Exiting.")
        sys.exit(1)
    
    # Analyze 4-combos
    drawn_4combos = analyze_4combos(draws)
    
    # Verify totals
    remaining = verify_totals(drawn_4combos, len(draws))
    
    # Show samples
    sample_remaining_4combos(drawn_4combos, 10)
    sample_good_6combos(drawn_4combos, 5)
    
    print(f"\n✅ Verification complete!")
    print(f"Expected remaining 4-combos: {remaining:,}")
    print(f"This should match the HTML app statistics.\n")

if __name__ == "__main__":
    main()