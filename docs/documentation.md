# URL Shortener System Documentation

## System Architecture

The URL shortener system consists of several microservices working together:

### 1. Key Generation Service (KGS)
- **Purpose**: Manages the pool of available short codes
- **Technology**: FastAPI + Redis
- **Key Features**:
  - Generates random 6-letter strings
  - Maintains two Redis sets:
    - `available_keys`: Unused short codes
    - `used_keys`: Currently used short codes
  - Ensures uniqueness of short codes
  - Automatically replenishes key pool

### 2. URL Service
- **Purpose**: Handles URL shortening and redirection
- **Technology**: FastAPI + PostgreSQL + Redis
- **Key Features**:
  - Creates shortened URLs
  - Handles URL lookups
  - Manages URL expiration
  - Tracks click analytics

### 3. Database Architecture

#### PostgreSQL (Permanent Storage)
```python
class URLModel:
    id: Integer
    original_url: String(2048)
    short_code: String(10)
    created_at: DateTime
    clicks: Integer
    is_expired: Boolean
    expiry_date: DateTime
    is_one_time: Boolean
    is_active: Boolean
```
- Stores all URL data permanently
- Tracks analytics and metadata
- Ensures data persistence

#### Redis (Caching & KGS)
1. **URL Caching**:
   - Fast lookups for active URLs
   - Reduces database load
   - Temporary storage

2. **KGS Storage**:
   - Manages available/used keys
   - Ensures key uniqueness
   - Fast key operations

### 4. Service Flow

#### URL Creation
1. Request short code from KGS
2. Save URL data to PostgreSQL
3. Cache URL data in Redis

#### URL Lookup
1. Check Redis cache first
2. If not found, query PostgreSQL
3. If found, cache in Redis
4. Increment click counter

#### URL Deletion
1. Delete from PostgreSQL
2. Remove from Redis cache
3. Return short code to KGS

### 5. API Endpoints

#### KGS API
- `GET /codes`: Get available short codes
- `POST /codes/return`: Return used code to pool
- `GET /health`: Health check

#### URL Service API
- `POST /urls`: Create shortened URL
- `GET /{short_code}`: Redirect to original URL
- `DELETE /urls/{short_code}`: Delete shortened URL
- `GET /urls/{short_code}/analytics`: Get URL analytics

### 6. Kubernetes Deployment

The system is deployed on Kubernetes with the following components:
- KGS deployment (2 replicas)
- URL service deployment
- PostgreSQL statefulset
- Redis statefulset
- ConfigMaps for configuration
- Services for internal communication

### 7. Best Practices

1. **Single Source of Truth**:
   - Shared Redis client
   - Centralized configuration
   - Consistent error handling

2. **Caching Strategy**:
   - Redis for fast lookups
   - PostgreSQL for persistence
   - KGS for key management

3. **Error Handling**:
   - Graceful degradation
   - Proper error responses
   - Circuit breakers

4. **Monitoring**:
   - Health checks
   - Metrics collection
   - Logging

### 8. Development Guidelines

1. **Code Organization**:
   ```
   backend/
   ├── database/
   │   ├── models.py      # SQLAlchemy models
   │   ├── redis_client.py # Redis operations
   │   └── db.py          # Database connection
   ├── kgs/
   │   └── main.py        # KGS service
   └── services/
       └── url_service.py # URL service
   ```

2. **Client Libraries**:
   - Use client libraries for service communication
   - Avoid direct HTTP calls
   - Handle connection management

3. **Testing**:
   - Unit tests for each component
   - Integration tests for services
   - End-to-end tests for flows 

### 9. Future Considerations

#### 1. Authentication & Authorization
- User authentication system
- API key management
- Rate limiting per user/IP
- Role-based access control
- JWT token implementation

#### 2. Error Handling & Logging
- Centralized error handling middleware
- Structured logging system
- Error tracking (e.g., Sentry integration)
- Log aggregation
- Error reporting and alerts

#### 3. Monitoring & Metrics
- Health check endpoints for all services
- Prometheus metrics collection
- Grafana dashboards for:
  - URL creation/lookup rates
  - Cache hit/miss ratios
  - Error rates
  - Response times
- Resource usage monitoring
- Alerting system

#### 4. Security
- Input validation middleware
- CORS configuration
- Security headers
- SQL injection prevention
- XSS protection
- Rate limiting
- IP blocking
- SSL/TLS configuration

#### 5. Configuration Management
- Environment variables management
- Config files for different environments
- Secrets management in Kubernetes
- Feature flags
- Service discovery

#### 6. API Documentation
- OpenAPI/Swagger documentation
- API versioning strategy
- Request/response examples
- Error code documentation
- API usage guidelines

#### 7. Background Tasks
- URL expiration cleanup job
- Analytics aggregation
- Cache invalidation
- Database maintenance
- Key pool maintenance

#### 8. Testing Strategy
- Unit tests for all components
- Integration tests for services
- End-to-end tests
- Load testing
- Security testing
- Performance testing

#### 9. Deployment & CI/CD
- Automated testing pipeline
- Deployment strategies
- Rollback procedures
- Blue-green deployments
- Canary releases

#### 10. Disaster Recovery
- Backup strategies
- Recovery procedures
- Data retention policies
- High availability setup
- Failover procedures

### 10. Implementation Priority

#### High Priority
1. Authentication & Authorization
2. Error Handling & Logging
3. Security
4. Monitoring & Metrics

#### Medium Priority
1. API Documentation
2. Configuration Management
3. Background Tasks
4. Testing Strategy

#### Low Priority
1. Deployment & CI/CD
2. Disaster Recovery
3. Advanced Monitoring
4. Performance Optimization 