# -*- coding: utf-8 -*-
from osv import osv
from osv import fields

import inspect

class model_columns(osv.osv_memory):
    _name = 'model.columns'
    _rec_name = 'Model Data'

    @staticmethod
    def string_cleanup(string):
        # Remove newlines
        result: str = string.replace('\n', '')
        # Remove multiples spaces
        result = ' '.join(result.split())
        # Replace string delimiters
        result = result.replace('"', "'")
        return result

    def onchange_model_name(self, cr, uid, ids, model_name, context=None):
        """
        """
        if context is None:
            context = {}
        # Prepare default results
        res = {
            'value': {}
        }
        # Check model_name
        if not model_name:
            res["value"]["columns"] = "Type in model name and click away"
            res["value"]["fields"] = "Type in model name and click away"
            return res
        # Search for model name
        model_obj = self.pool.get(model_name)
        if not model_obj:
            res["value"]["columns"] = "Model not found."
            res["value"]["fields"] = "Model not found."
            return res

        # Process model columns
        columns = model_obj._columns
        columns_str = ""
        fields_str = ""
        for field_name, field_data in columns.items():
            ## Extract field data ##
            # Type
            type = field_data._type
            new_type = type[0].upper() + type[1:]

            attributes = []
            # Get base field attributes
            if field_data.string != 'unknown':
                attributes.append(('string', f'"{field_data.string}"'))
            if field_data.required:
                attributes.append(('required', 'True'))
            if field_data.readonly:
                attributes.append(('readonly', 'True'))
            if field_data.help:
                attributes.append(('help', f'"{self.string_cleanup(field_data.help)}"'))
            if field_data._domain:
                attributes.append(('domain', f'"{field_data._domain}"'))
            # Default values
            if model_obj._defaults and field_name in model_obj._defaults:
                default_val = model_obj._defaults[field_name]
                # Default strings need to be encased by string delimiters (contrary to ints, bools, etc...)
                if isinstance(default_val, str):
                    default_val = f'"{self.string_cleanup(default_val)}"'
                # Check for lambdas and functions
                if callable(default_val):
                    if default_val.__name__ == "<lambda>":
                        # Cleanup initial field name attribute
                        default_val = inspect.getsource(default_val).split(': ', 1)[1].rstrip()
                        # Keep only first line (see issue with sale_delay default in product.product)
                        if "\n" in default_val:
                            default_val = default_val.split('\n', 1)[0]
                        # Remove potential post-lambda comments
                        default_val = default_val.rsplit('#', 1)[0]
                    # In case a function callback is used instead of lambda. (Haven't found an instance of it yet)
                    else:
                        default_val = default_val.__name__
                attributes.append(('default', f'{default_val}'))

            # Do field type specific adjustments for attributes (function -> compute, relational...)
            is_compute = field_data.__class__.__name__ == "function"
            is_related = field_data.__class__.__name__ == "related"
            # Selection
            if type == "selection":
                selection_val = field_data.selection if not callable(field_data.selection) else field_data.selection.__name__
                attributes.insert(1, ('selection', f'{selection_val}'))
            # Float
            if type == "float" and field_data.digits:
                attributes.insert(1, ('digits', f'{field_data.digits}'))
            # String fields
            if type in ["char", "selection", "text"] and field_data.size:
                attributes.insert(1, ('size', f'{field_data.size}'))
            if type in ["char", "text"] and field_data.translate:
                attributes.insert(1, ('translate', f'{field_data.translate}'))
            # Many2many
            if type == "many2many" and not is_compute:
                attributes.insert(1, ('column2', f'"{field_data._id2}"'))
                attributes.insert(1, ('column1', f'"{field_data._id1}"'))
                attributes.insert(1, ('relation', f'"{field_data._rel}"'))
            # One2many
            if type == "one2many":
                attributes.insert(1, ('inverse_name', f'"{field_data._fields_id}"'))
            # Many2one
            if type == "Many2one" and field_data.ondelete:
                attributes.insert(1, ('ondelete', f'"{field_data.ondelete}"'))
            # Relational
            if type in ["many2one", "one2many", "many2many"]:
                attributes.insert(1, ('comodel_name', f'"{field_data._obj}"'))

            if (is_related or is_compute) and field_data.store:
                attributes.insert(1, ('store', 'True'))
            # Related
            if is_related:
                attributes.insert(1, ('related', f'"{field_data._arg[0]}.{field_data._arg[1]}"'))
            # Compute
            if is_compute:
                if field_data._fnct_search:
                    attributes.insert(1, ('search', f'"{field_data._fnct_search.__name__}"'))
                if field_data._fnct_inv:
                    attributes.insert(1, ('inverse', f'"{field_data._fnct_inv.__name__}"'))
                attributes.insert(1, ('compute', f'"{field_data._fnct.__name__}"'))



            # Append new field definition
            fields_str += f"{field_name} = fields.{new_type}("
            for attr in attributes:
                fields_str += f"{attr[0]}={attr[1]}, "
            fields_str += ")\n"
            # Remove ", " in final attribute
            fields_str = ''.join(fields_str.rsplit(', ', 1))

        res["value"]["fields"] = fields_str
        # Return results
        return res

    _columns = {
        'fields': fields.text(
            string='Fields',
            readonly=True,
        ),
        'model_name': fields.char(
            size=128,
            string='Model name',
        ),
    }


model_columns()
