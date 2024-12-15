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

### Material Management

Fields: material_code, material_name, material_type, material_buy_price, supplier_id.
Supplier

### Res Partner (For Supplier)

Fields: name

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
- Test Material Creation
- Ensure material is created with valid data.
- Verify material_buy_price < 100 fails validation.
- Test Fetching Materials
- Retrieve all materials.
- Apply filters to return materials of a specific type.
- Test Updating Materials
- Validate updates are applied correctly.
- Ensure updates fail for non-existent materials.
- Test Deleting Materials
- Verify deletion of an existing material.
- Attempt deletion of non-existent materials.

## Example Unit Test Code
```
from odoo.tests.common import TransactionCase

class TestMaterialManagement(TransactionCase):
    def setUp(self):
        super(TestMaterialManagement, self).setUp()
        self.supplier = self.env['res.partner'].create({'name': 'Test Supplier'})
        self.material = self.env['material.management'].create({
            'material_code': 'MAT001',
            'material_name': 'Test Material',
            'material_type': 'Fabric',
            'material_buy_price': 150,
            'supplier_id': self.supplier.id
        })

    def test_material_creation(self):
        material = self.env['material.management'].create({
            'material_code': 'MAT002',
            'material_name': 'Another Material',
            'material_type': 'Cotton',
            'material_buy_price': 200,
            'supplier_id': self.supplier.id
        })
        self.assertEqual(material.material_code, 'MAT002')

    def test_material_buy_price_validation(self):
        with self.assertRaises(Exception):
            self.env['material.management'].create({
                'material_code': 'MAT003',
                'material_name': 'Invalid Material',
                'material_type': 'Jeans',
                'material_buy_price': 50,
                'supplier_id': self.supplier.id
            })

    def test_filter_materials(self):
        materials = self.env['material.management'].search([('material_type', '=', 'Fabric')])
        self.assertTrue(len(materials) > 0)

    def test_update_material(self):
        self.material.write({'material_name': 'Updated Material'})
        self.assertEqual(self.material.material_name, 'Updated Material')

    def test_delete_material(self):
        self.material.unlink()
        materials = self.env['material.management'].search([('id', '=', self.material.id)])
        self.assertEqual(len(materials), 0)
```
