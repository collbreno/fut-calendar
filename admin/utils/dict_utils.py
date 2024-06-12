class DictUtils:
    @staticmethod
    def sort_as_int(m: dict) -> dict:
        keys = [int(a) for a in m.keys()]
        keys.sort()
        return {str(i): m[str(i)] for i in keys}