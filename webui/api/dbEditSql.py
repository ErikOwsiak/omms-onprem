
class dbEditSql(object):

   @staticmethod
   def elec_meter_circuits():
      # , cmc.locl_tag as met_locl_tag
      return """select t.met_cir_rowid
         , t.met_syspath
         , mm.model_string as met_model_rowid
         , t.met_note 
         , cast(t.met_dt_crd as varchar) as met_dt_crd
         , t.cir_tag
         , t.cir_amps
         , t.cir_volts
         , t.cir_locl_tag
         , t.cir_note
         , cast(t.cir_dt_crd as varchar) as cir_dt_crd 
      from core.elec_meter_circuits t 
         join core.meter_models mm on t.met_model_rowid = mm.mm_rowid
         join config.client_meter_circuits cmc on cmc.cir_tag = t.cir_tag;"""

   @staticmethod
   def get_clients():
      return """select t.clt_rowid
            , t.clt_tag, t.clt_name
            , t.clt_access_pin, t.clt_phone
            , t.clt_email
            , t.note
            , t.bitflags
            , cast(t.dt_crd as varchar) as dt_crd
            , cast(t.dt_del as varchar) as dt_del 
         from config.clients t;"""

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
      return """select t.elec_met_cir_rowid
            , t.clt_tag
            , c.clt_name
            , emc.met_syspath
            , t.locl_tag
            , t.cir_tag
            , t.code
            , t.bitflags
            , cast(t.dt_link as varchar) as dt_link
            , cast(t.dt_unlink as varchar) as dt_unlink 
         from config.client_meter_circuits t join config.clients c on t.clt_tag = c.clt_tag 
            left join core.elec_meter_circuits emc on t.cir_tag = emc.cir_tag;"""

   @staticmethod
   def upsert_clients(d: []) -> str:
      """
         ('COL_clt_rowid', '3'), ('COL_clt_tag', '5242712882'), ('COL_clt_name', 'Dominos Pizza')
         , ('COL_clt_access_pin', ''), ('COL_clt_phone', ''), ('COL_clt_email', ''), ('COL_note', 'oldid_4')
         , ('COL_bitflags', '0'), ('COL_dt_crd', '2022-12-31'), ('COL_dt_del', '')
      """
      rowid: str = d["COL_clt_rowid"]
      clt_tag = d["COL_clt_tag"]
      clt_name = d["COL_clt_name"]
      clt_access_pin = d["COL_clt_access_pin"]
      clt_phone = d["COL_clt_phone"]
      clt_email = d["COL_clt_email"]
      note = d["COL_note"]
      tmp = d["COL_bitflags"]
      bitflags = int(tmp) if tmp != "" else 0
      dt_crd = d["COL_dt_crd"]
      dt_del = d["COL_dt_del"]
      if rowid == "auto":
         qry = f"insert into config.clients values(default, '{clt_tag}', '{clt_name}'" \
            f", '{clt_access_pin}', '{clt_phone}', '{clt_email}', '{note}', {bitflags}"\
            f", now(), null) returning clt_rowid;"
      else:
         qry = f"update config.clients set clt_tag='{clt_tag}', clt_name='{clt_name}'" \
               f", clt_access_pin='{clt_access_pin}', clt_phone='{clt_phone}'" \
               f", clt_email='{clt_email}', note='{note}', bitflags={bitflags}" \
               f" where clt_rowid = {rowid} returning clt_rowid;"
      # -- return query --
      return qry

   @staticmethod
   def upsert_client_meter_circuits(d: []) -> str:
      """
         ('COL_elec_met_cir_rowid', '2006'), ('COL_clt_tag', '1234567890'), ('COL_locl_tag', 'A3.3_A3.4'),
         ('COL_cir_tag', '1R7.04'), ('COL_code', ''), ('COL_bitflags', '0'), ('COL_dt_link', '2023-01-26'),
         ('COL_dt_unlink', '')
      """
      print(d)
      rowid: str = d["COL_elec_met_cir_rowid"]
      clt_tag = d["COL_clt_tag"]
      locl_tag = d["COL_locl_tag"]
      cir_tag = d["COL_cir_tag"]
      code = d["COL_code"]
      bitflags = d["COL_bitflags"]
      dt_link = d["COL_dt_link"]
      dt_unlink = d["COL_dt_unlink"]
      return ""
