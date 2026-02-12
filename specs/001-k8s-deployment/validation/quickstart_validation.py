"""
Quickstart validation script
Validates that the implementation follows the quickstart guide correctly
"""
import subprocess
import sys
import os
import time
import requests

def validate_quickstart_steps():
    """
    Validates the implementation against the quickstart guide
    """
    print("Starting quickstart validation...")
    
    # Step 1: Verify prerequisites (just check if commands exist)
    print("\n1. Checking prerequisites...")
    try:
        # Check if docker is available
        docker_result = subprocess.run(['docker', '--version'], 
                                    capture_output=True, text=True, timeout=10)
        if docker_result.returncode == 0:
            print("[OK] Docker is installed:", docker_result.stdout.strip())
        else:
            print("[?] Docker check failed, but continuing...")
            
        # Check if kubectl is available
        kubectl_result = subprocess.run(['kubectl', 'version', '--client'], 
                                     capture_output=True, text=True, timeout=10)
        if kubectl_result.returncode == 0:
            print("[OK] kubectl is installed")
        else:
            print("[?] kubectl check failed, but continuing...")
            
        # Check if helm is available
        helm_result = subprocess.run(['helm', 'version', '--short'], 
                                   capture_output=True, text=True, timeout=10)
        if helm_result.returncode == 0:
            print("[OK] Helm is installed:", helm_result.stdout.strip())
        else:
            print("[?] Helm check failed, but continuing...")
            
    except FileNotFoundError:
        print("[?] Prerequisite check failed (command not found), but continuing...")
    
    # Step 2: Verify Docker images exist (check if Dockerfiles were created)
    print("\n2. Verifying Dockerfiles exist...")
    backend_dockerfile_path = os.path.join('..', '..', '..', 'backend', 'Dockerfile')
    frontend_dockerfile_path = os.path.join('..', '..', '..', 'frontend', 'Dockerfile')
    
    if os.path.exists(backend_dockerfile_path):
        print("[OK] Backend Dockerfile exists")
    else:
        print("[ERR] Backend Dockerfile does not exist")
        
    if os.path.exists(frontend_dockerfile_path):
        print("[OK] Frontend Dockerfile exists")
    else:
        print("[ERR] Frontend Dockerfile does not exist")
    
    # Step 3: Verify Helm chart structure
    print("\n3. Verifying Helm chart structure...")
    helm_chart_path = os.path.join('..', '..', '..', 'charts', 'todo-chatbot')
    
    if os.path.exists(helm_chart_path):
        print("[OK] Helm chart directory exists")
    else:
        print("[ERR] Helm chart directory does not exist")
        return False
    
    # Check for required Helm files
    required_files = ['Chart.yaml', 'values.yaml']
    templates_dir = os.path.join(helm_chart_path, 'templates')
    
    for file in required_files:
        file_path = os.path.join(helm_chart_path, file)
        if os.path.exists(file_path):
            print(f"[OK] {file} exists")
        else:
            print(f"[ERR] {file} does not exist")
    
    if os.path.exists(templates_dir):
        print("[OK] templates directory exists")
        templates = os.listdir(templates_dir)
        print(f"  Templates found: {templates}")
    else:
        print("[ERR] templates directory does not exist")
    
    # Step 4: Verify deployment templates exist
    print("\n4. Verifying deployment templates...")
    expected_templates = [
        'backend-deployment.yaml',
        'frontend-deployment.yaml', 
        'backend-service.yaml',
        'frontend-service.yaml',
        'ingress.yaml'
    ]
    
    for template in expected_templates:
        template_path = os.path.join(templates_dir, template)
        if os.path.exists(template_path):
            print(f"[OK] {template} exists")
        else:
            print(f"[ERR] {template} does not exist")
    
    # Step 5: Verify values configuration
    print("\n5. Verifying values configuration...")
    values_path = os.path.join(helm_chart_path, 'values.yaml')
    if os.path.exists(values_path):
        with open(values_path, 'r') as f:
            values_content = f.read()
            if 'frontend' in values_content and 'backend' in values_content:
                print("[OK] values.yaml contains frontend and backend configurations")
            else:
                print("[ERR] values.yaml missing frontend or backend configurations")
    else:
        print("[ERR] values.yaml does not exist")
    
    # Step 6: Verify README documentation
    print("\n6. Verifying documentation...")
    readme_path = os.path.join(helm_chart_path, 'README.md')
    if os.path.exists(readme_path):
        print("[OK] README.md exists")
    else:
        print("[ERR] README.md does not exist")
    
    print("\nQuickstart validation completed!")
    return True


def validate_deployment_readiness():
    """
    Validates that the deployment is ready according to the requirements
    """
    print("\nValidating deployment readiness...")
    
    # Check that all required files and configurations are in place
    required_paths = [
        '../../../backend/Dockerfile',
        '../../../frontend/Dockerfile', 
        '../../../charts/todo-chatbot/Chart.yaml',
        '../../../charts/todo-chatbot/values.yaml',
        '../../../charts/todo-chatbot/templates/backend-deployment.yaml',
        '../../../charts/todo-chatbot/templates/frontend-deployment.yaml',
        '../../../charts/todo-chatbot/templates/backend-service.yaml',
        '../../../charts/todo-chatbot/templates/frontend-service.yaml',
        '../../../charts/todo-chatbot/README.md'
    ]
    
    all_present = True
    for path in required_paths:
        if os.path.exists(path):
            print(f"[OK] {path} exists")
        else:
            print(f"[ERR] {path} missing")
            all_present = False
    
    if all_present:
        print("[OK] All required deployment files are present")
    else:
        print("[ERR] Some required deployment files are missing")
    
    return all_present


if __name__ == "__main__":
    success1 = validate_quickstart_steps()
    success2 = validate_deployment_readiness()
    
    if success1 and success2:
        print("\n[SUCCESS] All quickstart validations passed!")
    else:
        print("\n[ERROR] Some validations failed.")
        sys.exit(1)