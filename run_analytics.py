#!/usr/bin/env python
"""
Top-level entrypoint for running the Maharashtra Skill Intelligence Analytics Pipeline.
SIH 2026 Problem Statement 26134.

Usage:
    python run_analytics.py
"""

import sys
from analytics.pipeline import run_pipeline

if __name__ == "__main__":
    try:
        results = run_pipeline()
        print("\nPipeline execution summary:")
        print(f"  Status:          {results['status']}")
        print(f"  Jobs Processed:  {results['total_jobs']}")
        print(f"  Courses Tested:  {results['total_courses']}")
        print(f"  Gaps Calculated: {results['gaps_count']}")
        print(f"  Priority Gaps:   {results['priority_counts']}")
        print(f"  Output Directory:{results['output_directory']}")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Analytics pipeline failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

