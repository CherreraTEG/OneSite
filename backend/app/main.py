from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.core.config import settings
from app.api.v1.api import api_router
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import time

# Configurar rate limiter global
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para el sistema OneSite",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar rate limiter en la aplicación
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

print("CORS_ORIGINS:", settings.CORS_ORIGINS)

# Middleware de hosts confiables (recomendado para producción)
# app.add_middleware(TrustedHostMiddleware, allowed_hosts=["teg.1sitesoft.com", "localhost", "127.0.0.1"])

# Middleware CORS ultra-simple - intercepta TODAS las solicitudes
@app.middleware("http")
async def ultra_simple_cors(request: Request, call_next):
    # Para solicitudes OPTIONS, responder inmediatamente
    if request.method == "OPTIONS":
        from fastapi.responses import Response
        response = Response(status_code=200, content="")
        response.headers["Access-Control-Allow-Origin"] = "*"  # Permitir todos los orígenes temporalmente
        response.headers["Access-Control-Allow-Methods"] = "*"  # Permitir todos los métodos
        response.headers["Access-Control-Allow-Headers"] = "*"  # Permitir todos los headers
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Max-Age"] = "86400"  # Cache por 24 horas
        return response
    
    # Para todas las demás requests
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"  # Permitir todos los orígenes temporalmente
    response.headers["Access-Control-Allow-Credentials"] = "true"
    
    return response

# Middleware de headers de seguridad
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    # Headers de seguridad
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; img-src 'self' data: https://fastapi.tiangolo.com; font-src 'self' https://cdn.jsdelivr.net"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    
    # Header de tiempo de respuesta
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    return response


# Middleware de logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Obtener información del cliente
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    
    # Procesar la request
    response = await call_next(request)
    
    # Calcular tiempo de respuesta
    process_time = time.time() - start_time
    
    # Log de la request (sin información sensible)
    print(f"{client_ip} - {request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    
    return response

# CORS Middleware deshabilitado temporalmente para usar middleware personalizado
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.CORS_ORIGINS,
#     allow_credentials=settings.CORS_CREDENTIALS,
#     allow_methods=settings.CORS_METHODS,
#     allow_headers=settings.CORS_HEADERS,
#     expose_headers=["X-Total-Count"],
#     max_age=3600
# )

# Incluir las rutas API
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a OneSite API",
        "version": settings.VERSION,
        "status": "operational"
    }

@app.get("/test")
async def test_endpoint():
    """Endpoint simple de prueba"""
    return {"status": "ok", "message": "Test successful"}

@app.options("/test")
async def test_options():
    """Maneja peticiones OPTIONS para CORS"""
    return {"status": "ok"}

@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud del sistema"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": settings.VERSION
    }

@app.options("/health")
async def health_options():
    """Maneja peticiones OPTIONS para CORS"""
    return {"status": "ok"}

@app.head("/health")  
async def health_head():
    """Maneja peticiones HEAD"""
    return {"status": "ok"} 