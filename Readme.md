# Odoo 14 Backend Module: Material Management Test
## Overview
This module is designed for managing materials in Odoo 14, enabling users to register, view, update, delete, and filter materials. The module meets the client requirements, which include handling material data with the following fields:

- Material Code
- Material Name
- Material Type (Dropdown: Fabric, Jeans, Cotton)
- Material Buy Price (Minimum value: 100)
- Related Supplier (Dropdown: Supplier names)

Additionally, users can perform the following operations:

- View all materials with filtering based on Material Type.
- Update an existing material.
- Delete a material.

## Entity-Relationship Diagram (ERD)
The ERD consists of the following entities:

![alt text](https://github.com/maulanayudha021/module-test-odoo-14/blob/main/erd.png?raw=true)

## Features
1. Material CRUD Operations
- Create Material: Ensures all fields are filled and material_buy_price >= 100.
- Read Materials: Fetches all materials or filters by material_type.
- Update Material: Allows modifications to an existing material.
- Delete Material: Removes a material entry.

2. Filtering
- Filter materials based on their material_type (Fabric, Jeans, Cotton).


## Installation
- Clone this repository to your Odoo addons folder.
- Restart the Odoo server.
- Install the module via the Odoo Apps interface.


## REST API Endpoints
1. Get All Materials
GET /api/materials
Returns all materials.

Response Example:
```
{
    "jsonrpc": "2.0",
    "id": null,
    "result": [
        {
            "id": 5,
            "material_code": "MAT001",
            "material_name": "Fabric Material",
            "material_type": "fabric",
            "material_buy_price": 150.0,
            "supplier": {
                "id": 1,
                "name": "YourCompany",
                "create_date": "2024-12-15 07:06:06",
                "display_name": "YourCompany",
                "lang": "en_US",
                "website": "http://www.example.com",
                "function": false,
                "type": "contact",
                "street": "250 Executive Park Blvd, Suite 3400",
                "street2": false,
                "zip": "94134",
                "city": "San Francisco",
                "partner_latitude": 0.0,
                "partner_longitude": 0.0,
                "email": "myudha317@gmail.com",
                "phone": "082246718208",
                "is_company": true,
                "commercial_partner_id": 1,
                "commercial_company_name": "YourCompany"
            }
        }
    ]
}
```

2. Get Single Material
GET /api/materials/<id>
Returns a single material.

Response Example:
```
{
    "jsonrpc": "2.0",
    "id": null,
    "result": {
        "id": 9,
        "material_code": "MAT005",
        "material_name": "Cotton Material",
        "material_type": "cotton",
        "material_buy_price": 150.0,
        "supplier": {
            "id": 1,
            "name": "YourCompany",
            "create_date": "2024-12-15 07:06:06",
            "display_name": "YourCompany",
            "lang": "en_US",
            "website": "http://www.example.com",
            "function": false,
            "type": "contact",
            "street": "250 Executive Park Blvd, Suite 3400",
            "street2": false,
            "zip": "94134",
            "city": "San Francisco",
            "partner_latitude": 0.0,
            "partner_longitude": 0.0,
            "email": "myudha317@gmail.com",
            "phone": "082246718208",
            "is_company": true,
            "commercial_partner_id": 1,
            "commercial_company_name": "YourCompany"
        }
    }
}
```

2. Create Material
POST /api/materials
Creates a new material.

Payload Example:
```
{
    "material_code": "MAT001",
    "material_name": "Cotton Cloth",
    "material_type": "Cotton",
    "material_buy_price": 150,
    "supplier_id": 1
}
```

3. Update Material
PUT /api/materials/<id>
Updates an existing material.

Payload Example:
```
{
    "material_name": "Updated Cotton Cloth",
    "material_buy_price": 200
}
```

4. Delete Material
DELETE /api/materials/<id>
Deletes a material.

5. Filter Materials by Type
GET /api/materials/filter
Filters materials based on material_type.

Payload Example:
```
{
    "material_type": "Fabric"
}
```

## Unit Testing
### Test Cases
The following test cases ensure the module's functionality:
- Test Supplier Creation
- Test Material Creation
- Test Get All Material
- Test Other Material Creation
- Test Invalid Buy Price
- Test Updating Materials
- Test Deleting Materials
- Test Material Filter
- Test Supplier Relation with Material

## Unit Test Code
```
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
        print('Create Data Supplier OK')

        # Create a test material
        self.material = self.env['material.management'].create({
            'material_code': 'MAT001',
            'material_name': 'Test Material',
            'material_type': 'fabric',
            'material_buy_price': 150,
            'supplier_id': self.supplier.id,
        })
        print('Create Data Material OK')

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
        print('Create Other Data Material OK')

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
```

![alt text](https://github.com/maulanayudha021/module-test-odoo-14/blob/main/unit_testing.png?raw=true)