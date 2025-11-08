# aura_grpc_server.py
import grpc
import time
import json
from concurrent import futures
import sys

# Importar archivos generados por protoc
try:
    import adaptiveservice_pb2
    import adaptiveservice_pb2_grpc
except ImportError:
    print("❌ ERROR: Los archivos gRPC (*_pb2.py) no se han generado. Ejecute el comando protoc.")
    sys.exit(1)

# Importar el sistema NeuroSynapse y DataProcessor
from NEUROSYNAPSE_CORE import neuro, DataProcessor

class EnhancedSystemSingleton:
    """Gestiona el sistema potenciado por IA"""
    def __init__(self):
        self.original_system = DataProcessor()
        # El sistema se adapta al iniciar el servidor
        self.system = neuro.adapt(self.original_system, "DynamicProcessor", "extreme")

SYSTEM_MANAGER = EnhancedSystemSingleton()

class AdaptiveAuraServicer(adaptiveservice_pb2_grpc.AdaptiveAuraServiceServicer):
    
    def AdaptiveExecute(self, request, context):
        """Ejecuta métodos a través del sistema IA"""
        system = SYSTEM_MANAGER.system
        
        try:
            args_data = json.loads(request.args_json.get('args', '[]'))
            kwargs_data = json.loads(request.args_json.get('kwargs', '{}'))
            
            # Llamada directa al método inyectado por Aura AI
            result = system.adaptive_execute(
                request.method_name, 
                *args_data, 
                **kwargs_data
            )
            
            return adaptiveservice_pb2.ExecutionResponse(
                result_json=json.dumps(result),
                status="EXECUTED_ADAPTIVELY",
                optimization_notes=f"Método '{request.method_name}' optimizado por IA"
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error: {e}")
            return adaptiveservice_pb2.ExecutionResponse(status="ERROR")

    def SelfOptimize(self, request, context):
        """Auto-optimización del sistema"""
        try:
            optimized_system = SYSTEM_MANAGER.system.self_optimize(request.target)
            SYSTEM_MANAGER.system = optimized_system
            
            return adaptiveservice_pb2.OptimizationResponse(
                message=f"Sistema optimizado para: {request.target}",
                original_hash=str(hash(str(SYSTEM_MANAGER.original_system))),
                optimized_hash=str(hash(str(SYSTEM_MANAGER.system)))
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error: {e}")
            return adaptiveservice_pb2.OptimizationResponse(message="Error")

    def GetMetrics(self, request, context):
        """Obtiene métricas del sistema IA"""
        metrics = SYSTEM_MANAGER.system.get_ai_metrics()
        return adaptiveservice_pb2.MetricsResponse(
            metrics_json=json.dumps(metrics)
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    adaptiveservice_pb2_grpc.add_AdaptiveAuraServiceServicer_to_server(
        AdaptiveAuraServicer(), server)
    
    server.add_insecure_port('[::]:50051')
    server.start()
    print("\n=======================================================")
    print("🚀 SERVIDOR AURA AI - MODO AUTOSUFICIENTE (gRPC) INICIADO")
    print("Puerto de comunicación binaria: 50051")
    print("=======================================================\n")
    
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
