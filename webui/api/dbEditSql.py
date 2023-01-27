
class dbEditSql(object):

   @staticmethod
   def elec_meter_circuits():
      return """select t.met_cir_rowid, t.met_syspath, mm.model_string
         , t.met_locl_tag, t.met_note, cast(t.met_dt_crd as varchar) as met_dt_crd
         , t.cir_tag, t.cir_amps, t.cir_volts, t.cir_locl_tag, t.cir_note
         , cast(t.cir_dt_crd as varchar) as cir_dt_crd from core.elec_meter_circuits t 
         join core.meter_models mm on t.met_model_rowid = mm.mm_rowid;"""

   @staticmethod
   def get_clients():
      return """select t.clt_rowid, t.clt_tag, t.clt_name, t.clt_access_pin, t.clt_phone
         , t.clt_email, t.note, t.bitflags, cast(t.dt_crd as varchar) as dt_crd
         , cast(t.dt_del as varchar) as dt_del from config.clients t;"""

   @staticmethod
   def table_info(tblname):
      qry = f"""select jsonb_agg(e) from 
         (select x.column_name
            , x.data_type
            , x.character_maximum_length
            , x.column_default
            , is_nullable 
         from INFORMATION_SCHEMA.columns x 
            where table_name = '{tblname}') e;"""
      return qry

   @staticmethod
   def clt_met_cirs_rows():
      return """select t.elec_met_cir_rowid, t.clt_tag, c.clt_name, emc.met_syspath
         , t.locl_tag, t.cir_tag, t.code, t.bitflags, cast(t.dt_link as varchar) as dt_link
         , cast(t.dt_unlink as varchar) as dt_unlink 
         from config.client_meter_circuits t join config.clients c on t.clt_tag = c.clt_tag 
         left join core.elec_meter_circuits emc on t.cir_tag = emc.cir_tag;"""
