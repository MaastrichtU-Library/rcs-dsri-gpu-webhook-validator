import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Get allowed namespaces from environment variable
ALLOWED_NAMESPACES = os.getenv('ALLOWED_NAMESPACES').split(',')

@app.route('/validate', methods=['POST'])
def validate():
    request_info = request.get_json()
    uid = request_info['request']['uid']
    namespace= request_info['request']['namespace']
    pod = request_info['request']['object']
    tolerations = pod.get('spec', {}).get('tolerations', [])

    allowed = True
    reason = ""

    # Check if the namespace is in the list of allowed namespaces
    if namespace not in ALLOWED_NAMESPACES:
        # If namespace is not allowed, we prevent scheduling on the L40S GPU node)
        gpu_toleration = next(
            (toleration for toleration in tolerations 
                if toleration.get('key') == 'nvidia.com/gpu.product' and toleration.get('value') == 'NVIDIA-L40S'),
            None
        )
        
        if gpu_toleration:
            allowed = False
            reason = (f"Namespace '{namespace}' is not allowed to be scheduled on the L40S GPU node.")
    else:
        # If the namespace is in the allowed list, we restrict it to L40S GPU only
        gpu_toleration = next(
            (toleration for toleration in tolerations 
                if toleration.get('key') == 'nvidia.com/gpu.product' and toleration.get('value') == 'NVIDIA-L40S'),
            None
        )
        
        if not gpu_toleration:
            allowed = False
            reason = (f"Namespace '{namespace}' can only be scheduled on the L40S GPU node. Please include the correct toleration in your deployment.")

    admission_response = {
        "apiVersion": "admission.k8s.io/v1",
        "kind": "AdmissionReview",
        "response": {
            "uid": uid,  # Include the UID from the request to match it with the incoming request
            "allowed": allowed,
            "status": {
                "reason": reason
            } if not allowed else {}
        }
    }

    return jsonify(admission_response)