# -*- coding: utf-8 -*-
from openerp import api,fields, models

class SessionPartner(models.Model):
    _name = "open_academy.session.partner"

    partner_id = fields.Many2one('res.partner')
    session_id = fields.Many2one('open_academy.session')
    create_date = fields.Datetime()

class Session(models.Model):
    _name = "open_academy.session"

    name = fields.Char(requied=True)## cuando no defines un string, por default aplica formato al nombre de la variable Name quedaria
    start_date = fields.Date()
    duration = fields.Float(digits=(6,2), help="duracion en dias")
    seats = fields.Integer(string="Numero de asientos en el curso")
    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')#podemos aplicar store=True
    instructor_id = fields.Many2one('res.partner',
                                    string="Instructor",
                                    on_delete="set null",
                                    index=True,
                                    domain=["|",
                                    ("instructor","=","True"),
                                    ("category_id","ilike","Teacher")])
                                    ##agregamos el dominio para que solo nos de a seleccionar partners que estan marcados
                                    ##como instructores o que contienen un tag teacher, Notese que utilizamos la notacion polaca
    course_id = fields.Many2one('open_academy.course',
                                on_delete="cascade",
                                string="Curso",
                                requied=True)
    attendes_ids = fields.Many2many('res.partner', relation='open_academy.session.partner',
                                    column1='session_id', column2='partner_id', string="Attendes")

    @api.one #para que entre a cada uno de los registros
    @api.depends('seats','attendes_ids') #de que campos depende para llevar acabo la def
    def _taken_seats(self):
        if not self.seats:
            self.seats = 0
        else:
            self.taken_seats = 100.0 * len(self.attendes_ids) / self.seats
