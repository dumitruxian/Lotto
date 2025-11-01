"""
Lottery Distance-Based Elimination System
Eliminates combinations from the full 13,983,816 pool based on distance from historical draws

For 6/49 lottery:
- Total possible combinations: 13,983,816
- Distance 3: combinations sharing exactly 3 numbers (eliminates 2-match combos)
- Distance 4: combinations sharing exactly 2 numbers (eliminates 4-match combos)

Usage:
python lottery_distance_eliminator.py
"""

import itertools
import os
import sys
from datetime import datetime

SP = 32

def tochar(ch):
    return (ch + SP) & 0xFF

def unchar(ch):
    return (ch - SP) & 0xFF

class DistanceEliminator:
    def __init__(self, max_num=49, max_play=6):
        self.max_num = max_num
        self.max_play = max_play
        self.total_combinations = self.calculate_total_combinations()
        self.eliminated = set()
        self.draws = []
        
    def calculate_total_combinations(self):
        """Calculate total possible combinations"""
        from math import factorial
        n = self.max_num
        k = self.max_play
        return factorial(n) // (factorial(k) * factorial(n - k))
    
    def calculate_distance(self, combo1, combo2):
        """Calculate distance between two combinations (number of non-matching numbers)"""
        set1 = set(combo1)
        set2 = set(combo2)
        matches = len(set1 & set2)
        return self.max_play - matches
    
    def load_draws(self, filename):
        """Load historical draws from file"""
        self.draws = []
        
        try:
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse format: YYMMDD:  n1, n2, n3, n4, n5, n6 / bonus
                    if ':' in line:
                        parts = line.split(':')[1].split('/')
                        nums_part = parts[0].strip()
                        
                        # Extract numbers
                        numbers = []
                        for num_str in nums_part.split(','):
                            num_str = num_str.strip()
                            if num_str.isdigit():
                                numbers.append(int(num_str))
                        
                        if len(numbers) == self.max_play:
                            self.draws.append(tuple(sorted(numbers)))
            
            print(f"✅ Loaded {len(self.draws)} draws from {filename}")
            return True
            
        except FileNotFoundError:
            print(f"❌ File not found: {filename}")
            return False
        except Exception as e:
            print(f"❌ Error loading draws: {e}")
            return False
    
    def eliminate_by_distance(self, draw, distance):
        """
        Eliminate all combinations at specified distance from draw
        Distance 3 = sharing 3 numbers (2 non-matching)
        Distance 4 = sharing 2 numbers (4 non-matching)
        """
        count = 0
        draw_set = set(draw)
        
        # Generate all possible combinations and check distance
        for combo in itertools.combinations(range(1, self.max_num + 1), self.max_play):
            if combo in self.eliminated:
                continue
            
            combo_set = set(combo)
            matches = len(draw_set & combo_set)
            combo_distance = self.max_play - matches
            
            if combo_distance == distance:
                self.eliminated.add(combo)
                count += 1
        
        return count
    
    def eliminate_from_draws(self, max_distance=3, specific_draws=None):
        """
        Eliminate combinations based on all loaded draws
        max_distance: 3 or 4
        specific_draws: number of most recent draws to process (None = all)
        """
        if not self.draws:
            print("No draws loaded")
            return
        
        draws_to_process = self.draws if specific_draws is None else self.draws[-specific_draws:]
        
        print(f"\n{'='*60}")
        print(f"Elimination Process - Distance {max_distance}")
        print(f"{'='*60}")
        print(f"Total possible combinations: {self.total_combinations:,}")
        print(f"Processing {len(draws_to_process)} draws...")
        print(f"{'='*60}\n")
        
        for i, draw in enumerate(draws_to_process, 1):
            eliminated = self.eliminate_by_distance(draw, max_distance)
            remaining = self.total_combinations - len(self.eliminated)
            
            print(f"Draw {i:4d}: {', '.join(f'{n:2d}' for n in draw)} | "
                  f"Eliminated: {eliminated:,} | Remaining: {remaining:,}")
            
            if i % 10 == 0:
                percentage = (len(self.eliminated) / self.total_combinations) * 100
                print(f"          Progress: {percentage:.2f}% eliminated\n")
        
        self.print_statistics()
    
    def eliminate_by_distance_efficient(self, draw, distance, batch_size=100000):
        """
        More efficient elimination using batch processing
        """
        count = 0
        draw_set = set(draw)
        batch = []
        
        for combo in itertools.combinations(range(1, self.max_num + 1), self.max_play):
            if combo in self.eliminated:
                continue
            
            matches = len(set(combo) & draw_set)
            combo_distance = self.max_play - matches
            
            if combo_distance == distance:
                batch.append(combo)
                count += 1
                
                if len(batch) >= batch_size:
                    self.eliminated.update(batch)
                    batch = []
        
        if batch:
            self.eliminated.update(batch)
        
        return count
    
    def print_statistics(self):
        """Print elimination statistics"""
        eliminated_count = len(self.eliminated)
        remaining_count = self.total_combinations - eliminated_count
        percentage_eliminated = (eliminated_count / self.total_combinations) * 100
        
        print(f"\n{'='*60}")
        print("ELIMINATION STATISTICS")
        print(f"{'='*60}")
        print(f"Total possible:      {self.total_combinations:,}")
        print(f"Eliminated:          {eliminated_count:,} ({percentage_eliminated:.2f}%)")
        print(f"Remaining:           {remaining_count:,}")
        print(f"Draws processed:     {len(self.draws)}")
        print(f"{'='*60}\n")
    
    def save_remaining(self, filename, format='text'):
        """Save remaining combinations to file"""
        remaining = []
        
        print(f"Generating remaining combinations...")
        
        for combo in itertools.combinations(range(1, self.max_num + 1), self.max_play):
            if combo not in self.eliminated:
                remaining.append(combo)
        
        if format == 'binary':
            with open(filename, 'wb') as f:
                for combo in remaining:
                    data = bytes([tochar(n) for n in combo])
                    f.write(data)
        else:
            with open(filename, 'w') as f:
                f.write(f"# Remaining Combinations after Distance Elimination\n")
                f.write(f"# Total: {len(remaining):,}\n")
                f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"#\n")
                
                for combo in remaining:
                    line = ', '.join(f'{n:2d}' for n in combo)
                    f.write(f"{line}\n")
        
        print(f"✅ Saved {len(remaining):,} remaining combinations to {filename}")
    
    def get_sample_remaining(self, count=10):
        """Get a sample of remaining combinations"""
        remaining = []
        
        for combo in itertools.combinations(range(1, self.max_num + 1), self.max_play):
            if combo not in self.eliminated:
                remaining.append(combo)
                if len(remaining) >= count:
                    break
        
        return remaining

def main():
    print("="*60)
    print("Lottery Distance-Based Elimination System")
    print("="*60)
    print("\nThis tool eliminates combinations from the full pool")
    print("based on distance from historical draws.")
    print()
    print("For 6/49 lottery: 13,983,816 total combinations")
    print("Distance 3: Eliminates combos sharing 3 numbers with draw")
    print("Distance 4: Eliminates combos sharing 2 numbers with draw")
    print("="*60)
    print()
    
    # Configuration
    max_num = 49
    max_play = 6
    
    # Ask for draw file
    print("Enter historical draws filename (e.g., a_649.txt): ", end='')
    draw_file = input().strip()
    
    if not draw_file:
        draw_file = 'a_649.txt'
    
    # Ask for distance
    print("\nDistance to use (3 or 4): ", end='')
    try:
        distance = int(input().strip())
        if distance not in [3, 4]:
            print("Invalid distance. Using 3.")
            distance = 3
    except:
        distance = 3
    
    # Ask for number of draws to process
    print("\nNumber of recent draws to process (0 = all): ", end='')
    try:
        num_draws = int(input().strip())
        if num_draws <= 0:
            num_draws = None
    except:
        num_draws = None
    
    # Create eliminator
    eliminator = DistanceEliminator(max_num, max_play)
    
    # Load draws
    if not eliminator.load_draws(draw_file):
        return
    
    # Process elimination
    print("\n⚠️  Warning: Processing all combinations may take significant time.")
    print("For full elimination, consider running overnight.\n")
    
    print("Start elimination? (y/n): ", end='')
    if input().strip().lower() != 'y':
        print("Cancelled.")
        return
    
    start_time = datetime.now()
    eliminator.eliminate_from_draws(distance, num_draws)
    elapsed = datetime.now() - start_time
    
    print(f"\n⏱️  Time elapsed: {elapsed}")
    
    # Ask to save
    print("\nSave remaining combinations? (y/n): ", end='')
    if input().strip().lower() == 'y':
        print("Output filename (e.g., remaining_649.txt): ", end='')
        output_file = input().strip()
        if output_file:
            eliminator.save_remaining(output_file, 'text')
    
    # Show sample
    print("\nSample of remaining combinations (first 10):")
    print("-" * 60)
    samples = eliminator.get_sample_remaining(10)
    for combo in samples:
        print(', '.join(f'{n:2d}' for n in combo))
    print("-" * 60)

if __name__ == "__main__":
    main()