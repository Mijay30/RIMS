class SearchService:
    @staticmethod
    def filter_assets(items: list, criteria: str):
        # Filtrează vehicule sau segmente de drum
        return [item for item in items if criteria in item.values()]