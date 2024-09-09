import re


class RegexPatterns:
    @classmethod
    def _convert_brazilian_number(cls, text: str) -> str:
        cleaned = re.sub(r"[^\d,.]", "", text)
        return cleaned.replace(".", "").replace(",", ".")

    @classmethod
    def _extract_number(cls, text: str, label: str) -> str:
        pattern = rf"{label}:([\d.,]+)"
        match = re.search(pattern, text)
        if match:
            return cls._convert_brazilian_number(match.group(1))
        return None

    @classmethod
    def quantity(cls, text: str) -> float:
        value = cls._extract_number(text, "Qtde.")
        return float(value) if value is not None else None

    @classmethod
    def unit_type(cls, text):
        return re.sub(r"UN:", "", text)

    @classmethod
    def unit_value(cls, text: str) -> float:
        value = cls._extract_number(text, "Vl. Unit.")
        return float(value) if value is not None else None

    @classmethod
    def code(cls, text: str) -> int:
        return int(re.sub(r"\D", "", text))

    @classmethod
    def monetary_value(cls, text: str) -> float:
        cleaned_text = cls._convert_brazilian_number(re.sub(r"[^\d.,]", "", text))
        return float(cleaned_text)
