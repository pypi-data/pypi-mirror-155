from enum import Enum


class MetafieldDataType(Enum):
    # String
    SINGLE_LINE_TEXT_FIELD = 'single_line_text_field'
    MULTI_LINE_TEXT_FIELD = 'multi_line_text_field'

    # Product Object
    PRODUCT_REFERENCE = 'product_reference'

    # Variant Object
    VARIANT_REFERENCE = 'variant_reference'

    # Page Object
    PAGE_REFERENCE = 'page_reference'

    # File / Media Object
    FILE_REFERENCE = 'file_reference'

    # Number
    NUMBER_INTEGER = 'number_integer'
    NUMBER_DECIMAL = 'number_decimal'

    # Date Object
    DATE = 'date'
    DATE_TIME = 'date_time'

    # URL String
    URL_REFERENCE = 'url_reference'

    # JSON Object
    JSON = 'json'

    # Boolean
    BOOLEAN = 'boolean'

    # Color Object
    COLOR = 'color'

    # Measurement Object
    WEIGHT = 'weight'
    VOLUME = 'volume'
    DIMENSION = 'dimension'

    # Rating Object
    RATING = 'rating'

    # List
    LIST = list
