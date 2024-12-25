import re


class RegexPatterns:
    CNPJ_PATTERN = re.compile(r"\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}")
    PURCHASE_TIMESTAMP_PATTERN = re.compile(r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}")
    ADDRESS_PATTERN = r"\s*,\s*|,{2,}"

    MG_CODE_PATTERN = r"\(Código:\s*(\d+)\)"
    MG_ITEM_QUANTITY_PATTERN = r"Qtde total de ítens: (\d+(\.\d+)?)"
    MG_ITEM_UNITY_TYPE = r"UN: (\w+)"
    MG_TOTAL_VALUE_PATTERN = r"R\$ ([\d\.]+,\d{2})"

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
    def unit_type(cls, text: str) -> str:
        return re.sub(r"UN:", "", text)

    @classmethod
    def unit_price(cls, text: str) -> float:
        value = cls._extract_number(text, "Vl. Unit.")
        return float(value) if value is not None else None

    @classmethod
    def total_value(cls, text: str) -> float:
        cleaned_text = cls._convert_brazilian_number(re.sub(r"Vl. Total", "", text))
        return float(cleaned_text)

    @classmethod
    def code(cls, text: str) -> str:
        return str(re.sub(r"\D", "", text))

    @classmethod
    def monetary_value(cls, text: str) -> float:
        cleaned_text = cls._convert_brazilian_number(re.sub(r"[^\d.,]", "", text))
        return float(cleaned_text)

    @classmethod
    def purchase_timestamp(cls, text: str) -> str:
        return re.search(cls.PURCHASE_TIMESTAMP_PATTERN, text).group()

    @classmethod
    def cnpj(cls, text: str) -> str:
        return cls._convert_brazilian_number(re.search(cls.CNPJ_PATTERN, text).group())

    @classmethod
    def sellers_address(cls, text: str) -> str:
        # Primeiro, remove os espaços ao redor das vírgulas e garante uma vírgula com espaço
        text = re.sub(cls.ADDRESS_PATTERN, ", ", text)
        # Em seguida, remove múltiplas vírgulas consecutivas
        text = re.sub(r",\s*,", ",", text)
        return text
