{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
   :members:

   {% block methods %}
   {% for item in methods %}
      ..automethod:: {{ name }}.{{ item }}
   {%- endfor %}

   {% if methods %}
   .. rubric:: Methods

   .. autosummary::
   {% for item in methods[1:] %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}
