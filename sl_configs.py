import psycopg2, psycopg2.extras, json
import sl_db

cursor = sl_db.database.cursor(cursor_factory=psycopg2.extras.DictCursor)
cursor.execute("""SELECT m.merchant_id as merchant_id, c.leaderboard_level_thresholds as levels,
	COALESCE(c.review_points, _default.review_points) as review_points,
	COALESCE(c.first_review_points, _default.first_review_points ) as first_review_points,
	COALESCE(c.photo_review_points, _default.photo_review_points ) as photo_review_points,
	COALESCE(c.long_review_points, _default.long_review_points ) as long_review_points,
	COALESCE(c.helpful_vote_points, _default.helpful_vote_points ) as helpful_vote_points,
	COALESCE(c.follower_points, _default.follower_points ) as follow_points,
	COALESCE(c.facebook_comment_review_points, _default.facebook_comment_review_points ) as facebook_comment_points,
	COALESCE(c.facebook_verify_review_points, _default.facebook_verify_review_points ) as facebook_verify_points,
	COALESCE(c.facebook_verify_review_points, _default.facebook_verify_review_points ) as facebook_post_points,
	COALESCE(c.get_advice_points, _default.get_advice_points ) as get_advice_points,
	COALESCE(c.answer_question_points, _default.answer_question_points ) as answer_points,
	COALESCE(c.first_answer_question_points, _default.first_answer_question_points ) as first_answer_points
	FROM social_loyalty_action_configuration c, merchant m 
	LEFT OUTER JOIN social_loyalty_action_configuration _default
	on _default.merchant_group_id=1
	WHERE m.merchant_group_id = c.merchant_group_id""")

def preprocess_config (cursor):
	for row in cursor:
		if row['levels']:
			row['levels'] = json.loads (row['levels'])
		yield row

configs = {row['merchant_id']: row for row in preprocess_config(cursor)}
cursor.close()
DEFAULT_CONFIG = configs[1]

def get_merchant_config (merchant_id):
	return configs.get(merchant_id, DEFAULT_CONFIG)