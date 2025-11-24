from flask import Flask, render_template, jsonify, request, session
from dao.juego_dao import JuegoDAO
import uuid
import os

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui_cambiarla'  # ⚠️ Cambiar en producción

# ✅ IMPORTANTE: Configurar carpeta estática (donde están las imágenes)
# Flask busca automáticamente en 'static/', pero lo definimos explícitamente
app.static_folder = 'static'
app.static_url_path = '/static'

# Inicializar DAO
juego_dao = JuegoDAO()

@app.route('/')
def index():
    """Página principal del juego"""
    # Generar ID de sesión único
    if 'id_sesion' not in session:
        session['id_sesion'] = str(uuid.uuid4())
    
    return render_template('juego.html')

@app.route('/api/iniciar_juego', methods=['POST'])
def iniciar_juego():
    """Inicia un nuevo juego"""
    id_sesion = session.get('id_sesion')
    data = request.get_json()
    nivel = data.get('nivel', 1)
    
    juego = juego_dao.crear_juego(id_sesion, nivel)
    tablero = juego_dao.obtener_tablero(id_sesion)
    
    return jsonify({
        'juego': juego.to_dict(),
        'tablero': tablero.to_dict(),
        'exito': True
    })

@app.route('/api/obtener_estado', methods=['GET'])
def obtener_estado():
    """Obtiene el estado actual del juego"""
    id_sesion = session.get('id_sesion')
    juego = juego_dao.obtener_juego(id_sesion)
    tablero = juego_dao.obtener_tablero(id_sesion)
    
    if not juego or not tablero:
        return jsonify({'exito': False, 'mensaje': 'No hay juego activo'})
    
    return jsonify({
        'juego': juego.to_dict(),
        'tablero': tablero.to_dict(),
        'exito': True
    })

@app.route('/api/voltear_carta', methods=['POST'])
def voltear_carta():
    """Voltea una carta"""
    id_sesion = session.get('id_sesion')
    data = request.get_json()
    posicion = data.get('posicion')
    
    juego = juego_dao.obtener_juego(id_sesion)
    
    if not juego:
        return jsonify({'exito': False, 'mensaje': 'No hay juego activo'})
    
    # Voltear la carta
    carta = juego_dao.voltear_carta(id_sesion, posicion)
    
    if carta is None:
        return jsonify({'exito': False, 'mensaje': 'No se puede voltear la carta'})
    
    # ✅ Agregar prefijo /static/ para que Flask sirva la imagen correctamente
    carta_url = f"/static/{carta}"
    
    return jsonify({
        'exito': True,
        'carta': carta_url,
        'cartas_volteadas': juego.cartas_volteadas,
        'puede_verificar': len(juego.cartas_volteadas) == 2
    })

@app.route('/api/verificar_pareja', methods=['POST'])
def verificar_pareja():
    """Verifica si las cartas volteadas son pareja"""
    id_sesion = session.get('id_sesion')
    
    resultado = juego_dao.verificar_pareja(id_sesion)
    juego = juego_dao.obtener_juego(id_sesion)
    
    if resultado is None:
        return jsonify({'exito': False, 'mensaje': 'Error al verificar pareja'})
    
    return jsonify({
        'exito': True,
        'es_pareja': resultado['es_pareja'],
        'juego_completado': resultado['juego_completado'],
        'juego': juego.to_dict()
    })

@app.route('/api/subir_nivel', methods=['POST'])
def subir_nivel():
    """Sube al siguiente nivel"""
    id_sesion = session.get('id_sesion')
    
    juego = juego_dao.subir_nivel(id_sesion)
    tablero = juego_dao.obtener_tablero(id_sesion)
    
    if not juego:
        return jsonify({'exito': False, 'mensaje': 'Error al subir de nivel'})
    
    return jsonify({
        'exito': True,
        'juego': juego.to_dict(),
        'tablero': tablero.to_dict()
    })

@app.route('/api/actualizar_tiempo', methods=['POST'])
def actualizar_tiempo():
    """Actualiza el tiempo del juego (llamado cada segundo desde el frontend)"""
    id_sesion = session.get('id_sesion')
    
    juego = juego_dao.reducir_tiempo(id_sesion)
    
    if not juego:
        return jsonify({'exito': False, 'mensaje': 'No hay juego activo'})
    
    return jsonify({
        'exito': True,
        'tiempo_restante': juego.tiempo_restante,
        'activo': juego.activo
    })

# ✅ Endpoint adicional para obtener todas las cartas del tablero (útil para debugging)
@app.route('/api/obtener_tablero', methods=['GET'])
def obtener_tablero_completo():
    """Obtiene todas las cartas del tablero (solo para desarrollo)"""
    id_sesion = session.get('id_sesion')
    tablero = juego_dao.obtener_tablero(id_sesion)
    
    if not tablero:
        return jsonify({'exito': False, 'mensaje': 'No hay tablero activo'})
    
    # Agregar prefijo /static/ a todas las cartas
    cartas_con_url = [f"/static/{carta}" for carta in tablero.cartas]
    
    return jsonify({
        'exito': True,
        'cartas': cartas_con_url,
        'filas': tablero.filas,
        'columnas': tablero.columnas
    })

if __name__ == '__main__':
    # ✅ Verificar que la carpeta de imágenes existe
    imagenes_path = os.path.join(app.static_folder, 'imagenes')
    if not os.path.exists(imagenes_path):
        print(f"⚠️ ADVERTENCIA: La carpeta {imagenes_path} no existe.")
        print(f"   Crea la carpeta y coloca las imágenes ahí:")
        print(f"   mkdir -p {imagenes_path}")
    else:
        # Listar imágenes disponibles
        imagenes = os.listdir(imagenes_path)
        print(f"✅ Imágenes encontradas: {imagenes}")
    
    app.run(debug=True)