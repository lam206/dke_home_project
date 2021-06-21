CREATE VIEW IF NOT EXISTS left_tag_counts
AS SELECT tag_label, count(*) as count_left
	FROM Tags
	JOIN Tweets ON Tags.tweet_id = Tweets.tweet_id
	WHERE left_leaning = 1
	GROUP BY tag_label;

CREATE VIEW IF NOT EXISTS right_tag_counts
AS SELECT tag_label, count(*) as count_right
	FROM Tags
	JOIN Tweets ON Tags.tweet_id = Tweets.tweet_id
	WHERE left_leaning = 0
	GROUP BY tag_label;

-- right leaning factors are negative and left leaning factors are positive
CREATE VIEW IF NOT EXISTS factors_for_common_tags
AS SELECT
		t1.tag_label AS tag_label,
		IIF(count_right > count_left,
			- (CAST(count_right AS float) + 1.0) / (CAST(count_left AS float) + 1.0),
			(CAST(count_left AS float) + 1.0) / (CAST(count_right AS float) + 1.0)) AS factor,
		count_right + count_left AS total_tag_mentions
	FROM
		left_tag_counts as t1
	JOIN
		right_tag_counts as t2
	ON t1.tag_label = t2.tag_label;


CREATE VIEW IF NOT EXISTS factors_for_right_tags
AS SELECT
		tag_label, - (CAST(count_right AS float) + 1.0) AS factor, count_right As total_tag_mentions
	FROM right_tag_counts
	WHERE tag_label not in (select distinct tag_label from left_tag_counts);

CREATE VIEW IF NOT EXISTS factors_for_left_tags
AS SELECT
		tag_label, CAST(count_left AS float) + 1.0 AS factor, count_left AS total_tag_mentions
	FROM left_tag_counts
	WHERE tag_label not in (select distinct tag_label from right_tag_counts);


CREATE VIEW IF NOT EXISTS factors
AS SELECT * FROM factors_for_common_tags UNION
	SELECT * FROM factors_for_left_tags UNION
	SELECT * FROM factors_for_right_tags;

CREATE VIEW TweetsWithFactorSum AS
    SELECT Tags.tweet_id, sum(f.factor), left_leaning
    FROM Tweets
    JOIN Tags ON Tags.tweet_id = Tweets.tweet_id
    JOIN factors f on Tags.tag_label = f.tag_label
    group by Tweets.tweet_id;





