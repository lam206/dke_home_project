CREATE VIEW IF NOT EXISTS left_user_counts
AS SELECT user, count(*) as count_left
	FROM Entities
	JOIN Tweets ON Entities.tweet_id = Tweets.tweet_id
	WHERE left_leaning = 1
	GROUP BY user;

CREATE VIEW IF NOT EXISTS right_user_counts
AS SELECT user, count(*) as count_right
	FROM Entities
	JOIN Tweets ON Entities.tweet_id = Tweets.tweet_id
	WHERE left_leaning = 0
	GROUP BY user;

-- right leaning factors are negative and left leaning factors are positive
CREATE VIEW IF NOT EXISTS factors_for_common_users
AS SELECT
		t1.user AS user,
		IIF(count_right > count_left,
			- (CAST(count_right AS float) + 1.0) / (CAST(count_left AS float) + 1.0),
			(CAST(count_left AS float) + 1.0) / (CAST(count_right AS float) + 1.0)) AS factor,
		count_right + count_left AS total_user_mentions
	FROM
		left_user_counts as t1
	JOIN
		right_user_counts as t2
	ON t1.user = t2.user;


CREATE VIEW IF NOT EXISTS factors_for_right_users
AS SELECT
		user, - (CAST(count_right AS float) + 1.0) AS factor, count_right As total_user_mentions
	FROM right_user_counts
	WHERE user not in (select distinct user from left_user_counts);

CREATE VIEW IF NOT EXISTS factors_for_left_users
AS SELECT
		user, (CAST(count_left AS float) + 1.0) AS factor, count_left As total_user_mentions
	FROM left_user_counts
	WHERE user not in (select distinct user from right_user_counts);


CREATE VIEW IF NOT EXISTS factors_users
AS SELECT * FROM factors_for_common_users UNION
	SELECT * FROM factors_for_left_users UNION
	SELECT * FROM factors_for_right_users;






