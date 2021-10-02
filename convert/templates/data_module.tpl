# -*- coding: utf-8 -*-
# This file is generated automatically by: ECConverter
# Raw excel file name: {{ excel_file_name }}
# Do not modify this file manually
# Your modification will be overridden when the automatic generation is performed
# Unless you know what you are doing
{%- if addtional_import_info %}{{ '\n' }}
{%- for module_name in addtional_import_info %}
import {{ module_name }}
{%- endfor %}
{%- endif %}
{%- if translate_meta_info != {} %}{{ '\n' }}
translate_meta_info = {{ translate_meta_info | ecc_formatter }}
{%- endif %}

data = {{ data | ecc_formatter }}

