from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestMaterialManagement(TransactionCase):
    def setUp(self):
        super(TestMaterialManagement, self).setUp()

        # Create a test supplier with realistic data based on the res.partner structure
        self.supplier = self.env['res.partner'].create({
            'name': 'Test Supplier',
            'email': 'test_supplier@example.com',
            'phone': '1234567890',
            'is_company': True,
            'street': '123 Test Street',
            'city': 'Test City',
            'zip': '12345',
            'country_id': self.env.ref('base.us').id,
            'active': True,
        })

        # Create a test material
        self.material = self.env['material.management'].create({
            'material_code': 'MAT001',
            'material_name': 'Test Material',
            'material_type': 'fabric',
            'material_buy_price': 150,
            'supplier_id': self.supplier.id,
        })

    def test_get_all_materials(self):
        """Test retrieving all materials."""
        all_materials = self.env['material.management'].search([])
        self.assertIn(self.material, all_materials)
        self.assertGreaterEqual(len(all_materials), 1)
        print('Get All Material OK')

    def test_material_creation(self):
        """Test the creation of a material."""
        material = self.env['material.management'].create({
            'material_code': 'MAT002',
            'material_name': 'New Material',
            'material_type': 'jeans',
            'material_buy_price': 200,
            'supplier_id': self.supplier.id,
        })
        self.assertEqual(material.material_code, 'MAT002')
        self.assertEqual(material.material_buy_price, 200)
        print('Create Data Material OK')

    def test_material_buy_price_validation(self):
        """Test that material_buy_price cannot be less than 100."""
        with self.assertRaises(ValidationError):
            self.env['material.management'].create({
                'material_code': 'MAT003',
                'material_name': 'Invalid Material',
                'material_type': 'cotton',
                'material_buy_price': 50,  # Invalid value
                'supplier_id': self.supplier.id,
            })
        print('Invalid Buy Price Validation OK')

    def test_material_update(self):
        """Test updating an existing material."""
        self.material.write({
            'material_name': 'Updated Material',
            'material_buy_price': 250,
        })
        self.assertEqual(self.material.material_name, 'Updated Material')
        self.assertEqual(self.material.material_buy_price, 250)
        print('Update Data Material OK')

    def test_material_deletion(self):
        """Test deleting a material."""
        material_id = self.material.id
        self.material.unlink()
        material = self.env['material.management'].search([('id', '=', material_id)])
        self.assertFalse(material)
        print('Delete Data Material OK')

    def test_material_filter_by_type(self):
        """Test filtering materials by type."""
        fabric_materials = self.env['material.management'].search([('material_type', '=', 'fabric')])
        self.assertIn(self.material, fabric_materials)
        print('Filter Data Material OK')

    def test_supplier_relation(self):
        """Test the relation between material and supplier."""
        self.assertEqual(self.material.supplier_id, self.supplier)
        self.assertEqual(self.material.supplier_id.name, 'Test Supplier')
        print('Test Supplier Relation With Material OK')
