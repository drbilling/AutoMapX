from flask import Flask, render_template, request, jsonify, send_file
from modules.git_handler import clone_repo, list_files
from modules.azure_handler import connect_to_azure, list_azure_repos
from modules.dependency_mapper import map_dependencies
from modules.visualizer import visualize_dependencies
from modules.exporter import export_to_csv, export_to_excel, export_to_pdf
from modules.logger import logger
from config import Config, allowed_file

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/repos', methods=['POST'])
def get_repos():
    data = request.json
    repo_url = data.get('repo_url')
    if not repo_url:
        return jsonify({'error': 'Repository URL is required'}), 400
    try:
        repo = clone_repo(repo_url, app.config['REPO_DIR'])
        files = list_files(repo)
        return jsonify(files)
    except Exception as e:
        logger.error(f"Error cloning repo: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/azure-repos', methods=['POST'])
def get_azure_repos():
    data = request.json
    personal_access_token = data.get('pat')
    organization_url = data.get('org_url')
    if not personal_access_token or not organization_url:
        return jsonify({'error': 'PAT and Organization URL are required'}), 400
    try:
        connection = connect_to_azure(personal_access_token, organization_url)
        repos = list_azure_repos(connection)
        return jsonify(repos)
    except Exception as e:
        logger.error(f"Error connecting to Azure DevOps: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/dependencies', methods=['GET'])
def get_dependencies():
    try:
        dependencies = map_dependencies(app.config['REPO_DIR'])
        visualize_dependencies(dependencies)
        return jsonify(dependencies)
    except Exception as e:
        logger.error(f"Error mapping dependencies: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/download/<file_type>', methods=['GET'])
def download_file(file_type):
    try:
        dependencies = map_dependencies(app.config['REPO_DIR'])
        if file_type == 'csv':
            export_to_csv(dependencies)
            return send_file('dependencies.csv', as_attachment=True)
        elif file_type == 'excel':
            export_to_excel(dependencies)
            return send_file('dependencies.xlsx', as_attachment=True)
        elif file_type == 'pdf':
            export_to_pdf(dependencies)
            return send_file('dependencies.pdf', as_attachment=True)
        else:
            return jsonify({'error': 'Invalid file type'}), 400
    except Exception as e:
        logger.error(f"Error exporting file: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
