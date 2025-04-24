import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Get allowed namespaces from environment variable
ALLOWED_NAMESPACES = os.getenv('ALLOWED_NAMESPACES').split(',')

@app.route('/validate', methods=['POST'])
def validate():
    request_info = request.get_json()
    namespace= request_info['request']['namespace']
    pod = request_info['request']['object']
    tolerations = pod.get('spec', {}).get('tolerations', [])

 
    # Check if the namespace is in the list of allowed namespaces
    if namespace not in ALLOWED_NAMESPACES:
        # If namespace is not allowed, we prevent scheduling on the L40S GPU node)
        gpu_toleration = next(
            (toleration for toleration in tolerations 
                if toleration.get('key') == 'nvidia.com/gpu.product' and toleration.get('value') == 'NVIDIA-L40S'),
            None
        )
        
        if gpu_toleration:
            return deny(f"Namespace '{namespace}' is not allowed to be scheduled on the L40S GPU node.")
    else:
        # If the namespace is in the allowed list, we restrict it to L40S GPU only
        gpu_toleration = next(
            (toleration for toleration in tolerations 
                if toleration.get('key') == 'nvidia.com/gpu.product' and toleration.get('value') == 'NVIDIA-L40S'),
            None
        )
        
        if not gpu_toleration:
            return deny(f"Namespace '{namespace}' can only be scheduled on the L40S GPU node. Please include the correct toleration to your deployment.")

    return allow()

def allow():
    return jsonify({
        "response": {
            "allowed": True,
            "status": {"message": "Your namespace is allowed to be scheduled on the L40S GPU node."}
        }
    })

def deny(message):
    return jsonify({
        "response": {
            "allowed": False,
            "status": {
                "message": message
            }
        }
    })

def start_validator():
    app.run(
    host='0.0.0.0',
    port=443,
    ssl_context=(
        '/etc/certs/tls.crt',
        '/etc/certs/tls.key'
        )
    )

if __name__ == "__main__":
    start_validator()




