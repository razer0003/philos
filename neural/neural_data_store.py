#!/usr/bin/env python3
"""
Neural Data Shared Storage
Allows neural data to be shared between AI companion and dashboard
"""

import json
import os
import threading
import time
from datetime import datetime
from typing import Dict, Any, List

class NeuralDataStore:
    """Shared storage for neural monitoring data"""
    
    def __init__(self, data_file="neural_data.json"):
        self.data_file = data_file
        self.data = {
            "timestamp": datetime.now().isoformat(),
            "monitoring_active": False,
            "recent_computations": [],
            "emotional_activation": {},
            "memory_zones": {},
            "decision_pathways": [],
            "stats": {
                "computation_rate": 0.0,
                "neural_coherence": 0.0,
                "total_computations": 0
            }
        }
        self._lock = threading.Lock()
    
    def update_computation(self, computation_data: Dict[str, Any]):
        """Add a new computation to the data store"""
        with self._lock:
            self.data["recent_computations"].append({
                **computation_data,
                "timestamp": datetime.now().isoformat()
            })
            
            # Keep only recent computations (last 20)
            if len(self.data["recent_computations"]) > 20:
                self.data["recent_computations"] = self.data["recent_computations"][-20:]
            
            self._save_to_file()
    
    def update_emotional_state(self, emotions: Dict[str, float]):
        """Update emotional activation state"""
        with self._lock:
            self.data["emotional_activation"] = {
                "emotion_levels": emotions,
                "emotional_intensity": sum(emotions.values()) / len(emotions) if emotions else 0.0,
                "dominant_emotion": max(emotions, key=emotions.get) if emotions else "neutral",
                "timestamp": datetime.now().isoformat()
            }
            self._save_to_file()
    
    def update_memory_zones(self, zones: Dict[str, Dict[str, Any]]):
        """Update memory activation zones"""
        with self._lock:
            self.data["memory_zones"] = zones
            self._save_to_file()
    
    def add_decision_pathway(self, decision: Dict[str, Any]):
        """Add a decision pathway"""
        with self._lock:
            self.data["decision_pathways"].append({
                **decision,
                "timestamp": datetime.now().isoformat()
            })
            
            # Keep only recent decisions (last 10)
            if len(self.data["decision_pathways"]) > 10:
                self.data["decision_pathways"] = self.data["decision_pathways"][-10:]
            
            self._save_to_file()
    
    def update_stats(self, stats: Dict[str, Any]):
        """Update neural statistics"""
        with self._lock:
            self.data["stats"].update(stats)
            self.data["timestamp"] = datetime.now().isoformat()
            self._save_to_file()
    
    def set_monitoring_active(self, active: bool):
        """Set monitoring status"""
        with self._lock:
            self.data["monitoring_active"] = active
            self._save_to_file()
    
    def get_data(self) -> Dict[str, Any]:
        """Get current neural data"""
        with self._lock:
            return self.data.copy()
    
    def _save_to_file(self):
        """Save data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving neural data: {e}")
    
    def load_from_file(self):
        """Load data from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    self.data = json.load(f)
        except Exception as e:
            print(f"Error loading neural data: {e}")

# Global neural data store instance
_neural_data_store = None

def get_neural_data_store() -> NeuralDataStore:
    """Get the global neural data store instance"""
    global _neural_data_store
    if _neural_data_store is None:
        _neural_data_store = NeuralDataStore()
        _neural_data_store.load_from_file()
    return _neural_data_store
