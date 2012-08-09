import redis

host_name = 'localhost'
# host_name = 'fisheye'

redis_conn = redis.StrictRedis(host=host_name, port=6379, db=0)
pipe = redis_conn.pipeline()
print "[Redis]    Connected to "+host_name


def put_profile (profile_id, stats):
	pipe.hmset ('user:'+str(profile_id), stats)

def put_leaderboard (merchant_id, profile_id, score, level):
	pipe.hset('user:'+str(profile_id), 'lb_score', score)
	pipe.hset('user:'+str(profile_id), 'lb_level', level)
	pipe.zadd('lb:'+str(merchant_id), score, profile_id)

def commit ():
	pipe.execute()