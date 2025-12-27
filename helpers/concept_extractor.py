import re
from typing import Dict, List

class ConceptExtractor:
    
    def dfs_extract_concepts(self, text: str):
        concepts = {}
        current_parent = None
        
        for line in text.split('\n'):
            stripped = line.strip()
            if not stripped:
                continue
            
            # Parse markdown headers (## or ###) as main concepts
            if stripped.startswith('##') or stripped.startswith('###'):
                concept = re.sub(r'^#+\s*', '', stripped).strip()
                if concept:
                    concepts[concept] = []
                    current_parent = concept
            
            elif current_parent:
                if stripped.startswith(('- ', '* ')):
                    subconcept = re.sub(r'^[-*]\s*', '', stripped).strip()
                elif stripped.startswith('**') and stripped.endswith('**'):
                    subconcept = stripped.replace('**', '').strip()
                else:
                    continue
                
                if subconcept and current_parent in concepts:
                    concepts[current_parent].append(subconcept)
        
        return concepts
    
    def build_quiz_topics(self, summary_text: str) -> List[Dict]:
        concepts = self.dfs_extract_concepts(summary_text)
        return [
            {"main": concept}
            for concept in concepts.keys()
        ]
    
    def analyze_concept_relationships(self, summary_text: str) -> Dict:
        concepts = self.dfs_extract_concepts(summary_text)
        
        return {
            "total_main_concepts": len(concepts),
            "total_subconcepts": sum(len(subs) for subs in concepts.values())
        }
