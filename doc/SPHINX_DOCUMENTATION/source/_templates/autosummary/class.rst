{% extends "!autosummary/class.rst" %}

{% block methods %}
{% if methods %}

..
   HACK -- meth the point here is that we don't want this to appear in the output, but the autosummary should still generate the pages.
   .. autosummary::
      :toctree:
      {% for item in methods %}
      {%- if not item.startswith('_') or item in ['__call__'] %}
      {{ name }}.{{ item }}
      {%- endif -%}
      {%- endfor %}

{% endif %}
{% endblock %}

{% block attributes %}
{% if attributes %}

..
   HACK -- attr the point here is that we don't want this to appear in the output, but the autosummary should still generate the pages.
   .. autosummary::
      :toctree:
      {% for item in all_attributes %}
      {%- if not item.startswith('_') %}
      {{ name }}.{{ item }}
      {%- endif -%}
      {%- endfor %}

{% endif %}
{% endblock %}
