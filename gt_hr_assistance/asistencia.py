import datetime
from osv import osv, fields
import time

class mdlRegistroAsistencia(osv.Model):
    _name = 'mdl.registro.asistencia'
    _columns = dict(
        registro_id = fields.many2one('lectura.biometrico','Lectura'),
        employee_id = fields.many2one('hr.employee', 'Empleado'),
        cedula = fields.char('Cedula',size=15),
        nombre = fields.char('Nombre',size=50),
        departamento = fields.char('Dep.',size=64),
        dep_superior = fields.char('Dep. Sup.',size=64),
        horario_trabajo = fields.char('Horario Trabajo',size=50),
        fecha = fields.date('Fecha',size=32),
        dia = fields.char('Dia',size=10),
        hora_inicio = fields.char('Hora Inicio', size=8),
        almuerzo_inicio = fields.char('Almuerzo Inicio',size=8),
        almuerzo_fin = fields.char('Almuerzo Fin',size=8),
        hora_fin = fields.char('Hora Fin',size=8),
    )
mdlRegistroAsistencia()

class mdlAsistencia(osv.Model):
    _name = 'mdl.asistencia'
    _columns = dict(
        nombre=fields.char('Nombre',size=50),
        cedula=fields.char('Cedula',size=15),
        fecha=fields.date('Fecha',size=32),
        fecha_hora=fields.datetime('Hora',size=10),
        planta=fields.char('Planta',size=50),
    )
mdlAsistencia()

class lecturaBiometrico(osv.Model):
    _name = 'lectura.biometrico'
    _columns = dict(
        lectura_id = fields.one2many('mdl.registro.asistencia','registro_id','Detalle Lecturas'),
        employee_id = fields.many2one('hr.employee', 'Empleado'),
        departamento = fields.char('Departamento',size=70),
        cedula=fields.char('Cedula',size=15),
        nombre=fields.char('Nombre',size=50),
        fecha=fields.date('Fecha',size=32),
        fecha_hora = fields.datetime('Fecha/Hora',size=32),
        planta=fields.char('Planta',size=50),
    )
    
    def cargar_marcaciones(self, cr, uid, ids, context=None):
        #search    select
        #update    update
        #unlink    delete
        #browse    objeto    

        lectura_mdl = self.pool.get('lectura.biometrico')
        asistencia_mdl = self.pool.get('mdl.asistencia')
        employee_mdl = self.pool.get('hr.employee')
                        
        for this in self.browse(cr, uid, ids):
            asistencias = asistencia_mdl.search(cr, uid, [('fecha','=',str(this.fecha))])
            
            if asistencias:
                for asistencia_id in asistencias:
                    

                    asistencia = asistencia_mdl.browse(cr,uid, asistencia_id)

                    employees = employee_mdl.search(cr, uid, [(str('name'),'=',str(asistencia.cedula))])

                    aux_fecha = str(asistencia.fecha_hora[5:7] + '-' + asistencia.fecha_hora[8:10] + '-' + asistencia.fecha_hora[0:4])
                    aux_fecha_hora = str(asistencia.fecha_hora[5:7] + '-'+asistencia.fecha_hora[8:10] + '-'+asistencia.fecha_hora[0:4] + ' '+asistencia.fecha_hora[11:19])

                    if employees:

                        employee = employee_mdl.browse(cr,uid, employees[0])

                        try:
                            lectura_mdl.create(cr,uid,{
                                'employee_id':employee.id,
                                'departamento':employee.department_id.name,
                                'cedula':asistencia.cedula,
                                'nombre':employee.complete_name,
                                'fecha':aux_fecha,
                                'fecha_hora':aux_fecha_hora,
                                'planta':asistencia.planta,
                            })
                        except:
                            print()
        return True
    _defaults = dict(
        fecha = time.strftime('%Y-%m-%d'),
    )

    def cargar_asistencias(self, cr, uid, ids, context=None): 

        registro_mdl = self.pool.get('mdl.registro.asistencia')
        lectura_mdl = self.pool.get('lectura.biometrico')
        employee_mdl = self.pool.get('hr.employee')
        department_mdl = self.pool.get('hr.department')

        asistencias = {}
        deps = {}
        l_asistencia = list()

        for this in self.browse(cr, uid, ids):
            lecturas = lectura_mdl.search(cr, uid, [('fecha','=',str(this.fecha))])  #[1,3,4,6]
            
            if lecturas:
                for lectura_id in lecturas:

                    lectura = lectura_mdl.browse(cr,uid, lectura_id)
                    aux_cedula = str(lectura.cedula)

                    if aux_cedula in asistencias:
                        l_asistencia = asistencias[aux_cedula]

                    aux_hora = str(lectura.fecha_hora)
                    aux_hora2 = str(aux_hora[11:16])

                    l_asistencia.append(aux_hora2)
                    l_asistencia.sort()
                    asistencias[aux_cedula] = l_asistencia
                    l_asistencia = []

                    deps[aux_cedula] = lectura.departamento

                for cedula in asistencias:

                    employees = employee_mdl.search(cr, uid, [(str('name'),'=',str(cedula))])
                    
                    if employees:
                        for employee_id in employees:               
                            employee = employee_mdl.browse(cr,uid, employee_id)
                                
                            #calculo de horas de ingreso, almuerzo y salida

                            horario_trabajo = list()
                            h1 = str(employee.hora_ingreso)

                            if (h1 != '00:00:00'):
                                h2 = str(employee.almuerzo_salida)
                                h3 = str(employee.almuerzo_ingreso)
                                h4 = str(employee.hora_salida)
                                
                                horario_trabajo.append(h1)
                                horario_trabajo.append(h2)
                                horario_trabajo.append(h3)
                                horario_trabajo.append(h4)

                                horario_asistencia = asistencias[cedula]

                                horas_trabajo = ["","","",""]

                                horario_trabajo_tmp = horario_trabajo[:]

                                horario_trabajo.pop(0)
                                horario_trabajo.pop(2)

                                if len(horario_asistencia) < len(horario_trabajo):
                                    for i in range(len(horario_trabajo) - len(horario_asistencia)):
                                        horario_asistencia.append('00:00:00')

                                horario_asistencia.sort()

                                indice = 1
                                rango = 60 #minutos
                                if(horario_trabajo[0] != "00:00:00"):
                                    for horaH in horario_trabajo:
                                        for horaA in horario_asistencia:
                                            for i in range(rango):

                                                r1 = datetime.datetime(100, 1, 1, int(horaH[0:2]), int(horaH[3:5])) + datetime.timedelta(0,60*1*i)
                                                r2 = datetime.datetime(100, 1, 1, int(horaH[0:2]), int(horaH[3:5])) - datetime.timedelta(0,60*1*i)
                                                t  = datetime.datetime(100, 1, 1, int(str(horaA[0:2])), int(str(horaA[3:5])))

                                                if (r1.time() >= t.time() and t.time() >= r2.time()):
                                                    horas_trabajo[indice] = str(t.time())
                                                    horario_asistencia.pop(horario_asistencia.index(horaA))
                                                    indice=2
                                                    break
                                                elif horaA == horario_asistencia[len(horario_asistencia) - 1]:
                                                    horas_trabajo[indice] = "00:00:00"
                                                    indice = 2
                                                    break
                                else:
                                    horas_trabajo[1] = "00:00:00"
                                    horas_trabajo[2] = "00:00:00"

                                if (horario_trabajo_tmp[0] == "19:00:00"):
                                    horas_trabajo[3] = min(horario_asistencia) + ':00'  # asigna la marcacion menor
                                    horas_trabajo[0] = max(horario_asistencia) + ':00'
                                else:
                                    horas_trabajo[0] = min(horario_asistencia) + ':00' #asigna la marcacion menor
                                    horas_trabajo[3] = max(horario_asistencia) + ':00'

                                dia = datetime.datetime(int(this.fecha[0:4]), int(this.fecha[5:7]), int(this.fecha[8:10]))

                                dias = {1:"Lunes",2:"Martes",3:"Miercoles",4:"Jueves",5:"Viernes",6:"Sabado",7:"Domingo"}

                                registro_mdl.create(cr,uid,{
                                    'registro_id':this.id,
                                    'employee_id':employee.id,
                                    'cedula':cedula,
                                    'nombre':employee.complete_name,
                                    'dep_superior':employee.department_id.name,
                                    'departamento':employee.department_id.parent_id.name,
                                    'horario_trabajo':str(horario_trabajo_tmp[0] + ' ' + horario_trabajo_tmp[1] + ' ' + horario_trabajo_tmp[2] + ' ' + horario_trabajo_tmp[3]),
                                    'fecha':this.fecha,
                                    'dia':dias[dia.isoweekday()],
                                    'hora_inicio':horas_trabajo[0],
                                    'almuerzo_inicio':horas_trabajo[1],
                                    'almuerzo_fin':horas_trabajo[2],
                                    'hora_fin':horas_trabajo[3]
                                })
		return True
    _defaults = dict(
        fecha = time.strftime('%Y-%m-%d'),
    )

    def ingresar_horas_extras(self, cr, uid, ids, context=None): #calculo de los valores de las horas extras
        emp_obj=self.pool.get('hr.employee')
        contract_obj=self.pool.get('hr.contract')
        #data = self.read(cr, uid, ids)[0]
        h_ad=self.pool.get('hr.he.register.line')
        self._bad_archivo(cr, uid, ids, data['archivo'],context=context)
        obj=self.pool.get('hr.he.register')
        if context is None:
            context = {}
        id_activo=context.get('active_id')
        parent=obj.browse(cr, uid, id_activo)
        ids_unlink=[]
        if parent.state!='draft':
            raise osv.except_osv(('Error de usuario!'),'No puede importar un archivo cuando el documento ya esta procesado.')
        for l in parent.line_ids:
             ids_unlink.append(l.id)
        h_ad.unlink(cr, uid, ids_unlink,context=context)
        if data['archivo']:
            arch = data['archivo']
            arch_xls = base64.b64decode(arch)
            book = xlrd.open_workbook(file_contents=arch_xls)
            sh = book.sheet_by_name(book.sheet_names()[0])
            context={}
            for r in range(sh.nrows)[1:]:
                if sh.cell(r,1).value:
                    emp_ids = emp_obj.search(cr, uid, [('ci','=',sh.cell(r,1).value)])
                    if emp_ids:
                        empleado=emp_obj.browse(cr, uid, emp_ids[0])
                        contract_ids = contract_obj.search(cr, uid, [('employee_id','=',emp_ids[0]),('activo','=',True)])
                        if contract_ids:
                            hr_125 = 0
                            hr_150 = 0
                            hr_200 = 0
                            if sh.cell(r,2).value:
                                hr_125 = sh.cell(r,2).value
                            if sh.cell(r,3).value:
                                hr_150 = sh.cell(r,3).value
                            if sh.cell(r,4).value:
                                hr_200 = sh.cell(r,4).value
                            h_ad.create(cr, uid, {
                                'date':data['date'],
                                'employee_id': empleado.id,
                                'employee_name': empleado.name + ' ' + empleado.employee_lastname,
                                'registro_id': parent.id,
                                'period_id': parent.period_id.id,
                                'hora_100': 80,
                                'costo_hora': empleado.contract_id.hour_cost,
                                'wage': empleado.contract_id.wage,
                                'hora_125': hr_125,
                                'hora_150': hr_150,
                                'hora_200': hr_200,
                            })
        else:
            raise osv.except_osv(('Error de usuario!'),'No ha seleccionado ningun archivo.')
        return {'type':'ir.actions.act_window_close' }
lecturaBiometrico()