-- This is because current Django version does not support Postgres Exclusion constraint
-- This will change as Django 3 lands. It is currently in alpha and not compatible with some
-- of the third-party apps used.
CREATE EXTENSION btree_gist;
ALTER TABLE clock_event
  add constraint no_overlapping_time_constraint
  EXCLUDE USING gist (user_id WITH =, time_range WITH &&)