import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src.config import Config
from src.database import Database

# Importar blueprints
from src.routes.auth import auth_bp
from src.routes.clientes import clientes_bp
from src.routes.leads import leads_bp
from src.routes.licitacoes import licitacoes_bp
from src.routes.dashboard import dashboard_bp
from src.routes.ia import ia_bp
from src.routes.documentos import documentos_bp
from src.routes.whatsapp import whatsapp_bp
from src.routes.integracoes import integracoes_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configurações
app.config.from_object(Config)

# CORS
CORS(app, origins=Config.CORS_ORIGINS)

# JWT
jwt = JWTManager(app)

# Inicializar banco de dados
db_instance = Database()

# Registrar blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(clientes_bp, url_prefix='/api/clientes')
app.register_blueprint(leads_bp, url_prefix='/api/leads')
app.register_blueprint(licitacoes_bp, url_prefix='/api/licitacoes')
app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
app.register_blueprint(ia_bp, url_prefix='/api/ia')
app.register_blueprint(documentos_bp, url_prefix='/api/documentos')
app.register_blueprint(whatsapp_bp, url_prefix='/api/whatsapp')
app.register_blueprint(integracoes_bp, url_prefix='/api/integracoes')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint de verificação de saúde"""
    return {"status": "ok", "message": "VIP Mudanças API está funcionando"}, 200

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """Servir arquivos estáticos do frontend"""
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

# Criar usuário admin padrão
@app.before_request
def create_default_user():
    """Criar usuário admin padrão"""
    if not hasattr(app, '_user_created'):
        from src.models.user import User
        
        # Verificar se já existe usuário admin
        try:
            admin_user = User.collection.find_one({"email": "admin@vipmudancas.com.br"})
            if not admin_user:
                User.create_user(
                    email="admin@vipmudancas.com.br",
                    password="vip123456",
                    name="Administrador VIP",
                    role="admin"
                )
                print("Usuário admin padrão criado: admin@vipmudancas.com.br / vip123456")
        except Exception as e:
            print(f"Erro ao criar usuário admin: {e}")
        
        app._user_created = True

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

