# services/products/project/tests/test_products.py


import json
import unittest

from project.tests.base import BaseTestCase

from project import db
from project.api.models import Product


def add_product(nombre, cantidad, serie, modelo, marca):
    product = Product(
        nombre=nombre,
        cantidad=cantidad,
        serie=serie,
        modelo=modelo,
        marca=marca
    )
    db.session.add(product)
    db.session.commit()
    return product


class TestProductService(BaseTestCase):
    """Pruebas para el Servicio de Productos """

    def test_products(self):
        """comprobado que la ruta /ping funcione correctamente."""
        response = self.client.get('/products/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('Conectado exitosamente!', data['mensaje'])
        self.assertIn('satisfactorio', data['estado'])

    def test_add_product(self):
        """ Asegurando que se pueda agregar
         un nuevo producto a la base de datos"""
        with self.client:
            response = self.client.post(
                '/products',
                data=json.dumps({
                    'nombre': 'Sansung',
                    'cantidad': 12,
                    'serie': 'MK3526',
                    'modelo': 'S4',
                    'marca': 'xiomi'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('Sansung se ha agregado!!!', data['mensaje'])

    def test_add_product_invalid_json(self):
        """  Asegurando de que se lance un error
         cuando el objeto JSON esta vacío."""
        with self.client:
            response = self.client.post(
                '/products',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Carga inválida.', data['mensaje'])

    def test_add_product_invalid_json_keys(self):
        """Asegurando de que se produce un error si el
         objeto JSON no tiene una clave de nombre de
          producto."""
        with self.client:
            response = self.client.post(
                '/products',
                data=json.dumps({'nombre': 'Sansung'}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Carga inválida.', data['mensaje'])

    def test_add_product_duplicate_name(self):
        """Asegurando que se produce un error si
         el nombre ya existe."""
        with self.client:
            self.client.post(
                '/products',
                data=json.dumps({
                    'nombre': 'Sansung',
                    'cantidad': 12,
                    'serie': 'MK3526',
                    'modelo': 'S4',
                    'marca': 'xiomi'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/products',
                data=json.dumps({
                    'nombre': 'Sansung',
                    'cantidad': 12,
                    'serie': 'MK3526',
                    'modelo': 'S4',
                    'marca': 'xiomi'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('El nombre ya existe.', data['mensaje'])
            self.assertIn('falló', data['estado'])

    def test_single_product(self):
        """Asegurando que el producto único se comporte
         correctamente."""
        product = add_product('Sansung', 12, 'MK3526', 'S4', 'xiomi')
        with self.client:
            response = self.client.get(f'/products/{product.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Sansung', data['data']['nombre'])
            self.assertEqual(12, data['data']['cantidad'])
            self.assertEqual('MK3526', data['data']['serie'])
            self.assertIn(
                'S4',
                data['data']['modelo'])
            self.assertIn(
                'xiomi',
                data['data']['marca']
                )

    def test_single_product_no_id(self):
        """Asegúrese de que se arroje un error si
         no se proporciona una identificación."""
        with self.client:
            response = self.client.get('/products/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn(
                'El producto no existe',
                data['mensaje']
                )
            self.assertIn('falló', data['estado'])

    def test_single_product_incorrect_id(self):
        """Asegurando de que se arroje un error si
         la identificación no existe."""
        with self.client:
            response = self.client.get('/products/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('El producto no existe', data['mensaje'])

    def test_all_products(self):
        """Asegurando obtener todos los productos
         correctamente."""
        add_product('Sansung', 12, 'MK3526', 'S4', 'xiomi')
        add_product('ipone', 12, 'JJ3526', 'M5', 'apple')
        with self.client:
            response = self.client.get('/products')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['products']), 2)
            self.assertIn(
                'Sansung',
                data['data']['products'][0]['nombre']
                )
            self.assertEqual(
                12,
                data['data']['products'][0]['cantidad']
                )
            self.assertEqual(
                'MK3526',
                data['data']['products'][0]['serie']
                )
            self.assertIn(
                'S4',
                data['data']['products'][0]['modelo']
                )
            self.assertIn(
                'xiomi',
                data['data']['products'][0]['marca']
                )
            self.assertIn(
                'ipone',
                data['data']['products'][1]['nombre']
                )
            self.assertEqual(
                12,
                data['data']['products'][1]['cantidad']
                )
            self.assertEqual(
                'JJ3526',
                data['data']['products'][1]['serie']
                )
            self.assertIn(
                'M5',
                data['data']['products'][1]['modelo']
                )
            self.assertIn(
                'apple',
                data['data']['products'][1]['marca']
                )

    def test_main_no_products(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Products', response.data)
        self.assertIn(b'<p>No hay productos!</p>', response.data)

    def test_main_with_products(self):
        """Asegura que la ruta principal actua
         correctamente cuando hay productos en la
          base de datos"""
        add_product('lg', 16, 'M6', 'lg300', 'lg')
        add_product('ulefone', 30, 'f5', 'ule365', 'ulefone')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Products', response.data)
            self.assertNotIn(b'<p>No hay productos!</p>', response.data)
            self.assertIn(b'lg', response.data)
            self.assertIn(b'ulefone', response.data)

    def test_main_add_product(self):
        """Asegura que un nuevo producto puede ser
         agregado a la db"""
        with self.client:
            response = self.client.post(
                '/',
                data=dict(
                    nombre='xiomi',
                    cantidad=5,
                    serie='S2',
                    modelo='LC04',
                    marca='xiomi'
                    ),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Products', response.data)
            self.assertNotIn(
                b'<p>No hay productos!</p>',
                response.data
                )
            self.assertIn(b'xiomi', response.data)


if __name__ == '__main__':
    unittest.main()
