"""
Government & Civic Codes Database

Government codes:
- Country codes (ISO)
- State/Province codes
- Currency codes (ISO)
- Language codes (ISO)
- Tax codes
- Timezone codes

Reference:
- ISO standards
- ISO 3166, ISO 4217, ISO 639
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


# =============================================================================
# ENTITIES
# =============================================================================

@dataclass
class CountryCode:
    """ISO 3166 Country"""
    code: str  # 2-letter
    code3: str  # 3-letter
    numeric: str  # 3-digit
    
    name: str
    
    region: str = ""
    
    subregion: str = ""
    
    continent: str = ""
    
    currency_code: str = ""
    currency_name: str = ""
    
    calling_code: str = ""
    
    tld: str = ""  # Top-level domain
    
    def to_dict(self) -> Dict:
        return {
            "code": self.code,
            "name": self.name,
            "currency": self.currency_code
        }


@dataclass
class CurrencyCode:
    """ISO 4217 Currency"""
    code: str  # e.g., "USD"
    
    name: str
    
    symbol: str = ""
    
    minor_unit: int = 2  # cents, etc.
    
    countries: List[str] = field(default_factory=list)


@dataclass
class LanguageCode:
    """ISO 639 Language"""
    code: str  # 2-letter
    code3: str  # 3-letter
    
    name: str
    
    native_name: str = ""
    
    family: str = ""  # Germanic, Slavic, etc.
    
    countries: List[str] = field(default_factory=list)


@dataclass
class TimezoneCode:
    """Timezone"""
    timezone: str  # e.g., "America/New_York"
    
    offset_hours: float  # e.g., -5.0
    
    dst: bool = True  # Observes DST
    
    abbreviation: str = ""  # EST, EDT
    
    location: str = ""  # Geographic location


@dataclass
class TaxCode:
    """Tax code"""
    code: str
    
    name: str
    
    country: str
    
    rate: float  # Percentage
    
    description: str = ""
    
    category: str = ""  # VAT, Sales, etc.


@dataclass
class IndustryCode:
    """Industry classification"""
    code: str  # NAICS, SIC, etc.
    
    name: str
    
    sector: str = ""
    
    description: str = ""


# =============================================================================
# DATABASE
# =============================================================================

class GovernmentCodesDatabase:
    """Government codes database"""
    
    def __init__(self):
        # Country codes (ISO 3166)
        self.countries: Dict[str, CountryCode] = {}
        
        # Currency codes (ISO 4217)
        self.currencies: Dict[str, CurrencyCode] = {}
        
        # Language codes (ISO 639)
        self.languages: Dict[str, LanguageCode] = {}
        
        # Timezones
        self.timezones: Dict[str, TimezoneCode] = {}
        
        # Tax codes
        self.tax_codes: Dict[str, TaxCode] = {}
        
        # Industry codes
        self.industry_codes: Dict[str, IndustryCode] = {}
        
        # Initialize with standard codes
        self._init_countries()
        self._init_currencies()
        self._init_languages()
        self._init_timezones()
        self._init_industry_codes()
    
    def _init_countries(self):
        """Initialize countries"""
        codes = [
            ("US", "USA", "840", "United States", "North America", "Americas", "USD", "US Dollar", "+1", ".us"),
            ("GB", "GBR", "826", "United Kingdom", "Europe", "Europe", "GBP", "British Pound", "+44", ".uk"),
            ("DE", "DEU", "276", "Germany", "Europe", "Europe", "EUR", "Euro", "+49", ".de"),
            ("FR", "FRA", "250", "France", "Europe", "Europe", "EUR", "Euro", "+33", ".fr"),
            ("JP", "JPN", "392", "Japan", "Asia", "Asia", "JPY", "Japanese Yen", "+81", ".jp"),
            ("CN", "CHN", "156", "China", "Asia", "Asia", "CNY", "Yuan", "+86", ".cn"),
            ("IN", "IND", "356", "India", "Asia", "Asia", "INR", "Indian Rupee", "+91", ".in"),
            ("CA", "CAN", "124", "Canada", "North America", "Americas", "CAD", "Canadian Dollar", "+1", ".ca"),
            ("AU", "AUS", "036", "Australia", "Oceania", "Oceania", "AUD", "Australian Dollar", "+61", ".au"),
            ("BR", "BRA", "076", "Brazil", "South America", "Americas", "BRL", "Brazilian Real", "+55", ".br"),
        ]
        
        for c, c3, num, name, sub, cont, curr, curr_name, call, tld in codes:
            self.countries[c] = CountryCode(
                code=c, code3=c3, numeric=num,
                name=name, region=sub, continent=cont,
                currency_code=curr, currency_name=curr_name,
                calling_code=call, tld=tld
            )
    
    def _init_currencies(self):
        """Initialize currencies"""
        codes = [
            ("USD", "US Dollar", "$", 2, ["US"]),
            ("EUR", "Euro", "€", 2, ["DE", "FR", "ES", "IT"]),
            ("GBP", "British Pound", "£", 2, ["GB"]),
            ("JPY", "Japanese Yen", "¥", 0, ["JP"]),
            ("CNY", "Chinese Yuan", "¥", 2, ["CN"]),
            ("INR", "Indian Rupee", "₹", 2, ["IN"]),
            ("CAD", "Canadian Dollar", "$", 2, ["CA"]),
            ("AUD", "Australian Dollar", "$", 2, ["AU"]),
            ("CHF", "Swiss Franc", "CHF", 2, ["CH"]),
            ("BRL", "Brazilian Real", "R$", 2, ["BR"]),
        ]
        
        for code, name, symbol, minor, countries in codes:
            self.currencies[code] = CurrencyCode(
                code=code, name=name, symbol=symbol,
                minor_unit=minor, countries=countries
            )
    
    def _init_languages(self):
        """Initialize languages"""
        codes = [
            ("en", "eng", "English", "English", "Germanic", ["US", "GB", "CA", "AU"]),
            ("es", "spa", "Spanish", "Español", "Romance", ["ES", "MX", "AR"]),
            ("zh", "zho", "Chinese", "中文", "Sino-Tibetan", ["CN"]),
            ("fr", "fra", "French", "Français", "Romance", ["FR", "CA"]),
            ("de", "deu", "German", "Deutsch", "Germanic", ["DE"]),
            ("ja", "jpn", "Japanese", "日本語", "Japonic", ["JP"]),
            ("ko", "kor", "Korean", "한국어", "Koreanic", ["KR"]),
            ("pt", "por", "Portuguese", "Português", "Romance", ["PT", "BR"]),
            ("ar", "ara", "Arabic", "العربية", "Semitic", ["SA", "EG"]),
            ("hi", "hin", "Hindi", "हिन्दी", "Indo-Aryan", ["IN"]),
        ]
        
        for code, code3, name, native, family, countries in codes:
            self.languages[code] = LanguageCode(
                code=code, code3=code3, name=name,
                native_name=native, family=family, countries=countries
            )
    
    def _init_timezones(self):
        """Initialize timezones"""
        zones = [
            ("America/New_York", -5.0, True, "EST"),
            ("America/Los_Angeles", -8.0, True, "PST"),
            ("America/Chicago", -6.0, True, "CST"),
            ("Europe/London", 0.0, True, "GMT"),
            ("Europe/Paris", 1.0, True, "CET"),
            ("Asia/Tokyo", 9.0, False, "JST"),
            ("Asia/Shanghai", 8.0, False, "CST"),
            ("Australia/Sydney", 10.0, True, "AEST"),
        ]
        
        for tz, offset, dst, abbr in zones:
            self.timezones[tz] = TimezoneCode(
                timezone=tz, offset_hours=offset,
                dst=dst, abbreviation=abbr
            )
    
    def _init_industry_codes(self):
        """Initialize industry codes"""
        codes = [
            ("11", "Agriculture, Forestry, Fishing", "Agriculture"),
            ("21", "Mining, Quarrying, Oil and Gas Extraction", "Mining"),
            ("31", "Manufacturing", "Manufacturing"),
            ("51", "Information", "Technology"),
            ("52", "Finance and Insurance", "Finance"),
            ("54", "Professional, Scientific, and Technical Services", "Services"),
            ("61", "Educational Services", "Education"),
            ("62", "Health Care and Social Assistance", "Healthcare"),
            ("72", "Accommodation and Food Services", "Hospitality"),
            ("92", "Public Administration", "Government"),
        ]
        
        for code, name, sector in codes:
            self.industry_codes[code] = IndustryCode(
                code=code, name=name, sector=sector
            )
    
    # Countries
    def get_country(self, code: str) -> Optional[CountryCode]:
        return self.countries.get(code.upper())
    
    def get_country_by_name(self, name: str) -> Optional[CountryCode]:
        name_lower = name.lower()
        for country in self.countries.values():
            if name_lower in country.name.lower():
                return country
        return None
    
    def get_countries_by_region(self, region: str) -> List[CountryCode]:
        region = region.lower()
        return [
            c for c in self.countries.values()
            if region in c.region.lower() or region in c.continent.lower()
        ]
    
    def get_all_countries(self) -> List[CountryCode]:
        return sorted(self.countries.values(), key=lambda c: c.name)
    
    # Currencies
    def get_currency(self, code: str) -> Optional[CurrencyCode]:
        return self.currencies.get(code.upper())
    
    def get_currency_for_country(self, country_code: str) -> Optional[CurrencyCode]:
        country = self.countries.get(country_code.upper())
        if not country:
            return None
        return self.currencies.get(country.currency_code)
    
    # Languages
    def get_language(self, code: str) -> Optional[LanguageCode]:
        return self.languages.get(code.lower())
    
    def get_language_by_name(self, name: str) -> Optional[LanguageCode]:
        name_lower = name.lower()
        for lang in self.languages.values():
            if name_lower in lang.name.lower():
                return lang
        return None
    
    def get_all_languages(self) -> List[LanguageCode]:
        return sorted(self.languages.values(), key=lambda l: l.name)
    
    # Timezones
    def get_timezone(self, timezone: str) -> Optional[TimezoneCode]:
        return self.timezones.get(timezone)
    
    def get_timezone_for_offset(self, offset: float) -> List[TimezoneCode]:
        return [
            t for t in self.timezones.values()
            if t.offset_hours == offset
        ]
    
    # Industry codes
    def get_industry_code(self, code: str) -> Optional[IndustryCode]:
        return self.industry_codes.get(code)
    
    def search_industry_codes(self, query: str) -> List[IndustryCode]:
        q = query.lower()
        return [
            i for i in self.industry_codes.values()
            if q in i.name.lower() or q in i.sector.lower()
        ]
    
    # Tax codes (add custom)
    def add_tax_code(self, code: TaxCode) -> str:
        self.tax_codes[code.code] = code
        return code.code
    
    def get_tax_codes_for_country(self, country: str) -> List[TaxCode]:
        return [
            t for t in self.tax_codes.values()
            if t.country == country
        ]
    
    # Utilities
    def validate_country_code(self, code: str) -> bool:
        return code.upper() in self.countries
    
    def validate_currency_code(self, code: str) -> bool:
        return code.upper() in self.currencies
    
    def validate_language_code(self, code: str) -> bool:
        return code.lower() in self.languages
    
    # Statistics
    def stats(self) -> Dict:
        return {
            "countries": len(self.countries),
            "currencies": len(self.currencies),
            "languages": len(self.languages),
            "timezones": len(self.timezones),
            "industry_codes": len(self.industry_codes),
            "tax_codes": len(self.tax_codes)
        }


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Example"""
    
    print("=" * 50)
    print("Government Codes Database")
    print("=" * 50)
    
    db = GovernmentCodesDatabase()
    
    # Stats
    print(f"\nCodes loaded:")
    stats = db.stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Countries
    print(f"\nCountry lookup:")
    us = db.get_country("US")
    if us:
        print(f"  US: {us.name}, Currency: {us.currency_name}")
    
    # Get by region
    print(f"\nCountries in Europe:")
    europe = db.get_countries_by_region("Europe")
    for c in europe:
        print(f"  {c.code}: {c.name}")
    
    # Languages
    print(f"\nLanguage lookup:")
    en = db.get_language("en")
    if en:
        print(f"  English: Family {en.family}")
    
    # Timezones
    print(f"\nTimezones:")
    tz = db.get_timezone("America/New_York")
    if tz:
        print(f"  {tz.timezone}: UTC {tz.offset_hours:+.1f}")
    
    # Industry
    print(f"\nIndustry codes:")
    ict = db.get_industry_code("51")
    if ict:
        print(f"  51: {ict.name}")
    
    # Tax codes
    print(f"\nTax codes:")
    db.add_tax_code(TaxCode("US-VAT", "US Sales Tax", "US", 7.25, "State sales tax", "Sales"))
    taxes = db.get_tax_codes_for_country("US")
    for t in taxes:
        print(f"  {t.code}: {t.name} at {t.rate}%")


if __name__ == "__main__":
    main()


"""
Government Codes Usage

    db = GovernmentCodesDatabase()
    
    # Countries
    country = db.get_country("US")
    countries = db.get_countries_by_region("Europe")
    
    # Currencies
    currency = db.get_currency("USD")
    currency = db.get_currency_for_country("US")
    
    # Languages
    language = db.get_language("en")
    languages = db.get_all_languages()
    
    # Timezones
    timezone = db.get_timezone("America/New_York")
    timezones = db.get_timezone_for_offset(-5.0)
    
    # Industry
    industry = db.get_industry_code("51")
    industries = db.search_industry_codes("Technology")
    
    # Tax
    db.add_tax_code(TaxCode(...))
    taxes = db.get_tax_codes_for_country("US")
    
    # Validate
    db.validate_country_code("US")
    db.validate_currency_code("USD")
"""