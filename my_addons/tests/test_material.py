from odoo.tests.common import TransactionCase

class TestMaterial(TransactionCase):
    def setUp(self):
        super(TestMaterial, self).setUp()
        self.supplier = self.env['res.partner'].create({'name': 'Test Supplier', 'supplier': True})
        self.material = self.env['material.management'].create({
            'material_code': 'MAT001',
            'material_name': 'Test Material',
            'material_type': 'fabric',
            'material_buy_price': 200,
            'supplier_id': self.supplier.id
        })

    def test_material_creation(self):
        self.assertEqual(self.material.material_code, 'MAT001')
        self.assertEqual(self.material.material_type, 'fabric')

    def test_material_buy_price_constraint(self):
        with self.assertRaises(ValidationError):
            self.env['material.management'].create({
                'material_code': 'MAT002',
                'material_name': 'Invalid Material',
                'material_type': 'jeans',
                'material_buy_price': 50,
                'supplier_id': self.supplier.id
            })

    def test_material_update(self):
        self.material.write({'material_name': 'Updated Material'})
        self.assertEqual(self.material.material_name, 'Updated Material')

    def test_material_deletion(self):
        material_id = self.material.id
        self.material.unlink()
        self.assertFalse(self.env['material.management'].browse(material_id).exists())
