# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta
from openerp.osv import osv, fields
from openerp.report import report_sxw

class Location_Details_Report(osv.AbstractModel):

    _name="report.location_details_report_pdf"


    def render_html(self, cr, uid, ids, data=None, context=None):
        report_obj = self.pool('report')
        report = report_obj.get_report_from_name(
            cr, uid, 'location_details_report_pdf'
        )

        docargs = {
            'doc_ids': ids,
            'doc_model': report.model,
            'docs': self.pool(report.model).browse(cr, uid, ids, context=context),
        }
        return report_obj.render(cr, uid, ids, 'location_details_report_pdf', docargs, context)
