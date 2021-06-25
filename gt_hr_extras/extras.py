import datetime
from osv import osv, fields
import time

class mdlExtrasDetalle(osv.Model):
    _name = 'mdl.extras.detalle'
    _columns = dict(
        registro_id = fields.many2one('mdl.extras','Lectura'),
        employee_id = fields.many2one('hr.employee', 'Empleado'),
        cedula = fields.char('Cedula',size=15),
        nombre = fields.char('Nombre',size=50),
        departamento = fields.char('Dep.',size=64),
        dep_superior = fields.char('Dep. Sup.',size=64),
        fecha = fields.date('Fecha',size=32),
        dia = fields.char('Dia',size=10),
        horas_trabajadas = fields.char('Horas Trabajadas', size=10),
        horas_faltantes = fields.char('Horas Faltantes',size=10),
        horas_extras = fields.char('Horas Extras',size=10),
    )
mdlExtrasDetalle()

class mdlExtras(osv.Model):
    _name = 'mdl.extras'
    _columns = dict(
        lectura_id = fields.one2many('mdl.extras.detalle','registro_id','Detalle Lecturas'),
        fecha=fields.date('Fecha',size=32),
    )

    def calcular_extras(self, cr, uid, ids, context = None):
        #search    select
        #update    update
        #unlink    delete
        #browse    objeto    

        registro_mdl = self.pool.get('mdl.registro.asistencia')
        line_obj = self.pool.get('mdl.extras.detalle')
                        
        for this in self.browse(cr, uid, ids):
            registros = registro_mdl.search(cr, uid, [('fecha','=',str(this.fecha))])
            
            if registros:
                for registro_id in registros:

                    registro = registro_mdl.browse(cr,uid, registro_id)
                    
                    #cargamos las horas de trabajo y de marcacion por usuario
                    tmp_trabajadas = str(registro.hora_inicio + ' ' + registro.almuerzo_inicio + ' ' + registro.almuerzo_fin + ' ' + registro.hora_fin)
                    tmp_trabajo = str(registro.horario_trabajo)

                    horas_realizadas = []
                    horario_trabajo = []

                    registro_dia = str(registro.dia)
                    tiempo_almuerzo = str(registro.employee_id.tiempo_almuerzo)

                    if str(tmp_trabajo).split(" ")[1] == "13:00:00":
                        tiempo_almuerzo = "00:00:00"
                    tiempo_almuerzo = datetime.datetime(100, 1, 1, int(tiempo_almuerzo[0:2]), int(tiempo_almuerzo[3:5]), int(tiempo_almuerzo[6:8]))

                    horas_realizadas.append(datetime.datetime(100, 1, 1, int(tmp_trabajadas[0:2]), int(tmp_trabajadas[3:5]), int(tmp_trabajadas[6:8])))
                    horas_realizadas.append(datetime.datetime(100, 1, 1, int(tmp_trabajadas[9:11]), int(tmp_trabajadas[12:14]), int(tmp_trabajadas[15:17])))
                    horas_realizadas.append(datetime.datetime(100, 1, 1, int(tmp_trabajadas[18:20]), int(tmp_trabajadas[21:23]), int(tmp_trabajadas[24:26])))
                    horas_realizadas.append(datetime.datetime(100, 1, 1, int(tmp_trabajadas[27:29]), int(tmp_trabajadas[30:32]), int(tmp_trabajadas[33:34])))

                    horario_trabajo.append(datetime.datetime(100, 1, 1, int(tmp_trabajo[0:2]), int(tmp_trabajo[3:5]), int(tmp_trabajo[6:8])))
                    horario_trabajo.append(datetime.datetime(100, 1, 1, int(tmp_trabajo[9:11]), int(tmp_trabajo[12:14]), int(tmp_trabajo[15:17])))
                    horario_trabajo.append(datetime.datetime(100, 1, 1, int(tmp_trabajo[18:20]), int(tmp_trabajo[21:23]), int(tmp_trabajo[24:26])))
                    horario_trabajo.append(datetime.datetime(100, 1, 1, int(tmp_trabajo[27:29]), int(tmp_trabajo[30:32]), int(tmp_trabajo[33:35])))

                    if str(tmp_trabajo).split(" ")[3] == "03:00:00":
                        horas_realizadas[0] = horas_realizadas[0] + datetime.timedelta(hours=12)
                        horas_realizadas[3] = horas_realizadas[3] + datetime.timedelta(hours=12)
                        horario_trabajo[0] = horario_trabajo[0] + datetime.timedelta(hours=12)
                        horario_trabajo[3] = horario_trabajo[3] + datetime.timedelta(hours=12)
                    else:
                        horas_realizadas[3] = horas_realizadas[3] - datetime.timedelta(hours=tiempo_almuerzo.hour, minutes=tiempo_almuerzo.minute, seconds=tiempo_almuerzo.second)
                        horario_trabajo[3] = horario_trabajo[3] - datetime.timedelta(hours=tiempo_almuerzo.hour, minutes=tiempo_almuerzo.minute, seconds=tiempo_almuerzo.second)

                    ingreso = ''
                    almuerzo_ingreso = ''
                    almuerzo_salida = ''

                    if horas_realizadas[0] >= horario_trabajo[0]:
                        ingreso = horas_realizadas[0]
                    else:
                        ingreso = horario_trabajo[0]

                    if horas_realizadas[1] >= horario_trabajo[1]:
                        almuerzo_ingreso = horario_trabajo[1]
                    else:
                        almuerzo_ingreso = horas_realizadas[1]

                    if horas_realizadas[2] >= horario_trabajo[2]:
                        almuerzo_salida = horas_realizadas[2]
                    else:
                        almuerzo_salida = horario_trabajo[2]

                    salida = horas_realizadas[3]

                    if horario_trabajo[3] < horas_realizadas[3]:
                        a = horario_trabajo[3] - datetime.timedelta(hours=ingreso.hour, minutes=ingreso.minute, seconds=ingreso.second)
                        b = almuerzo_salida - datetime.timedelta(hours=almuerzo_ingreso.hour, minutes=almuerzo_ingreso.minute, seconds=almuerzo_ingreso.second)
                        horas_trabajadas = a - datetime.timedelta(hours=b.hour, minutes=b.minute, seconds=b.second)
                    else:
                        a = salida - datetime.timedelta(hours=ingreso.hour, minutes=ingreso.minute, seconds=ingreso.second)
                        b = almuerzo_salida - datetime.timedelta(hours=almuerzo_ingreso.hour, minutes=almuerzo_ingreso.minute, seconds=almuerzo_ingreso.second)
                        horas_trabajadas = a - datetime.timedelta(hours=b.hour, minutes=b.minute, seconds=b.second)

                    h1 = horario_trabajo[0]
                    h2 = horario_trabajo[1]
                    h3 = horario_trabajo[2]
                    h4 = horario_trabajo[3]

                    a = h4 - datetime.timedelta(hours=h1.hour, minutes=h1.minute, seconds=h1.second)
                    b = h3 - datetime.timedelta(hours=h2.hour, minutes=h2.minute, seconds=h2.second)
                    horas_debe_trabajar = a - datetime.timedelta(hours=b.hour, minutes=b.minute, seconds=b.second)
                    horas_faltantes = datetime.datetime(100, 1, 1, 0, 0, 0)

                    if horas_trabajadas < horas_debe_trabajar:
                        horas_faltantes = horas_debe_trabajar - datetime.timedelta(hours=horas_trabajadas.hour, minutes=horas_trabajadas.minute, seconds=horas_trabajadas.second)

                    if horas_realizadas[3] > horario_trabajo[3]:
                        horas_extras = horas_realizadas[3] - datetime.timedelta(hours=horario_trabajo[3].hour, minutes=horario_trabajo[3].minute, seconds=horario_trabajo[3].second)
                    else:
                        horas_extras = datetime.datetime(100, 1, 1, 0, 0, 0)

                    horas_extras_tmp = horas_extras

                    if horas_extras_tmp.minute >= 55:
                        horas_extras = horas_extras + datetime.timedelta(hours=1)
                        horas_extras = datetime.datetime(100, 1, 1, horas_extras.hour, 0, 0)
                    elif horas_extras_tmp.minute > 24 and horas_extras_tmp.hour == 0:
                        horas_extras = datetime.datetime(100, 1, 1, horas_extras_tmp.hour, 0, 0)
                    elif horas_extras_tmp.minute > 24:
                        horas_extras = datetime.datetime(100, 1, 1, horas_extras_tmp.hour, 30, 0)
                    else:
                        horas_extras = datetime.datetime(100, 1, 1, horas_extras_tmp.hour, 0, 0)

                    if registro_dia == "Sabado" or registro_dia == "Domingo":
                        horas_trabajadas = horas_realizadas[len(horas_realizadas) - 1] - datetime.timedelta(hours=horas_realizadas[0].hour, minutes=horas_realizadas[0].minute, seconds=horas_realizadas[0].second)

                        horas_faltantes = datetime.datetime(100, 1, 1, 0, 0, 0)

                        if (horas_realizadas[3] + datetime.timedelta(minutes=30)) >= datetime.datetime(100, 1, 1, 14, 0, 0):
                            horas_trabajadas = horas_trabajadas - datetime.timedelta(hours=tiempo_almuerzo.hour, minutes=tiempo_almuerzo.minute, seconds=tiempo_almuerzo.second)
                        horas_extras = horas_trabajadas

                        horas_extras_tmp = horas_extras

                        if horas_extras_tmp.minute >= 55:
                            horas_extras = horas_extras + datetime.timedelta(hours=1)
                            horas_extras = datetime.datetime(100, 1, 1, horas_extras.hour, 0, 0)
                        elif horas_extras_tmp.minute > 24 and horas_extras_tmp.hour == 00:
                            horas_extras = datetime.datetime(100, 1, 1, horas_extras_tmp.hour, 0, 0)
                        elif horas_extras_tmp.minute > 24:
                            horas_extras = datetime.datetime(100, 1, 1, horas_extras_tmp.hour, 30, 0)
                        else:
                            horas_extras = datetime.datetime(100, 1, 1, horas_extras_tmp.hour, 0, 0)

                        if str(tmp_trabajo).split(" ")[3] == "19:00:00":
                            horas_extras = horas_extras
                    else:
                        if str(tmp_trabajo).split(" ")[3] == "19:00:00":
                            a = horario_trabajo[0]
                            b = horas_realizadas[0] - datetime.timedelta(hours=12)
                            horas_trabajadas = a - datetime.timedelta(hours=b.hour, minutes=b.minute, seconds=b.second)
                            horas_extras = horas_trabajadas - datetime.timedelta(hours=tiempo_almuerzo.hour, minutes=tiempo_almuerzo.minute, seconds=tiempo_almuerzo.second)
                            horas_faltantes = datetime.datetime(100, 1, 1, 0, 0, 0)

                    horas_trabajadas = str(horas_trabajadas.time())
                    horas_faltantes = str(horas_faltantes.time())
                    horas_extras = str(horas_extras.time())

                    dia = datetime.datetime(int(this.fecha[0:4]), int(this.fecha[5:7]), int(this.fecha[8:10]))
                    dias = {1:"Lunes",2:"Martes",3:"Miercoles",4:"Jueves",5:"Viernes",6:"Sabado",7:"Domingo"}


                    line_obj.create(cr, uid, {
                        'registro_id':this.id,
                        'employee_id':registro.employee_id.id,
                        'cedula':registro.cedula,
                        'nombre':registro.nombre,
                        'departamento':registro.departamento,
                        'dep_superior':registro.dep_superior,
                        'fecha':registro.fecha,
                        'dia':dias[dia.isoweekday()],
                        'horas_trabajadas':horas_trabajadas,
                        'horas_faltantes':horas_faltantes,
                        'horas_extras':horas_extras,
                    })
        return True
    
    def calcular_salario_extras(self, cr, uid, ids, context = None):
        #search    select
        #update    update
        #unlink    delete
        #browse    objeto    

        extras_mdl = self.pool.get('mdl.extras.detalle')
        employee_mdl = self.pool.get('hr.employee')

        contract_obj = self.pool.get('hr.contract')
        obj = self.pool.get('hr.he.register')
        h_ad = self.pool.get('hr.he.register.alone')
        line_obj=self.pool.get('hr.he.register.alone.line')

        work_period = self.pool.get('hr.work.period.line')

        head_head_obj = self.pool.get('hr.he.register')
                        
        for this in self.browse(cr, uid, ids):

            work_lines = work_period.search(cr, uid, [('name','=',str(this.fecha[5:7] + "/" + this.fecha[0:4]))])
                                
            if work_lines:
                for work_line_id in work_lines:

                    work_line = work_period.browse(cr,uid, work_line_id)

                    #raise osv.except_osv(('Error!'), work_line.id)

                    head_head_id = head_head_obj.create(cr, uid, {
                        'name':'REGISTRO HORAS EXTRAS',
                        'date':this.fecha,
                        'period_id':work_line.id
                    })
                    
                    extrass = extras_mdl.search(cr, uid, [('fecha','=',this.fecha)])  
                    
                    if extrass:
                        for extra_id in extrass:
                            extra_mdl = extras_mdl.browse(cr,uid, extra_id)

                            # 06:00:00 19:00:00 #suplementaria
                            # 19:00:00 06:00:00 #nocturna
                            # fines de semana y feriados #extraordinarias

                            horas_extras = str(extra_mdl.horas_extras).split(":")
                            horas_extras = datetime.datetime(100, 1, 1, int(horas_extras[0]), int(horas_extras[1]), 0)
                            registro_dia = str(extra_mdl.dia)

                            employees = employee_mdl.search(cr, uid, [('name','=',str(extra_mdl.cedula)), ('horas_extras','=',True)])

                            if employees:
                                for employee_id in employees:

                                    employee = employee_mdl.browse(cr,uid,employee_id)

                                    if horas_extras > datetime.datetime(100, 1, 1, 0, 0, 0):

                                        trabajo = str(employee.hora_salida).split(":")
                                        trabajo = datetime.datetime(100, 1, 1, int(trabajo[0]), int(trabajo[1]), 0)

                                        #nocturna, suplementarias, extraordinarias (fines de semana)
                                        extras = [datetime.datetime(100, 1, 1, 0, 0, 0), datetime.datetime(100, 1, 1, 0, 0, 0), datetime.datetime(100, 1, 1, 0, 0, 0)]

                                        extra = trabajo + datetime.timedelta(hours = horas_extras.hour, minutes=horas_extras.minute, seconds=horas_extras.second)

                                        if registro_dia != "Sabado" and registro_dia != "Domingo" and registro_dia != "Feriado":
                                            if trabajo < datetime.datetime(100, 1, 1, 19, 0, 0) and extra <= datetime.datetime(100, 1, 1, 19, 0, 0):
                                                extras[0] = datetime.datetime(100, 1, 1, 0, 0, 0)
                                                extras[1] = horas_extras
                                            elif trabajo <= datetime.datetime(100, 1, 1, 19, 0, 0) and extra >= datetime.datetime(100, 1, 1, 19, 0, 0) and extra <= datetime.datetime(100, 1, 2, 7, 0, 0):
                                                extras[1] = datetime.datetime(100, 1, 1, 19, 0, 0) - datetime.timedelta(hours=trabajo.hour, minutes=trabajo.minute, seconds=trabajo.second)
                                                extras[0] = horas_extras - datetime.timedelta(hours=extras[1].hour, minutes=extras[1].minute, seconds=extras[1].second)
                                            elif trabajo <= datetime.datetime(100, 1, 1, 19, 0, 0) and extra >= datetime.datetime(100, 1, 2, 7, 0, 0):
                                                extras[1] = datetime.datetime(100, 1, 1, 19, 0, 0) - datetime.timedelta(hours=trabajo.hour, minutes=trabajo.minute, seconds=trabajo.second)
                                                tmp = extra - datetime.timedelta(hours=7)
                                                extras[1] = extras[1] + datetime.timedelta(hours=tmp.hour, minutes=tmp.minute, seconds=tmp.second)
                                                extras[0] = horas_extras - datetime.timedelta(hours=extras[1].hour, minutes=extras[1].minute, seconds=extras[1].second)
                                            elif trabajo > datetime.datetime(100, 1, 1, 19, 0, 0) and extra <= datetime.datetime(100, 1, 2, 7, 0, 0):
                                                extras[0] = horas_extras
                                            elif trabajo > datetime.datetime(100, 1, 1, 19, 0, 0) and extra > datetime.datetime(100, 1, 2, 7, 0, 0):
                                                extras[0] = datetime.datetime(100, 1, 2, 7, 0, 0) - datetime.timedelta(hours=trabajo.hour, minutes=trabajo.minute, seconds=trabajo.second)
                                                extras[1] = horas_extras - datetime.timedelta(hours=extras[0].hour, minutes=extras[0].minute, seconds=extras[0].second)
                                        else: #fin de semana se paga extraordinaria y va las horas extras completas
                                            extras[2] = horas_extras

                                        extras[2] = str(extras[2].time())
                                        extras[1] = str(extras[1].time())
                                        extras[0] = str(extras[0].time())

                                        extras_val = []

                                        for hora in extras:
                                            tmp = ""
                                            if int(str(hora).split(":")[0]) >= 0:
                                                tmp = str(int(str(hora).split(":")[0]))
                                                if int(str(hora.split(":")[1])) == 30:
                                                    tmp = tmp + ".50"
                                            extras_val.append(tmp)

                                        #proceso para ingresar en el sistema

                                        if context is None:
                                            context = {}
                                        id_activo = context.get('active_id')
                                        parent = obj.browse(cr, uid, id_activo)

                                        ids_unlink = []

                                        contract_ids = contract_obj.search(cr, uid, [('employee_id','=',employee.id),('activo','=',True)])
                                        if contract_ids:

                                            #raise osv.except_osv(('Error!'), "6")
                                            contract = contract_obj.browse(cr,uid,contract_ids[0])

                                            hr_25 = hr_50 = hr_60 = hr_100 = 0
                                            head_id = h_ad.create(cr, uid, {
                                                'contract_id': contract.id,
                                                'period_id': work_line.id,
                                                'date':this.fecha,
                                                'registro_d_id':head_head_id,
                                            })
                                            
                                            line_obj.create(cr, uid, {
                                                'h_25':extras_val[0],
                                                'h_50':extras_val[1],
                                                'h_60':0,
                                                'h_100':extras_val[2],
                                                'registro_id':head_id,
                                            })
                                            #h_ad.compute_he_alone(cr, uid, [head_id],context={})
                                            h_ad.he_alone_draft_process(cr, uid, [head_id],context={})
            
    _defaults = dict(
        fecha = time.strftime('%Y-%m-%d'),
    )
mdlExtras()