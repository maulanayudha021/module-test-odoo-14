from odoo import http
from odoo.http import request
import json

class MaterialController(http.Controller):
    @http.route('/api/materials', type='json', auth='public', methods=['GET'], csrf=False)
    def get_materials(self):
        """Fetch all materials."""
        materials = request.env['material.management'].sudo().search([])
        result = []
        for material in materials:
            supplier = material.supplier_id
            supplier_data = {
                'id': supplier.id,
                'name': supplier.name,
                'create_date': supplier.create_date,
                'display_name': supplier.display_name,
                'lang': supplier.lang,
                'website': supplier.website,
                'function': supplier.function,
                'type': supplier.type,
                'street': supplier.street,
                'street2': supplier.street2,
                'zip': supplier.zip,
                'city': supplier.city,
                'partner_latitude': supplier.partner_latitude,
                'partner_longitude': supplier.partner_longitude,
                'email': supplier.email,
                'phone': supplier.phone,
                'is_company': supplier.is_company,
                'commercial_partner_id': supplier.commercial_partner_id.id if supplier.commercial_partner_id else None,
                'commercial_company_name': supplier.commercial_company_name
            } if supplier else None

            result.append({
                'id': material.id,
                'material_code': material.material_code,
                'material_name': material.material_name,
                'material_type': material.material_type,
                'material_buy_price': material.material_buy_price,
                'supplier': supplier_data
            })
        return result

    @http.route('/api/materials/<int:id>', type='json', auth='public', methods=['GET'], csrf=False)
    def get_material_by_id(self, id):
        """Fetch material by ID."""
        material = request.env['material.management'].sudo().browse(id)
        if not material.exists():
            return {'error': 'Material not found'}

        supplier = material.supplier_id
        supplier_data = {
            'id': supplier.id,
            'name': supplier.name,
            'create_date': supplier.create_date,
            'display_name': supplier.display_name,
            'lang': supplier.lang,
            'website': supplier.website,
            'function': supplier.function,
            'type': supplier.type,
            'street': supplier.street,
            'street2': supplier.street2,
            'zip': supplier.zip,
            'city': supplier.city,
            'partner_latitude': supplier.partner_latitude,
            'partner_longitude': supplier.partner_longitude,
            'email': supplier.email,
            'phone': supplier.phone,
            'is_company': supplier.is_company,
            'commercial_partner_id': supplier.commercial_partner_id.id if supplier.commercial_partner_id else None,
            'commercial_company_name': supplier.commercial_company_name
        } if supplier else None

        return {
            'id': material.id,
            'material_code': material.material_code,
            'material_name': material.material_name,
            'material_type': material.material_type,
            'material_buy_price': material.material_buy_price,
            'supplier': supplier_data
        }

    @http.route('/api/materials', type='json', auth='public', methods=['POST'], csrf=False)
    def create_material(self):
        """Create a new material."""
        data = request.jsonrequest
        material = request.env['material.management'].sudo().create(data)
        return {'id': material.id, 'message': 'Material created successfully'}

    @http.route('/api/materials/<int:id>', type='json', auth='public', methods=['PUT'], csrf=False)
    def update_material(self, id):
        """Update an existing material."""
        data = request.jsonrequest
        material = request.env['material.management'].sudo().browse(id)
        if not material.exists():
            return {'error': 'Material not found'}
        material.write(data)
        return {'message': 'Material updated successfully'}

    @http.route('/api/materials/<int:id>', type='json', auth='public', methods=['DELETE'], csrf=False)
    def delete_material(self, id):
        """Delete a material."""
        material = request.env['material.management'].sudo().browse(id)
        if not material.exists():
            return {'error': 'Material not found'}
        material.unlink()
        return {'message': 'Material deleted successfully'}

    @http.route('/api/materials/filter', type='json', auth='public', methods=['GET'], csrf=False)
    def filter_materials(self):
        """Filter materials by type."""
        material_type = request.jsonrequest.get('material_type')
        materials = request.env['material.management'].sudo().search([('material_type', '=', material_type)])
        result = []
        for material in materials:
            supplier = material.supplier_id
            supplier_data = {
                'id': supplier.id,
                'name': supplier.name,
                'create_date': supplier.create_date,
                'display_name': supplier.display_name,
                'lang': supplier.lang,
                'website': supplier.website,
                'function': supplier.function,
                'type': supplier.type,
                'street': supplier.street,
                'street2': supplier.street2,
                'zip': supplier.zip,
                'city': supplier.city,
                'partner_latitude': supplier.partner_latitude,
                'partner_longitude': supplier.partner_longitude,
                'email': supplier.email,
                'phone': supplier.phone,
                'is_company': supplier.is_company,
                'commercial_partner_id': supplier.commercial_partner_id.id if supplier.commercial_partner_id else None,
                'commercial_company_name': supplier.commercial_company_name
            } if supplier else None

            result.append({
                'id': material.id,
                'material_code': material.material_code,
                'material_name': material.material_name,
                'material_type': material.material_type,
                'material_buy_price': material.material_buy_price,
                'supplier': supplier_data
            })
        return result
