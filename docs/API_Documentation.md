# API Documentation

## Overview

This API provides a wallet management system built with FastAPI. It allows users to create wallets, manage addresses, perform transactions, and access their transaction history. The API is designed to be secure, efficient, and easy to use.

## Base URL

```
http://localhost:8000
```

## Authentication

### Token Generation

To access protected endpoints, users must authenticate and obtain a JWT token.

**Endpoint**: `/token`  
**Method**: `POST`  
**Request Body**:
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

**Response**:
```json
{
    "access_token": "your_jwt_token",
    "token_type": "bearer"
}
```

## User Management

### Register User

**Endpoint**: `/register`  
**Method**: `POST`  
**Request Body**:
```json
{
    "username": "your_username",
    "email": "your_email@example.com",
    "full_name": "Your Full Name",
    "password": "your_password"
}
```

**Response**:
```json
{
    "username": "your_username",
    "email": "your_email@example.com",
    "full_name": "Your Full Name"
}
```

### Get User Addresses

**Endpoint**: `/addresses`  
**Method**: `GET`  
**Headers**:
```
Authorization: Bearer your_jwt_token
```

**Response**:
```json
[
    {
        "address": "address_1",
        "balance": 100.0
    },
    {
        "address": "address_2",
        "balance": 50.0
    }
]
```

### Create Address

**Endpoint**: `/addresses`  
**Method**: `POST`  
**Headers**:
```
Authorization: Bearer your_jwt_token
```

**Response**:
```json
{
    "address": "new_address",
    "balance": 0.0
}
```

### Delete Address

**Endpoint**: `/addresses/{address}`  
**Method**: `DELETE`  
**Headers**:
```
Authorization: Bearer your_jwt_token
```

**Response**:
```json
{
    "success": true,
    "message": "Address deleted successfully"
}
```

## Transaction Management

### Create Transaction

**Endpoint**: `/transactions`  
**Method**: `POST`  
**Headers**:
```
Authorization: Bearer your_jwt_token
```

**Request Body**:
```json
{
    "from_address": "source_address",
    "to_address": "destination_address",
    "amount": 10.0
}
```

**Response**:
```json
{
    "success": true,
    "message": "Transaction successful"
}
```

### Get Transaction History

**Endpoint**: `/transactions`  
**Method**: `GET`  
**Headers**:
```
Authorization: Bearer your_jwt_token
```

**Response**:
```json
[
    {
        "transaction_id": "tx_1",
        "from_address": "source_address",
        "to_address": "destination_address",
        "amount": 10.0,
        "timestamp": "2023-10-01T12:00:00Z"
    },
    {
        "transaction_id": "tx_2",
        "from_address": "source_address",
        "to_address": "another_address",
        "amount": 5.0,
        "timestamp": "2023-10-02T12:00:00Z"
    }
]
```

### Get Balance

**Endpoint**: `/balance/{address}`  
**Method**: `GET`  
**Headers**:
```
Authorization: Bearer your_jwt_token
```

**Response**:
```json
{
    "balance": 100.0
}
```

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of requests. Common error responses include:

- **400 Bad Request**: Invalid input or missing required fields.
- **401 Unauthorized**: Invalid or missing authentication token.
- **404 Not Found**: Resource not found (e.g., address or user).
- **500 Internal Server Error**: Unexpected server error.

**Error Response Format**:
```json
{
    "detail": "Error message",
    "status_code": 400
}
```

## Health Check

### Health Check Endpoint

**Endpoint**: `/health`  
**Method**: `GET`  

**Response**:
```json
{
    "status": "healthy"
}
```

## Conclusion

This API provides a robust and secure way to manage wallets and transactions. For further information or support, please refer to the project documentation or contact the development team.
