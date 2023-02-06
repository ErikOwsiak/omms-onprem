
import redis
# import psycopg2.extensions
from psycopg2.extensions import connection, cursor
from lib.utils import utils
# -- system --
from psql.dbConnServer import dbConnServer
from core.logProxy import logProxy


class dbOps(object):

   NULL = 'null'
   PWR_STATS_TBL = "streams.power_stats"
   METER_MODEL_INFO_REDIS_KEY = "MODEL_INFO"
   DB_IDX_READS: int = 2

   def __init__(self, conn_str: str, red: redis.Redis = None):
      self.conn_str = conn_str
      self.conn: connection = dbConnServer.getConnection(self.conn_str)
      self.red: redis.Redis = red

   def get_meter_syspath_dbid(self, syspath: str) -> int:
      cur: cursor = self.conn.cursor()
      try:
         tbl = "core.meters"
         qry = f"select t.met_rowid from {tbl} t where t.syspath = '{syspath}';"
         cur.execute(qry)
         row = cur.fetchone()
         if row is not None:
            return int(row[0])
         else:
            m_tp = "Unknown"; m_bnd = m_tp
            m_mdl = m_tp; m_tag = m_tp
            # -- -- -- --
            DB_IDX_READS: int = 2
            if self.red is not None:
               # " type: xxx | brand: orno | model: orno516 | tag: xxxx "
               self.red.select(DB_IDX_READS)
               meter_info = self.red.hget(syspath, dbOps.METER_MODEL_INFO_REDIS_KEY)
               if meter_info:
                  m_tp, m_bnd, m_mdl, m_tag = \
                     self.__parse_meter_info_str(meter_info.decode("utf-8"))
               else:
                  logProxy.log_warning(f"METER_INFO_NOT_FOUND: {syspath}")
            # -- -- -- --
            qry = f"insert into {tbl}" \
               f" values(default, '{syspath}', '{m_tp}', '{m_bnd}', '{m_mdl}', '{m_tag}'," \
               f" now()) returning met_rowid;"
            cur.execute(qry)
            row = cur.fetchone()
            self.conn.commit()
            if cur.rowcount == 1:
               dbid: int = row[0]
               return dbid
            else:
               pass
      except Exception as e:
         print(e)
      finally:
         cur.close()

   # def insert_elect_kwhrs(self, dbid: int, tkwhs: float, l1kwhs, l2kwhs, l3kwhs) -> bool:
   #    # -- -- -- --
   #    ins = f"insert into streams.kwhs_raw" \
   #       f" values(default, {dbid}, now(), {tkwhs}, {l1kwhs}, {l2kwhs}, {l3kwhs}) returning row_dbid;"
   #    cur: cursor = self.conn.cursor()
   #    cur.execute(ins)
   #    self.conn.commit()
   #    rowcount = cur.rowcount
   #    cur.close()
   #    return rowcount == 1

   def insert_elect_kwhrs_dict(self, dbid: int, _dict: {}) -> bool:
      cur: cursor = None
      try:
         # -- this needs to be fixed --
         syspath = _dict["PATH"]
         if "pzem" in syspath:
            tl_kwh = _dict["kWh"] if "kWh" in _dict.keys() else dbOps.NULL
         else:
            tl_kwh = _dict["tl_kwh"] if "tl_kwh" in _dict.keys() else dbOps.NULL
         # -- -- -- --
         l1_kwh = _dict["l1_kwh"] if "l1_kwh" in _dict.keys() else dbOps.NULL
         l2_kwh = _dict["l2_kwh"] if "l2_kwh" in _dict.keys() else dbOps.NULL
         l3_kwh = _dict["l3_kwh"] if "l3_kwh" in _dict.keys() else dbOps.NULL
         ins = f"insert into streams.kwhs_raw" \
            f" (met_circ_dbid, dts_utc, total_kwhs, l1_kwhs, l2_kwhs, l3_kwhs)" \
            f" values({dbid}, now(), {tl_kwh}, {l1_kwh}, {l2_kwh}, {l3_kwh})" \
            f" returning row_dbid;"
         # -- print text block --
         lns: [] = utils.txt_block_formatted(ins, color="blue")
         [print(ln) for ln in lns]
         # -- -- -- --
         cur = self.conn.cursor()
         cur.execute(ins)
         self.conn.commit()
         if cur.rowcount == 1:
            row_dbid = cur.fetchone()
            print(f"\t\tGOOD INSERT: {row_dbid}\n")
            return True
         else:
            print(f"\t\tINSERT ERROR!\n")
            return False
      except Exception as e:
         logProxy.log_exp(e)
      finally:
         cur.close()

   def insert_elect_pwr_stats(self, dbid: int, _dict: {}):
      cur: cursor = None
      try:
         # -- misc --
         ghz = _dict["grid_hz"] if "grid_hz" in _dict.keys() else dbOps.NULL
         # -- volts --
         lnv = _dict["ln_v"] if "ln_v" in _dict.keys() else dbOps.NULL
         l1v = _dict["l1_v"] if "l1_v" in _dict.keys() else dbOps.NULL
         l2v = _dict["l2_v"] if "l2_v" in _dict.keys() else dbOps.NULL
         l3v = _dict["l3_v"] if "l3_v" in _dict.keys() else dbOps.NULL
         # -- amps --
         tla = _dict["tl_a"] if "tl_a" in _dict.keys() else dbOps.NULL
         l1a = _dict["l1_a"] if "l1_a" in _dict.keys() else dbOps.NULL
         l2a = _dict["l2_a"] if "l2_a" in _dict.keys() else dbOps.NULL
         l3a = _dict["l3_a"] if "l3_a" in _dict.keys() else dbOps.NULL
         # -- watts --
         tlw = _dict["tl_w"] if "tl_w" in _dict.keys() else dbOps.NULL
         l1w = _dict["l1_w"] if "l1_w" in _dict.keys() else dbOps.NULL
         l2w = _dict["l2_w"] if "l2_w" in _dict.keys() else dbOps.NULL
         l3w = _dict["l3_w"] if "l3_w" in _dict.keys() else dbOps.NULL
         # -- power factor --
         tlpf = _dict["tl_pf"] if "tl_pf" in _dict.keys() else dbOps.NULL
         l1pf = _dict["l1_pf"] if "l1_pf" in _dict.keys() else dbOps.NULL
         l2pf = _dict["l2_pf"] if "l2_pf" in _dict.keys() else dbOps.NULL
         l3pf = _dict["l3_pf"] if "l3_pf" in _dict.keys() else dbOps.NULL
         # -- build insert --
         ins = f"insert into {dbOps.PWR_STATS_TBL} values(default, {dbid}, now(), {ghz}," \
            f" {lnv}, {l1v}, {l2v}, {l3v}, {tla}, {l1a}, {l2a}, {l3a}," \
            f" {tlw}, {l1w}, {l2w}, {l3w}, {tlpf}, {l1pf}, {l2pf}, {l3pf}) returning row_dbid;"
         # -- print text block --
         lns: [] = utils.txt_block_formatted(ins)
         [print(ln) for ln in lns]
         # -- insert --
         cur: cursor = self.conn.cursor()
         cur.execute(ins)
         self.conn.commit()
         if cur.rowcount == 1:
            row_dbid = cur.fetchone()
            print(f"\t\tGOOD INSERT: {row_dbid}\n")
            return True
         else:
            print(f"\t\tINSERT ERROR!\n")
            return False
      except Exception as e:
         logProxy.log_exp(e)
      finally:
         cur.close()

   def get_active_clients(self) -> []:
      conn: connection = dbConnServer.getConnection(self.conn_str, readonly=True)
      cur: cursor = conn.cursor()
      try:
         qry = "select t.clt_rowid rowid, t.clt_tag as tag, t.clt_name as clt_name" \
            " from config.clients t where t.dt_del is null;"
         cur.execute(qry)
         return cur.fetchall()
      except Exception as e:
         logProxy.log_exp(e)
      finally:
         cur.close()
         conn.close()

   def get_client_circuits(self, clt_tag: str):
      conn: connection = dbConnServer.getConnection(self.conn_str, readonly=True)
      cur: cursor = conn.cursor()
      try:
         qry = f"""select t.row_sid
            , t.locl_tag
            , t.cir_tag
            , m.met_rowid 
            , emc.met_syspath
            , t.code 
         from config.client_circuits t join core.elec_meter_circuits emc on t.cir_tag = emc.cir_tag 
               join core.meters m on m.syspath = emc.met_syspath 
            where t.clt_tag = '{clt_tag}' and t.dt_unlink is null;"""
         cur.execute(qry)
         return cur.fetchall()
      except Exception as e:
         logProxy.log_exp(e)
      finally:
         cur.close()
         conn.close()

   def get_system_circuits(self) -> []:
      qry = """select t.met_cir_rowid rowid
         , t.met_syspath spath
         , t.elec_room_locl_tag ltag from core.elec_meter_circuits t;"""
      cur: cursor = self.conn.cursor()
      try:
         cur.execute(qry)
         rows = cur.fetchall()
         return rows
      except Exception as e:
         logProxy.log_exp(e)
      finally:
         cur.close()

   def get_client_meters(self, clt_dbid: int) -> []:
      cur: cursor = self.conn.cursor()
      try:
         # -- get circuits --
         qry = f"select t.cir_rowid from config.clt_locl_cirs t where" \
            f" t.clt_rowid = {clt_dbid} and t.status = 1;"
         cur.execute(qry)
         return cur.fetchall()
      except Exception as e:
         logProxy.log_exp(e)
      finally:
         cur.close()

   def __parse_meter_info_str(self, buff: str, dlm: str = "|") -> (str, str, str, str):
      """
         # type: e3; brand: orno; model: orno516; tag: n/s
      """
      ty, b, m, tg = buff.split(dlm)
      ty = ty.replace("type:", "").strip()
      b = b.replace("brand:", "").strip()
      m = m.replace("model:", "").strip()
      tg = tg.replace("tag:", "").strip()
      return ty, b, m, tg

   def get_client_kwhrs(self, dts, cirs: str) -> []:
      # -- get meter rowids from cirs --
      cur: cursor = self.conn.cursor()
      qry = f"""select t.met_cir_rowid
            , t.cir_tag 
         from core.elec_meter_circuits t
            where position(t.cir_tag in '{cirs}') > 0;"""
      try:
         cur.execute(qry)
         rows = cur.fetchall()
         readings: [] = []
         # -- -- -- --
         def qry(rid, ct):
            return f"""select t.met_dbid
               , '{ct}' cirtag
               , cast(t.dts_utc::timestamp(0) as varchar)
               , t.total_kwhs
               , t.l1_kwhs
               , t.l2_kwhs
               , t.l3_kwhs
               , emc.met_syspath
            from streams.kwhs_raw t
               join core.elec_meter_circuits emc on emc.met_cir_rowid = t.met_dbid
            where cast(t.dts_utc as date) = cast('{dts}' as date)
               and met_dbid = {rid} order by t.dts_utc desc limit 1;"""
         # -- -- -- --
         for rowid, _ct in rows:
            cur.execute(qry(rowid, _ct))
            row = cur.fetchone()
            if row is not None:
               readings.append(row)
            else:
               readings.append((rowid, _ct, None))
         # -- -- -- --
         return readings
      except Exception as e:
         logProxy.log_exp(e)
      finally:
         cur.close()

   def get_client_circuit_history(self) -> []:
      qry = """select cc.locl_tag
            , cc.cir_tag
            , emc.met_syspath
            , cc.bitflags
            , cast(cc.dt_link as varchar)
            , cast(cc.dt_unlink as varchar)
            , c.clt_name
            , cast(c.dt_crd as varchar)
            , cast(c.dt_del as varchar)
         from config.client_circuits cc 
            join config.clients c on cc.clt_tag = c.clt_tag
            join core.elec_meter_circuits emc on cc.cir_tag = emc.cir_tag
         where cc.dt_unlink is not null order by c.clt_name, cc.dt_link;"""
      cur: cursor = self.conn.cursor()
      try:
         cur.execute(qry)
         rows = cur.fetchall()
         if rows is None:
            return []
         else:
            return rows
      except Exception as e:
         logProxy.log_exp(e)
      finally:
         cur.close()

   def get_met_circ_info(self, met_syspath: str) -> (int, int):
      # -- -- -- -- -- -- -- --
      # for now; todo: try to reconnect
      if self.conn is None:
         pass
      # -- -- -- -- -- -- -- --
      cur: cursor = self.conn.cursor()
      try:
         # -- if exists it MUST have model info rowid string --
         qry = f"select t.met_cir_rowid, t.met_model_rowid from" \
            f" core.elec_meter_circuits t where t.met_syspath = '{met_syspath}';"
         cur.execute(qry)
         read_row = cur.fetchone()
         if read_row:
            return (int(x) for x in read_row)
         else:
            # -- insert model string in --
            model_rowid: int = 0
            err_code, minfo = self.__redis_model_info(met_syspath)
            if err_code == 0:
               qry = f"select t.mm_rowid from core.meter_models t" \
                  f" where t.model_string = '{minfo}';"
               cur.execute(qry)
               read_row = cur.fetchone()
               if read_row:
                  model_rowid = int(read_row[0])
               else:
                  qry = f"insert into core.meter_models" \
                     f" values(default, '{minfo}', now()) returning mm_rowid;"
                  cur.execute(qry)
                  write_row = cur.fetchone()
                  self.conn.commit()
                  model_rowid = int(write_row[0])
            else:
               pass
            # -- -- -- --
            met_cir_rowid: int = 0
            qry = f"insert into core.elec_meter_circuits" \
               f" (met_cir_rowid, met_syspath, met_model_rowid, met_dt_crd)" \
               f" values(default, '{met_syspath}', {model_rowid}, now()) returning met_cir_rowid;"
            cur.execute(qry)
            write_row = cur.fetchone()
            if write_row:
               met_cir_rowid = int(write_row[0])
            # -- -- -- --
            return met_cir_rowid, model_rowid
      except Exception as e:
         logProxy.log_exp(e)
      finally:
         cur.close()

   def get_report_data(self, rowid: int) -> []:
      cur: cursor = self.conn.cursor()
      try:
         tbl = "reports.report_jobs"
         qry = f"select * from {tbl} t where t.row_serid = {rowid} limit 1;"
         cur.execute(qry)
         row = cur.fetchone()
         if row is not None:
            cur.execute(f"update {tbl} set dts_start = now() where row_serid = {rowid};")
            if cur.rowcount == 1:
               self.conn.commit()
            else:
               pass
         return row
      except Exception as e:
         logProxy.log_exp(e)
      finally:
         cur.close()

   def get_fst_lst_circuit_reading(self, cirdbid: int
         , year: int
         , month: int) -> []:
      qry = f"""(select * from streams.kwhs_raw t where t.met_dbid = {cirdbid} 
         and extract(year from cast(t.dts_utc as date))::int = {year}
         and extract(month from cast(t.dts_utc as date))::int = {month}
         order by t.dts_utc asc limit 1) 
            union
         (select * from streams.kwhs_raw t where t.met_dbid = {cirdbid}
         and extract(year from cast(t.dts_utc as date))::int = {year}
         and extract(month from cast(t.dts_utc as date))::int = {month}
         order by t.dts_utc desc limit 1);"""
      cur: cursor = self.conn.cursor()
      try:
         cur.execute(qry)
         rows = cur.fetchall()
         return rows
      except Exception as e:
         logProxy.log_exp(e)
      finally:
         cur.close()

   def update_report_data(self, rowid: int, err: int, buff: str) -> bool:
      # -- do --
      tbl = "reports.report_jobs"
      qry = f"update {tbl} set error_code = {err}," \
         f" output_buff = concat(output_buff, '{buff}\n')," \
         f" dts_error_code = now() where row_serid = {rowid};"
      cur: cursor = self.conn.cursor()
      try:
         cur.execute(qry)
         if cur.rowcount != 1:
            return False
         self.conn.commit()
         return True
      except Exception as e:
         logProxy.log_exp(e)
      finally:
         cur.close()

   def insert_report_job(self, rtype, y, m) -> int:
      cur: cursor = self.conn.cursor()
      try:
         args = f"year: {y}; month: {m};"
         ins = f"""insert into reports.report_jobs 
            values(default, '{rtype}', now(), '{args}', null, 0, null, null) 
            returning row_serid;"""
         cur.execute(ins)
         self.conn.commit()
         row = cur.fetchone()
         return row[0]
      except Exception as e:
         logProxy.log_exp(e)
      finally:
         cur.close()

   def __redis_model_info(self, met_syspath: str) -> (int, str):
      self.red.select(dbOps.DB_IDX_READS)
      meter_info = self.red.hget(met_syspath, dbOps.METER_MODEL_INFO_REDIS_KEY)
      if meter_info:
         minfo: str = meter_info.decode("utf-8").strip()
         return 0, minfo
      else:
         msg = f"METER_INFO_NOT_FOUND: {meter_info}"
         logProxy.log_warning(msg)
         return 1, msg
