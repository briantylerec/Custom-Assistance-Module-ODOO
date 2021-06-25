import datetime
from osv import osv, fields
import time

class mdlFaltasDetalle(osv.Model):
    _name = 'mdl.faltas.detalle'
    _columns = dict(
        registro_id = fields.many2one('mdl.faltas','Lectura'),
        employee_id = fields.many2one('hr.employee', 'Empleado'),
        cedula = fields.char('Cedula',size=15),
        nombre = fields.char('Nombre',size=50),
        fecha = fields.date('Fecha',size=32),
        departamento = fields.char('Dep.',size=64),
        dep_superior = fields.char('Dep. Sup.',size=64),
    )
mdlFaltasDetalle()

class mdlFaltas(osv.Model):
    _name = 'mdl.faltas'
    _columns = dict(
        lectura_id = fields.one2many('mdl.faltas.detalle','registro_id','Detalle Faltas'),
        fecha=fields.date('Fecha',size=32),
    )

    def calcular_faltas(self, cr, uid, ids, context = None):
        #search    select
        #update    update
        #unlink    delete
        #browse    objeto    

        registro_mdl = self.pool.get('mdl.registro.asistencia')
        faltas_mdl = self.pool.get('mdl.faltas.detalle')
        contrato_mdl = self.pool.get('hr.contract')
                        
        for this in self.browse(cr, uid, ids):
            contratos = contrato_mdl.search(cr, uid, [('activo','=',True)])
            
            if contratos:
                for contrato_id in contratos:

                    contrato = contrato_mdl.browse(cr,uid, contrato_id)

                    registros = registro_mdl.search(cr, uid, [('cedula','=',str(contrato.cedula)), ('fecha','=',str(this.fecha))])
                    
                    if registros:
                        print("si existe")
                    else:
                        faltas_mdl.create(cr, uid, {
                            'registro_id':this.id,
                            'employee_id':contrato.employee_id.id,
                            'cedula':contrato.cedula,
                            'nombre':contrato.employee_id.complete_name,
                            'fecha':this.fecha,
                            'departamento':contrato.employee_id.department_id.parent_id.name,
                            'dep_superior':contrato.employee_id.department_id.name,
                        })
        return True

    _defaults = dict(
        fecha = time.strftime('%Y-%m-%d'),
    )
mdlFaltas()