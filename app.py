from flask import Flask, render_template, jsonify, request, session
from dao.juego_dao import JuegoDAO
import uuid

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui_cambiarla'  # Cambiar en producción

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
    
    carta = juego_dao.voltear_carta(id_sesion, posicion)
    juego = juego_dao.obtener_juego(id_sesion)
    
    if carta is None:
        return jsonify({'exito': False, 'mensaje': 'No se puede voltear la carta'})
    
    return jsonify({
        'exito': True,
        'carta': carta,
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
    """Actualiza el tiempo del juego"""
    id_sesion = session.get('id_sesion')
    
    juego = juego_dao.reducir_tiempo(id_sesion)
    
    if not juego:
        return jsonify({'exito': False, 'mensaje': 'No hay juego activo'})
    
    return jsonify({
        'exito': True,
        'tiempo_restante': juego.tiempo_restante,
        'activo': juego.activo
    })

if __name__ == '__main__':
    app.run(debug=True)