# Series Name Management & Cascade Effect Analysis

## Overview
This document outlines the critical discovery about how series names are used throughout the WhatsItCost system and the cascade effects that occur when attempting to correct misspellings.

## The Problem
We have misspellings in our series names (e.g., "Diesel Fule" instead of "Diesel Fuel"), but correcting them creates a cascade effect that breaks the AI system.

## System Architecture Analysis

### 1. Data Flow
```
BLS API → theBehemoth.csv → JSON Files → Backend AI → Frontend
```

### 2. Key Discovery: JSON Files Use Series Names as Keys
**Critical Finding:** All JSON files in `AIBrain/JSONS/` use **series names** as keys, NOT series IDs.

#### Evidence from `prepare_data.py`:
```python
# Line 14: Creates pivot table with series_name as columns
df_pivot = df.pivot(index="Date", columns="series_name", values="value")

# All JSON generation uses df_pivot.columns (which are series names)
for series in df_pivot.columns:  # series = series_name
    trendlines[series] = []      # Key = series_name
```

#### Affected JSON Files:
- `material_trendlines.json`
- `material_trends.json` 
- `material_spikes.json`
- `material_rolling.json`
- `material_rolling_12mo.json`
- `material_rolling_3yr.json`
- `material_correlations.json`

### 3. How Series Names Are Preserved
**Source:** `Scrapers/Behometh Injector.py` (Lines 34-36)
```python
try:
    series_name = behemoth[behemoth['series_id'] == sid]['series_name'].iloc[0]
except IndexError:
    series_name = "UNKNOWN"
```

**Key Insight:** BLS API only provides `series_id` + `value` + `date`. Series names come from existing theBehemoth.csv data.

## The Cascade Effect

### When You Change a Series Name in theBehemoth.csv:

1. **JSON Regeneration** (`prepare_data.py`)
   - Creates NEW key with corrected name
   - OLD key with misspelled name disappears
   - All historical data moves to new key

2. **Backend AI System** (`main.py`)
   - Can't find old misspelled name in JSON files
   - Looks for new corrected name
   - If aliases don't match → "Material not found" error

3. **Frontend System**
   - Firestore uses `series_id` for matching (safe)
   - Display names can be corrected independently

4. **Cluster Data** (`cluster_JSON_creator.py`)
   - Uses `series_id` for matching (safe)
   - Gets `series_name` from theBehemoth.csv
   - Updates to new name automatically

## Current Safety Mechanisms

### 1. Alias System in `main.py`
```python
ALIASES = {
    "diesel": "#2 Diesel Fuel",
    "diesel fuel": "#2 Diesel Fuel",
    "ppi": "Producer Price Index (PPI For Final Demand",
    "cpi": "Consumer Price Index (CPI-U)",
    # ... more aliases
}
```

### 2. Material Map (`material_map.json`)
- Provides additional alias mappings
- Loaded via `get_material_map()` function

## Step-by-Step Fix Approach

### Phase 1: Assessment & Planning
1. **Identify All Misspellings**
   - Audit theBehemoth.csv for series name errors
   - Document current vs. desired names
   - Prioritize by frequency of use

2. **Map Dependencies**
   - Identify which materials are used in clusters
   - Check which have existing aliases
   - Document user-facing vs. internal usage

### Phase 2: Safe Implementation Strategy

#### Option A: Firestore-Only Fixes (Safest)
1. **Keep theBehemoth.csv unchanged**
2. **Fix display names in Firestore only**
3. **No cascade effects**
4. **Pros:** Zero risk, immediate fix
5. **Cons:** Misspellings remain in source data

#### Option B: Systematic Name Correction (Recommended)
1. **Prepare Alias Updates**
   - Add old misspelled names to ALIASES dict
   - Update material_map.json if needed
   - Test alias resolution

2. **Correct theBehemoth.csv**
   - Fix one material at a time
   - Run full pipeline after each change
   - Verify AI system still works

3. **Update Backend Aliases**
   - Add old name as alias pointing to new name
   - Test with both old and new names
   - Monitor for "Material not found" errors

4. **Gradual Migration**
   - Keep old aliases for backward compatibility
   - Update documentation to use new names
   - Eventually deprecate old aliases

#### Option C: Hybrid Approach
1. **Fix Critical Misspellings Only**
   - Focus on most commonly used materials
   - Leave minor misspellings unchanged
   - Balance risk vs. benefit

### Phase 3: Testing & Validation

1. **Local Testing**
   - Run full pipeline after each change
   - Test AI queries with both old and new names
   - Verify chart generation works

2. **Production Testing**
   - Deploy to staging environment
   - Test all major user flows
   - Monitor error logs

3. **Rollback Plan**
   - Keep backup of original theBehemoth.csv
   - Document exact changes made
   - Prepare quick rollback procedure

## Risk Mitigation

### High-Risk Scenarios
- **Materials used in clusters** (affects cluster summaries)
- **Materials with no existing aliases** (complete breakage)
- **Materials used in visualization** (chart generation fails)

### Safety Measures
1. **Always update aliases BEFORE changing names**
2. **Test each change individually**
3. **Keep old names as aliases permanently**
4. **Monitor error logs after deployment**

## Recommended Implementation Order

### Priority 1: Low-Risk Materials
- Materials with existing aliases
- Materials not used in clusters
- Materials with clear, obvious misspellings

### Priority 2: Medium-Risk Materials
- Materials used in clusters
- Materials with complex names
- Materials with multiple possible spellings

### Priority 3: High-Risk Materials
- Core index materials (CPI, PPI)
- Materials with no aliases
- Materials used extensively in visualizations

## Monitoring & Maintenance

### Post-Implementation
1. **Monitor error logs** for "Material not found" messages
2. **Track user queries** to identify missing aliases
3. **Update documentation** with new naming conventions
4. **Plan regular audits** of series names

### Long-term Strategy
1. **Establish naming conventions** for new materials
2. **Create validation scripts** to catch misspellings early
3. **Implement automated testing** for alias resolution
4. **Document all changes** for future reference

## Conclusion

The series name cascade effect is a real and significant risk. However, with proper planning, systematic implementation, and comprehensive alias management, it can be managed safely. The key is to never change a series name without first ensuring backward compatibility through aliases.

**Remember: The system is working now. Any changes must be made carefully to avoid breaking existing functionality.**


