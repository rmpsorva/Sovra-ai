# client_test.py
import grpc
import json
import adaptiveservice_pb2
import adaptiveservice_pb2_grpc

def run_client():
    try:
        # Conexión al canal gRPC (no HTTP)
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = adaptiveservice_pb2_grpc.AdaptiveAuraServiceStub(channel)
            
            print("🧪 Probando servidor Aura AI...")
            
            # Test 1: Ejecutar método adaptativo
            print("\n1. 🔄 Ejecutando método adaptativo (process_data)...")
            response = stub.AdaptiveExecute(adaptiveservice_pb2.ExecutionRequest(
                method_name="process_data",
                args_json={
                    'args': json.dumps(['hello', 'world', 2, 3]),
                    'kwargs': json.dumps({})
                }
            ))
            print(f"Resultado: {json.loads(response.result_json)}")
            print(f"Estado: {response.status}")
            
            # Test 2: Auto-optimización
            print("\n2. 🔧 Activando auto-optimización (performance)...")
            opt_response = stub.SelfOptimize(adaptiveservice_pb2.OptimizationRequest(
                target="performance"
            ))
            print(f"Mensaje: {opt_response.message}")
            
            # Test 3: Obtener métricas
            print("\n3. 📊 Obteniendo métricas IA...")
            metrics_response = stub.GetMetrics(adaptiveservice_pb2.MetricsRequest())
            metrics = json.loads(metrics_response.metrics_json)
            print(f"Métricas (Optimizations: {len(metrics.get('optimization_history', []))}):")
            print(json.dumps(metrics, indent=2))
            
    except grpc.RpcError as e:
        print(f"\n❌ ERROR de gRPC: Asegúrese de que 'aura_grpc_server.py' esté corriendo.")
        print(f"Detalle: {e.details()}")

if __name__ == '__main__':
    run_client()
