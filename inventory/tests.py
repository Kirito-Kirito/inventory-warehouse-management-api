from django.contrib.auth import get_user_model
User = get_user_model()
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Category, Product, Supplier, Warehouse


class ProductAPITests(APITestCase):

    def setUp(self):
        # Create Test User
        self.normal_user = User.objects.create_user(
            username='NormalUser', password='testpassword123',
            )
        self.staff_user = User.objects.create_user(
            username='StaffUser',password='testpassword123',is_staff=True
            )

        
        # Create Test Category and Supplier
        self.category = Category.objects.create(name='Electronic') 
        self.supplier = Supplier.objects.create(name='Lin')
        self.warehouse = Warehouse.objects.create(name='MainWarehouse')

        # Create Test Products
        self.product1 = Product.objects.create(
            sku='SKU001',
            name='Laptop',
            category=self.category,
            supplier=self.supplier,
            current_stock=3,
            unit_price=1200.00,
        )
        self.product2 = Product.objects.create(
            sku='SKU002',
            name='Mouse',
            category=self.category,
            supplier=self.supplier,
            current_stock=25,
            unit_price=25.00,
        )
        #Taking JWT Token URL
        self.token_url = reverse('token_obtain_pair')
        self.product_url = 'http://127.0.0.1:8000/api/v1/products/'
    def authenticate_with_credentials(self, username, password):
        #Login and Taking 'access' and 'refresh' token
        response = self.client.post(
            self.token_url,
            {'username':username,'password':password}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']
        #Authorization Header for any request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def authenticate_as_normal_user(self):
        self.authenticate_with_credentials('NormalUser','testpassword123')

    def authenticate_as_staff_user(self):
        self.authenticate_with_credentials('StaffUser','testpassword123')

    def test_create_product(self):
        self.authenticate_as_normal_user()
        initial_count = Product.objects.count()
        payload = {
            'sku': 'SKU003',
            'name': 'Keyboard',
            'category':self.category.id,
            'supplier':self.supplier.id,
            'current_stock':15,
            'unit_price':75.00
        }
        response = self.client.post(self.product_url,payload,format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), initial_count + 1)
        self.assertEqual(response.data['name'], 'Keyboard')

    def test_partial_update_product(self):
        self.authenticate_as_normal_user()
        url = f'{self.product_url}{self.product1.id}/'
        payload = {
            'name': 'Tablet',
            'current_stock': 8,
        }
        response = self.client.patch(url,payload,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        self.product1.refresh_from_db()
        self.assertEqual(self.product1.name, 'Tablet')
        self.assertEqual(self.product1.current_stock, 8)

    def test_partial_update_exist_sku_product(self):
        self.authenticate_as_normal_user()
        url = f'{self.product_url}{self.product1.id}/'
        payload = {
            'sku': 'SKU002',
            'name': 'Tablet',
            'current_stock': 8,
        }
        response = self.client.patch(url,payload,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_get_product_list(self):
        self.authenticate_as_normal_user()
        response = self.client.get(self.product_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results',response.data)),2)

    def test_get_category(self):
        self.authenticate_as_normal_user()
        response = self.client.get('http://127.0.0.1:8000/api/v1/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results',response.data)),1)

    def test_low_stock_alert_endpoint(self):
        self.authenticate_as_normal_user()
        low_stock_url = 'http://127.0.0.1:8000/api/v1/products/low-stock/'
        response = self.client.get(low_stock_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get('results', response.data)
        self.assertEqual(len(results),1)
        self.assertEqual(results[0]['name'], 'Laptop')

    def test_low_stock_custom_threshold(self):
        self.authenticate_as_normal_user()
        url = f'{self.product_url}low-stock/?threshold=5'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get('results',response.data)
        self.assertEqual(len(results),1)
        self.assertEqual(results[0]['name'], 'Laptop')

    def test_unauthenticated_access_denied(self):
        self.client.credentials()

        response = self.client.get(self.product_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_product_search_by_name(self):
        self.authenticate_as_normal_user()
        url = f'{self.product_url}?search=Mouse'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get('results', response.data)
        self.assertEqual(len(results),1)
        self.assertEqual(results[0]['name'], 'Mouse')

    def test_get_nonexistent_product_id_return_404(self):
        self.authenticate_as_normal_user()
        url = f'{self.product_url}9999/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_stock_movement(self):
        self.authenticate_as_staff_user()
        stock_movement_url = 'http://127.0.0.1:8000/api/v1/movements/'
        payload = {
            'product': self.product1.id,
            'warehouse': self.warehouse.id,
            'quantity': 7,
            'movement_type': 'IN',
        }

        response = self.client.post(stock_movement_url, payload, format='json')
        # print('STATUS:', response.status_code, 'DATA:', response.data)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])

        self.product1.refresh_from_db()
        self.assertEqual(self.product1.current_stock, 10)

    def test_regular_user_cannot_delete_product_with_token(self):
        self.authenticate_as_normal_user()
        url = f'{self.product_url}{self.product1.id}/'

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Product.objects.filter(pk=self.product1.id).exists())

    def test_staff_user_can_delete_product(self):
        self.authenticate_as_staff_user()
        url = f'{self.product_url}{self.product1.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product1.id).exists())

    def test_stock_out_exceeding_current_stock_fails(self):
        self.authenticate_as_staff_user()
        stock_movement_url = 'http://127.0.0.1:8000/api/v1/movements/'
        payload = {
            'product': self.product1.id,
            'warehouse': self.warehouse.id,
            'quantity': 5,
            'movement_type': 'OUT',
        }
        response = self.client.post(stock_movement_url,payload,format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.current_stock, 3)

    def test_stock_out_exact_current_stock_succeeds_and_becomes_zero(self):
        self.authenticate_as_staff_user()
        stock_movement_url = 'http://127.0.0.1:8000/api/v1/movements/'
        payload = {
            'product': self.product1.id,
            'warehouse': self.warehouse.id,
            'quantity': 3,
            'movement_type': 'OUT',
        }
        response = self.client.post(stock_movement_url,payload,format='json')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.current_stock,0)


    def test_stock_out_zero_or_negative_quantity_fails(self):
        self.authenticate_as_staff_user()
        stock_movement_url = 'http://127.0.0.1:8000/api/v1/movements/'
        for invalid_qty in [0, -2]:
            payload = {
                'product': self.product1.id,
                'warehouse': self.warehouse.id,
                'quantity': invalid_qty,
                'movement_type': 'OUT',
            }
            response = self.client.post(stock_movement_url,payload,format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.product1.refresh_from_db()
        self.assertEqual(self.product1.current_stock,3)