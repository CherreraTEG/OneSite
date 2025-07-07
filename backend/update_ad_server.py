#!/usr/bin/env python3
"""
Script para actualizar el AD_SERVER en el archivo .env
"""

def update_ad_server():
    """Actualiza el AD_SERVER en el archivo .env"""
    
    try:
        # Leer el archivo .env
        with open('.env', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar la línea AD_SERVER
        old_line = 'AD_SERVER=10.50.5.200'
        new_line = 'AD_SERVER=ELT-DC1-MIA.elite.local'
        
        if old_line in content:
            content = content.replace(old_line, new_line)
            
            # Escribir el archivo actualizado
            with open('.env', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ AD_SERVER actualizado: {old_line} -> {new_line}")
            return True
        else:
            print("⚠️  No se encontró la línea AD_SERVER=10.50.5.200")
            return False
            
    except Exception as e:
        print(f"❌ Error al actualizar AD_SERVER: {e}")
        return False

if __name__ == "__main__":
    update_ad_server() 