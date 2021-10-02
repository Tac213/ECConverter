
class {{ class_name }}(object):
    """
    {{ class_comment }}
    """
{%- for member in members %}
    {{ member.id }} = {{ member.value | ecc_formatter }}  # {{ member.comment }}
{%- endfor %}