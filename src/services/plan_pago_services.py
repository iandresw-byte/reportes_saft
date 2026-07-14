
from datetime import datetime
import os
import webbrowser
from dateutil.relativedelta import relativedelta
import threading
from pandas import DataFrame
from src.repositories.planes_pago_repository import PlanesPagoRepository
from src.ui.modals.confirma_anula_pp_modal import abrir_modal_anular_pp
from src.ui.modals.datos_actualizados_modal import abrir_datos_actualizados
from src.reports.pfds.rpt_plan_pago_anulado import PlanDePagoReport
from src.utils.config_manager import Config
RESULTADO_DIR = Config.obtener("RUTAS", "carpeta_reportes")

class PlanesPagoService:
    def __init__(self, conexion , sistem,municipalidad, admin_municipio):
        self.repo = PlanesPagoRepository(conexion)
        self.system = sistem
        self.muni= municipalidad
        self.admin = admin_municipio

    def anular_plan_de_pago(self,vista, num_plan_pago):

        plan_pago = self.repo.get_data_plan_pago(num_plan_pago)

        if not plan_pago:
            vista.dialog = abrir_datos_actualizados(vista,None, "Plan de Pago Anulado",  f"No se encontro Informacion para el Plan de Pago Numero {num_plan_pago}")
            vista.page.open(vista.dialog)
            vista.page.update()
            raise ValueError("Respauesta Vacia")
        
        if plan_pago["EstadoPP"] != 0:
            if plan_pago["EstadoPP"] ==1:
                estado = "Anulado"
            elif plan_pago["EstadoPP"] == 2:
                estado = "Pagado"
            else:
                estado="No Definido"
            vista.dialog = abrir_datos_actualizados(vista,None, "Plan de Pago Anulado",  f"El plan de pago numero {num_plan_pago} se encuentra {estado}")
            vista.page.open(vista.dialog)
            vista.page.update()
            raise ValueError(
                "Plan de Pago se encuentra anulafo")
        
        facturas_en_pp = self.repo.obtener_facturas_en_plan_pago(num_plan_pago)
        cuotas_pp = self.repo.obtener_cuotas_plan_pago(num_plan_pago)

        if not facturas_en_pp:
            vista.dialog = abrir_datos_actualizados(vista,None, "Plan de Pago Anulado",  f"No se Encontraron Facturas en Plan de Pago Asociadas a Este Numero de Plan de Pago {num_plan_pago} , (Respuesta vacía).")
            vista.page.open(vista.dialog)
            vista.page.update()
            raise ValueError(
                "No se Facturas de Cuotas de Plan de Pago Asociadas a Este Numero de Plan de Pago, (Respuesta vacía).")

        if not cuotas_pp:
            vista.dialog = abrir_datos_actualizados(vista,None, "Plan de Pago Anulado",  f"No se Facturas de Cuotas de Plan de Pago Asociadas a Este Numero de Plan de Pago {num_plan_pago} , (Respuesta vacía).")
            vista.page.open(vista.dialog)
            vista.page.update()
            raise ValueError(
                "No se Facturas de Cuotas de Plan de Pago Asociadas a Este Numero de Plan de Pago, (Respuesta vacía).")
        
        resultado = {
        "total_pp_pagado":0,
        "total_pp_vencido":0,
        "total_pp_vigente":0,
        "total_pp_pagado_tentativo":0,
        "total_fnp_cubre" : 0 ,
        "total_fnp_no_cubre" :0,
        "total_residuo_pagado":0,
        "total_residuo_vencido":0,
        "num_avpg_add":0,
        "num_avpg_res":0,
        "cant_fnp_cubre":0,
        "cant_fnp_no_cubre":0,
        }
        cuota_pp_pagada = []
        cuota_pp_vencida = []
        cuota_pp_vigente = []
        cuota_fnp_mantiene = []
        cuota_fnp_activar = []

        evento = threading.Event()
        opcion_calculo = None

        def respuesta_modal(opcion):
            nonlocal opcion_calculo
            opcion_calculo = opcion
            evento.set()

        
        for cuota in cuotas_pp:
            if cuota["AvPgEstado"]==2:
                resultado["total_pp_pagado"]+=cuota["ValorCouta"]
                cuota["srtEstado"] = "Pagada"
                cuota["srObservacion"] = "Cuota Pagada, Mantiene Estado"
                cuota_pp_pagada.append(cuota)
            else:
                if cuota["MesesVencidos"]>= 0:
                    resultado["total_pp_vencido"]+=cuota["ValorCouta"]
                    cuota["srtEstado"] = "No Pagada"
                    cuota["srObservacion"] = "Vencida, Cambio Anulada"
                    cuota_pp_vigente.append(cuota)
                else:
                    resultado["total_pp_vigente"]+=cuota["ValorCouta"]
                    cuota["srtEstado"] = "No Pagada"
                    cuota["srObservacion"] = "Al Dia, No Se Puede Anular"
                    cuota_pp_vencida.append(cuota)
        
        if len(cuota_pp_vigente)>=0 and resultado["total_pp_vigente"]>0:
            vista.dialog = abrir_datos_actualizados(vista,None, "Plan de Pago Anulado",  f"El Plan de Pago Numero {num_plan_pago} tiene cuotas vigentes")
            vista.page.open(vista.dialog)
            vista.page.update()
            raise ValueError("Plan de Pago Anulado",  f"El Plan de Pago Numero {num_plan_pago} tiene cuotas vigentes")
            
        if len(cuota_pp_vigente)==0 and len(cuota_pp_vencida)==0 and  len(cuota_pp_pagada)==len(cuotas_pp):
            vista.dialog = abrir_datos_actualizados(vista,None, "Plan de Pago Anulado",  f"El Plan de Pago Numero {num_plan_pago} tiene todas las cuotas pagadas")
            vista.page.open(vista.dialog)
            vista.page.update()
            raise ValueError(
                "Las Cuotas del Plan de Pago se Encuentan Pagadas")
        

        for factura in facturas_en_pp:
   
            if resultado["total_fnp_cubre"]+factura["valorFacturaenPP"]<=resultado["total_pp_pagado"] and resultado["total_residuo_pagado"] == 0:
                resultado["total_fnp_cubre"]+=factura["valorFacturaenPP"]
                cuota_fnp_mantiene.append(factura)
                resultado["num_avpg_add"] = factura["NumAvPg"]
                factura["strEstado"] = "En Pp"
            else:
                if resultado["num_avpg_res"] == 0:
                    resultado["total_residuo_pagado"] = resultado["total_pp_pagado"]-resultado["total_fnp_cubre"]
                    resultado["total_residuo_vencido"] = factura["valorFacturaenPP"]-resultado["total_residuo_pagado"]
                    resultado["num_avpg_res"] = factura["NumAvPg"]
                    resultado["total_fnp_no_cubre"]=0
                    resultado["total_pp_pagado_tentativo"]=resultado["total_pp_pagado"]+resultado["total_residuo_pagado"]
                    factura["strEstado"] = "Restar"
                    
                else:
                    resultado["total_fnp_no_cubre"]+=factura["valorFacturaenPP"]
                    cuota_fnp_activar.append(factura)
                    factura["strEstado"] = "Activar"
       


        avpg_det_suma = self.repo.get_factura_detalle(resultado["num_avpg_add"])
        avpg_det_esta = self.repo.get_factura_detalle(resultado["num_avpg_res"])
        
        if not avpg_det_suma:
            vista.dialog = abrir_datos_actualizados(vista,None, "Plan de Pago Anulado",  f"El Plan de Pago Numero {num_plan_pago} No se encontro la ultima factura para modificar.")
            vista.page.open(vista.dialog)
            vista.page.update()
            raise ValueError("No se encontro la factura para modificar.")
        total_detalle = sum(item["ValorUnitAvPgDet"] for item in avpg_det_suma)
        
        for cuenta in avpg_det_suma:
            porcentaje = cuenta["ValorUnitAvPgDet"]/total_detalle
            cuenta["porcentaje"] = porcentaje
            cuenta["valor_distribuido"] = porcentaje * resultado["total_residuo_pagado"]
            cuenta["nuevo_valor"] = cuenta["ValorUnitAvPgDet"] + cuenta["valor_distribuido"]

    



        if not avpg_det_esta:
            vista.dialog = abrir_datos_actualizados(vista,None, "Plan de Pago Anulado",  f"No se encontro la primer factura que cambia de estado para modificar su valor")
            vista.page.open(vista.dialog)
            vista.page.update()
            raise ValueError("No se encontro la factura para modificar.")
        total_detalle = sum(item["ValorUnitAvPgDet"] for item in avpg_det_esta)
        for cuenta in avpg_det_esta:
            porcentaje = cuenta["ValorUnitAvPgDet"]/total_detalle
            cuenta["porcentaje"] = porcentaje
            cuenta["valor_distribuido"] = porcentaje  * resultado["total_residuo_pagado"]
            cuenta["nuevo_valor"] = cuenta["ValorUnitAvPgDet"] - cuenta["valor_distribuido"]
      
        
        df_esta = DataFrame(avpg_det_esta)
        df_suma = DataFrame(avpg_det_suma)
  
        df_plan = DataFrame([plan_pago])

        df_plan["Nombre_Completo"] = (
        df_plan["PNombre"].fillna('') + ' ' +
        df_plan["SNombre"].fillna('') + ' ' +
        df_plan["PApellido"].fillna('') + ' ' +
        df_plan["SApellido"].fillna('')
        ).str.replace(r'\s+', ' ', regex=True).str.strip()

        resultado["cant_fnp_cubre"]=len(cuota_fnp_mantiene)
        resultado["cant_fnp_no_cubre"]=len(cuota_fnp_activar)
        
        df_cuotas = DataFrame(cuotas_pp)
        df_facturas = DataFrame(facturas_en_pp)
  
        vista.dialog = abrir_modal_anular_pp(vista, resultado, df_cuotas, df_facturas, df_plan, respuesta_modal)
        vista.page.open(vista.dialog)
        vista.page.update()
        evento.wait()

        if opcion_calculo == "ACEPTAR":
            for factura in cuota_fnp_activar:
                print(factura)
                self.repo.reversar_factura_en_pp(num_plan_pago, factura["NumAvPg"])
            self.repo.anular_cuota_pp(num_plan_pago)
            self.repo.anular_num_plan(num_plan_pago)
            self.repo.reversar_factura_en_pp(num_plan_pago, resultado["num_avpg_res"])

            for avpg_det in avpg_det_suma:
                self.repo.modificar_ultima_factura_plan_pago(avpg_det["nuevo_valor"],avpg_det["NumAvPg"],avpg_det["CtaIngreso"],)
            
            for avpg_det in avpg_det_esta:
                self.repo.modificar_ultima_factura_plan_pago(avpg_det["nuevo_valor"],avpg_det["NumAvPg"],avpg_det["CtaIngreso"],)

            
            vista.dialog = abrir_datos_actualizados(vista,None,"Plan de Pago Anulado", f"El plan de pago numero {num_plan_pago} ha sido anulado")
            vista.page.open(vista.dialog)
            vista.page.update()
         
            # nombre_archivo = "Plan_de_Pago-Anulado.pdf"
            # if RESULTADO_DIR:
            #     carpeta_pdf = os.path.join(RESULTADO_DIR, "pdf")
            #     os.makedirs(carpeta_pdf, exist_ok=True)
            #     ruta = os.path.join(carpeta_pdf, nombre_archivo)
            # else:
            #     carpeta_pdf = os.path.join(os.getcwd(), "res", "pdf")
            #     os.makedirs(carpeta_pdf, exist_ok=True)
            #     ruta = os.path.join(carpeta_pdf, nombre_archivo)
            # documento = PlanDePagoReport(self.muni, self.admin, "Plan de Pago Anulado",df_cuotas,df_facturas, df_plan, df_suma, df_esta, resultado) # type: ignore
            # documento.generar_pdf(ruta)
            # webbrowser.open_new_tab(f"file://{ruta}")
        elif opcion_calculo == "CANCELAR":
            raise ValueError(
                "Anulacion Cancelada") 
            




        

        