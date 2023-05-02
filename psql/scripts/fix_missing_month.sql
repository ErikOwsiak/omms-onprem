do $$
declare
	mid int;
	mdly float;
	lstread float;
	calcread float;
	_y int = 2023;
	_m int = 4;
begin
	for mid in select t.met_circ_dbid from streams.kwhs_raw t
		where t.backfill_notes = 'APR_FIX'
	loop
		mdly := meter_daily(mid, 2023, 3);
		-- get today reading --
		select t.total_kwhs into lstread
				from streams.kwhs_raw t where t.met_circ_dbid = mid
			and extract(year from t.dts_utc) = _y
			and extract(month from t.dts_utc) = 5
			order by t.dts_utc desc limit 1;
		calcread := round((lstread - (2 * mdly))::numeric, 2);
		insert  into streams.kwhs_raw (met_circ_dbid, dts_utc, is_backfilled
				, total_kwhs, l1_kwhs, l2_kwhs, l3_kwhs, backfill_notes)
			values(mid, '2023-04-30 23:58:58', true, calcread
				, null, null, null, 'APR_2023_END_FIX');
		-- end of loop; print some junk --
		raise notice '% | % | % | %', mid, mdly, calcread, lstread;
	end loop;
end$$;
