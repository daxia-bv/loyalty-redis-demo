#! /usr/bin/env python
import sl_db, sl_configs, sl_redis, logs, args, psycopg2.extras

def update_profile (profile):
	sl_redis.put_profile (profile['id'], profile)
	calculate_leaderboard (profile)
	return True

def calculate_leaderboard (profile):
	config         = sl_configs.get_merchant_config (profile['merchant_id'])
	lb_score       = sum( (config.get(type+'_points', 0)*profile[type] for type in profile) )
	lb_level       = 1 + sum( (1 for level in config['levels'] if lb_score > level) )
	sl_redis.put_leaderboard (profile['merchant_id'], profile['id'], lb_score, lb_level)

def get_profiles():
	cursor = sl_db.database.cursor (cursor_factory=psycopg2.extras.DictCursor)
	whereStr = "" if args.merchantGroupId is None else "WHERE merchant_group_id="+str(args.merchantGroupId)
	cursor.execute (" SELECT profile_id, action_type as type, merchant_id FROM social_loyalty_action_event "
					+ whereStr
					+ " ORDER BY profile_id, action_date ASC ")
	current_profile = None
	for row in cursor:
		if not current_profile:
			current_profile = {'id': row['profile_id'], 'merchant_id': row['merchant_id']}
 		if row['profile_id'] != current_profile['id']:
			yield current_profile
			current_profile = {'id': row['profile_id'], 'merchant_id': row['merchant_id']}
		current_profile[row['type']] = current_profile.get(row['type'], 0) + 1
	cursor.close()
	if current_profile: yield current_profile

num_profiles = 0
for profile in get_profiles():
	num_profiles += 1
	update_profile (profile)
logs.logging.info ("\n %d profiles touched", num_profiles)
sl_redis.commit()
sl_db.database.close()