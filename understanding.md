# AI Study Assistant - Algorithm Understanding

## Overview

This document explains the two core algorithms used in the AI Study Assistant application with practical code flow and UI integration:

1. **DFS (Depth-First Search) Concept Extraction** - Extracts topic hierarchy from markdown
2. **K-Means Clustering for Difficulty Planning** - Groups topics by similarity

---

## Algorithm 1: DFS-Based Concept Extraction

### Location
**File:** [helpers/concept_extractor.py](helpers/concept_extractor.py)  
**Class:** `ConceptExtractor`

---

### Function 1: `dfs_extract_concepts(text: str)`

#### **Input:**
```python
text = """
## Photosynthesis
- Light reactions
- Calvin cycle

## Cell Respiration
- Glycolysis
- **Krebs cycle**
"""
```

#### **Algorithm:**
Line-by-line parsing with DFS traversal:
1. Detect headers (`##` or `###`) as main concepts
2. Collect bullet points (`-` or `*`) under each concept
3. Collect bold text (`**...**`) under each concept
4. Build hierarchical dictionary

#### **Output:**
```python
{
    "Photosynthesis": ["Light reactions", "Calvin cycle"],
    "Cell Respiration": ["Glycolysis", "Krebs cycle"]
}
```

#### **Where Used:**
- Called by `build_quiz_topics()`
- Called by `analyze_concept_relationships()`

---

### Function 2: `build_quiz_topics(summary_text: str) -> List[Dict]`

#### **What It Does:**
Wraps the dictionary from `dfs_extract_concepts()` into a list format.

#### **Input:**
```python
summary_text = """## Photosynthesis
- Light reactions
## Cell Respiration
- Glycolysis"""
```

#### **Step-by-Step:**
```python
# Step 1: Call dfs_extract_concepts()
concepts = {
    "Photosynthesis": ["Light reactions"],
    "Cell Respiration": ["Glycolysis"]
}

# Step 2: Convert to list of dicts
return [
    {"main": "Photosynthesis"},
    {"main": "Cell Respiration"}
]
```

#### **Output:**
```python
[
    {"main": "Photosynthesis"},
    {"main": "Cell Respiration"}
]
```

#### **Where Used in Code:**
**File:** [pages/2_Create_Quiz.py](pages/2_Create_Quiz.py) - Line 24
```python
topics = extractor.build_quiz_topics(st.session_state["selected_summary"])
# topics now = [{"main": "Photosynthesis"}, {"main": "Cell Respiration"}]
```

#### **Where Shown in UI:**
Passed to the K-Means clustering algorithm (see Algorithm 2)

---

### Function 3: `analyze_concept_relationships(summary_text: str) -> Dict`

#### **Input:**
Same markdown summary text

#### **What It Does:**
Counts main concepts and sub-concepts from the DFS extraction.

#### **Output:**
```python
{
    "total_main_concepts": 2,
    "total_subconcepts": 4
}
```

#### **Where Used in Code:**
**File:** [pages/2_Create_Quiz.py](pages/2_Create_Quiz.py) - Line 25
```python
analysis = extractor.analyze_concept_relationships(st.session_state["selected_summary"])
```

#### **Where Shown in UI:**
**Create Quiz Page - "Summary Structure Analysis" Section:**
```
┌─────────────────────────────────────────┐
│  Main Concepts: 2  Sub-Topics: 4        │
│  Total Topics: 6                        │
└─────────────────────────────────────────┘
```

Three metric cards displayed using:
```python
col1.metric("Main Concepts", analysis["total_main_concepts"])
col2.metric("Sub-Topics", analysis["total_subconcepts"])
col3.metric("Total Topics", analysis["total_main_concepts"] + analysis["total_subconcepts"])
```

---

## Algorithm 2: K-Means Clustering for Difficulty Planning

### Location
**File:** [helpers/difficulty_planner.py](helpers/difficulty_planner.py)  
**Class:** `DifficultyPlanner`

---

### Function 1: `cluster_topics_by_similarity(topics: List[Dict]) -> Dict[int, List[str]]`

#### **Input:**
```python
topics = [
    {"main": "Photosynthesis"},
    {"main": "Cell Respiration"},
    {"main": "Quantum Mechanics"},
    {"main": "Atomic Bonding"}
]
```

#### **Algorithm:**
```
Step 1: Extract topic names
["Photosynthesis", "Cell Respiration", "Quantum Mechanics", "Atomic Bonding"]

Step 2: Convert to TF-IDF vectors (numerical representation)
TfidfVectorizer() → Convert text to semantic vectors

Step 3: Apply K-Means clustering
KMeans(n_clusters=4) → Group similar topics into clusters

Step 4: Return cluster assignments
{
    0: ["Photosynthesis", "Cell Respiration"],
    1: ["Quantum Mechanics", "Atomic Bonding"],
    2: [],
    3: []
}
```

#### **Output:**
```python
{
    cluster_id: [list_of_topic_names]
}
```

#### **Where Used:**
Called by `get_topic_clusters_by_difficulty()`

---

### Function 2: `get_topic_clusters_by_difficulty(topics: List[Dict]) -> Dict[str, List[str]]`

#### **Input:**
Same topics list from `build_quiz_topics()`

#### **What It Does:**
1. Calls `cluster_topics_by_similarity()` to get clusters
2. Maps clusters to difficulty labels: Bronze → Silver → Gold → Platinum

#### **Step-by-Step Flow:**

```python
# Input
topics = [
    {"main": "Photosynthesis"},
    {"main": "Cell Respiration"},
    {"main": "Quantum Mechanics"},
    {"main": "Atomic Bonding"}
]

# Step 1: Get clusters (similar topics grouped)
clusters = self.cluster_topics_by_similarity(topics)
# Result: {0: ["Photosynthesis", "Cell Respiration"], 1: [...]}

# Step 2: Map to difficulty levels
result = {
    "Bronze": clusters[0],      # Easiest
    "Silver": clusters[1],      # Intermediate
    "Gold": clusters[2],        # Advanced
    "Platinum": clusters[3]     # Most Difficult
}
```

#### **Output:**
```python
{
    "Bronze": ["Photosynthesis", "Cell Respiration"],
    "Silver": ["Quantum Mechanics"],
    "Gold": ["Atomic Bonding"],
    "Platinum": []
}
```

#### **Where Used in Code:**
**File:** [pages/2_Create_Quiz.py](pages/2_Create_Quiz.py) - Line 40
```python
clustered_topics = difficulty_planner.get_topic_clusters_by_difficulty(topics)
# Now clustered_topics has Bronze, Silver, Gold, Platinum keys
```

#### **Where Shown in UI:**
**Create Quiz Page - "Topics Grouped by Similarity (K-Means)" Section:**

Four tabs are displayed:
```
┌─────────────────────────────────────────────────────────┐
│ 🥉 Bronze      🥈 Silver      🏆 Gold      ⭐ Platinum │
├─────────────────────────────────────────────────────────┤
│ ✓ Photosynthesis       ✓ Quantum Mechanics              │
│ ✓ Cell Respiration     ✓ Atomic Bonding                 │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

Code:
```python
tab1, tab2, tab3, tab4 = st.tabs(["🥉 Bronze", "🥈 Silver", "🏆 Gold", "⭐ Platinum"])

with tab1:
    for topic in clustered_topics["Bronze"]:
        st.write(f"✓ {topic}")

with tab2:
    for topic in clustered_topics["Silver"]:
        st.write(f"✓ {topic}")
# ... and so on for Gold and Platinum
```

---

## Complete Code Flow in Application

### Where Everything Happens:
**File:** [pages/2_Create_Quiz.py](pages/2_Create_Quiz.py)

```python
# Line 14-16: Initialize both classes
extractor = ConceptExtractor()
difficulty_planner = DifficultyPlanner()

# Line 24: Extract concepts using DFS
topics = extractor.build_quiz_topics(st.session_state["selected_summary"])
# Output: [{"main": "Topic1"}, {"main": "Topic2"}, ...]

# Line 25: Get concept analysis
analysis = extractor.analyze_concept_relationships(st.session_state["selected_summary"])
# Output: {"total_main_concepts": N, "total_subconcepts": M}

# Lines 27-31: Display metrics in UI
st.metric("Main Concepts", analysis["total_main_concepts"])
st.metric("Sub-Topics", analysis["total_subconcepts"])
st.metric("Total Topics", analysis["total_main_concepts"] + analysis["total_subconcepts"])
# ↑ Shown in "Summary Structure Analysis" section

# Line 40: Cluster topics by difficulty
clustered_topics = difficulty_planner.get_topic_clusters_by_difficulty(topics)
# Output: {"Bronze": [...], "Silver": [...], "Gold": [...], "Platinum": [...]}

# Lines 42-74: Display in 4 tabs
for topic in clustered_topics["Bronze"]:
    st.write(f"✓ {topic}")
# ↑ Shown in "Topics Grouped by Similarity (K-Means)" section

# Line 80: Generate quiz (uses ALL topics, not filtered by difficulty)
quiz_text = generate_quiz(st.session_state["selected_summary"], topics_for_quiz)
```

---

## Visual UI Flow

```
┌──────────────────────────────────────────────────────┐
│           📖 Currently viewing: Summary X            │
└──────────────────────────────────────────────────────┘
                         ↓
┌──────────────────────────────────────────────────────┐
│   🧠 Summary Structure Analysis (DFS)                │
│  ┌────────────┬────────────┬────────────┐            │
│  │  Main      │  Sub-      │   Total    │            │
│  │ Concepts   │  Topics    │   Topics   │            │
│  │     2      │     4      │     6      │            │
│  └────────────┴────────────┴────────────┘            │
│         (analyze_concept_relationships)              │
└──────────────────────────────────────────────────────┘
                         ↓
┌──────────────────────────────────────────────────────┐
│  📊 Topics Grouped by Similarity (K-Means)           │
│  ┌──────────────────────────────────────────────┐   │
│  │ 🥉 Bronze │ 🥈 Silver │ 🏆 Gold │ ⭐ Platinum│   │
│  ├──────────────────────────────────────────────┤   │
│  │ ✓ Topic A  │ ✓ Topic C │           │         │   │
│  │ ✓ Topic B  │ ✓ Topic D │           │         │   │
│  │            │           │           │         │   │
│  └──────────────────────────────────────────────┘   │
│      (get_topic_clusters_by_difficulty)             │
└──────────────────────────────────────────────────────┘
                         ↓
┌──────────────────────────────────────────────────────┐
│       Generate Quiz from Summary                     │
│  ┌──────────────────────────────────────────┐       │
│  │        [Create QUIZ] Button               │       │
│  │  (generates from ALL topics)              │       │
│  └──────────────────────────────────────────┘       │
│       (generate_quiz with topics_for_quiz)          │
└──────────────────────────────────────────────────────┘
                         ↓
┌──────────────────────────────────────────────────────┐
│            Quiz Interface                            │
│  Question 1/10                                       │
│  📚 Topic: photosynthesis                            │
│  What is the light reaction?                         │
│  ○ Option A                                          │
│  ○ Option B                                          │
│  ○ Option C                                          │
--------------------------------------------------------