import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app
import os

os.environ["API_KEY"] = "testing"
os.environ["DATABASE_URL"] = "postgres://test:test@localhost:5432/test_db"

client = TestClient(app)

# Test headers with valid API key
VALID_HEADERS = {"X-API-KEY": "testing"}
INVALID_HEADERS = {"X-API-KEY": "invalid_key"}

class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_health_check(self):
        """Test health endpoint - no auth required"""
        response = client.get("/api/v1/healths/")
        assert response.status_code == 200
        assert response.json() == {"status": "You app has a good health ✅"}

class TestAuthenticationEndpoints:
    """Test authentication and security"""
    
    def test_views_with_valid_api_key(self):
        """Test secure view with valid API key"""
        response = client.get("/api/v1/views/", headers=VALID_HEADERS)
        assert response.status_code == 200
        assert response.json() == {"status": "You have access ✅"}
    
    def test_views_with_invalid_api_key(self):
        """Test secure view with invalid API key"""
        response = client.get("/api/v1/views/", headers=INVALID_HEADERS)
        assert response.status_code == 403
        assert "Invalid API Key" in response.json()["detail"]
    
    def test_views_without_api_key(self):
        """Test secure view without API key"""
        response = client.get("/api/v1/views/")
        assert response.status_code == 422

class TestSettingsEndpoints:
    """Test settings endpoints"""
    
    def test_get_settings(self):
        """Test getting settings with valid API key"""
        response = client.get("/api/v1/settings/", headers=VALID_HEADERS)
        assert response.status_code == 200
        assert response.json() == {"api_key": "test_api_key"}
    
    def test_get_settings_unauthorized(self):
        """Test getting settings without valid API key"""
        response = client.get("/api/v1/settings/", headers=INVALID_HEADERS)
        assert response.status_code == 403

class TestProductEndpoints:
    """Test product CRUD operations"""
    
    def test_get_all_products(self):
        """Test getting all products"""
        response = client.get("/api/v1/product/", headers=VALID_HEADERS)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) >= 4  # Initial inventory has 4 items
    
    def test_get_product_by_id(self):
        """Test getting a specific product by ID"""
        response = client.get("/api/v1/product/1", headers=VALID_HEADERS)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Product 1"
        assert data["price"] == 24.99
        assert data["in_stock"] == True
    
    def test_get_nonexistent_product(self):
        """Test getting a product that doesn't exist"""
        response = client.get("/api/v1/product/999", headers=VALID_HEADERS)
        assert response.status_code == 404
        assert "Product Not Found" in response.json()["detail"]
    
    def test_create_product(self):
        """Test creating a new product"""
        new_product = {
            "name": "Test Product",
            "price": 29.99,
            "in_stock": True,
            "discount": 5.0
        }
        response = client.post("/api/v1/product/create", 
                             json=new_product, 
                             headers=VALID_HEADERS)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "Product added successfully"
        assert "product_id" in data
        assert data["product"]["name"] == "Test Product"
    
    def test_create_product_invalid_data(self):
        """Test creating a product with invalid data"""
        invalid_product = {
            "name": "A",  # Too short (min_length=2)
            "price": 0.5,  # Too low (gt=1)
            "in_stock": True
        }
        response = client.post("/api/v1/product/create", 
                             json=invalid_product, 
                             headers=VALID_HEADERS)
        assert response.status_code == 422    

    def test_update_product(self):
        """Test updating an existing product"""
        updated_product = {
            "name": "Updated Product",
            "price": 39.99,
            "in_stock": False,
            "discount": 10.0
        }
        response = client.put("/api/v1/product/product/update/1", 
                            json=updated_product, 
                            headers=VALID_HEADERS)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "Product updated successfully"
        assert data["product"]["name"] == "Updated Product"
    
    def test_update_nonexistent_product(self):
        """Test updating a product that doesn't exist"""
        updated_product = {
            "name": "Updated Product",
            "price": 39.99,
            "in_stock": False
        }
        response = client.put("/api/v1/product/product/update/999", 
                            json=updated_product, 
                            headers=VALID_HEADERS)
        assert response.status_code == 404
        assert "Product Not Found" in response.json()["detail"]
    
    def test_delete_product(self):
        """Test deleting a product"""
        response = client.delete("/api/v1/product/product/remove/2", 
                               headers=VALID_HEADERS)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "Deleted product successfully"
        assert data["product_id"] == 2
        assert "deleted_product" in data
    
    def test_delete_nonexistent_product(self):
        """Test deleting a product that doesn't exist"""
        response = client.delete("/api/v1/product/product/remove/999", 
                               headers=VALID_HEADERS)
        assert response.status_code == 404
        assert "Product Not Found" in response.json()["detail"]
    
    def test_product_endpoints_unauthorized(self):
        """Test product endpoints without valid API key"""
        endpoints = [
            ("GET", "/api/v1/product/"),
            ("GET", "/api/v1/product/1"),
            ("POST", "/api/v1/product/create"),
            ("PUT", "/api/v1/product/product/update/1"),
            ("DELETE", "/api/v1/product/product/remove/1")
        ]
        
        for method, endpoint in endpoints:
            if method == "GET":
                response = client.get(endpoint, headers=INVALID_HEADERS)
            elif method == "POST":
                response = client.post(endpoint, json={}, headers=INVALID_HEADERS)
            elif method == "PUT":
                response = client.put(endpoint, json={}, headers=INVALID_HEADERS)
            elif method == "DELETE":
                response = client.delete(endpoint, headers=INVALID_HEADERS)
            
            assert response.status_code == 403

class TestDatabaseEndpoints:
    """Test database connection endpoints"""
    
    @patch('routers.connections.connections.get')
    def test_database_connection_success(self, mock_get_connection):
        """Test successful database connection"""
        # Mock the database connection
        mock_connection = AsyncMock()
        mock_connection.execute_query.return_value = (None, [["PostgreSQL 13.0"]])
        mock_get_connection.return_value = mock_connection
        
        response = client.get("/api/v1/database/", headers=VALID_HEADERS)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["message"] == "It works ✅"
        assert "database_info" in data
        assert "connection_url" in data
        assert "***:***" in data["connection_url"]  # Password should be masked
    
    @patch('routers.connections.connections.get')
    def test_database_connection_failure(self, mock_get_connection):
        """Test database connection failure"""
        # Mock connection failure
        mock_get_connection.side_effect = Exception("Connection failed")
        
        response = client.get("/api/v1/database/", headers=INVALID_HEADERS)
        assert response.status_code == 500
        assert "Database connection failed" in response.json()["detail"]
    
    def test_database_connection_unauthorized(self):
        """Test database connection without valid API key"""
        response = client.get("/api/v1/database/", headers=INVALID_HEADERS)
        assert response.status_code == 403

# Integration tests
class TestIntegrationScenarios:
    """Test complete workflows"""
    
    def test_product_lifecycle(self):
        """Test complete product CRUD lifecycle"""
        # Create a product
        new_product = {
            "name": "Lifecycle Test",
            "price": 15.99,
            "in_stock": True
        }
        create_response = client.post("/api/v1/product/create", 
                                    json=new_product, 
                                    headers=VALID_HEADERS)
        assert create_response.status_code == 200
        product_id = create_response.json()["product_id"]
        
        # Read the product
        read_response = client.get(f"/api/v1/product/{product_id}", 
                                 headers=VALID_HEADERS)
        assert read_response.status_code == 200
        assert read_response.json()["name"] == "Lifecycle Test"
        
        # Update the product
        updated_product = {
            "name": "Updated Lifecycle",
            "price": 25.99,
            "in_stock": False
        }
        update_response = client.put(f"/api/v1/product/update/{product_id}", 
                                   json=updated_product, 
                                   headers=VALID_HEADERS)
        assert update_response.status_code == 200
        assert update_response.json()["product"]["name"] == "Updated Lifecycle"
        
        # Delete the product
        delete_response = client.delete(f"/api/v1/product/remove/{product_id}", 
                                      headers=VALID_HEADERS)
        assert delete_response.status_code == 200
        
        # Verify deletion
        verify_response = client.get(f"/api/v1/product/{product_id}", 
                                   headers=VALID_HEADERS)
        assert verify_response.status_code == 404