class SymbolicLegacyBank:
    def __init__(self, legacy_records):
        self.records = legacy_records

    def get_high_value_essences(self, threshold=0.9):
        return [r for r in self.records if r["reuse_score"] >= threshold]

    def find_by_geometry(self, shape):
        return [r for r in self.records if r["geometry"].lower() == shape.lower()]

    def recommend_for_seed_integration(self):
        sorted_records = sorted(self.records, key=lambda r: r["reuse_score"], reverse=True)
        return sorted_records[:3]

    def summarize(self):
        return [
            {
                "id": r["id"],
                "essence": r["essence"],
                "reuse_score": r["reuse_score"]
            }
            for r in self.records
        ]
