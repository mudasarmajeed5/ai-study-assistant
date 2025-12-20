from collections import defaultdict

class NaiveBayesClassifier:
    """Predicts weak topics from quiz performance"""
    
    def __init__(self):
        self.topic_stats = defaultdict(lambda: {"correct": 0, "total": 0})
    
    def train(self, topic_results):
        """
        Train on topic results
        topic_results: [(topic, correct/incorrect), ...]
        """
        for topic, is_correct in topic_results:
            self.topic_stats[topic]["total"] += 1
            if is_correct:
                self.topic_stats[topic]["correct"] += 1
    
    def predict_weak_topics(self, threshold=0.7):
        """Find topics where accuracy < threshold"""
        weak = []
        for topic, stats in self.topic_stats.items():
            accuracy = stats["correct"] / stats["total"] if stats["total"] > 0 else 0
            if accuracy < threshold:
                weak.append({
                    "topic": topic,
                    "accuracy": accuracy,
                    "questions": stats["total"]
                })
        return sorted(weak, key=lambda x: x["accuracy"])
    
    def get_mastery_level(self):
        """Overall mastery: Expert/Advanced/Intermediate/Beginner"""
        all_correct = sum(s["correct"] for s in self.topic_stats.values())
        all_total = sum(s["total"] for s in self.topic_stats.values())
        
        if all_total == 0:
            return "No Data"
        
        avg = all_correct / all_total
        if avg >= 0.9:
            return "Expert"
        elif avg >= 0.8:
            return "Advanced"
        elif avg >= 0.7:
            return "Intermediate"
        else:
            return "Beginner"
